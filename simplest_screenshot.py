import os
import time
import cv2

from selenium import webdriver


class FsMethods:
    def __init__(self, folder_name='screenshots'):
        self.folder_name = folder_name

    def clear_folder(self):
        for file_name in os.listdir(self.folder_name):
            os.remove(f"{self.folder_name}/{file_name}")

    def path_exist(self):
        return os.path.exists(self.folder_name)

    def create_clear_folder(self):
        if self.path_exist():
            self.clear_folder()
        else:
            try:
                os.mkdir(self.folder_name)
            except OSError:
                print(f"Создать директорию '{self.folder_name}' не удалось")
                exit()

    def image_bonding(self, img_num, scroll_height, last_screen_height):
        img_list = list(map(lambda x: f'{self.folder_name}/{x}.png', range(img_num + 1)))
        images = list(map(cv2.imread, img_list))
        # Обрезаем последний скриншот
        images[-1] = images[-1][(scroll_height- last_screen_height) * 2:]
        im_v = cv2.vconcat(images)
        self.clear_folder()
        cv2.imwrite(f'{self.folder_name}/screenshot.jpg', im_v)


if __name__ == "__main__":
    url = 'https://www.mrhostel.ru'
    window_size_x = 950
    window_size_y = 540

    screen_shot = FsMethods()

    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/81.0.4044.138 YaBrowser/20.6.0.905 Yowser/2.5 Yptp/1.23 Safari/537.36')
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument(f'--window-size={window_size_x},{window_size_y}')
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(100)

    driver.get(url)

    SCROLL_PAUSE_TIME = 4
    FOLDER_NAME = 'screenshots'
    i = 0

    # Получаем максимально возможную глубину прокрутки
    height_delta = window_size_y
    last_height = window_size_y
    max_height = driver.execute_script("return document.body.scrollHeight")

    last_screen_height = max_height - int(max_height / window_size_y) * window_size_y

    print(max_height)
    print('Всего целых экранов: ', int(max_height / window_size_y))
    print('Высота последнего экрана: ', last_screen_height)

    screen_shot.create_clear_folder()

    while True:
        # Прокручиваем экран сверху вниз
        driver.save_screenshot(f"{FOLDER_NAME}/{i}.png")
        driver.execute_script(f"window.scrollTo(0, {last_height});")
        i += 1
        time.sleep(SCROLL_PAUSE_TIME)

        # Вычисляем текущую высоту после прокрутки и сравниваем с максимально возможно прокруткой
        new_height = last_height + height_delta
        if max_height < new_height:
            driver.save_screenshot(f"{FOLDER_NAME}/{i}.png")
            break
        last_height = new_height

    driver.quit()

    screen_shot.image_bonding(i, window_size_y, last_screen_height)
