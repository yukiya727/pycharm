import threading
import time
import os
import sys
import keyboard
import pynput.mouse
import pynput.keyboard


def on_move(x, y):
    global file_path, t_offset, no_lag_mode, acc_lag, lag
    print('MouseMove,{0},{1},{2}'.format(
        x, y, time.time()))
    t_offset = time.time() - t_offset
    with open(file_path, 'a') as f:
        if no_lag_mode:
            pass
        else:
            f.write('MouseMove,{0},{1},{2}'.format(
                x, y, (time.time() - t_offset)))
            f.write('\n')
            t_offset = time.time()


def on_click(x, y, button, pressed):
    global file_path, t_offset, no_lag_mode, acc_lag, lag
    print('{0},{1},{2},{3},{4}'.format(
        'MousePressed' if pressed else 'MouseReleased', button, x, y, time.time()))
    t_offset = time.time() - t_offset
    with open(file_path, 'a') as f:
        if no_lag_mode:
            acc_lag += lag
            f.write('{0},{1},{2},{3},{4}'.format(
                'MousePressed' if pressed else 'MouseReleased', button, x, y, acc_lag))
            f.write('\n')
            t_offset = time.time()
        else:
            f.write('{0},{1},{2},{3},{4}'.format(
                'MousePressed' if pressed else 'MouseReleased', button, x, y, (time.time() - t_offset)))
            f.write('\n')
            t_offset = time.time()


def on_scroll(x, y, dx, dy):
    global file_path, t_offset, no_lag_mode, acc_lag, lag
    print('MouseScrolled,{0},{1},{2}'.format(
        x, y, time.time()))
    t_offset = time.time() - t_offset
    with open(file_path, 'a') as f:
        if no_lag_mode:
            acc_lag += lag
            f.write('MouseScrolled,{0},{1},{2}'.format(
                x, y, acc_lag))
            f.write('\n')
            t_offset = time.time()
        else:
            f.write('MouseScrolled,{0},{1},{2}'.format(
                x, y, (time.time() - t_offset)))
            f.write('\n')
            t_offset = time.time()


def on_press(key):
    global file_path, t_offset, no_lag_mode, acc_lag, lag
    try:
        print('KeyPressed,{0},{1}'.format(
            key.char, time.time()))
        t_offset = time.time() - t_offset
        with open(file_path, 'a') as f:
            if no_lag_mode:
                acc_lag += lag
                f.write('KeyPressed,{0},{1}'.format(
                    key.char, acc_lag))
                f.write('\n')
                t_offset = time.time()
            else:
                f.write('KeyPressed,{0},{1}'.format(
                    key.char, (time.time() - t_offset)))
                f.write('\n')
                t_offset = time.time()
    except AttributeError:
        print('KeyPressed,{0},{1}'.format(
            key, time.time()))
        t_offset = time.time() - t_offset
        with open(file_path, 'a') as f:
            if no_lag_mode:
                acc_lag += lag
                f.write('KeyPressed,{0},{1}'.format(
                    key, acc_lag))
                f.write('\n')
                t_offset = time.time()
            else:
                f.write('KeyPressed,{0},{1}'.format(
                    key, (time.time() - t_offset)))
                f.write('\n')
                t_offset = time.time()


def on_release(key):
    global file_path, t_offset, no_lag_mode, acc_lag, lag

    print('KeyReleased,{0},{1}'.format(
        key, time.time()))
    t_offset = time.time() - t_offset
    with open(file_path, 'a') as f:
        f.write('KeyReleased,{0},{1}'.format(
            key, (time.time() - t_offset)))
        f.write('\n')
        t_offset = time.time()

    if key == pynput.keyboard.Key.f10:
        with open(file_path, 'a') as f:
            f.write('done')
            f.write('\n')
        # Stop listener
        print(time.time() - timer)
        pynput.mouse.Listener.stop(m_listener)
        return False
    if key == pynput.keyboard.Key.f8:
        with open(file_path, 'a') as f:
            f.write('start')
            f.write('\n')


os.chdir(os.path.dirname(os.path.realpath(__file__)))
directory = 'mouse_recorder'
try:
    session_name = "pynput_record"
except:
    print('you must enter a name for the session\nfor example: python record.py session_name')
    sys.exit()
dir_path = os.path.join(os.getcwd(), directory, session_name)
if not os.path.exists(dir_path):
    os.makedirs(dir_path)
file_name = 'history'
i = 0
while os.path.isfile(dir_path+'/'+file_name+str(i)+'.txt'):
    i += 1
file_name += str(i) + '.txt'
print(file_name)
file_path = os.path.join(dir_path, file_name)
print(dir_path)

print("Please press 'F8' key to start recording")
keyboard.wait("F8")
timer = time.time()
t_offset = timer
acc_lag = timer
lag = 0.1
no_lag_mode = True

with pynput.keyboard.Listener(
        on_press=on_press,
        on_release=on_release
) as k_listener, \
        pynput.mouse.Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll) as m_listener:
    k_listener.join()
    m_listener.join()
