import keyboard
import psutil
import pydirectinput
import pygetwindow as gw
import ray
import win32con
import win32gui
import win32process
from PIL import ImageGrab
from pyautogui import *
from python_imagesearch.imagesearch import *
from win32api import *

import macros

print_cd = 0
pyautogui.FAILSAFE = False
pydirectinput.FAILSAFE = False
already_checked_game_tips = False
script_start_time = time.perf_counter()
key_states = {"left": False, "right": False, "up": False, "down": False}
current_map = None
in_game = False
shoot_cd = 0

ray.init()


def main():
    global in_game
    global current_map
    time.sleep(3)

    while True:

        if get_process_name_of_focused_window() != "Paladins.exe":
            time.sleep(3)
            global_click(2,2)
            continue
        else:
            move_selected_window_to_top_left()
        #realtime_processor_for_movement_handling()
        time.sleep(.001)

        close_fucking_battle_pass_crap()
        close_annoying_ad()
        check_if_game_tips_are_still_on()
        queue_from_main_menu() #may set in_game to True

        while in_game:
            if get_process_name_of_focused_window() != "Paladins.exe":
                time.sleep(3)
                global_click(2,2)
                continue
            time.sleep(.001)

            close_fucking_battle_pass_crap()
            map_setter()

            if current_map is not None:
                champion_selection()

            result = legendary_selector()

            if result and current_map is not None:
                move_and_shoot()

            requeue()

            if is_on_main_menu(10):
                print("Main menu detected")
                in_game = False
                break


def itemization_handler():
    not_remote_hold_key_for("i", .05)
    time.sleep(.5)
    result = adap_image_search("Data\\Images\\turn_off_auto_purchase.PNG")
    if result:
        click(930, 329)
        time.sleep(.05)
    result = adap_image_search("Data\\Images\\item_shop.PNG")
    if not result:
        return
    time.sleep(1)
    double_click(640, 150)
    time.sleep(.5)
    double_click(642, 280)
    time.sleep(.5)
    double_click(368, 156)
    time.sleep(.5)
    double_click(507, 156)
    time.sleep(.5)
    not_remote_hold_key_for("i", .05)
    time.sleep(.5)


def queue_from_main_menu(game_mode = "onslaught"):
    global current_map
    p1 = adap_image_search("Data\\Images\\match_ready.PNG")
    if p1:
        current_map = None
        return

    result = adap_image_search("Data\\Images\\MainMenu.PNG")
    if result:
        result = adap_image_search("Data\\Images\\MainMenuGUI.PNG")
        if result:
            click(120, 116)
            time.sleep(2)
            click(618, 51)
            time.sleep(1.5)
            click(172, 315)
            time.sleep(2)
            while adap_image_search("Data\\Images\\in_queue.png", .9):
                time.sleep(.001)
        else:
            click(618, 51)
            time.sleep(1.5)
            click(172, 315)
            time.sleep(2)
            while adap_image_search("Data\\Images\\in_queue.png", .9):
                time.sleep(.001)
        global in_game

        current_map = None
        in_game = True

def in_a_match():
    if adap_image_search("Data\\Images\\LoadingScreenFlag.PNG", .95):
        while True:
            time.sleep(.001)
            if not adap_image_search("Data\\Images\\LoadingScreenFlag.PNG", .95):
                return True

def map_setter():
    global current_map
    global print_cd
    print_cd = get_script_uptime_ms()
    if get_script_uptime_ms() > print_cd:
        print("Is champ selection screen: "+str(is_champion_selection_screen())+" Current map: "+str(current_map))
        print_cd = get_script_uptime_ms() + 10000

    if is_champion_selection_screen() and current_map is None:
        print("Running map_setter()")
        maps = os.listdir("Data\\Images\\Maps")
        for m in maps.copy():
            if adap_image_search("Data\\Images\\Maps\\"+m):
                current_map = m.replace(".PNG", "")
                print("Current map is "+current_map)
                return
            print("Negative for "+m)

def is_cursor_confined():
    prev_position = pyautogui.position()
    time.sleep(0.1)  # Wait for a short interval
    new_position = pyautogui.position()

    # Check if the cursor is stuck at the same position
    return prev_position == new_position

def is_champion_selection_screen():
    result = adap_image_search("Data\\Images\\champion_selection_screen_flag.PNG", precision = .6)
    if result:
        return True
    else:
        return False

