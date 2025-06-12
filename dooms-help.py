import pyautogui
import pygetwindow as gw
from pynput import mouse, keyboard
import time 
import csv
import sys


def get_window(window_title):
    window = gw.getWindowsWithTitle(window_title)
    nwindow = len(window)
    if nwindow == 0:
        print('ウィンドウが見つかりませんでした')
        return None
    elif nwindow == 1:
        return window[0]
    elif nwindow > 1:
        print('複数のウィンドウが見つかりました: {}'.format(window))
        for win in window:
            if win.title == window_title:
                return win
        return None
    

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

def on_press_key(key):
    # Escが押されると終了
    global esc_pressed
    if key == keyboard.Key.esc:
        esc_pressed = True
    if hasattr(key, "char") and key.char and key.char == "c":
        esc_pressed = True


def check_window_pos(tposx, tposy, window):
    is_click_ok = True
    if window is None:
        is_click_ok = False
    if (not isinstance(tposx, int)) or (not isinstance(tposy, int)):
        is_click_ok = False
    return is_click_ok

def activate_window(window):
    # window.activate()ではエラーが生じる可能性があるため、最小化、復元で強制的にアクティブ化
    if not window is None:
        window.minimize()
        window.restore()

def auto_click(tposx, tposy, window, waittime=1, printstep=1):
    print(window.title)
    is_click_ok = check_window_pos(tposx, tposy, window)
    if not is_click_ok:
        print('ウィンドウもしくはクリック座標が不適切なため未実行')
        return ['Error']
    # ---
    # global esc_pressed
    # esc_pressed = False
    pyautogui.FAILSAFE=False
    pyautogui.PAUSE=waittime
    time1 = time.time()   
    try:
        window.activate()  # 対象の画面をアクティブ化 
        # activate_window(window)
        # pyautogui.click(window.left+10, window.top+10)
    except Exception as e:
        time.sleep(waittime)
        return
    time.sleep(waittime)
    
    time2 = time.time()
    dtime = time2 - time1
    print('activate time: {:g}'.format(dtime))
    # ---
    time0 = time.time()  # 初期時間
    time1 = time.time()   
    # --- メイン処理 ---
    try:
        pyautogui.click(x=tposx, y=tposy)  # 所定の位置に移動してクリック。クリック内容を変える場合は、本行を変更。
    except Exception as e:
        time.sleep(waittime)
        return
    time2 = time.time()
    dtime = time2 - time1
    totaltime = time2 - time0
    print('click time: {:g}'.format(dtime))

    # ---
    return 

# left, top = 312, 160
# ヘルプボタン: 970, 842 = 658, 682
# 緑ボタン: *, * = 1248, 559
# get_cursor_position()


# titles=[
#     "[#] [6Mur 3-1] Doomsday: Last Survivors [#]",
#     "[#] [6Mur 3-2] Doomsday: Last Survivors [#]",
#     "[#] [6Mur 3-3] Doomsday: Last Survivors [#]",
#     "[#] [6Mur 3-4] Doomsday: Last Survivors [#]",
#     "[#] [6Mur 3-5] Doomsday: Last Survivors [#]",
#     "[#] [6Mur 3-6] Doomsday: Last Survivors [#]",
#     "[#] [6Mur 3-7] Doomsday: Last Survivors [#]",
#     "[#] [6Mur 3-8] Doomsday: Last Survivors [#]",
#     "[#] [6Mur 3-9] Doomsday: Last Survivors [#]",
#     "[#] [6Mur 3-10] Doomsday: Last Survivors [#]",
#     # "[#] [6Mur 4-1] Doomsday: Last Survivors [#]",
#     # "[#] [6Mur 4-2] Doomsday: Last Survivors [#]",
#     # "[#] [6Mur 4-3] Doomsday: Last Survivors [#]",
#     # "[#] [6Mur 4-4] Doomsday: Last Survivors [#]",
#     # "[#] [6Mur 4-5] Doomsday: Last Survivors [#]",
#     # "[#] [6Mur 4-6] Doomsday: Last Survivors [#]",
#     # "[#] [6Mur 4-7] Doomsday: Last Survivors [#]",
#     # "[#] [6Mur 4-8] Doomsday: Last Survivors [#]",
#     # "[#] [6Mur 4-9] Doomsday: Last Survivors [#]",
#     # "[#] [6Mur 4-10] Doomsday: Last Survivors [#]",
# ]

with open('titles.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 各行から改行文字を取り除く（必要に応じて）
titles = [line.strip() for line in lines]


listener = keyboard.Listener(on_press=on_press_key)
listener.start()
global esc_pressed
esc_pressed = False

while True:
    if  esc_pressed: # Escが押されたらループを抜ける
        break
    for title in titles:
        print(title)
        if  esc_pressed: # Escが押されたらループを抜ける
            break
        window = get_window(title)
        if window:
            auto_click(window.left + 658, window.top + 682, window, waittime=0.005)

listener.stop()  # キーボード検知を停止