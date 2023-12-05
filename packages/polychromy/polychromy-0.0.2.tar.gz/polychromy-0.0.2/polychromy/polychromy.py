import os
import re
import sys
import json
from textlinebreaker import split_line

# Get the current directory of the module
module_dir = os.path.dirname(__file__)

# Navigate to the parent directory and then to the "data" directory
parent_dir = os.path.abspath(os.path.join(module_dir, ".."))
json_file_path = os.path.join(parent_dir, "data", "colors.json")

# Check if the file exists
if os.path.exists(json_file_path):
    
    # Load the JSON file
    with open(json_file_path, "r") as file:
        all_colors = json.load(file)
    # Now 'all_colors' contains the content of the JSON file
else:
    print(f"File '{json_file_path}' not found.")

print()


def color_show(color_in=""):

    text = []
    
    if color_in != "":
        comment_1 = ""
        comment_2 = ""
        comment_3 = ""
        pass

    elif len(sys.argv) == 1:

        color_in = all_colors["Pale Turquoise"]["rgb"]
        comment_1 = "  ^^^ Returning color name"
        comment_2 = "Returning HEX code ^^^"
        comment_3 = "Returning RGB code ^^^"
        
    else:

        color_in = sys.argv[1]
        comment_1 = ""
        comment_2 = ""
        comment_3 = ""

    color_name, alt_names, color_hex, color_rgb, unknown = color_details(color_in)

    if unknown:
        rgb_out = color_rgb
        color_rgb = all_colors["Light Gray"]["rgb"]
        cr = 255
        cg = 0
        cb = 0
    else:
        r,g,b = color_rgb.split(";")
        rgb_out = f"{r},{g},{b}"
        cr = abs(int(r)-255)
        if 100<cr<150:
            cr =  255
        cg = abs(int(g)-255)
        if 100<cg<150:
            cg =  255
        cb = abs(int(b)-255)
        if 100<cb<150:
            cb =  255
    
    l = 0
    for line in split_line(f"{color_name}",26):
        text.append(line)
        l += 1
    for line in split_line(f"({alt_names})",26):
        text.append(line)
        l += 1
    if l < 5:
        text.append("{:^26}".format(f"{comment_1}"))
    if l < 6:
        text.append("{:^26}".format(""))
    text.append("{:<26}".format("Hex triplet:"))
    text.append("{:>26}".format(f"{color_hex}"))
    if l < 3:
        text.append("{:^26}".format(f"{comment_2}"))
    text.append("{:<26}".format("sRGB (r, g, b):"))
    text.append("{:>26}".format(f"{rgb_out}"))
    if l < 4:
        text.append("{:^26}".format(f"{comment_3}"))

    # Retrieve terminal width and setting up frame size
    adjustment = " " * int(((os.get_terminal_size().columns) - (40)) / 2)
    or_line = "═" * 38
    filling = " " * 38
    side_space = " " * 6

    # Printing color details

    display_menu  = adjustment + f"\033[38;2;{cr};{cg};{cb};48;2;{color_rgb}m" + "╔" + or_line + "╗" + "\033[0m" + "\n"
    display_menu += adjustment + f"\033[38;2;{cr};{cg};{cb};48;2;{color_rgb}m" + "║" + filling + "║" +"\033[0m\n"
    
    for item in text:
        display_menu += adjustment + f"\033[38;2;{cr};{cg};{cb};48;2;{color_rgb}m" + "║" + side_space + item + side_space + "║" +"\033[0m\n"
    
    display_menu += adjustment + f"\033[38;2;{cr};{cg};{cb};48;2;{color_rgb}m" + "║" + filling + "║" + "\033[0m\n"
    display_menu += adjustment + f"\033[38;2;{cr};{cg};{cb};48;2;{color_rgb}m" + "╚" + or_line + "╝" + "\033[0m\n"

    print(display_menu)


def valid_color(color, text=True):

    if text:
        ansi_colours = {
    "Black": 30, "Red": 31, "Green": 32, "Yellow": 33, "Blue": 34, "Magenta": 35, "Cyan": 36, "White": 37,
    "Bright Black": 90, "Bright Red": 91, "Bright Green": 92, "Bright Yellow": 93, "Bright Blue": 94, "Bright Magenta": 95, "Bright Cyan": 96, "Bright White": 97,
    "Reset": 0,
    }
    else:
        ansi_colours = {
    "Black": 40, "Red": 41, "Green": 42, "Yellow": 43, "Blue": 44, "Magenta": 45, "Cyan": 46, "White": 47,
    "Bright Black": 100, "Bright Red": 101, "Bright Green": 102, "Bright Yellow": 103, "Bright Blue": 104, "Bright Magenta": 105, "Bright Cyan": 106, "Bright White": 107,
    "Reset": 0,
    }

    try:
        _, _, _, color_rgb, unknown = color_details(color)
        if unknown:
            if text:
                return 15
            else:
                return 0
        else:
            return color_rgb
    except:
        ...


def color_details(color):

    text = []
    unknown = False

    # Check if the color name is in the list of colors
    
    if color.title() in all_colors.keys():
        color_name = color.title()

    # Check if the RGB color code is valid and in the list of colors
    
    elif matches := re.search("^([0-9]*;[0-9]*;[0-9]*)$", color):

        r,g,b = color.split(";")

        if (0<=int(r)<=255) and (0<=int(g)<=255) and (0<=int(b)<=255):

            try:
                color_name = list(all_colors.keys())[list(map(lambda x: x['rgb'], all_colors.values())).index(matches.group(1))]
            except:
                return _no_name(matches.group(1))
            
        # Return an error message for an invalid color code
        else:
            return _invalid_range()
                
    # Check if the HEX color code is valid and in the list of colors
    elif matches := re.search("^(#[0-9A-Za-z]{6})$", color):
        color = matches.group(1).upper()
        try:
            color_name = list(all_colors.keys())[list(map(lambda x: x['hex'], all_colors.values(color))).index()]
        except:
            if matches := re.search("^(#[0-9A-F]{6})$", color):
                return _no_name(matches.group(1))
            
            # Return an error message for an invalid color range
            else:
                return _invalid_range()

    # Return an error message for an unknown color name
    else:
        color_name = f"Color '{color.title()}' Unknown"
        alt_names = f"No other names known for '{color.title()}'"
        color_hex = "#??????"
        color_rgb = "???,???,???"
        unknown = True
        return color_name, alt_names, color_hex, color_rgb, unknown

    # Get the HEX and RGB values of the given color
    alt_names = all_colors[color_name]["alt"] # This will include alternative names
    color_hex = all_colors[color_name]["hex"]
    color_rgb = all_colors[color_name]["rgb"]
    

    return color_name, alt_names, color_hex, color_rgb, unknown


def _no_name(color):
    color_name = "Name Unknown"
    
    try:
        r,g,b = color.split(";")
    except:
        r = int(color[1:3],16)
        g = int(color[3:5],16)
        b = int(color[5:7],16)

    alt_names = "No other names known"
    color_hex = f"#{hex(int(r))[2:].zfill(2)}{hex(int(g))[2:].zfill(2)}{hex(int(b))[2:].zfill(2)}"
    color_rgb = f"{r};{g};{b}"
    
    return color_name, alt_names, color_hex, color_rgb, False


def _invalid_range():
    color_name = "Invalid Color Range!"
    alt_names = ""
    color_hex = "#[00-FF][00-FF][00-FF]"
    color_rgb = "[0-255],[0-255],[0-255]"
    
    return color_name, alt_names, color_hex, color_rgb, True


if __name__ == "__main__":
    color_show()