def champion_selection():
    if not is_champion_selection_screen():
        return
    image_path = "Data\\Images\\Barik.PNG"
    pos = get_image_position(image_path)
    if pos[0] != -1:
        click(pos[0]+3,pos[1]+3)
        time.sleep(.1)
        click(pos[0] + 3, pos[1] + 3)
        time.sleep(.5)
        click(589, 607)
        time.sleep(1)
        click(pos[0] + 3, pos[1] + 3)
        time.sleep(1)
        click(589, 607)
        time.sleep(1)
        p = get_image_position("Data\\Images\\LOCK_IN.PNG")
        click(p[0], p[1])
        time.sleep(1)

def in_queue():
    result = adap_image_search("Data\\Images\\in_queue.png")
    if result != -1:
        return True
    else:
        return False

def requeue():
    result = get_image_position("Data\\Images\\requeue.PNG")
    if result[0] != -1:
        click(result[0]+3,result[1]+3)
        time.sleep(.1)
        global current_map
        current_map = None
        time.sleep(2)
        SetCursorPos((5, 5))
        result = get_image_position("Data\\Images\\requeue.PNG")
        if result[0] != -1:
            pyautogui.keyDown("esc")
            time.sleep(.05)
            pyautogui.keyUp("esc")
            time.sleep(5)


def click(x,y):
    SetCursorPos((x+get_selected_window_position()[0],y+get_selected_window_position()[1]))
    mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.05)
    mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def global_click(x,y):
    SetCursorPos((x,y))
    mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.05)
    mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def double_click(x,y):
    SetCursorPos((x+get_selected_window_position()[0],y+get_selected_window_position()[1]))
    pyautogui.doubleClick(duration = .01)

def get_script_uptime_ms():
    current_time = time.perf_counter()
    elapsed_time_ms = int((current_time - script_start_time) * 1000)
    return elapsed_time_ms

def realtime_processor_for_movement_handling():
    if keyboard.is_pressed("up"):
        key_states["up"] = True
    if keyboard.is_pressed("down"):
        key_states["down"] = True
    if keyboard.is_pressed("right"):
        key_states["right"] = True
    if keyboard.is_pressed("left"):
        key_states["left"] = True
    if not keyboard.is_pressed("up"):
        key_states["up"] = False
    if not keyboard.is_pressed("down"):
        key_states["down"] = False
    if not keyboard.is_pressed("right"):
        key_states["right"] = False
    if not keyboard.is_pressed("left"):
        key_states["left"] = False

@ray.remote
def new_movement_handling(key, duration):
    func_start_time = get_script_uptime_ms()
    while get_script_uptime_ms() - func_start_time <= duration:
        if key == "left":
            pydirectinput.moveRel(-3, 0, relative=True, _pause=False)
        if key == "right":
            pydirectinput.moveRel(3, 0, relative=True, _pause=False)
        if key == "up":
            pydirectinput.moveRel(0, -3, relative=True, _pause=False)
        if key == "down":
            pydirectinput.moveRel(0, 3, relative=True, _pause=False)
        time.sleep(.001)

@ray.remote
def movement_handling(time_limit):
    thread_start_time = get_script_uptime_ms()
    while True:
        if get_script_uptime_ms() - thread_start_time >= time_limit:
            return

        if key_states["left"]:
            pydirectinput.moveRel(-3, 0, relative=True, _pause = False)
            print("Tried moving the mouse left")

        if key_states["right"]:
            pydirectinput.moveRel(3, 0, relative=True, _pause = False)
            print("Tried moving the mouse right")

        if key_states["up"]:
            pydirectinput.moveRel(0, -3, relative=True, _pause = False)
            print("Tried moving the mouse up")

        if key_states["down"]:
            pydirectinput.moveRel(0, 3, relative=True, _pause = False)
            print("Tried moving the mouse down")

        time.sleep(.001)

def new_movement_handling_non_remote(key, duration):
    func_start_time = get_script_uptime_ms()
    while get_script_uptime_ms() - func_start_time < duration:
        if key == "left":
            pydirectinput.moveRel(-5, 0, relative=True, _pause=False)
        if key == "right":
            pydirectinput.moveRel(5, 0, relative=True, _pause=False)
        if key == "up":
            pydirectinput.moveRel(0, -5, relative=True, _pause=False)
        if key == "down":
            pydirectinput.moveRel(0, 5, relative=True, _pause=False)
        time.sleep(.001)

