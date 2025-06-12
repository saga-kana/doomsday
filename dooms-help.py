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
    pyautogui.PAUSE=0.002
    time1 = time.time()   
    window.activate()  # 対象の画面をアクティブ化 
    time.sleep(0.002)
    # activate_window(window)
    # pyautogui.click(window.left+10, window.top+10)
    time2 = time.time()
    dtime = time2 - time1
    print('activate time: {:g}'.format(dtime))
    # --- 出力リスト ---
    outlist = []
    outlist.append(['cnt', 'total_time', 'dtime'])
    # ---　ループを抜けるためのキーボード検知用 ---
    # listener = keyboard.Listener(on_press=on_press_key)
    # listener.start()
    # ---
    cnt = 0
    time0 = time.time()  # 初期時間
    while True:
        time1 = time.time()   
        # --- メイン処理 ---
        pyautogui.click(x=tposx, y=tposy)  # 所定の位置に移動してクリック。クリック内容を変える場合は、本行を変更。
        # if  esc_pressed: # Escが押されたらループを抜ける
        #     break
        # time.sleep(waittime)  # 所定の時間待機
        # --- 出力用 ---
        cnt += 1
        time2 = time.time()
        dtime = time2 - time1
        totaltime = time2 - time0
        outlist.append([cnt, totaltime, dtime])
        if cnt%printstep == 0:
            print('cnt: {}, time: {:g}'.format(cnt, dtime))

        break
    # ---
    # listener.stop()  # キーボード検知を停止
    print('\n --- End: Auto Click ---')
    return outlist

# left, top = 312, 160
# ヘルプボタン: 970, 842 = 658, 682
# 緑ボタン: *, * = 1248, 559
# get_cursor_position()


titles=[
    "[#] [6Mur 3-1] Doomsday: Last Survivors [#]",
    "[#] [6Mur 3-2] Doomsday: Last Survivors [#]",
    "[#] [6Mur 3-3] Doomsday: Last Survivors [#]",
    "[#] [6Mur 3-4] Doomsday: Last Survivors [#]",
    "[#] [6Mur 3-5] Doomsday: Last Survivors [#]",
    "[#] [6Mur 3-6] Doomsday: Last Survivors [#]",
    "[#] [6Mur 3-7] Doomsday: Last Survivors [#]",
    "[#] [6Mur 3-8] Doomsday: Last Survivors [#]",
    "[#] [6Mur 3-9] Doomsday: Last Survivors [#]",
    "[#] [6Mur 3-10] Doomsday: Last Survivors [#]",
    # "Doomsday: Last Survivors"
    # "[#] [6Mur 4-1] Doomsday: Last Survivors [#]",
    # "[#] [6Mur 4-2] Doomsday: Last Survivors [#]",
    # "[#] [6Mur 4-3] Doomsday: Last Survivors [#]",
    # "[#] [6Mur 4-4] Doomsday: Last Survivors [#]",
    # "[#] [6Mur 4-5] Doomsday: Last Survivors [#]",
    # "[#] [6Mur 4-6] Doomsday: Last Survivors [#]",
    # "[#] [6Mur 4-7] Doomsday: Last Survivors [#]",
    # "[#] [6Mur 4-8] Doomsday: Last Survivors [#]",
    # "[#] [6Mur 4-9] Doomsday: Last Survivors [#]",
    # "[#] [6Mur 4-10] Doomsday: Last Survivors [#]",
]

listener = keyboard.Listener(on_press=on_press_key)
listener.start()
global esc_pressed
esc_pressed = False

while True:
    if  esc_pressed: # Escが押されたらループを抜ける
        break
    for title in titles:
        window = get_window(title)
        if window:
            # activate_window(window)
            auto_click(window.left + 658, window.top + 682, window, waittime=0.2)
            # time.sleep(1.2)
            # esc_pressed = True

listener.stop()  # キーボード検知を停止