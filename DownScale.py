import os
import subprocess


# Проверка и установка необходимых модулей
required_modules = ['os', 'glob', 'opencv-python']

def install_missing_modules(modules):
    for module in modules:
        try:
            __import__(module)
        except ImportError:
            print(f"Module '{module}' is missing. Installing...")
            subprocess.check_call(['pip', 'install', module])
            print(f"Module '{module}' installed successfully.")

install_missing_modules(required_modules)

# Импорт модуля cv2 после установки всех необходимых модулей
import cv2
import glob

# Определение пути к папке MyScripts
current_dir = os.path.dirname(os.path.abspath(__file__))
my_scripts_path = current_dir

# Пути к папкам Input и Output относительно папки MyScripts
input_path = os.path.join(my_scripts_path, 'Downscale', 'Input')
output_path = os.path.join(my_scripts_path, 'Downscale', 'Output')

# Создание папок, если они не существуют
for path in [input_path, output_path]:
    if not os.path.exists(path):
        os.makedirs(path)
        print("Directory", path, "created.")
    else:
        print("Directory", path, "already exists.")

files = glob.glob(os.path.join(input_path, '*.*g'))
for f, file in enumerate(files[:]):
    filename = os.path.basename(file)
    img = cv2.imread(file, cv2.IMREAD_COLOR)
    #img_scale = cv2.resize(img, (1920, 1080), interpolation=cv2.INTER_LANCZOS4)
    img_scale = cv2.resize(img, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_LANCZOS4)
    cv2.imwrite(os.path.join(output_path, '.'.join(filename.split('.')[:-1]) + '.png'), img_scale)
