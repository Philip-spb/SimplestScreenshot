import os
import cv2


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
