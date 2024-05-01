import tkinter as tk
from tkinter import messagebox
from Automatic_Speech_Recognition.transper import *
import pyaudiowpatch as pyaudio
from faster_whisper import WhisperModel as whisper
import zhconv

import time
import cv2
import numpy as np
import pyautogui
from Gesture_Recognition.HandTrackingModule import HandDetector

class UI:
    def __init__(self):
        # 创建语音识别模块
        self.Transfer = Transper()
        
        # 创建一个窗口对象
        self.root = tk.Tk()

        # 设置窗口的标题
        self.root.title("教学辅助系统")

        # 设置窗口的大小
        self.root.geometry("200x200")

        # 创建一个标签
        label = tk.Label(self.root, text="欢迎使用教学辅助系统!")
        #label.pack(side=tk.TOP, fill=tk.X, anchor=tk.NW)
        label.place(x=10,y=5)

        # 创建一个按钮，并设置其文本为"点击我"
        # 当按钮被点击时，调用show_message函数
        button1 = tk.Button(self.root, text="使用手势辅助教学", command=self.hand_control)

        # 将按钮放置在窗口上
        button1.place(x=10,y= 50)  # pady 参数添加一些垂直填充

        button2 = tk.Button(self.root, text="退出", command=self.on_button_click)
        button2.place(x=10,y=150)
        
        button3 = tk.Button(self.root, text="使用课堂字幕", command=self.create_scrollable_popup)
        button3.place(x=10,y=100)
        self.popup = 0 # 创建一个弹窗
        self.popup_label = 0 # 弹窗里的文字
        self.segments = [] # 语音识别的分段
        self.break_transfer = False
    
            
    def hand_control(self): # 手势辅助教学提示框
        # 使用messagebox显示一个提示
        messagebox.showinfo("提示", "开始手势辅助教学！")
        self.gesturecontrol()
        
    # 关闭窗口
    def on_button_click(self):
        self.root.quit()
    
    def create_scrollable_popup(self):
        # 创建一个Toplevel窗口
        self.popup = tk.Toplevel(self.root)
        self.popup.title("课堂字幕")
        self.popup.geometry("400x100")  # 设置弹出窗口的大小

        def on_popup_destroy():
            self.break_transfer = True
            self.popup.after(100, lambda: self.popup.destroy())  # 设置延迟100ms后关闭窗口

        self.popup.protocol("WM_DELETE_WINDOW", on_popup_destroy)  # 绑定destroy事件

        # 创建一个Label组件，用于显示滚动字幕
        self.popup_label = tk.Label(self.popup, text="欢迎使用课堂字幕！", bg="black", fg="white", font=("Helvetica", 16))
        self.popup_label.pack(fill=tk.BOTH, expand=True)
        self.append_text(self.popup_label,'加载语音识别模块！')

        # 创建一个新的线程来执行耗时任务
        self.break_transfer=False
        thread = threading.Thread(target=self.transper)
        thread.start()

    def append_text(self, label, text):
        # 获取当前文本
        current_text = label.cget('text')
        # 拼接新的文本
        new_text = current_text + '\n' + text
        # 设置新的文本
        label.config(text=new_text)
        # 如果文本超过一定长度，则清空
        if len(new_text) > 20:
            label.config(text=text)
    
    def mainloop(self):
        self.root.mainloop()
        
    def transper(self):
        """Load model record audio and transcribe from default output device."""
        print("Loading model...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using {device} device.")
        #model = whisper(r"faster-whisper-small", device=device, compute_type="float16")
        model = whisper(r"faster-whisper-small", device='cpu', local_files_only=True)

        print("Model loaded.")

        with pyaudio.PyAudio() as pya:
            # 获取麦克风设备信息
            microphone_info = pya.get_default_input_device_info()
            
            print(f"Using {microphone_info['name']} ({microphone_info['index']})")

            # 设置音频流参数
            sample_rate = 44100  # 采样率
            channels = 1  # 单声道
            format = pyaudio.paInt16  # 数据格式
            frames_per_buffer = 1024  # 每块音频数据帧的大小

            # 打开音频流
            stream = pya.open(
                format=format,
                channels=channels,
                rate=sample_rate,
                input=True,
                frames_per_buffer=frames_per_buffer
            )
            # Create PyAudio instance via context manager.
            try:
                # Get default WASAPI info
                wasapi_info = pya.get_host_api_info_by_type(pyaudio.paWASAPI)
            except OSError:
                print("Looks like WASAPI is not available on the system. Exiting...")
                sys.exit()

            # Get default WASAPI speakers
            default_speakers = pya.get_device_info_by_index(
                wasapi_info["defaultInputDevice"]
            )
            print(default_speakers)

            print(
                f"Recording from: {default_speakers['name']} ({default_speakers['index']})\n"
            )

            while not self.break_transfer:
                filename = self.Transfer.record_audio(pya, default_speakers)
                thread = threading.Thread(target=self.whisper_audio, args=(filename, model))
                thread.start()
                for segment in self.segments:
                    if self.transform2_zh_hans(segment.text) == '字幕by索兰娅' :
                        if not self.break_transfer:
                            self.append_text(self.popup_label,'Wait to speak!')
                        print('Wait to speak!')
                        continue
                    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, self.transform2_zh_hans(segment.text)))
                    if not self.break_transfer:
                        self.append_text(self.popup_label, self.transform2_zh_hans(segment.text))

    def whisper_audio(self, filename, model):
        """Transcribe audio buffer and display."""
        # segments, info = model.transcribe(filename, beam_size=5, task="translate", language="zh", vad_filter=True, vad_parameters=dict(min_silence_duration_ms=1000))
        self.segments, info = model.transcribe(filename, beam_size=5, language="zh", vad_filter=True,
                                               vad_parameters=dict(min_silence_duration_ms=1000))
        os.remove(filename)

    def transform2_zh_hans(self, string): # 中文繁体转为中文简体
        new_str = zhconv.convert(string, 'zh-hans')
        return new_str

    def gesturecontrol(self):
        # 设置屏幕尺寸和摄像头分辨率
        wScr, hScr = pyautogui.size()
        wCam, hCam = 1280, 720

        # 设置虚拟鼠标移动范围的矩形框
        # pt1, pt2 = (100, 100), (1000, 500)
        pt1, pt2 = (300, 50), (wCam - 100, hCam - 200)

        # 打开摄像头
        cap = cv2.VideoCapture(0)  # 使用第二个摄像头
        cap.set(3, wCam)  # 设置摄像头的宽度
        cap.set(4, hCam)  # 设置摄像头的高度

        pTime = 0  # 初始化上一帧开始处理的时间
        pLocx, pLocy = 0, 0  # 初始化上一帧鼠标的位置
        smooth = 6  # 平滑系数，用于使鼠标移动平滑
        frame = 0  # 初始化帧计数器
        toggle = False  # 标志变量，用于拖拽操作的切换
        prev_state = [1, 1, 1, 1, 1]  # 初始化上一帧手势状态
        current_state = [1, 1, 1, 1, 1]  # 初始化当前帧手势状态

        detector = HandDetector(mode=False,  # 视频流
                                maxHands=1,  # 最多检测一只手
                                detectionCon=0.8,  # 最小检测置信度
                                minTrackCon=0.5)  # 最小跟踪置信度

        while True:
            # 图片是否成功接收、img帧图像
            success, img = cap.read()
            img = cv2.flip(img, flipCode=1)
            # 在图像窗口上创建一个矩形框，在该区域内移动鼠标
            cv2.rectangle(img, pt1, pt2, (0, 255, 255), 5)
            # 手部关键点检测
            hands, img = detector.findHands(img, flipType=False, draw=True)
            if hands:
                lmList = hands[0]['lmList']  # hands是由N部字典组成的列表，字典包括每只手的关键点信息,此处代表第0个手
                hand_center = hands[0]['center']
                # 获取食指指尖坐标，和中指指尖坐标
                x1, y1, z1 = lmList[8]  # 食指尖的关键点索引号为8
                x2, y2, z2 = lmList[12]  # 中指指尖索引12
                cx, cy, cz = (x1 + x2) // 2, (y1 + y2) // 2, (z1 + z2) // 2  # 计算食指和中指两指之间的中点坐标
                hand_cx, hand_cy = hand_center[0], hand_center[1]
                # 检查哪个手指是朝上的
                fingers = detector.fingersUp(hands[0])
                # 计算食指尖和中指尖之间的距离distance,绘制好了的图像img,指尖连线的信息info
                distance, info, img = detector.findDistance((x1, y1), (x2, y2), img)
                # 将食指指尖的移动范围从预制的窗口范围，映射到电脑屏幕范围
                x3 = np.interp(x1, (pt1[0], pt2[0]), (0, wScr))
                y3 = np.interp(y1, (pt1[1], pt2[1]), (0, hScr))
                # 手心坐标映射到屏幕范围
                x4 = np.interp(hand_cx, (pt1[0], pt2[0]), (0, wScr))
                y4 = np.interp(hand_cy, (pt1[1], pt2[1]), (0, hScr))
                # 平滑插值，使手指在移动鼠标时，鼠标箭头不会一直晃动
                cLocx = pLocx + (x3 - pLocx) / smooth
                cLocy = pLocy + (y3 - pLocy) / smooth
                # 记录当前手势状态
                current_state = fingers
                # 记录相同状态的帧数
                if prev_state == current_state:
                    frame = frame + 1
                else:
                    frame = 0
                prev_state = current_state

                if fingers != [0, 0, 0, 0, 0] and toggle and frame >= 2:
                    pyautogui.mouseUp()  # 释放
                    toggle = False
                    print("释放左键")

                # 只有食指和中指竖起，就认为是移动鼠标
                if fingers[1] == 1 and fingers[2] == 1 and sum(fingers) == 2 and frame >= 1:
                    # 给出鼠标移动位置坐标
                    pyautogui.moveTo(cLocx, cLocy)
                    # print("移动鼠标")
                    # 更新前一帧的鼠标所在位置坐标
                    pLocx, pLocy = cLocx, cLocy

                    # 当指间距离小于43（像素距离）就认为是点击鼠标
                    if distance < 43 and frame >= 1:
                        # 在食指尖画个绿色的圆，表示点击鼠标
                        cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                        pyautogui.click(button='left')
                        cv2.putText(img, "left_click", (150, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                        print("左击鼠标")

                # 中指弯下食指在上，右击鼠标
                elif fingers[1] == 1 and fingers[2] == 0 and sum(fingers) == 1 and frame >= 2:
                    pyautogui.rightClick()
                    print("右击鼠标")
                    cv2.putText(img, "right_click", (150, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                    cv2.circle(img, (x2, y2), 15, (0, 255, 0), cv2.FILLED)

                # 五指紧握，按紧左键进行拖拽
                elif fingers == [0, 0, 0, 0, 0]:
                    if not toggle:
                        pyautogui.mouseDown()  # 按下
                    toggle = True
                    pyautogui.moveTo(cLocx, cLocy)
                    pLocx, pLocy = cLocx, cLocy

                # 拇指张开，其他弯曲，按一次上键
                elif fingers == [1, 0, 0, 0, 0] and frame >= 2:
                    pyautogui.press('up')
                    print("按下上键")
                    time.sleep(0.5)

                # 拇指弯曲，其他竖直，按一次下键
                elif fingers == [0, 1, 1, 1, 1] and frame >= 2:
                    pyautogui.press('down')
                    print("按下下键")
                    time.sleep(0.5)

            # 查看FPS
            cTime = time.time()
            fps = 1 / (cTime - pTime)  # 处理完一帧图像的时间
            pTime = cTime  # 重置起始时
            # 显示fps信息
            cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

            cv2.imshow('frame', img)
            if cv2.waitKey(1) & 0xFF == 27:  # ESC键退出
                break

        # 释放视频资源
        cap.release()
        cv2.destroyAllWindows()


if __name__=='__main__':
    my_ui = UI()
    # 开始事件循环
    my_ui.mainloop()