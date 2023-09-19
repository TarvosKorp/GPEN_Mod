from PIL import Image
import os

# Пути к папкам и маске
folder1 = "/content/GPEN_Mod/examples/outs/Combined/"
folder2 = "/content/CodeFormer/results/imgs_1.0/final_results/"
mask_path = "/content/GPEN_Mod/Combine/Mask.png"

# Папка для сохранения результатов
output_folder = "/content/GPEN_Mod/Final_1024/"
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# Получаем список файлов в папках
files1 = sorted([f for f in os.listdir(folder1) if os.path.isfile(os.path.join(folder1, f))])
files2 = sorted([f for f in os.listdir(folder2) if os.path.isfile(os.path.join(folder2, f))])

# Проверяем, что количество файлов одинаковое
if len(files1) != len(files2):
    print("Количество файлов в папках не совпадает.")
else:
    # Загружаем маску
    mask = Image.open(mask_path)

    for file1, file2 in zip(files1, files2):
        # Открываем изображения из обеих папок
        img1 = Image.open(os.path.join(folder1, file1))
        img2 = Image.open(os.path.join(folder2, file2))

        # Проверяем, что размеры изображений совпадают
        if img1.size != img2.size:
            print(f"Размеры изображений {file1} и {file2} не совпадают.")
            continue

        # Накладываем маску
        result = Image.composite(img1, img2, mask)

        # Даунскейлим изображение в 2 раза с использованием INTER_LANCZOS4
        result = result.resize((result.width // 2, result.height // 2), Image.LANCZOS)

        # Сохраняем результат в указанную папку
        output_path = os.path.join(output_folder, file1)
        result.save(output_path, "PNG")

    print("Завершено.")
