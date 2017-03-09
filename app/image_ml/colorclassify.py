def determineColor(rgb, hsl):
    if determine_GREY(rgb):
        return "Grey"
    elif determine_BLACK(rgb):
        return "Black"
    elif determine_WHITE(rgb):
        return "White"
    elif hsl[0] >= 355 or hsl[0] <= 10:
        return determine_RED(rgb)
    elif hsl[0] >= 11 and hsl[0] <= 20:
        return determine_RED_ORANGE(hsl)
    elif hsl[0] >= 21 and hsl[0] <= 40:
        return determine_ORANGE(rgb)
    elif hsl[0] >= 41 and hsl[0] <= 50:
        return determine_ORANGE_YELLOW(rgb)
    elif hsl[0] >= 51 and hsl[0] <= 60:
        return determine_YELLOW(rgb)
    elif hsl[0] >= 61 and hsl[0] <= 80:
        return determine_YELLOW_GREEN(rgb)
    elif hsl[0] >= 81 and hsl[0] <= 140:
        return "Green"
    elif hsl[0] >= 141 and hsl[0] <= 169:
        return determine_GREEN_CYAN(hsl)
    elif hsl[0] >= 170 and hsl[0] <= 200:
        return determine_CYAN(hsl)
    elif hsl[0] >= 201 and hsl[0] <= 220:
        return determine_CYAN_BLUE(hsl)
    elif hsl[0] >= 221 and hsl[0] <= 240:
        return "Blue"
    elif hsl[0] >= 241 and hsl[0] <= 280:
        return "Blue-Magenta"
    elif hsl[0] >= 281 and hsl[0] <= 320:
        return "Magenta"
    elif hsl[0] >= 321 and hsl[0] <= 330:
        return "Magenta-Pink"
    elif hsl[0] >= 331 and hsl[0] <= 345:
        return determine_PINK(rgb)
    elif hsl[0] >= 346 and hsl[0] <= 355:
        return determine_PINK_RED(rgb)

def determine_RED(rgb):
    sum = rgb[0] + rgb[1] + rgb[2]
    if sum < 100:
        return "Brown"
    elif sum > 439:
        return "Pink"
    return "Red"

def determine_RED_ORANGE(hsl):
    if hsl[2] <= 35:
        return "Brown"
    return "Red-Orange"

def determine_ORANGE(rgb):
    if rgb[0] < 200:
        return "Brown"
    return "Orange"

def determine_ORANGE_YELLOW(rgb):
    if rgb[0] < 200:
        return "Brown"
    return "Orange-Yellow"

def determine_YELLOW(rgb):
    if rgb[0] < 190:
        return "Brown"
    return "Yellow"

def determine_YELLOW_GREEN(rgb):
    if rgb[0] < 165:
        return "Green"
    return "Yellow-Green"

def determine_GREEN_CYAN(hsl):
    if hsl[2] < 25:
        return "Green"
    return "Green-Cyan"

def determine_CYAN(hsl):
    if hsl[2] < 25:
        return "Blue"
    return "Cyan"

def determine_CYAN_BLUE(hsl):
    if hsl[2] < 40:
        return "Blue"
    return "Cyan-Blue"

def determine_PINK(rgb):
    if rgb[0] < 150:
        return "Brown"
    return "Pink"

def determine_PINK_RED(rgb):
    if rgb[0] < 128:
        return "Brown"
    return "Pink-Red"

def determine_WHITE(rgb):
    if abs(rgb[0] - 255) <= 20 and abs(rgb[2] - 255) <= 20 and abs(rgb[1] - 255) <= 20:
        return True
    else:
        return False

def determine_BLACK(rgb):
    if abs(rgb[0] - 0) <= 20 and abs(rgb[2] - 0) <= 20 and abs(rgb[1] - 0) <= 20:
        return True
    else:
        return False

def determine_GREY(rgb):
    if abs(rgb[0] - rgb[1]) <= 30 and abs(rgb[2] - rgb[1]) <= 30 and abs(rgb[0] - rgb[2]) <= 30:
        return True
    else:
        return False