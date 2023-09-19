from PIL import Image
import os.path

from os import listdir
from os.path import isfile
from os.path import join as joinpath

mypath = "/content/GPEN_Mod/examples/outs/"
maskpath = "/content/GPEN_Mod/Combine/"
final = (mypath + "Combined/")
if not os.path.exists(final):
    os.mkdir(final)

mylist = []
myimage = []
mymask = []

def GetFiles():
    global myimage, mylist  # Объявляем переменные как глобальные
    # получаем список файлов в папке в список
    image_files = sorted([f for f in listdir(mypath) if isfile(joinpath(mypath, f))])
    for f in image_files:
        try:
            if f.endswith("_1.png"):
                # если это начало новой группы, очищаем списки
                myimage = []
                mylist = []
            
            # если это нужный нам файл открываем его и засовывает в список
            myimage.append(Image.open(joinpath(mypath, f)))
            mylist.append(f)

            if len(myimage) == 6:
                # обрабатываем группу, если набралось 6 картинок
                MakeImage()
        except Exception:
            pass

    return len(myimage)

def GetMask():
    # цикл от 2 до 6, открывам маски
    for i in range(2, 7):
        mymask.append(Image.open(joinpath(maskpath, "mask", f"{i}.png")).convert('L'))

def MakeImage():
    global myimage, mylist  # Объявляем переменные как глобальные
    res1 = Image.composite(myimage[2], myimage[0], mymask[1])
    res2 = Image.composite(myimage[1], res1, mymask[0])
    res3 = Image.composite(myimage[3], res2, mymask[2])
    res4 = Image.composite(myimage[5], res3, mymask[4])
    res = Image.composite(myimage[4], res4, mymask[3])

    # формирование имени
    name = mylist[0].split('.')[0]
    l = len(name)
    name = name[:l - 2]

    output_path = joinpath(final, name + ".png")
    res.save(output_path, "PNG")
    #print(f"Saved {output_path}")

    # удаляем из массива отработанные файлы
    myimage.clear()
    mylist.clear()

# вход
if __name__ == '__main__':
    GetMask()
    GetFiles()
