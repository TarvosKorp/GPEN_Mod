import os
import subprocess

required_modules = ['os', 'pillow']

def install_missing_modules(modules):
    for module in modules:
        try:
            __import__(module)
        except ImportError:
            print(f"Module '{module}' is missing. Installing...")
            subprocess.check_call(['pip', 'install', module])
            print(f"Module '{module}' installed successfully.")

install_missing_modules(required_modules)

from PIL import Image
import os.path

from os import listdir
from os.path import isfile
from os.path import join as joinpath


#mypath = "D:/Neural Results/GPEN_FULL/"
mypath = "C:/Users/Haldjarvi/Desktop/Notes/Compare/"
final = (mypath + "Final/")
if not os.path.exists(final):
    os.mkdir(final)

mylist = []
myimage = []
mymask = []

def GetFiles():
    # получаем список файлов в папке в список
    for f in listdir(mypath):
        if isfile(joinpath(mypath, f)):
            try:
                if f[-6] == "_":
                    # если это нужный нам файл открываем его и засовывает в список
                    myimage.append(Image.open(mypath+f))
                    mylist.append(f)

            except Exception:
                pass

    return len(myimage)

def GetMask():
    # цикл от 2 до 6, открывам маски
    for i in range(2, 7):
        mymask.append(Image.open(mypath + "/mask/" + str(i) + ".png").convert('L'))

def MakeImage():
    res1 = Image.composite(myimage[2], myimage[0], mymask[1])
    res2 = Image.composite(myimage[1], res1, mymask[0])
    res3 = Image.composite(myimage[3], res2, mymask[2])
    res4 = Image.composite(myimage[5], res3, mymask[4])
    res = Image.composite(myimage[4], res4, mymask[3])


    # формирование имени
    str = mylist[0].split('.')[0]
    l = len(str)
    name = str[:l - 2]

    res.save(final + name + ".png", "PNG")

    # удаляем из массива отработанные файлы
    for i in range(0, 6):
        myimage.remove(myimage[0])
        mylist.remove(mylist[0])


# вход
if __name__ == '__main__':
    count = GetFiles()/6
    GetMask()
    for i in range(0, int(count)):
        MakeImage()
