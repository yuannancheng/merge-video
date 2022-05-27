#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import os
from tkinter import filedialog


def merge(video, audio, output):
    return os.system(f"ffmpeg -i \"{video}\" -i \"{audio}\" -acodec copy -vcodec copy \"{output}\" -loglevel quiet")


def get_file_name(path, show_type=False):
    path = os.path.basename(path)
    return (path.split('.')[0], path.split('.')[1]) if show_type else path.split('.')[0]


def main():
    video_file_types = [('常用视频格式', ['*.mp4', '*.wmv', '*.m4v', '*.avi', '*.mkv', '*.flv'])]
    audio_file_types = [('常用音频格式', ['*.mp3', '*.m4a', '*.wav', '*.wma', '*.acc', '*.ogg'])]

    video_files = filedialog.askopenfilenames(title='选择视频文件', filetypes=video_file_types)
    audio_files = filedialog.askopenfilenames(title='选择音频文件', filetypes=audio_file_types)

    video_file_names = {}
    audio_file_names = {}

    # 记录同名不同后缀文件
    repeat = {
        'video': [],
        'audio': []
    }

    for audio_file_path in audio_files:
        file_name = get_file_name(audio_file_path)
        if file_name in audio_file_names:
            # 存在同名不同后缀音频文件
            repeat['audio'].append(audio_file_path)
        else:
            # 保存音频文件信息
            audio_file_names[file_name] = audio_file_path

    for video_file_path in video_files:
        file_name, file_type = get_file_name(video_file_path, show_type=True)
        if file_name in video_file_names:
            # 存在同名不同后缀视频文件
            repeat['video'].append(video_file_path)
        elif file_name in audio_file_names:
            # 音视频文件都存在，合并音视频
            print('正在处理 {}'.format(video_file_path))
            merge(video_file_path, audio_file_names[file_name],
                  os.path.join(os.path.dirname(os.path.abspath(video_file_path)), # 取得文件所在目录绝对路径
                               '{}.merge.{}'.format(file_name, file_type)
                               )
                  )
            audio_file_names.pop(file_name)  # 删除已使用的音频文件
        else:
            # 没有对应的音频文件
            video_file_names[file_name] = video_file_path



    if repeat['video']:
        print('{} 个视频重名：\n  {}'.format(len(repeat['video']), '\n  '.join(repeat['video'])))
    if repeat['audio']:
        print('{} 个音频重名：\n  {}'.format(len(repeat['audio']), '\n  '.join(repeat['audio'])))
    if video_file_names:
        print('{} 个视频未找到同名音频文件：\n  {}'.format(len(video_file_names.keys()), '\n  '.join(video_file_names.values())))
    if audio_file_names:
        print('{} 个音频未找到同名视频文件：\n  {}'.format(len(audio_file_names.keys()), '\n  '.join(audio_file_names.values())))


if __name__ == '__main__':
    main()
