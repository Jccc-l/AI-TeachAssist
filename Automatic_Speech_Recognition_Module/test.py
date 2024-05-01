# local_files_only=True 表示加载本地模型
# model_size_or_path=path 指定加载模型路径
# device="cuda" 指定使用cuda
# compute_type="int8_float16" 量化为8位
# language="zh" 指定音频语言
# vad_filter=True 开启vad
# vad_parameters=dict(min_silence_duration_ms=1000) 设置vad参数
from faster_whisper import WhisperModel

model_size = "large-v3"
path = r"E:\大创\faster_whispher_asr\small"

# Run on GPU with FP16
model = WhisperModel(model_size_or_path=path, device="cpu", compute_type="int8")
 
# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")

segments, info = model.transcribe(r"faster_whispher_asr\\audio.wav", beam_size=5, language="zh", vad_filter=True, vad_parameters=dict(min_silence_duration_ms=1000))

print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))


