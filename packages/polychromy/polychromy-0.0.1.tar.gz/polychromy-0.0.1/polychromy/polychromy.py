import os
import sys
import json

print()

hex_colors = {
    "Alice Blue": "#F0F8FF", "Antique White": "#FAEBD7", "Aqua": "#00FFFF", "Aquamarine": "#7FFFD4", "Azure": "#F0FFFF",
    "Beige": "#F5F5DC", "Bisque": "#FFE4C4", "Black": "#000000", "Blanched Almond": "#FFEBCD", "Blue": "#0000FF", "Blue Violet": "#8A2BE2", "Brown": "#A52A2A", "Burly Wood": "#DEB887",
    "Cadet Blue": "#5F9EA0", "Chartreuse": "#7FFF00", "Chocolate": "#D2691E", "Coral": "#FF7F50", "Cornflower Blue": "#6495ED", "Corn Silk": "#FFF8DC", "Cosmic Latte": "#FFF8E7", "Crimson": "#DC143C", "Cyan": "#00FFFF",
    "Dark Blue": "#00008B", "Dark Cyan": "#008B8B", "Dark Golden Rod": "#B8860B", "Dark Gray": "#A9A9A9", "Dark Green": "#006400", "Dark Khaki": "#BDB76B", "Dark Magenta": "#8B008B", "Dark Olive Green": "#556B2F", "Dark Orange": "#FF8C00", "Dark Orchid": "#9932CC", "Dark Red": "#8B0000", "Dark Salmon": "#E9967A", "Dark Sea Green": "#8FBC8F", "Dark Slate Blue": "#483D8B", "Dark Slate Gray": "#2F4F4F", "Dark Turquoise": "#00CED1", "Dark Violet": "#9400D3", "Deep Pink": "#FF1493", "Deep Sky Blue": "#00BFFF", "Dim Gray": "#696969", "Dodger Blue": "#1E90FF",
    "Firebrick": "#B22222", "Floral White": "#FFFAF0", "Forest Green": "#228B22", "Fuchsia": "#FF00FF",
    "Gainsboro Gray": "#DCDCDC", "Ghost White": "#F8F8FF", "Gold": "#FFD700", "Goldenrod": "#DAA520", "Gray": "#808080", "Green": "#008000", "Green Yellow": "#ADFF2F",
    "Honeydew": "#F0FFF0", "Hot Pink": "#FF69B4",
    "Indian Red": "#CD5C5C", "Indigo": "#4B0082", "Ivory": "#FFFFF0", 
    "Khaki": "#F0E68C",
    "Lavender": "#E6E6FA", "Lavender Blush": "#FFF0F5", "Lawn Green": "#7CFC00", "Lemon Chiffon": "#FFFACD", "Light Blue": "#ADD8E6", "Light Coral": "#F08080", "Light Cyan": "#E0FFFF", "Light Goldenrod Yellow": "#FAFAD2", "Light Green": "#90EE90", "Light Gray": "#D3D3D3", "Light Pink": "#FFB6C1", "Light Salmon": "#FFA07A", "Light Sea Green": "#20B2AA", "Light Sky Blue": "#87CEFA", "Light Slate Gray": "#778899", "Light Steel Blue": "#B0C4DE", "Light Yellow": "#FFFFE0", "Lime": "#00FF00", "Lime Green": "#32CD32", "Linen": "#FAF0E6",
    "Magenta": "#FF00FF", "Maroon": "#800000", "Medium Aquamarine": "#66CDAA", "Medium Blue": "#0000CD", "Medium Orchid": "#BA55D3", "Medium Purple": "#9370DB", "Medium Sea Green": "#3CB371", "Medium Slate Blue": "#7B68EE", "Medium Spring Green": "#00FA9A", "Medium Turquoise": "#48D1CC", "Medium Violet Red": "#C71585", "Midnight Blue": "#191970", "Mint Cream": "#F5FFFA", "Misty Rose": "#FFE4E1", "Moccasin": "#FFE4B5",
    "Navajo White": "#FFDEAD", "Navy": "#000080",
    "Old Lace": "#FDF5E6", "Olive": "#808000", "Olive Drab": "#6B8E23", "Orange": "#FFA500", "Orange Red": "#FF4500", "Orchid": "#DA70D6", 
    "Pale Goldenrod": "#EEE8AA", "Pale Green": "#98FB98", "Pale Turquoise": "#AFEEEE", "Pale Violet Red": "#DB7093", "Papaya Whip": "#FFEFD5", "Peach Puff": "#FFDAB9", "Peru": "#CD853F", "Pink": "#FFC0CB", "Plum": "#DDA0DD", "Powder Blue": "#B0E0E6", "Purple": "#800080",
    "Red": "#FF0000", "Rosy Brown": "#BC8F8F", "Royal Blue": "#4169E1",
    "Saddle Brown": "#8B4513", "Salmon": "#FA8072", "Sandy Brown": "#FAA460", "Sea Green": "#2E8B57", "Seashell": "#FFF5EE", "Sienna": "#A0522D", "Silver": "#C0C0C0", "Sky Blue": "#87CEEB", "Slate Blue": "#6A5ACD", "Slate Gray": "#708090", "Snow": "#FFFAFA", "Spring Green": "#00FF7F", "Steel Blue": "#4682B4",
    "Tan": "#D2B48C", "Teal": "#008080", "Thistle": "#D8BFD8", "Tomato": "#FF6347", "Turquoise": "#40E0D0",
    "Violet": "#EE82EE",
    "Wheat": "#F5DEB3", "White": "#FFFFFF", "White Smoke": "#F5F5F5",
    "Yellow": "#FFFF00", "Yellow Green": "#9ACD32"
}

