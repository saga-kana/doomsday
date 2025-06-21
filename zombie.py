import pyautogui
import pygetwindow as gw
from pynput import mouse, keyboard
import time 
import csv
import sys


# global esc_pressed
esc_pressed = False

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
    


def on_press_key(key):
    # Escが押されると終了
    global esc_pressed
    if key == keyboard.Key.esc:
        esc_pressed = True
        print("BREAK!!!")
    if hasattr(key, "char") and key.char and key.char == "c":
        esc_pressed = True
        print("BREAK!!!")   


def check_window_pos(tposx, tposy, window):
    is_click_ok = True
    if window is None:
        is_click_ok = False
    if (not isinstance(tposx, int)) or (not isinstance(tposy, int)):
        is_click_ok = False
    return is_click_ok

def activate_window(window):
    # window.activate() # ではエラーが生じる可能性があるため、最小化、復元で強制的にアクティブ化
    if not window is None:
        # window.activate()
        window.minimize()
        window.restore()

def auto_click(tposx, tposy, window, waittime=1, printstep=1):
    print(window.title, tposx, tposy)
    is_click_ok = check_window_pos(tposx, tposy, window)
    if not is_click_ok:
        print('ウィンドウもしくはクリック座標が不適切なため未実行')
        return ['Error']
    # ---
    pyautogui.FAILSAFE=False
    pyautogui.PAUSE=0.002
    # ---
    time1 = time.time()   
    # --- メイン処理 ---
    pyautogui.moveTo(tposx, tposy + 38)
    pyautogui.mouseDown()
    time.sleep(0.096)
    pyautogui.mouseUp()
    time.sleep(waittime)  # 所定の時間待機
    # --- 出力用 ---
    time2 = time.time()
    dtime = time2 - time1
    print('time: {:g}'.format(dtime))

    return 


def click_img(img: str, **kwargs):
    # 可変長引数を代入
    sleep_time = kwargs.pop('sleep_time', 0.5)  # クリック後の待機時間
    offset_x = kwargs.pop('offset_x', 0)         # 画像認識した座標とクリック座標をx方向にオフセット
    offset_y = kwargs.pop('offset_y', 0)         # 画像認識した座標とクリック座標をy方向にオフセット
    click_lr = kwargs.pop('click_lr', 'left')    # 左クリックor右クリック
    gray_scale = kwargs.pop('gray_scale', True)  # 画像認識時のグレースケールONOFF
    confidence = kwargs.pop('confidence', 0.8)   # 画像認識時の判定度合い
    # 画像の座標を代入
    x, y = pyautogui.locateCenterOnScreen(f'./img/{img}', grayscale=gray_scale, confidence=confidence)
    print("img",x,y)
    # 座標をクリック
    # pyautogui.click(x + offset_x, y + offset_y, button=click_lr)
    pyautogui.moveTo(x + offset_x, y + offset_y)
    pyautogui.mouseDown()
    time.sleep(0.096)
    pyautogui.mouseUp()
    # 指定時間の待機
    time.sleep(sleep_time)

def watch_img(img: str, **kwargs):    # 可変長引数を代入
    sleep_time = kwargs.pop('sleep_time', 0.5)  # チェック後の待機時間
    gray_scale = kwargs.pop('gray_scale', True)  # 画像認識時のグレースケールONOFF
    confidence = kwargs.pop('confidence', 0.8)   # 画像認識時の判定度合い
    
    cnt=0
    while True:
        print(f"\r待機中: {cnt}秒", end="")
        sys.stdout.flush()        
        if esc_pressed: # Escが押されたらループを抜ける
            break
        try:
            pyautogui.locateCenterOnScreen(f'./img/{img}', grayscale=gray_scale, confidence=confidence)
            time.sleep(sleep_time)
            cnt+=1
        except pyautogui.ImageNotFoundException:
            return
    print()
        

def wait_img(img: str, **kwargs):    # 可変長引数を代入
    sleep_time = kwargs.pop('sleep_time', 0.5)  # チェック後の待機時間
    gray_scale = kwargs.pop('gray_scale', True)  # 画像認識時のグレースケールONOFF
    confidence = kwargs.pop('confidence', 0.8)   # 画像認識時の判定度合い
    
    cnt=0
    while True:
        print(f"\r待機中: {cnt}秒", end="")
        sys.stdout.flush()        
        if esc_pressed: # Escが押されたらループを抜ける
            print()
            break
        try:
            x, y = pyautogui.locateCenterOnScreen(f'./img/{img}', grayscale=gray_scale, confidence=confidence)
        except pyautogui.ImageNotFoundException:
            time.sleep(sleep_time)
            cnt+=1
            continue
        print()
        break
        
        

