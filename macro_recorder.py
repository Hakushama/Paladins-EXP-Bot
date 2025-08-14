import time
import keyboard
import pyperclip as pc
import pydirectinput
import threading

script_start_time = time.perf_counter()
key_states = {"left": False, "right": False, "up": False, "down": False}
base_cooldown = 1 #delay between emulated key presses

def get_script_uptime_ms():
    # Current time in seconds
    current_time = time.perf_counter()
    # Elapsed time in milliseconds
    elapsed_time_ms = int((current_time - script_start_time) * 1000)
    return elapsed_time_ms

def move_mouse_from_code():
    cooldowns = {"left" : 1, "right": 1, "up": 1, "down": 1}

    while True:
        if keyboard.is_pressed("left"):
            key_states["left"] = True
        else:
            key_states["left"] = False

        if keyboard.is_pressed("right"):
            key_states["right"] = True
        else:
            key_states["right"] = False

        if keyboard.is_pressed("up"):
            key_states["up"] = True
        else:
            key_states["up"] = False

        if keyboard.is_pressed("down"):
            key_states["down"] = True
        else:
            key_states["down"] = False

        if key_states["left"] and cooldowns["left"] < get_script_uptime_ms():
            pydirectinput.moveRel(-3, 0, _pause=False, relative=True)
            cooldowns["left"] = get_script_uptime_ms() + base_cooldown

        if key_states["right"] and cooldowns["right"] < get_script_uptime_ms():
            pydirectinput.moveRel(3, 0, _pause=False, relative=True)
            cooldowns["right"] = get_script_uptime_ms() + base_cooldown

        if key_states["up"] and cooldowns["up"] < get_script_uptime_ms():
            pydirectinput.moveRel(0, -3, _pause=False, relative=True)
            cooldowns["up"] = get_script_uptime_ms() + base_cooldown

        if key_states["down"] and cooldowns["down"] < get_script_uptime_ms():
            pydirectinput.moveRel(0, 3, _pause=False, relative=True)
            cooldowns["down"] = get_script_uptime_ms() + base_cooldown

        time.sleep(.001)

def record_macro():
    key_cd = {
        "w": [0, 0],
        "a": [0, 0],
        "s": [0, 0],
        "d": [0, 0],
        "q": [0, 0],
        "e": [0, 0],
        "f": [0, 0],
        "z": [0, 0],
        "space": [0, 0],
        "up": [0, 0],
        "left": [0, 0],
        "right": [0, 0],
        "enter": [0, 0],
        "down": [0, 0]
    }

    key_tracker = []

    held_keys = {
        "w": False,
        "a": False,
        "s": False,
        "d": False,
        "q": False,
        "e": False,
        "f": False,
        "z": False,
        "space": False,
        "up": False,
        "left": False,
        "right": False,
        "enter": False,
        "down": False
    }

    while True:
        #time.sleep(.001)
        event = keyboard.read_event()
        if event.name == "esc" and event.event_type == "down":
            break
        if event.name not in key_cd:
            continue

        if event.event_type == "down" and not held_keys[event.name]:
            if event.name in key_cd:
                key_cd[event.name][0] = get_script_uptime_ms()
                held_keys[event.name] = True
        if event.event_type == "up" and held_keys[event.name]:
            if event.name in key_cd:
                key_cd[event.name][1] = get_script_uptime_ms()
                key_tracker.append([event.name, key_cd[event.name][0], key_cd[event.name][1]])
                held_keys[event.name] = False

    key_tracker.append(get_script_uptime_ms())
    stringify_data = ""
    for k in key_tracker:
        stringify_data = stringify_data+",\n"+str(k)
    print(stringify_data)
    pc.copy(stringify_data)


movement_thread = threading.Thread(target=move_mouse_from_code, daemon=True)
movement_thread.start()

record_macro()

