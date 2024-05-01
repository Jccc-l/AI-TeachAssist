import os
import sys
import time
import wave
import tempfile
import threading

import torch
import pyaudiowpatch as pyaudio
from faster_whisper import WhisperModel as whisper
import zhconv

class Transper:
    def __init__(self):
        # A bigger audio buffer gives better accuracy
        # but also increases latency in response.
        # 表示音频缓冲时间的常量
        self.AUDIO_BUFFER = 5
        # 表示记录输出的字符串
        self.segments=[]

    
    def transform2_zh_hans(self, string): # 中文繁体转为中文简体
        new_str = zhconv.convert(string, 'zh-hans')
        return new_str
    
    # 此函数使用 PyAudio 库录制音频，并将其保存为一个临时的 WAV 文件。
    # 使用 pyaudio.PyAudio 实例创建一个音频流，通过指定回调函数 callback 来实时写入音频数据到 WAV 文件。
    # time.sleep(AUDIO_BUFFER) 会阻塞执行，确保录制足够的音频时间。
    # 最后，函数返回保存的 WAV 文件的文件名。
    def record_audio(self, p, device):
        """Record audio from output device and save to temporary WAV file."""
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            filename = f.name
            wave_file = wave.open(filename, "wb")
            wave_file.setnchannels(device["maxInputChannels"])
            wave_file.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
            wave_file.setframerate(int(device["defaultSampleRate"]))

            def callback(in_data, frame_count, time_info, status):
                """Write frames and return PA flag"""
                wave_file.writeframes(in_data)
                return (in_data, pyaudio.paContinue)

            stream = p.open(
                format=pyaudio.paInt16,
                channels=device["maxInputChannels"],
                rate=int(device["defaultSampleRate"]),
                frames_per_buffer=pyaudio.get_sample_size(pyaudio.paInt16),
                input=True,
                input_device_index=device["index"],
                stream_callback=callback,
            )

            try:
                time.sleep(self.AUDIO_BUFFER)  # Blocking execution while playing
            finally:
                stream.stop_stream()
                stream.close()
                wave_file.close()
                # print(f"{filename} saved.")
        return filename

    # 此函数使用 Whisper 模型对录制的音频进行转录，并输出转录结果。
    def whisper_audio(self, filename, model):
        """Transcribe audio buffer and display."""
        # segments, info = model.transcribe(filename, beam_size=5, task="translate", language="zh", vad_filter=True, vad_parameters=dict(min_silence_duration_ms=1000))
        self.segments, info = model.transcribe(filename, beam_size=5, language="zh", vad_filter=True, vad_parameters=dict(min_silence_duration_ms=1000))
        os.remove(filename)
        # print(f"{filename} removed.")
        #for segment in self.segments:
            # print(f"[{segment.start:.2f} -> {segment.end:.2f}] {segment.text.strip()}")
            #print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            #self.transper = "[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text)

    # main 函数是整个脚本的主控制函数。
    # 加载 Whisper 模型，选择合适的计算设备（GPU 或 CPU）。
    # 获取默认的 WASAPI 输出设备信息，并选择默认的扬声器（输出设备）。
    # 使用 PyAudio 开始录制音频，并通过多线程运行 whisper_audio 函数进行音频转录。
    def transper(self):
        """Load model record audio and transcribe from default output device."""
        print("Loading model...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using {device} device.")
        # model = whisper("large-v3", device=device, compute_type="float16")
        model = whisper(r"faster_whispher_asr\\small", device='cpu', local_files_only=True)

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
            # if not default_speakers["isLoopbackDevice"]:
            #     for loopback in pya.get_loopback_device_info_generator():
            #         # Try to find loopback device with same name(and [Loopback suffix]).
            #         # Unfortunately, this is the most adequate way at the moment.
            #         print(loopback["name"])
            #         if default_speakers["name"] in loopback["name"]:
            #             default_speakers = loopback
            #             break
            #     else:
            #         print(
            #             """
            #             Default loopback output device not found.
            #             Run `python -m pyaudiowpatch` to check available devices.
            #             Exiting...
            #             """
            #         )
            #         sys.exit()

            print(
                f"Recording from: {default_speakers['name']} ({default_speakers['index']})\n"
            )

            while True:
                filename = self.record_audio(pya, default_speakers)
                thread = threading.Thread(target=self.whisper_audio, args=(filename, model))
                thread.start()
                for segment in self.segments:
                    if self.transform2_zh_hans(segment.text) == '字幕by索兰娅' :
                        print('Wait to speak!')
                        continue
                    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, self.transform2_zh_hans(segment.text)))

if __name__=='__main__':
    my_transper = Transper()
    my_transper.transper()
