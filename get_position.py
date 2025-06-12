import pyautogui
import pygetwindow as gw
from pynput import mouse, keyboard
import time 
import csv
import sys


def on_click_for_pos(x, y, button, pressed):
    if pressed:
        return False


def get_cursor_position():
    # マウスのクリック検知
    with mouse.Listener(on_click=on_click_for_pos) as listener:
        listener.join()
    # ---
    x, y = pyautogui.position()  # カーソルの位置を取得
    print('カーソルの位置: x = {}, y = {}'.format(x, y))
    # --- ウィンドウの取得 ---
    time.sleep(1)
    active_window = gw.getActiveWindow()
    if not active_window is None:
        print('対象ウィンドウ: {}'.format(active_window.title))
    else:
        print('対象ウィンドウ: なし')
    print('\n --- END: Get Cursor Position ---')
    return x, y, active_window


tposx, tposy, window = get_cursor_position()
print(window)
sys.exit()
