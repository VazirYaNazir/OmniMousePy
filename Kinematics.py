import math
import pyautogui





def adjust_mouse(adjusted_roll, adjusted_pitch) -> None:
    #set sensitivity for movement:
    roll_sens = 0.25
    pitch_sens = 0.25

    #set max pitch and roll angle:
    max_pitch = 30
    max_roll = 30

    #Screen dimensions:
    screen_width, screen_height = pyautogui.size()

    #normalized movement:
    normalized_pitch = max(-1, min(1, adjusted_pitch/max_pitch))
    normalized_roll = max(-1, min(1, adjusted_roll/max_roll))

    target_x = int(screen_width/2 + normalized_roll * (screen_width/2)) * roll_sens
    target_y= int(screen_height/2 + normalized_pitch * (screen_height/2)) * pitch_sens

    #ensure target co-ords are within screen bounds
    target_x = max(0, min(screen_width - 1, target_x))
    target_y = max(0, min(screen_height - 1, target_y))

    #move Mouse to co-ordinate
    pyautogui.moveTo(target_x, target_y)
