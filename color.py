from strip import ColorTuple
import colorsys


def calculate_color_percent(color: ColorTuple, percent: float) -> ColorTuple:
    return tuple(int(percent * c) for c in color)


def wheel(position: int) -> ColorTuple:
    if position < 85:
        return position * 3, 255 - position * 3, 0
    elif position < 170:
        position -= 85
        return 255 - position * 3,  0, position * 3
    else:
        position -= 170
        return 0, position * 3, 255 - position * 3


def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def antipodal_index(count: int, i: int):
    top = count // 2
    iN = i + top

    if i >= top:
        iN = (i + top) % count

    return iN

