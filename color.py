from strip import ColorTuple


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
