# tkinterとpygameをインポートする
import tkinter as tk
import pygame
import sys

sound_files = []

for i in range(1, 101):
    sound_files.append("sound/iejuu (" + str(i) + ").wav")

# pygameのモジュールを初期化する
pygame.init()

# pygame.mixerモジュールを初期化する
pygame.mixer.init()

# 音声ファイルをpygame.mixer.Soundオブジェクトとして読み込む
sounds = [pygame.mixer.Sound(file) for file in sound_files]

# 音声ファイルの長さをリストに格納する
sound_lengths = [sound.get_length() * 1000 for sound in sounds] # ミリ秒単位に変換

# 音声ファイルが終了したときに発生するイベントを定義する
SONG_END = pygame.USEREVENT + 1

def is_sound_playing():
    # グローバル変数を参照する
    global current_index
    # ミキサーモジュールの再生状態を返す
    return pygame.mixer.get_busy()

# 音声の再生と時間の管理
def play_sound(event):
    global current_index
    
    # ハイライトを全て消す
    for num in range(label1.index, label8.index+1):
        labels[num].config(bg="white smoke") # 背景色を白に戻す
    
    # 音声の再生
    index = event.widget.index    # イベントが発生したウィジェットのインデックスを取得する
    current_index = index         # グローバル変数にインデックスを代入する
    sounds[current_index].play()  # そのインデックスに対応する音声ファイルを再生する
    
    is_playing = True
    
    start_time = pygame.time.get_ticks()        # 音声ファイルが再生された時点の時間を取得
    elapsed_time = 0                            # 再生から経過した時間
    
    # テキストの背景色を変える
    highlight_text(index, start_time)


# 音声の停止
def stop_sound(event):
    global current_index, is_playing
    
    # 音声ファイルを停止
    sounds[current_index].stop()
    
    is_playing = False


# 背景色を黄色にする
def highlight_text(index, start_time):
    global elapsed_time
    
    # 時間の取得
    current_time = pygame.time.get_ticks()    # 現在の時間を取得
    elapsed_time = current_time - start_time  # 音声ファイルが再生された時点の時間と現在の時間の差分を計算する
    
    # 差分が音声ファイルの長さより小さい間は，テキストの背景色を変える
    if elapsed_time < sound_lengths[index] - 100:  # elapsed_timeは元音声より大きくならないため100引いた値にしている
        #print(elapsed_time) 
        #print(sound_lengths[index])
        labels[index].config(bg="yellow")     # 背景色を黄色にする
        
        # 音声ファイルが再生中であれば，10ミリ秒後に再帰的に呼ぶ
        if is_sound_playing():
            root.after(10, highlight_text, index, start_time) 
    else:
        #labels[index].config(bg="white") # 背景色を白に戻す
        play_next()


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
    global current_index, is_playing

    # 前のテキストの背景色を白に戻す
    #labels[current_index].config(bg="white")
    
    current_index += 1
    
    # 次の音声の再生
    pygame.mixer.music.load(sound_files[current_index])  # そのインデックスに対応する音声ファイルを読み込む
    sounds[current_index].play()                         # 音声ファイルを再生する
    
    # 音声ファイルが再生された時点の時間を取得する
    start_time = pygame.time.get_ticks()
    
    # 音声ファイルが再生されている間は，テキストの背景色を変える関数を呼ぶ
    highlight_text(current_index, start_time)
        
    

# ルートウィンドウを作成する
root = tk.Tk()
root.title("音声付き文章")
root.config(bg="white smoke")

# ラベルウィジェットを作成し，文章を表示する
label1 = tk.Label(root, text="家じゅうの人たちは、なんと言ったでしょうか？")
label2 = tk.Label(root, text="まずさいしょに、マリーちゃんの言ったことを聞きましょう。")
label3 = tk.Label(root, text="その日は、マリーちゃんのお誕生日でした。")
label4 = tk.Label(root, text="マリーちゃんにとっては、いちばん楽しい日のような気がしました。")
label5 = tk.Label(root, text="小さなお友だちが、大ぜいあそびにきました。")
label6 = tk.Label(root, text="マリーちゃんは、いちばんきれいな着物を着ました。")
label7 = tk.Label(root, text="その着物は、いまでは神さまのところにいらっしゃるおばあさまから、いただいたものでした。")
label8 = tk.Label(root, text="おばあさまは、明るい美しい天国にいらっしゃるまえに、自分でこの着物をたって、ぬってくださったのです。")

# ラベルウィジェットを配置する
label1.pack()
label2.pack()
label3.pack()
label4.pack()
label5.pack()
label6.pack()
label7.pack()
label8.pack()

# 音声ファイルの長さをリストに格納する
sound_lengths = [pygame.mixer.Sound(file).get_length() * 1000 + 100 for file in sound_files] # ミリ秒単位に変換し，100ミリ秒足す

# 音声ファイルのインデックスを保持するグローバル変数を定義する
current_index = 0

# 音声ファイルが再生中かどうかを保持するグローバル変数を定義する
#is_playing = False

elapsed_time = 0
current_time = 0

# ラベルウィジェットに左クリックで音声再生または停止のイベントをバインドする # ここを修正
label1.bind("<Button-1>", toggle_sound)
label2.bind("<Button-1>", toggle_sound)
label3.bind("<Button-1>", toggle_sound)
label4.bind("<Button-1>", toggle_sound)
label5.bind("<Button-1>", toggle_sound)
label6.bind("<Button-1>", toggle_sound)
label7.bind("<Button-1>", toggle_sound)
label8.bind("<Button-1>", toggle_sound)


# ラベルウィジェットにインデックス属性を追加する
label1.index = 0
label2.index = 1
label3.index = 2
label4.index = 3
label5.index = 4
label6.index = 5
label7.index = 6
label8.index = 7

# ラベルウィジェットのリストを作成する
labels = [label1, label2, label3, label4, label5, label6, label7, label8]

# pygame.time.Clockオブジェクトを作成する
clock = pygame.time.Clock()

# ルートウィンドウのメインループを開始する
while True:
    # フレームレートを30フレームに固定する
    clock.tick(30)
    # イベント処理を行う
    for event in pygame.event.get():
        # 閉じるボタンが押されたら終了する
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            toggle_sound(event)
    # 画面を更新する
    root.update()