def is_on_main_menu(seconds = 1):
    result = adap_image_search("Data\\Images\\MainMenu.PNG", precision = .8)
    if result:
        for i in range(seconds):
            if is_champion_selection_screen():
                return False
            time.sleep(1)
            result = adap_image_search("Data\\Images\\MainMenu.PNG", precision=.8)
            if not result:
                return False
        return True
    else:
        return False

def is_end_game_screen():
    result = adap_image_search("Data\\Images\\requeue.PNG", .94)
    result2 = adap_image_search("Data\\Images\\end_of_match_flag.PNG", .96)
    global current_map
    if result or result2:
        print("End of game, current_map was set to None")
        current_map = None
        return True
    else:
        return False

def is_death_screen():
    result = adap_image_search("Data\\Images\\DeathFlag.PNG")
    if result:
        return True
    else:
        return False

def is_nade_out_of_cd():
    result = adap_image_search("Data\\Images\\out_of_cd_grenade.PNG")
    if result:
        return True
    else:
        return False

def is_barricade_out_of_cd():
    result = adap_image_search("Data\\Images\\out_of_cd_barricade.PNG", .7)
    if result:
        return True
    else:
        return False

def is_turret_out_of_cd():
    result = adap_image_search("Data\\Images\\out_of_cd_turret.PNG", .7)
    if result:
        return True
    else:
        return False

def is_dome_out_of_cd():
    result = adap_image_search("Data\\Images\\out_of_cd_dome.PNG", .7)
    if result:
        return True
    else:
        return False

def is_low_health():
    pos = get_selected_window_position()
    px = ImageGrab.grab(pos).load()
    color_code = px[117, 605]
    healthy_color = (52, 232, 255)
    if all(abs(c1 - c2) <= 8 for c1, c2 in zip(color_code, healthy_color)):
        return False
    else:
        return True


def is_aim_hovering_an_enemy(tolerance = 34):
    global shoot_cd
    if shoot_cd > get_script_uptime_ms():
        return False

    pos = get_selected_window_position()
    px = ImageGrab.grab(pos).load()
    color_code_samples = [px[588, 325], px[584, 331], px[592, 331], px[588, 335]]
    enemy_colors = [(250, 95, 101), (255, 253, 117)]
    for i in range(len(color_code_samples)):
        for j in range(len(enemy_colors)):
            if all(abs(c1 - c2) <= tolerance for c1, c2 in zip(color_code_samples[i], enemy_colors[j])):
                shoot_cd = get_script_uptime_ms() + 1000
                return True
    return False

def auto_grenade_thrower(cook_time = .6):
    global in_game
    while True:

        print("auto_grenade_thrower is running!")

        if get_process_name_of_focused_window() != "Paladins.exe":
            time.sleep(3)
            global_click(2,2)
            continue

        if is_on_main_menu(3):
            print("Main menu detected")
            in_game = False
            break

        close_fucking_battle_pass_crap()

        if is_death_screen():
            time.sleep(10)
            move_and_shoot(True)

        if is_end_game_screen():
            print("End game screen detected")
            return

        #if is_nade_out_of_cd():
        #    not_remote_hold_key_for("q",cook_time)
        #else:

        if is_dome_out_of_cd() and is_low_health():
            print("Tried ulting!")
            not_remote_hold_key_for("e", .05)
            time.sleep(1)

        if is_barricade_out_of_cd():
            print("Tried barricade!")
            mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
            time.sleep(.05)
            mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
            time.sleep(1)

        if is_turret_out_of_cd():
            print("Tried placing turret!")
            not_remote_hold_key_for("q",.05)
            time.sleep(1)


        move_mouse_left_or_right("right", 40)

        if get_process_name_of_focused_window() != "Paladins.exe":
            time.sleep(3)
            global_click(2,2)
            continue

        if is_death_screen():
            time.sleep(10)
            move_and_shoot(True)

        move_mouse_left_or_right("left", 80)

        if is_death_screen():
            time.sleep(10)
            move_and_shoot(True)

        if get_process_name_of_focused_window() != "Paladins.exe":
            time.sleep(3)
            global_click(2,2)
            continue

        move_mouse_left_or_right("right", 40)




