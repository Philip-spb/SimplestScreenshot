import os
import time
import cv2

from selenium import webdriver


def clear_folder(folder_name):
    for file_name in os.listdir(folder_name):
        os.remove(f"{folder_name}/{file_name}")


if __name__ == "__main__":
    url = 'https://www.python.org'
    window_size_x = 1900
    window_size_y = 1080

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
    driver.set_page_load_timeout(1000)

    driver.get(url)

    SCROLL_PAUSE_TIME = 4
    FOLDER_NAME = 'screenshots'
    i = 0

    # Get scroll height
    height_delta = 1080
    last_height = 1080
    max_height = driver.execute_script("return document.body.scrollHeight")

    if os.path.exists(FOLDER_NAME):
        clear_folder(FOLDER_NAME)
    else:
        try:
            os.mkdir(FOLDER_NAME)
        except OSError:
            print(f"Создать директорию '{FOLDER_NAME}' не удалось")
            exit()

    while True:
        # Scroll down to bottom
        driver.save_screenshot(f"{FOLDER_NAME}/screenshot{i}.png")
        driver.execute_script(f"window.scrollTo(0, {last_height});")
        i += 1
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = last_height + height_delta
        if max_height < new_height:
            driver.save_screenshot(f"{FOLDER_NAME}/screenshot{i}.png")
            break
        last_height = new_height

    driver.quit()

    # Склеиваем скриншоты
    img_list = list(map(lambda x: f'{FOLDER_NAME}/' + x, os.listdir(FOLDER_NAME)))
    images = list(map(cv2.imread, sorted(img_list)))
    im_v = cv2.vconcat(images)
    clear_folder(FOLDER_NAME)
    cv2.imwrite(f'{FOLDER_NAME}/screenshot.jpg', im_v)

# + Добавить создание папки screenshots в корне (если она отсустсвует)
# + Добавить удаление всех файлов скриншотов из папки screenshots (если такие файлы есть)
# + Склеить полученные файлы
# Обрезать последний файл


