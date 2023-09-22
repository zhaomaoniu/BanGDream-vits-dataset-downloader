import os
import random
import subprocess

# 设置相关路径和参数
character_id = 40
character_name = "taki"
speaker_id = 4

input_dir = f"voice/{character_id}/"
output_dir = "dataset/"
train_file = f"{character_id}_train.txt"
val_file = f"{character_id}_val.txt"
sample_rate = 22050
bit_depth = 16
channels = 1
min_duration = 1
max_duration = 10
train_val_ratio = 20  # train样本数量与val样本数量的比例

# 创建输出目录
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 获取所有mp3文件路径
mp3_files = [file for file in os.listdir(input_dir) if file.endswith(".mp3")]

transcript_dict = {}

# 将所有mp3文件处理为wav文件
for idx, file in enumerate(mp3_files):
    mp3_path = os.path.join(input_dir, file)
    wav_filename = f"{character_name}_{idx}.wav"
    wav_path = os.path.join(output_dir, wav_filename)

    transcript_dict[file[:-4]] = f"{character_name}_{idx}"

    if not os.path.exists(wav_path):
        # 使用ffmpeg将mp3文件转换为wav文件
        subprocess.call(
            [
                "ffmpeg",
                "-i",
                mp3_path,
                "-acodec",
                "pcm_s16le",
                "-ac",
                str(channels),
                "-ar",
                str(sample_rate),
                wav_path,
            ]
        )

# 随机选择一部分文件作为训练样本
num_train_samples = int(len(mp3_files) / (train_val_ratio + 1) * train_val_ratio)
train_files = random.sample(mp3_files, num_train_samples)

# 将训练样本处理为数据集
with open(train_file, "w", encoding="UTF-8") as train_txt:
    for file in train_files:
        transcript = file[:-4]
        wav_path = os.path.join(output_dir, transcript_dict[transcript] + ".wav")

        # 获取wav文件的时长
        duration = subprocess.check_output(
            [
                "ffprobe",
                "-i",
                wav_path,
                "-show_entries",
                "format=duration",
                "-v",
                "quiet",
                "-of",
                "csv=p=0",
            ]
        ).decode("utf-8")
        duration = float(duration)

        # 根据时长限制过滤掉不符合要求的音频文件
        if duration >= min_duration and duration <= max_duration:
            if speaker_id is not None:
                train_txt.write(f"{wav_path}|{speaker_id}|{transcript}\n")
            else:
                train_txt.write(f"{wav_path}|{transcript}\n")

# 选择另一部分文件作为验证样本
val_files = list(set(mp3_files) - set(train_files))

# 将验证样本处理为数据集
with open(val_file, "w", encoding="UTF-8") as val_txt:
    for file in val_files:
        transcript = file[:-4]
        wav_path = os.path.join(output_dir, transcript_dict[transcript] + ".wav")

        # 获取wav文件的时长
        duration = subprocess.check_output(
            [
                "ffprobe",
                "-i",
                wav_path,
                "-show_entries",
                "format=duration",
                "-v",
                "quiet",
                "-of",
                "csv=p=0",
            ]
        ).decode("utf-8")
        duration = float(duration)

        # 根据时长限制过滤掉不符合要求的音频文件
        if duration >= min_duration and duration <= max_duration:
            if speaker_id is not None:
                val_txt.write(f"{wav_path}|{speaker_id}|{transcript}\n")
            else:
                val_txt.write(f"{wav_path}|{transcript}\n")


# 输出处理完成的消息
print("数据集创建成功！")
print(f"训练样本数: {len(train_files)}")
print(f"验证样本数: {len(val_files)}")
print(f"训练样本文件: {train_file}")
print(f"验证样本文件: {val_file}")
