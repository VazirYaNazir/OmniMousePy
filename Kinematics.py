import math
import pyautogui
import time

last_update_time = 0
update_interval = 0.005

target_x, target_y = pyautogui.position()

def adjust_mouse(adjusted_roll, adjusted_pitch) -> None:
    global last_update_time, target_x, target_y
    current_time = time.time()

    if current_time - last_update_time < update_interval:
        return

    last_update_time = current_time

    roll_sens = 0.5
    pitch_sens = 0.5

    max_pitch = 50.0
    max_roll = 50.0

    normalized_pitch = max(-1, min(1, adjusted_pitch / max_pitch)) * pitch_sens
    normalized_roll = max(-1, min(1, adjusted_roll / max_roll)) * roll_sens

    target_x += normalized_roll * 10
    target_y += normalized_pitch * 10

    screen_width, screen_height = pyautogui.size()
    target_x = max(0, min(screen_width - 1, int(target_x)))
    target_y = max(0, min(screen_height - 1, int(target_y)))

    current_x, current_y = pyautogui.position()

    rel_x = target_x - current_x
    rel_y = target_y - current_y

    distance = math.sqrt(rel_x ** 2 + rel_y ** 2)

    if distance > 100:
        smooth_factor = 10
    elif distance > 50:
        smooth_factor = 5
    elif distance > 20:
        smooth_factor = 2
    else:
        smooth_factor = 1

    rel_x //= smooth_factor
    rel_y //= smooth_factor

    pyautogui.moveRel(rel_x, rel_y)
    time.sleep(0.001)