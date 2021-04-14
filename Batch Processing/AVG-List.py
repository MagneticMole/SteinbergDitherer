import sys
from colorthief import ColorThief

file_path = sys.argv[1]
color_thief = ColorThief(file_path)
num_colors = int(sys.argv[2])
qual_colors = int(sys.argv[3])
output = color_thief.get_palette(color_count= num_colors, quality= qual_colors)
with open("pallet_dump.txt", "a+") as dump:
    dump.write(file_path + "\n" + str(output)+ "\n\n")
sys.exit()
