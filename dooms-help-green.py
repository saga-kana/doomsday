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
        # for win in window:
        #     if win.title == window_title:
        #         return win
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
        print("BREAK!!!")
        esc_pressed = True
    if hasattr(key, "char") and key.char and key.char == "c":
        print("BREAK!!!")
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

def auto_click(tposx, tposy, window, waittime=1, printstep=1, gray_scale=True, confidence=0.95):
    # print(window.title)
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
        if window.isMinimized:
            window.restore()
        window.activate()  # 対象の画面をアクティブ化 
    except Exception as e:
        print(e)
        time.sleep(waittime)
        try:
            activate_window(window)
        except Exception as e2:
            print(e2)
            time.sleep(waittime)
            return
    # wait to be activated
    for _ in range(100):
        if gw.getActiveWindow() == window:
            break
        time.sleep(0.002)

    time.sleep(waittime)
    
    time2 = time.time()
    dtime1 = time2 - time1
    print('activate time: {:g}'.format(dtime1))
    # ---
    # time0 = time.time()  # 初期時間
    time1 = time.time()   
    # --- メイン処理 ---
    if esc_pressed:
        return
    try:
        x,y  = pyautogui.locateCenterOnScreen(f'./img/green_help.png', grayscale=gray_scale, confidence=confidence)
        pyautogui.click(x=x, y=y)
    except pyautogui.ImageNotFoundException:
        print("no req.")

    
    time2 = time.time()
    dtime2 = time2 - time1
    # totaltime = time2 - time0
    print('click time: {:g}'.format(dtime2))

    # ---
    return dtime1+dtime2


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


if __name__ == '__main__':
    with open('titles.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 各行から改行文字を取り除く（必要に応じて）
    titles = [line.strip() for line in lines if not line.strip().startswith('/')]


    listener = keyboard.Listener(on_press=on_press_key)
    listener.start()
    # global esc_pressed
    esc_pressed = False

    print("マウスを画面外へ")
    time.sleep(10)

    total_time = 0
    total_cnt = 0
    while True:
        if  esc_pressed: # Escが押されたらループを抜ける
            break
        sumtime = 0
        cnt = 0
        for title in titles:
            print(title)
            if  esc_pressed: # Escが押されたらループを抜ける
                break
            try:
                window = get_window(title)
            except Exception as e:
                print(e)
                continue
            if window:
                dtime = auto_click(window.left + 658, window.top + 682, window, waittime=0.09)
                if dtime:
                    sumtime += dtime
                    cnt += 1
        if cnt > 0:
            print(f"one cycle: {sumtime:g}, cnt: {cnt}, avg: {sumtime/cnt}\n")
        total_time += sumtime
        total_cnt += cnt

        # time.sleep(2)

    if total_cnt > 0:
        print(f"\ntotal : {total_time:g}, cnt: {total_cnt}, avg: {total_time/total_cnt}")



    listener.stop()  # キーボード検知を停止