rgb_colors = {
    "Alice Blue": "240;248;255", "Antique White": "250;235;215", "Aqua": "0;255;255", "Aquamarine": "127;255;212", "Azure": "240;255;255",
    "Beige": "245;245;220", "Bisque": "255;228;196", "Black": "0;0;0", "Blanched Almond": "255;235;205", "Blue": "0;0;255", "Blue Violet": "138;43;226", "Brown": "165;42;42", "Burly Wood": "222;184;135",
    "Cadet Blue": "95;158;160", "Chartreuse": "127;255;0", "Chocolate": "210;105;30", "Coral": "255;127;80", "Cornflower Blue": "100;149;237", "Corn Silk": "255;248;220", "Cosmic Latte": "255;248;231", "Crimson": "220;20;60", "Cyan": "0;255;255",
    "Dark Blue": "0;0;139", "Dark Cyan": "0;139;139", "Dark Golden Rod": "184;134;11", "Dark Gray": "169;169;169", "Dark Green": "0;100;0", "Dark Khaki": "189;183;107", "Dark Magenta": "139;0;139", "Dark Olive Green": "85;107;47", "Dark Orange": "255;140;0", "Dark Orchid": "153;50;204", "Dark Red": "139;0;0", "Dark Salmon": "233;150;122", "Dark Sea Green": "143;188;143", "Dark Slate Blue": "72;61;139", "Dark Slate Gray": "47;79;79", "Dark Turquoise": "0;206;209", "Dark Violet": "148;0;211", "Deep Pink": "255;20;147", "Deep Sky Blue": "0;191;255", "Dim Gray": "105;105;105", "Dodger Blue": "30;144;255",
    "Firebrick": "178;34;34", "Floral White": "255;250;240", "Forest Green": "34;139;34", "Fuchsia": "255;0;255",
    "Gainsboro Gray": "220;220;220", "Ghost White": "248;248;255", "Gold": "255;215;0", "Goldenrod": "218;165;32", "Gray": "128;128;128", "Green": "0;128;0", "Green Yellow": "173;255;47",
    "Honeydew": "240;255;240", "Hot Pink": "255;105;180",
    "Indian Red": "205;92;92", "Indigo": "75;0;130", "Ivory": "255;255;240",
    "Khaki": "240;230;140",
    "Lavender": "230;230;250", "Lavender Blush": "255;240;245", "Lawn Green": "124;252;0", "Lemon Chiffon": "255;250;205", "Light Blue": "173;216;230", "Light Coral": "240;128;128", "Light Cyan": "224;255;255", "Light Goldenrod Yellow": "250;250;210", "Light Green": "144;238;144", "Light Gray": "211;211;211", "Light Pink": "255;182;193", "Light Salmon": "255;160;122", "Light Sea Green": "32;178;170", "Light Sky Blue": "135;206;250", "Light Slate Gray": "119;136;153", "Light Steel Blue": "176;196;222", "Light Yellow": "255;255;224", "Lime": "0;255;0", "Lime Green": "50;205;50", "Linen": "250;240;230",
    "Magenta": "255;0;255", "Maroon": "128;0;0", "Medium Aquamarine": "102;205;170", "Medium Blue": "0;0;205", "Medium Orchid": "186;85;211", "Medium Purple": "147;112;219", "Medium Sea Green": "60;179;113", "Medium Slate Blue": "123;104;238", "Medium Spring Green": "0;250;154", "Medium Turquoise": "72;209;204", "Medium Violet Red": "199;21;133", "Midnight Blue": "25;25;112", "Mint Cream": "245;255;250", "Misty Rose": "255;228;225", "Moccasin": "255;228;181",
    "Navajo White": "255;222;173", "Navy": "0;0;128",
    "Old Lace": "253;245;230", "Olive": "128;128;0", "Olive Drab": "107;142;35", "Orange": "255;165;0", "Orange Red": "255;69;0", "Orchid": "218;112;214",
    "Pale Goldenrod": "238;232;170", "Pale Green": "152;251;152", "Pale Turquoise": "175;238;238", "Pale Violet Red": "219;112;147", "Papaya Whip": "255;239;213", "Peach Puff": "255;218;185", "Peru": "205;133;63", "Pink": "255;192;203", "Plum": "221;160;221", "Powder Blue": "176;224;230", "Purple": "128;0;128",
    "Red": "255;0;0", "Rosy Brown": "188;143;143", "Royal Blue": "65;105;225",
    "Saddle Brown": "139;69;19", "Salmon": "250;128;114", "Sandy Brown": "250;164;96", "Sea Green": "46;139;87", "Seashell": "255;245;238", "Sienna": "160;82;45", "Silver": "192;192;192", "Sky Blue": "135;206;235", "Slate Blue": "106;90;205", "Slate Gray": "112;128;144", "Snow": "255;250;250", "Spring Green": "0;255;127", "Steel Blue": "70;130;180",
    "Tan": "210;180;140", "Teal": "0;128;128", "Thistle": "216;191;216", "Tomato": "255;99;71", "Turquoise": "64;224;208",
    "Violet": "238;130;238",
    "Wheat": "245;222;179", "White": "255;255;255", "White Smoke": "245;245;245",
    "Yellow": "255;255;0", "Yellow Green": "154;205;50",
}


