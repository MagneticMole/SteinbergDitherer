import sys
import cv2
import Ditherer as dith
from colorthief import ColorThief
from PIL import Image
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

root = tk.Tk()
root.withdraw()

global color_thief

found_image = 0
while found_image == 0:
    try:
        file_path = filedialog.askopenfilename()
        color_thief = ColorThief(file_path)
        image = cv2.imread(file_path)
        found_image = 1
    except:
        print('Incorrect file type. Only accepts pictures.')

ditherer = dith.Steinberg(image)
options = ['1', '2', '3', '4']
choice = ''
print('Choose dithering method: ')
while choice not in options:
    print('\t1. Two-Tone')
    print('\t2. RGB')
    print('\t3. Extract Pallet')
    print('\t4. Average Pallet')

    choice = input('Choice: ')
if choice == '1':
    ditherer.dither2Tone()
if choice == '2':
    ditherer.dither()
if choice == '3':
    im = Image.open(file_path)
    pixels = list(im.getdata())
    output = list(dict.fromkeys(pixels))
    print(output)
    sys.exit()
elif choice == '4':
    num_colors = int(input('Number of colors to generate: '))
    qual_colors = int(input('Quality of the sarch: '))
    output = color_thief.get_palette(color_count= num_colors, quality= qual_colors)
    with open("EXT_VALUES.txt", "w+") as dump:
        dump.write(file_path + "\n" + str(output)+ "\n\n")
    sys.exit()
    
print('Done')
ditherer.show()