# left, top = 312, 160
# ヘルプボタン: 970, 842 = 658, 682
# 緑ボタン: *, * = 1248, 559
# get_cursor_position()


titles=[
    # "[#] [6Mur 3-1] Doomsday: Last Survivors [#]",
    # "[#] [6Mur 3-2] Doomsday: Last Survivors [#]",
    # "[#] [6Mur 3-3] Doomsday: Last Survivors [#]",
    # "[#] [6Mur 3-4] Doomsday: Last Survivors [#]",
    # "[#] [6Mur 3-5] Doomsday: Last Survivors [#]",
    # "[#] [6Mur 3-6] Doomsday: Last Survivors [#]",
    # "[#] [6Mur 3-7] Doomsday: Last Survivors [#]",
    # "[#] [6Mur 3-8] Doomsday: Last Survivors [#]",
    # "[#] [6Mur 3-9] Doomsday: Last Survivors [#]",
    # "[#] [6Mur 3-10] Doomsday: Last Survivors [#]",
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
    # "[#] [36k] Doomsday: Last Survivors [#]",
    "[#] [AssignBolt] Doomsday: Last Survivors [#]",
]

title = "[#] [36k] Doomsday: Last Survivors [#]"

listener = keyboard.Listener(on_press=on_press_key)
listener.start()

if __name__ == '__main__':
    print("カーソルを画面外へ")
    time.sleep(3)
    
    while True:
        if  esc_pressed: # Escが押されたらループを抜ける
            break

        window = get_window(title)
        if window:
            activate_window(window)
            time.sleep(1)

            while True:
                if esc_pressed:
                    break
                auto_click(window.left + 44, window.top + 445, window, waittime=0.5) # 虫眼鏡
                auto_click(window.left + 217, window.top + 465, window, waittime=1.8) # Search
                auto_click(window.left + 666, window.top + 355, window, waittime=0.5) # ゾンビ
                # auto_click(window.left + 960, window.top + 560, window, waittime=0.5) # ATTACK
                
                if esc_pressed:
                    break

                try:
                    click_img("ATTACK.png")
                    break
                except pyautogui.ImageNotFoundException as e:
                    auto_click(window.left + 44, window.top + 445, window, waittime=0.5) # 虫眼鏡
                    auto_click(window.left + 73, window.top + 391, window, waittime=0.5) # マイナス
                    # auto_click(window.left + 360, window.top + 391, window, waittime=0.5) # プラス
                    auto_click(window.left + 600, window.top + 400, window, waittime=1.5) # 閉じる
            
            if esc_pressed:
                break
            # create everytime
            # auto_click(window.left + 972, window.top + 209, window, waittime=0.8) # Create Squad
            # auto_click(window.left + 1096, window.top + 245, window, waittime=0.5) # Load 1

            # peggy
            # click_img("peggy_large.png")
            # click_img("MARCH.png")
            # time.sleep(3)
            # wait_img("peggy_wait.png", confidence=0.95)

            # multi
            # auto_click(window.left + 1180, window.top + 682, window, waittime=0.8) # Create Squad

            # create multi
            # auto_click(window.left + 972, window.top + 265, window, waittime=0.8) # Create Squad
            # auto_click(window.left + 1000, window.top + 486, window, waittime=0.8) # preset 1
            # auto_click(window.left + 1000, window.top + 609, window, waittime=0.8) # MARCH

            # create multi preset
            auto_click(window.left + 972, window.top + 265, window, waittime=0.8) # Create Squad
            auto_click(window.left + 1000, window.top + 195, window, waittime=0.8) # preset 1
            auto_click(window.left + 1000, window.top + 609, window, waittime=0.8) # MARCH
            time.sleep(3)
            watch_img("squad-2-5.png", confidence=0.9)



            # watch_img("squad.png", confidence=0.9)

            time.sleep(10)

    listener.stop()  # キーボード検知を停止