# tkinterとpygameをインポートする
import tkinter as tk
import pygame
import sys
import os
import azure.cognitiveservices.speech as speechsdk

# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

# The language of the voice that speaks.
speech_config.speech_synthesis_voice_name='ja-JP-NanamiNeural'

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

# pygameのモジュールを初期化する
pygame.init()

# pygame.mixerモジュールを初期化する
pygame.mixer.init()

#def speech_synthesizer_synthesis_canceled_cb(evt: speechsdk.SessionEventArgs):
#    print('SynthesisCanceled event')
#
def speech_synthesizer_synthesis_completed_cb(evt: speechsdk.SessionEventArgs):
    print('SynthesisCompleted event:')
    print('\tAudioData: {} bytes'.format(len(evt.result.audio_data)))
    print('\tAudioDuration: {}'.format(evt.result.audio_duration))
#
#def speech_synthesizer_synthesis_started_cb(evt: speechsdk.SessionEventArgs):
#    print('SynthesisStarted event')
#
def speech_synthesizer_synthesizing_cb(evt: speechsdk.SessionEventArgs):
    print('Synthesizing event:')
    print('\tAudioData: {} bytes'.format(len(evt.result.audio_data)))
#
#speech_synthesizer.synthesis_canceled.connect(speech_synthesizer_synthesis_canceled_cb)
speech_synthesizer.synthesis_completed.connect(speech_synthesizer_synthesis_completed_cb)
#speech_synthesizer.synthesis_started.connect(speech_synthesizer_synthesis_started_cb)
#speech_synthesizer.synthesizing.connect(speech_synthesizer_synthesizing_cb)

# 音声の再生と時間の管理
def play_sound(event):
    global current_index, version
    
    # ハイライトを全て消す
    for num in range(labels[0].index, labels[99].index+1):
        labels[num].config(bg="whitesmoke") # 背景色を白に戻す

    # 音声の再生
    index = event.widget.index    # イベントが発生したウィジェットのインデックスを取得する
    current_index = index         # グローバル変数にインデックスを代入する
    
    ssml = """<speak version='1.0' xml:lang='ja-JP' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts'>
        <voice name='{}'>
            <mstts:viseme type='redlips_front'/>
            {}
        </voice>
    </speak>""".format(speech_config.speech_synthesis_voice_name, texts[current_index])
    
    speech_synthesizer.start_speaking_ssml_async(ssml).get()

    
# 音声の停止
def stop_sound(event):
    global current_index
    
    # 音声ファイルを停止
    speech_synthesizer.stop_speaking_async()
    

# 次の音声を再生
def play_next():
    global current_index
    
    current_index += 1
    
    ssml = """<speak version='1.0' xml:lang='ja-JP' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts'>
        <voice name='{}'>
            <mstts:viseme type='redlips_front'/>
            {}
        </voice>
    </speak>""".format(speech_config.speech_synthesis_voice_name, texts[current_index])
    
    # 次の音声の再生
    speech_synthesis_result = speech_synthesizer.start_speaking_ssml_async(ssml).get()


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