@ray.remote
def keep_mouse_from_leaving_window_for(seconds):
    seconds_100ms = seconds*10
    for i in range(seconds_100ms):
        if pyautogui.position()[0] < 200 or pyautogui.position()[1] > 950:
            pos = get_selected_window_position()
            SetCursorPos((pos[0] + (pos[3]//2), pos[1] + (pos[4]//2)))
        time.sleep(.1)

def move_mouse_left_or_right(direction, duration_ms, pixels = 15):
   if direction == "left":
       pixels = pixels * -1

   for i in range(duration_ms):
       if is_aim_hovering_an_enemy():
           pyautogui.click(duration = .05)
       pydirectinput.moveRel(pixels, 0, relative=True, _pause=False)
       time.sleep(.001)
       #pos = pyautogui.position()
       #if pos[0] < 150 or pos[1] > 980:
       #    pos = get_selected_window_position()
       #    SetCursorPos((pos[0] + (pos[2] // 2), pos[1] + (pos[3] // 2)))


def adap_image_search(path, precision = .8):
    window_pos = get_selected_window_position()
    pos = imagesearcharea(path, window_pos[0], window_pos[1], window_pos[2], window_pos[3], precision = precision)
    if pos[0] != -1:
        return True
    else:
        return False

def get_image_position(path):
    window_pos = get_selected_window_position()
    pos = imagesearcharea(path, window_pos[0], window_pos[1], window_pos[2], window_pos[3])
    return pos


def search_half_of_game_viewport_for_image(path, side):
    window_pos = get_selected_window_position()
    x = window_pos[0]
    y = window_pos[1]
    width = window_pos[2] // 2
    height = window_pos[3]

    offset = 0
    if side == "right":
        offset = width
    else:
        offset = 0
    pos = imagesearcharea(path, x+offset, y+offset, width, height)
    if pos[0] != -1:
        return True
    else:
        return False

def close_fucking_battle_pass_crap():
    pos = get_image_position("Data\\Images\\close_bp.PNG")
    if pos[0] != -1:
        click(676, 555)

def search_half_of_game_viewport_for_3_images(path1, path2, path3, side, precision = .8):
    window_pos = get_selected_window_position()
    x = window_pos[0]
    y = window_pos[1]
    width = window_pos[2] // 2
    height = window_pos[3]

    offset = 0
    if side == "right":
        offset = width
    else:
        offset = 0

    pos1 = imagesearcharea(path1, x+offset, y+offset, width, height, precision = precision)
    pos2 = imagesearcharea(path2, x+offset, y+offset, width, height, precision = precision)
    pos3 = imagesearcharea(path3, x+offset, y+offset, width, height, precision = precision)

    if pos1[0] != -1 or pos2[0] != -1 or pos3[0] != -1:
        return True
    else:
        return False

@ray.remote
def hold_key_for(key, t):
    pyautogui.keyDown(key)
    time.sleep(t)
    pyautogui.keyUp(key)

def not_remote_hold_key_for(key, t):
    pyautogui.keyDown(key)
    time.sleep(t)
    pyautogui.keyUp(key)

def search_point_marker_in_the_middle_of_the_screen_for_x_time(white_marker_path, red_marker_path, blue_marker_path, time_limit_seconds, accuracy : .8):
    window_pos = get_selected_window_position()
    x = window_pos[0]
    y = window_pos[1]
    height = window_pos[3]
    for i in range(time_limit_seconds):
        pos = imagesearcharea(white_marker_path, x + 420, y, x + 756, y + height, precision = accuracy)
        pos_red = imagesearcharea(red_marker_path, x + 420, y, x + 756, y + height, precision = accuracy)
        pos_blue = imagesearcharea(blue_marker_path, x + 420, y, x + 756, y + height, precision = accuracy)
        if pos[0] != -1 or pos_red[0] != -1 or pos_blue[0] != -1:
            return True
        time.sleep(1)
    return False

def close_annoying_ad():
    pos = get_image_position("Data\\Images\\CloseAnnoyingAd.PNG")
    if pos[0] != -1:
        click(pos[0], pos[1])

def click_the_reconnect_button():
    pos = get_image_position("Data\\Images\\reconnect.PNG")
    if pos[0] != -1:
        click(pos[0], pos[1])
        time.sleep(.1)

def move_and_shoot(from_the_dead = False):
    global current_map

    if current_map == "AscensionPeak":
        if not from_the_dead:
            time.sleep(43)
        itemization_handler()
        run_macro(macros.ascension_peak_main.copy())
        pydirectinput.moveRel(0, 10, relative=True, _pause=False)
        auto_grenade_thrower(1)

    if current_map == "Foreman'sRise":
        if not from_the_dead:
            time.sleep(43)
        itemization_handler()
        run_macro(macros.foremans_rise_main_macro.copy())
        pydirectinput.moveRel(0, 10, relative=True, _pause=False)
        auto_grenade_thrower(1)

    if current_map == "Brightmarsh":
        if not from_the_dead:
            time.sleep(43)
        itemization_handler()
        run_macro(macros.brightmarsh_main.copy())
        pydirectinput.moveRel(0, 10, relative=True, _pause=False)
        auto_grenade_thrower(1)

    if current_map == "Bazaar":
        if not from_the_dead:
            time.sleep(43)
        itemization_handler()
        run_macro(macros.bazaar_main.copy())
        pydirectinput.moveRel(0, 10, relative=True, _pause=False)
        auto_grenade_thrower(1)

    if current_map == "Magistrate'sArchives":
        if not from_the_dead:
            time.sleep(43)
        itemization_handler()
        result = search_point_marker_in_the_middle_of_the_screen_for_x_time(
            "Data\\Images\\PointRefsA\\Magistrate'sArchives_point_mark.PNG",
            "Data\\Images\\PointRefsA\\Magistrate'sArchives_point_mark_red.PNG",
            "Data\\Images\\PointRefsA\\Magistrate'sArchives_point_mark_blue.png",
            5, .6)
        if result:
            print("Running macro A")
            run_macro(macros.magistrates_archives_main_macro_A.copy())
        else:
            print("Running macro B")
            run_macro(macros.magistrates_archives_main_macro_B.copy())

        pydirectinput.moveRel(0, 10, relative=True, _pause=False)
        auto_grenade_thrower(1)

    if current_map == "Marauder'sPort":
        if not from_the_dead:
            time.sleep(43)
        itemization_handler()
        run_macro(macros.marauders_port_main_macro.copy())
        pydirectinput.moveRel(0, 10, relative=True, _pause=False)
        auto_grenade_thrower(1)

    if  current_map == "PrimalCourt":
        if not from_the_dead:
            time.sleep(43)
        itemization_handler()

        image_paths = ["Data\\Images\\PointRefsA\\PrimalCourt_point_mark.PNG", "Data\\Images\\PointRefsA\\PrimalCourt_point_mark_red.PNG", "Data\\Images\\PointRefsA\\PrimalCourt_point_mark_blue.png"]

        print_cd = 0
        found = False
        pixel_value = 15
        result = search_half_of_game_viewport_for_3_images(image_paths[0],image_paths[1],image_paths[2],"left", .7)
        if result:
            pixel_value = -15
        for i in range(200):
            if print_cd < get_script_uptime_ms():
                print_cd = get_script_uptime_ms() + 1000
                print("Spinning!")


            if found:
                break
            time.sleep(.001)
            pydirectinput.moveRel(pixel_value, 0, relative=True, _pause=False)
            for j in range(3):
                pos = imagesearcharea(image_paths[j], 548, 284, 628, 480, precision = .6)
                if pos[0] != -1:
                    print("Positive for facing mid")
                    found = True
                    break

        run_macro(macros.primal_court_move_to_right_corner.copy())

        found = False
        pixel_value = 10
        result = search_half_of_game_viewport_for_3_images(image_paths[0], image_paths[1], image_paths[2], "left", .6)
        if result:
            pixel_value = -10
        for i in range(600):
            if found:
                break
            time.sleep(.001)
            pydirectinput.moveRel(pixel_value, 0, relative=True, _pause=False)
            for j in range(3):
                pos = imagesearcharea(image_paths[j], 558, 286, 618, 480, precision = .6)
                if pos[0] != -1:
                    print("Positive for facing mid")
                    found = True
                    break
    

        run_macro(macros.primal_court_main.copy())
        pydirectinput.moveRel(0, 10, relative=True, _pause=False)
        auto_grenade_thrower(1)

    if current_map == "SnowfallJunction":
        if not from_the_dead:
            time.sleep(43)
        itemization_handler()
        run_macro(macros.snowfall_junction_main_macro_single.copy())

        if adap_image_search("Data\\Images\\snowfall_junction_failsafe_A.PNG", .8):
            run_macro(macros.snowfall_junction_failsafe_A.copy())

        if adap_image_search("Data\\Images\\snowfall_junction_failsafe_B.PNG", .8):
            run_macro(macros.snowfall_junction_failsafe_B.copy())

        pydirectinput.moveRel(0, 10, relative=True, _pause=False)
        auto_grenade_thrower(1)


def await_for_image_to_be_detected_for_x_time(image_path, time_limit):
    time_range = time_limit*10
    for i in range(time_range):
        result = adap_image_search(image_path, .9)
        if result:
            print("Clear to leave base")
            break
        time.sleep(.1)

def legendary_selector():
    if adap_image_search("Data\\Images\\fortify_legendary.PNG"):
        time.sleep(1)
        click(203, 376)
        time.sleep(2)
        click(298, 265)
        time.sleep(2)
        click(589, 503)
        time.sleep(2)
        return True
    else:
        return False

        

def check_if_game_tips_are_still_on():
    global already_checked_game_tips
    if already_checked_game_tips:
        return
    result = adap_image_search("Data\\Images\\MainMenu.PNG")
    if not result:
        return

    click(1114, 30)
    time.sleep(1)
    click(525, 48)
    time.sleep(.4)

    img = "Data\\Images\\enabled.PNG"
    pos = imagesearcharea(img, 862, 145, 981, 178, precision = .75)
    if pos[0] != -1:
        click(761, 161)
        time.sleep(.2)
        click(587, 569)
        time.sleep(.3)
        pyautogui.keyDown("esc")
        time.sleep(.2)
        pyautogui.keyUp("esc")
        time.sleep(.8)
    else:
        pyautogui.keyDown("esc")
        time.sleep(.2)
        pyautogui.keyUp("esc")
        time.sleep(1)
    already_checked_game_tips = True

def simulate_keypress():
    time.sleep(1)  # Allow time for the mouse movement function to start

    # Simulate pressing the "left" key
    key_states["left"] = True
    time.sleep(0.5)
    key_states["left"] = False

    # Simulate pressing the "up" key
    key_states["up"] = True
    time.sleep(0.5)
    key_states["up"] = False

    # Simulate pressing the "right" key
    key_states["right"] = True
    time.sleep(0.5)
    key_states["right"] = False

    # Simulate pressing the "down" key
    key_states["down"] = True
    time.sleep(0.5)
    key_states["down"] = False

def get_process_name_of_focused_window():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        return process.name()
    except Exception as e:
        return f"Error: {str(e)}"

def get_selected_window_position():
    # Get the currently active window
    active_window = gw.getActiveWindow()

    if active_window:
        # Get the position and size of the window
        x, y, width, height = active_window.left, active_window.top, active_window.width, active_window.height
        return x, y, width, height
    else:
        print("No active window found.")
        return None


def activate_window_by_process(window_name):
    windows = gw.getWindowsWithTitle(window_name)
    if not windows:
        print(f"No window found with name containing: {window_name}")
        return False

    # Activate the first window that matches
    window = windows[0]
    try:
        window.activate()
        return True
    except Exception as e:
        print(f"Failed to activate window: {e}")
        return False

def move_selected_window_to_top_left():
    # Get the currently active window
    active_window = gw.getActiveWindow()

    if active_window:
        # Move the window to (0, 0)
        active_window.moveTo(0, 0)
    else:
        print("No active window found.")

def run_macro(m : list):
    if not m:
        print("An empty list was passed to run_macro")
        return
    duration = m.pop(-1)
    global key_states
    function_start_time = get_script_uptime_ms()
    time_ms = 0
    #movement_handling.remote(duration)
    while time_ms < duration:
        time_ms = get_script_uptime_ms() - function_start_time
        for k in m:
            if k[0] in key_states:
                if time_ms >= k[1] and time_ms < k[1]+10:
                    new_movement_handling.remote(k[0], k[2]-k[1])
                    print("Tried pressing " + str(k)+" at"+str(time_ms))
                    m.remove(k)
            else:
                if time_ms >= k[1] and time_ms < k[1]+10:
                    hold_key_for.remote(k[0],(k[2]-k[1])/1000)
                    print("Tried pressing " + str(k)+" at"+str(time_ms))
                    m.remove(k)
        time.sleep(.001)



if __name__ == "__main__":
    main()