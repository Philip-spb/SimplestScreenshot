import os
import time
import cv2

from selenium import webdriver


def clear_folder(folder_name):
    for file_name in os.listdir(folder_name):
        os.remove(f"{folder_name}/{file_name}")


if __name__ == "__main__":
    url = 'http://vk.com/@mrhostel-ansambl-centralnyh-ploschadei'
    window_size_x = 950
    window_size_y = 540

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
    driver.set_page_load_timeout(10)

    driver.get(url)

    SCROLL_PAUSE_TIME = 2
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

    if os.path.exists(FOLDER_NAME):
        clear_folder(FOLDER_NAME)
    else:
        try:
            os.mkdir(FOLDER_NAME)
        except OSError:
            print(f"Создать директорию '{FOLDER_NAME}' не удалось")
            exit()

    while True:
        # Прокручиваем экран сверху вниз
        driver.save_screenshot(f"{FOLDER_NAME}/{i}.png")
        driver.execute_script(f"window.scrollTo(0, {last_height});")
        i += 1
        time.sleep(SCROLL_PAUSE_TIME)

        # Вычисляем ткущую высоту после прокрутки и сравниваем с максимально возможно прокруткой
        new_height = last_height + height_delta
        if max_height < new_height:
            driver.save_screenshot(f"{FOLDER_NAME}/{i}.png")
            break
        last_height = new_height

    driver.quit()

    # Склеиваем скриншоты
    img_list = list(map(lambda x: f'{FOLDER_NAME}/{x}.png', range(i + 1)))
    images = list(map(cv2.imread, img_list))
    # Обрезаем последний скриншот
    images[-1] = images[-1][(window_size_y - last_screen_height) * 2:]
    im_v = cv2.vconcat(images)
    clear_folder(FOLDER_NAME)
    cv2.imwrite(f'{FOLDER_NAME}/screenshot.jpg', im_v)
