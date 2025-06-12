import tkinter as tk
from tkinter import ttk, scrolledtext
import win32gui
import win32con
import win32api
import pyautogui
import threading
import time
from PIL import Image, ImageTk
import io

class ClickPositionReader:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("クリック位置取得・読み取りツール")
        self.root.geometry("800x600")
        
        self.is_monitoring = False
        self.click_history = []
        
        self.setup_ui()
        self.update_mouse_position()
        
    def setup_ui(self):
        # メインフレーム
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 現在のマウス位置表示
        pos_frame = ttk.LabelFrame(main_frame, text="現在のマウス位置", padding="5")
        pos_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.pos_label = ttk.Label(pos_frame, text="座標: (0, 0)")
        self.pos_label.grid(row=0, column=0, sticky=tk.W)
        
        self.window_label = ttk.Label(pos_frame, text="ウィンドウ: なし")
        self.window_label.grid(row=1, column=0, sticky=tk.W)
        
        self.client_pos_label = ttk.Label(pos_frame, text="クライアント座標: (0, 0)")
        self.client_pos_label.grid(row=2, column=0, sticky=tk.W)
        
        # コントロールボタン
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.monitor_btn = ttk.Button(control_frame, text="クリック監視開始", 
                                    command=self.toggle_monitoring)
        self.monitor_btn.grid(row=0, column=0, padx=5)
        
        ttk.Button(control_frame, text="現在位置を記録", 
                  command=self.record_current_position).grid(row=0, column=1, padx=5)
        
        ttk.Button(control_frame, text="履歴クリア", 
                  command=self.clear_history).grid(row=0, column=2, padx=5)
        
        ttk.Button(control_frame, text="スクリーンショット", 
                  command=self.take_screenshot).grid(row=0, column=3, padx=5)
        
        # クリック履歴表示
        history_frame = ttk.LabelFrame(main_frame, text="クリック履歴", padding="5")
        history_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.history_text = scrolledtext.ScrolledText(history_frame, height=15, width=70)
        self.history_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # ウィンドウ選択
        window_frame = ttk.LabelFrame(main_frame, text="ウィンドウ選択", padding="5")
        window_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(window_frame, text="ウィンドウ一覧更新", 
                  command=self.update_window_list).grid(row=0, column=0, padx=5)
        
        self.window_var = tk.StringVar()
        self.window_combo = ttk.Combobox(window_frame, textvariable=self.window_var, width=50)
        self.window_combo.grid(row=0, column=1, padx=5)
        
        # グリッドの重み設定
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
    def update_mouse_position(self):
        """マウス位置を継続的に更新"""
        try:
            x, y = pyautogui.position()
            self.pos_label.config(text=f"スクリーン座標: ({x}, {y})")
            
            # カーソル下のウィンドウを取得
            hwnd = win32gui.WindowFromPoint((x, y))
            if hwnd:
                try:
                    window_title = win32gui.GetWindowText(hwnd)
                    class_name = win32gui.GetClassName(hwnd)
                    self.window_label.config(text=f"ウィンドウ: {window_title} ({class_name})")
                    
                    # クライアント座標を計算
                    try:
                        client_x, client_y = win32gui.ScreenToClient(hwnd, (x, y))
                        self.client_pos_label.config(text=f"クライアント座標: ({client_x}, {client_y})")
                    except:
                        self.client_pos_label.config(text="クライアント座標: 取得不可")
                        
                except:
                    self.window_label.config(text="ウィンドウ: 取得不可")
                    self.client_pos_label.config(text="クライアント座標: 取得不可")
            else:
                self.window_label.config(text="ウィンドウ: なし")
                self.client_pos_label.config(text="クライアント座標: なし")
                
        except Exception as e:
            print(f"マウス位置更新エラー: {e}")
            
        # 100ms後に再実行
        self.root.after(100, self.update_mouse_position)
        
    def toggle_monitoring(self):
        """クリック監視の開始/停止"""
        if self.is_monitoring:
            self.is_monitoring = False
            self.monitor_btn.config(text="クリック監視開始")
        else:
            self.is_monitoring = True
            self.monitor_btn.config(text="クリック監視停止")
            threading.Thread(target=self.monitor_clicks, daemon=True).start()
            
    def monitor_clicks(self):
        """クリックを監視"""
        last_state = win32api.GetKeyState(0x01)  # 左クリック
        
        while self.is_monitoring:
            current_state = win32api.GetKeyState(0x01)
            
            # クリックが検出された場合
            if current_state != last_state and current_state < 0:
                self.record_click()
                
            last_state = current_state
            time.sleep(0.01)
            
    def record_click(self):
        """クリック位置を記録"""
        try:
            x, y = pyautogui.position()
            hwnd = win32gui.WindowFromPoint((x, y))
            
            click_info = {
                'time': time.strftime('%H:%M:%S'),
                'screen_pos': (x, y),
                'hwnd': hwnd,
                'window_title': '',
                'class_name': '',
                'client_pos': None
            }
            
            if hwnd:
                try:
                    click_info['window_title'] = win32gui.GetWindowText(hwnd)
                    click_info['class_name'] = win32gui.GetClassName(hwnd)
                    click_info['client_pos'] = win32gui.ScreenToClient(hwnd, (x, y))
                except:
                    pass
                    
            self.click_history.append(click_info)
            self.update_history_display()
            
        except Exception as e:
            print(f"クリック記録エラー: {e}")
            
    def record_current_position(self):
        """現在のマウス位置を記録"""
        self.record_click()
        
    def update_history_display(self):
        """履歴表示を更新"""
        self.history_text.delete(1.0, tk.END)
        
        for i, click in enumerate(reversed(self.click_history[-20:])):  # 最新20件
            info_text = f"[{click['time']}] "
            info_text += f"スクリーン: ({click['screen_pos'][0]}, {click['screen_pos'][1]}) "
            
            if click['client_pos']:
                info_text += f"クライアント: ({click['client_pos'][0]}, {click['client_pos'][1]}) "
                
            if click['window_title']:
                info_text += f"ウィンドウ: {click['window_title']} "
                
            if click['class_name']:
                info_text += f"クラス: {click['class_name']}"
                
            info_text += f" HWND: {click['hwnd']}\n"
            
            # Pythonコード生成
            if click['client_pos']:
                code_text = f"# クリック用コード\n"
                code_text += f"hwnd = win32gui.FindWindow(None, \"{click['window_title']}\")\n"
                code_text += f"click(hwnd, {click['client_pos'][0]}, {click['client_pos'][1]})  # クライアント座標\n"
                code_text += f"# または\n"
                code_text += f"pyautogui.click({click['screen_pos'][0]}, {click['screen_pos'][1]})  # スクリーン座標\n\n"
                info_text += code_text
                
            self.history_text.insert(tk.END, info_text + "\n" + "-"*80 + "\n")
            
    def clear_history(self):
        """履歴をクリア"""
        self.click_history.clear()
        self.history_text.delete(1.0, tk.END)
        
    def update_window_list(self):
        """ウィンドウ一覧を更新"""
        windows = []
        
        def enum_windows_proc(hwnd, lParam):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:
                    windows.append(f"{title} (HWND: {hwnd})")
            return True
            
        win32gui.EnumWindows(enum_windows_proc, 0)
        self.window_combo['values'] = windows
        
    def take_screenshot(self):
        """現在のマウス位置周辺のスクリーンショットを取得"""
        try:
            x, y = pyautogui.position()
            # マウス位置を中心とした200x200の範囲をキャプチャ
            screenshot = pyautogui.screenshot(region=(x-100, y-100, 200, 200))
            
            # ファイルに保存
            filename = f"click_area_{int(time.time())}.png"
            screenshot.save(filename)
            
            info_text = f"[{time.strftime('%H:%M:%S')}] スクリーンショット保存: {filename}\n"
            info_text += f"中心座標: ({x}, {y})\n\n"
            self.history_text.insert(tk.END, info_text)
            
        except Exception as e:
            print(f"スクリーンショットエラー: {e}")
            
    def run(self):
        """アプリケーション実行"""
        self.update_window_list()
        self.root.mainloop()