def main():

    text = []
    
    if len(sys.argv) == 1:

        color_in = rgb_colors["Pale Turquoise"]
        comment_1 = "  ^^^ Returning color name"
        comment_2 = "Returning HEX code ^^^"
        comment_3 = "Returning RGB code ^^^"
        
    else:

        color_in = sys.argv[1]
        comment_1 = ""
        comment_2 = ""
        comment_3 = ""

    color_name, color_hex, color_rgb, unknown = valid_color(color_in)

    if unknown:
        r,g,b = "???"
        cr = 255
        cg = 0
        cb = 0
    else:
        r,g,b = color_rgb.split(";")
        cr = abs(int(r)-255)
        cg = abs(int(g)-255)
        cb = abs(int(b)-255)

    text = [
            "{:<26}".format(f"{color_name}"),
            "{:^26}".format(f"{comment_1}"),
            "{:^26}".format(""),
            "{:^26}".format(""),
            "{:<26}".format("Hex triplet:"),
            "{:>26}".format(f"{color_hex}"),
            "{:^26}".format(f"{comment_2}"),
            "{:<26}".format("sRGB (r, g, b):"),
            "{:>26}".format(f"{r},{g},{b}"),
            "{:^26}".format(f"{comment_3}"),
    ]

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


def valid_color(color):

    text = []
    unknown = False

    if color.title() in rgb_colors.keys():
        color_name = color.title()
        color_hex = hex_colors[color_name]
        color_rgb = rgb_colors[color_name]

    elif color in rgb_colors.values():
        color_name = list(rgb_colors.keys())[list(rgb_colors.values()).index(color)]
        color_hex = hex_colors[color_name]
        color_rgb = color

    elif color.upper() in hex_colors.values():
        color_name = list(hex_colors.keys())[list(hex_colors.values()).index(color.upper())]
        color_hex = color.upper()
        color_rgb = rgb_colors[color_name]

    else:
        color_name = f"{color} Unknown Colour"
        color_hex = "#??????"
        color_rgb = rgb_colors["Light Gray"]
        unknown = True

    return color_name, color_hex, color_rgb, unknown


if __name__ == "__main__":
    main()