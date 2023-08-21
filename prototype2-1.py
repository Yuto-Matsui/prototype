# tkinterとpygameをインポートする
import tkinter as tk
import pygame
import sys
import signal
from pydub import AudioSegment
from pydub.playback import play
import win32gui

def handler(signum, frame):
    sys.exit(0) # プログラムを終了させる

signal.signal(signal.SIGINT, handler) # Ctrl+cのシグナルに対応する関数を登録する
# signal.signal(signal.SIGINT, signal.SIG_DFL) # OS標準のハンドラーに戻す

# 音声ファイルのパスをsound.pyから読み込む
from sound1 import sound_files1
from sound2 import sound_files2
from sound3 import sound_files3

# pygameのモジュールを初期化する
pygame.init()

# pygame.mixerモジュールを初期化する
pygame.mixer.init()

# 音声ファイルをpygame.mixer.Soundオブジェクトとして読み込む
sounds1 = [pygame.mixer.Sound(file) for file in sound_files1]
sounds2 = [pygame.mixer.Sound(file) for file in sound_files2]
sounds3 = [pygame.mixer.Sound(file) for file in sound_files3]

sounds = [sounds1, sounds2, sounds3]

# 音声ファイルの長さをリストに格納する
sound_lengths1 = [sound.get_length() * 1000 + 100 for sound in sounds1] # ミリ秒単位に変換
sound_lengths2 = [sound.get_length() * 1000 + 100 for sound in sounds2] # ミリ秒単位に変換
sound_lengths3 = [sound.get_length() * 1000 + 100 for sound in sounds3] # ミリ秒単位に変換

sound_lengths = [sound_lengths1, sound_lengths2, sound_lengths3]

#どの音声速度を使用するか
version = 0
next_version = 0


# 音声ファイルが終了したときに発生するイベントを定義する
SONG_END = pygame.USEREVENT + 1


def is_sound_playing():
    # グローバル変数を参照する
    global current_index
    # ミキサーモジュールの再生状態を返す
    return pygame.mixer.get_busy()


# 音声の再生と時間の管理
def play_sound(event):
    global current_index, version
    
    # ハイライトを全て消す
    for num in range(labels[0].index, labels[99].index+1):
        labels[num].config(bg="whitesmoke") # 背景色を白に戻す

    # 音声の再生
    index = event.widget.index    # イベントが発生したウィジェットのインデックスを取得する
    current_index = index         # グローバル変数にインデックスを代入する
    sounds[version][current_index].play()  # そのインデックスに対応する音声ファイルを再生する
    is_playing = True
    
    start_time = pygame.time.get_ticks()        # 音声ファイルが再生された時点の時間を取得
    elapsed_time = 0                            # 再生から経過した時間
    
    # テキストの背景色を変える
    highlight_text(index, start_time)


# 音声の停止
def stop_sound(event):
    global current_index, is_playing
    
    # 音声ファイルを停止
    sounds[version][current_index].stop()
    #sourceAudio
    
    is_playing = False


# 背景色を黄色にする
def highlight_text(index, start_time):
    global elapsed_time
    
    # 時間の取得
    current_time = pygame.time.get_ticks()    # 現在の時間を取得
    elapsed_time = current_time - start_time  # 音声ファイルが再生された時点の時間と現在の時間の差分を計算する
    
    # 差分が音声ファイルの長さより小さい間は，テキストの背景色を変える
    if elapsed_time < sound_lengths[version][index] - 110:  # elapsed_timeは元音声より大きくならないため100引いた値にしている
        labels[index].config(bg="yellow")     # 背景色を黄色にする
        
        # 音声ファイルが再生中であれば，10ミリ秒後に再帰的に呼ぶ
        if is_sound_playing():
            root.after(10, highlight_text, index, start_time) 
    else:
        labels[index].config(bg="white smoke") # 背景色を白に戻す
        play_next()


def increase_speed():
    global next_version
    
    if next_version <= 1:
        next_version += 1
    
    print(next_version)
        

def decrease_speed():
    global next_version
    
    if next_version >= 1:
        next_version -= 1
        
    print(next_version)


# クリックの回数を保持するグローバル変数を定義する
click_count = 0


# 音声の再生と停止の切り替え
def toggle_sound(event):
    global click_count
    
    # クリックの回数を増やす
    click_count += 1
    
    # クリックの回数が奇数ならplay_sound()を呼び出し，偶数ならstop_sound()を呼び出す
    if click_count % 2 == 1:
        play_sound(event)
    else:
        stop_sound(event)


