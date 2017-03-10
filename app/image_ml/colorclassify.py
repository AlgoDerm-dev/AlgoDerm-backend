def determineColor(rgb, hsl):
    color = None
    if determine_GREY(rgb):
        color =  "Grey"
    elif determine_BLACK(rgb):
        color =  "Black"
    elif determine_WHITE(rgb):
        color =  "White"
    elif hsl[0] >= 355 or hsl[0] <= 10:
        color =  determine_RED(rgb)
    elif hsl[0] > 10 and hsl[0] <= 20:
        color =  determine_RED_ORANGE(hsl)
    elif hsl[0] > 20 and hsl[0] <= 40:
        color =  determine_ORANGE(rgb)
    elif hsl[0] > 40 and hsl[0] <= 50:
        color =  determine_ORANGE_YELLOW(rgb)
    elif hsl[0] > 50 and hsl[0] <= 60:
        color =  determine_YELLOW(rgb)
    elif hsl[0] > 60 and hsl[0] <= 80:
        color =  determine_YELLOW_GREEN(rgb)
    elif hsl[0] > 80 and hsl[0] <= 140:
        color =  "Green"
    elif hsl[0] > 140 and hsl[0] <= 169:
        color =  determine_GREEN_CYAN(hsl)
    elif hsl[0] > 169 and hsl[0] <= 200:
        color =  determine_CYAN(hsl)
    elif hsl[0] > 200 and hsl[0] <= 220:
        color =  determine_CYAN_BLUE(hsl)
    elif hsl[0] > 220 and hsl[0] <= 240:
        color =  "Blue"
    elif hsl[0] > 240 and hsl[0] <= 280:
        color =  "Blue-Magenta"
    elif hsl[0] > 280 and hsl[0] <= 320:
        color =  "Magenta"
    elif hsl[0] > 320 and hsl[0] <= 330:
        color =  "Magenta-Pink"
    elif hsl[0] > 330 and hsl[0] <= 345:
        color =  determine_PINK(rgb)
    elif hsl[0] > 345 and hsl[0] <= 355:
        color =  determine_PINK_RED(rgb)
    return color

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
    if abs(rgb[0] - rgb[1]) <= 15 and abs(rgb[2] - rgb[1]) <= 15 and abs(rgb[0] - rgb[2]) <= 15:
        return True
    else:
        return False