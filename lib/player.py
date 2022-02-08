

def dir_to_angle(dir: list) -> int:
    angle = 0
    dir_sorted = sorted(dir)
    if len(dir_sorted) > 0:
        if ["left", "up"] == dir_sorted:
            angle = 180 + 90/2
        elif ["right", "up"] == dir_sorted:
            angle = 135
        elif ["down", "left"] == dir_sorted:
            angle = 315
        elif ["down", "right"] == dir_sorted:
            angle = 45
        elif ["up"] == dir_sorted:
            angle = 180
        elif ["down"] == dir_sorted:
            angle = 0
        elif ["left"] == dir_sorted:
            angle = 270
        elif ["right"] == dir_sorted:
            angle = 90
    return angle