# 簡単な座標取得スクリプト（コマンドライン用）
def simple_position_getter():
    """シンプルな座標取得（ESCで終了）"""
    print("マウス位置取得モード - ESCキーで終了")
    print("左クリックで位置を記録します")
    
    try:
        last_click_state = win32api.GetKeyState(0x01)
        
        while True:
            # ESCキーチェック
            if win32api.GetAsyncKeyState(0x1B) & 0x8000:  # ESC
                break
                
            # 左クリックチェック
            current_click_state = win32api.GetKeyState(0x01)
            if current_click_state != last_click_state and current_click_state < 0:
                x, y = pyautogui.position()
                hwnd = win32gui.WindowFromPoint((x, y))
                
                print(f"\n--- クリック検出 ---")
                print(f"スクリーン座標: ({x}, {y})")
                
                if hwnd:
                    try:
                        title = win32gui.GetWindowText(hwnd)
                        class_name = win32gui.GetClassName(hwnd)
                        client_x, client_y = win32gui.ScreenToClient(hwnd, (x, y))
                        
                        print(f"ウィンドウタイトル: {title}")
                        print(f"クラス名: {class_name}")
                        print(f"クライアント座標: ({client_x}, {client_y})")
                        print(f"HWND: {hwnd}")
                        
                        # コード生成
                        print(f"\n# 生成されたクリックコード:")
                        print(f"hwnd = win32gui.FindWindow(None, \"{title}\")")
                        print(f"click(hwnd, {client_x}, {client_y})")
                        
                    except Exception as e:
                        print(f"ウィンドウ情報取得エラー: {e}")
                        
            last_click_state = current_click_state
            time.sleep(0.01)
            
    except KeyboardInterrupt:
        pass
    
    print("終了します")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "simple":
        # コマンドライン版実行
        simple_position_getter()
    else:
        # GUI版実行
        app = ClickPositionReader()
        app.run()