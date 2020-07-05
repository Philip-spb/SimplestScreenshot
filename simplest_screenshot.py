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
        images[-1] = images[-1][(scroll_height - last_screen_height) * 2:]
        im_v = cv2.vconcat(images)
        self.clear_folder()
        cv2.imwrite(f'{self.folder_name}/screenshot.jpg', im_v)


class ScreenshotBot:
    SCROLL_PAUSE_TIME = 4

    def __init__(self, screenshot_url, screen_size_x, screen_size_y, folder_name='screenshots'):
        self.screenshot_url = screenshot_url
        self.screen_size_x = screen_size_x
        self.screen_size_y = screen_size_y
        self.height_delta = screen_size_y
        self.last_height = screen_size_y
        self.folder_name = folder_name
        self.last_screen_height = 0
        self.max_height = 0
        self.screen_num = 0

        options = webdriver.ChromeOptions()
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/81.0.4044.138 YaBrowser/20.6.0.905 Yowser/2.5 Yptp/1.23 Safari/537.36')
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-notifications")
        options.add_argument(f'--window-size={self.screen_size_x},{self.screen_size_y}')
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_page_load_timeout(120)

    def __del__(self):
        self.driver.quit()

    def get_max_scroll_depth(self):
        self.driver.get(self.screenshot_url)
        self.max_height = self.driver.execute_script("return document.body.scrollHeight")

        self.last_screen_height = self.max_height - int(self.max_height / self.screen_size_y) * self.screen_size_y
        self.screen_num = int(self.max_height / self.screen_size_y)
        # print(self.max_height)
        # print('Всего целых экранов: ', self.screen_num)
        # print('Высота последнего экрана: ', self.last_screen_height)

        return self.screen_size_y, self.screen_num, self.last_screen_height

    def site_scrolling(self):
        i = 0
        new_height = 0
        while True:
            self.driver.save_screenshot(f"{self.folder_name}/{i}.png")
            self.driver.execute_script(f"window.scrollTo(0, {self.last_height});")
            i += 1
            time.sleep(ScreenshotBot.SCROLL_PAUSE_TIME)

            # Вычисляем текущую высоту после прокрутки и сравниваем с максимально возможно прокруткой
            new_height = self.last_height + self.height_delta
            if self.max_height < new_height:
                self.driver.save_screenshot(f"{self.folder_name}/{i}.png")
                break
            self.last_height = new_height


if __name__ == "__main__":

    screen_shot = FsMethods()
    screen_shot_bot = ScreenshotBot(screenshot_url='https://www.mrhostel.ru', screen_size_x=950, screen_size_y=540)
    screen_size_y, screen_num, last_screen_height = screen_shot_bot.get_max_scroll_depth()
    screen_shot.create_clear_folder()
    screen_shot_bot.site_scrolling()
    del screen_shot_bot
    screen_shot.image_bonding(screen_num, screen_size_y, last_screen_height)
