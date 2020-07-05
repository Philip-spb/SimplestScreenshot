from FsMethods import FsMethods
from ScreenshotBot import ScreenshotBot


def main():
    screen_shot = FsMethods()
    screen_shot_bot = ScreenshotBot(screenshot_url='http://www.hostelvariant.ru', screen_size_x=950, screen_size_y=540)
    screen_size_y, screen_num, last_screen_height = screen_shot_bot.get_max_scroll_depth()
    screen_shot.create_clear_folder()
    screen_shot_bot.site_scrolling()
    del screen_shot_bot
    screen_shot.image_bonding(screen_num, screen_size_y, last_screen_height)


if __name__ == "__main__":
    main()
