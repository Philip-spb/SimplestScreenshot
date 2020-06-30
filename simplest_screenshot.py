from selenium import webdriver

if __name__ == "__main__":
    url = 'https://www.yandex.ru'

    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/81.0.4044.138 YaBrowser/20.6.0.905 Yowser/2.5 Yptp/1.23 Safari/537.36')
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)

    driver.set_page_load_timeout(100000)
    driver.get(url)

    driver.save_screenshot("screenshots/my_screenshot.png")

    driver.quit()