# 次の音声を再生
def play_next():
    global current_index, is_playing, version, next_version
    
    current_index += 1
    version = next_version
    
    # 次の音声の再生
    #pygame.mixer.music.load(sounds[version][current_index])  # そのインデックスに対応する音声ファイルを読み込む
    sounds[version][current_index].play()                         # 音声ファイルを再生する
    
    # 音声ファイルが再生された時点の時間を取得する
    start_time = pygame.time.get_ticks()
    
    # 音声ファイルが再生されている間は，テキストの背景色を変える関数を呼ぶ
    highlight_text(current_index, start_time)


# ルートウィンドウを作成する
root = tk.Tk()
root.title("音声付き文章")
root.config(bg="whitesmoke")

# 全画面モードにする
#root.attributes("-fullscreen", True)

# Canvasウィジェットを作成する
canvas = tk.Canvas(root, width=1250, height=1300)

# FrameウィジェットをCanvasの中に埋め込む
frame = tk.Frame(canvas)

# Scrollbarウィジェットを作成し、Canvasと連動させる
scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview, bg="red") # 背景色を赤にする
canvas.configure(yscrollcommand=scrollbar.set)

# CanvasとScrollbarをrootに配置する
scrollbar.grid(row=0, column=1, sticky=tk.N + tk.S) # gridメソッドで配置する
canvas.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W) # gridメソッドで配置し、stickyオプションで引き伸ばす

# ルートウィンドウのサイズ変更に対応する
root.rowconfigure(0, weight=1) # weightオプションで優先度を指定する
root.columnconfigure(0, weight=1) # weightオプションで優先度を指定する

# label_widget.txtから文章を読み込む
with open("label_widget.txt", "r", encoding="utf-8") as f:
    texts = f.read().splitlines()

# ラベルウィジェットのリストを作成する
labels = []

# ラベルウィジェットにインデックス属性と左クリックイベントを追加する
for i, text in enumerate(texts):
    label = tk.Label(frame, text=text, font=("Helvetica", 15), anchor="w")
    label.index = i
    label.bind("<Button-1>", toggle_sound)
    labels.append(label)
    
#右ボタンウィジェットを作成
right_button = tk.Button(root, text=">>", font=("Helvetica", 15), command=increase_speed)

#左ボタンウィジェットを作成
left_button = tk.Button(root, text="<<", font=("Helvetica", 15), command=decrease_speed)

#ボタンウィジェットをrootに配置
right_button.grid(row=1, column=1, sticky=tk.E) 
left_button.grid(row=1, column=0, sticky=tk.W)

# Ctrl+Cが押されたときにプログラムを終了する関数
def quit(event):
    pygame.quit()
    root.destroy()
    sys.exit(0)

# ルートウィンドウにキーバインドを設定
root.bind("<Control-c>", quit)

# ラベルウィジェットを配置する
for label in labels:
    label.pack()

# Canvasのスクロール領域をFrameのサイズに合わせる
frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# CanvasにFrameを埋め込む
canvas.create_window((0, 0), window=frame, anchor="nw")

# pygame.time.Clockオブジェクトを作成する
clock = pygame.time.Clock()

# マウスホイールのイベント名とdelta値をプラットフォームごとに設定する
if sys.platform == "win32":
    # Windowsでは<MouseWheel>イベントを使い、delta値を120で割る
    mousewheel = "<MouseWheel>"
    def delta(event):
        return -1 * event.delta // 120
elif sys.platform == "darwin":
    # Macでは<MouseWheel>イベントを使い、delta値をそのまま使う
    mousewheel = "<MouseWheel>"
    def delta(event):
        return event.delta
else:
    # Linuxでは<Button-4>と<Button-5>イベントを使い、delta値は1か-1にする
    mousewheel = "<Button-4><Button-5>"
    def delta(event):
        return 1 if event.num == 4 else -1

# マウスホイールのイベントハンドラを定義する
def on_mousewheel(event):
    # Canvasのyview_scrollメソッドを呼び、unitsオプションで単位を指定する
    canvas.yview_scroll(delta(event), "units")

# Canvasにマウスホイールのイベントをバインドする
canvas.bind(mousewheel, on_mousewheel)

# Canvas全体にマウスホイールのイベントをバインドする
canvas.bind_all(mousewheel, on_mousewheel)

# ルートウィンドウのメインループを開始する
while True:
    try:
        # フレームレートを30フレームに固定する
        clock.tick(30)
    except KeyboardInterrupt:
        # Ctrl+cが押されたら終了する
        pygame.quit()
        sys.exit()
     #イベント処理を行う
    for event in pygame.event.get():
        # 閉じるボタンが押されたら終了する
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        # マウスボタンが押されたら対応する関数を呼ぶ
        elif event.type == pygame.MOUSEBUTTONDOWN:
            toggle_sound()
    root.update()
