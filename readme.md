# SimplestScreenshot – программа для создания скриншотов сайта с использованием Selenium

Программа запускается на удаленном сервере.
В процессе выполнения программа постепенно делает скриншот 
активного окна сайта, далее передвигает активное окно вниз и 
так далее пока не достигнет самого "низа" сайта. Далее все 
скриншоты склеиваются в один файл. 

**Для работы программы требуется:**
+ Chrome + ChromeDriver
    + Chrome запускается в headless режиме
+ Установленные библиотеки
    + cv2 *(opencv-python-headless)*
    + selenium

**Что сделано:**
+ Добавить создание папки screenshots в корне (если она отсутствует)
+ Добавить удаление всех файлов скриншотов из папки screenshots (если такие файлы есть)
+ Склеить полученные файлы
+ Сохранять скриншоты только с номерами в имена и затем уже сортировать их преобразовав в int
+ Обрезать последний файл
+ Переписать имеющийся код с использованием классов
+ Переместить логические блоки в отдельные модули

**Что необходимо доделать:**
+ Убрать справа бегунок прокрутки
+ В финальной версии сделать ограничение на максимальное количество экранов для принтскрина
+ Сделать нажатие на кнопку перед запуском процесса снятия скриншота (скинуть xpath в качестве параметра запуска)
+ Сделать возможность удаления отдельного элемента страницы по xpath (например плавающей шапки)
