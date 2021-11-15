'''
Создание видео
Исходник - папка с изображениями
'''



import moviepy.video.io.ImageSequenceClip
from moviepy.editor import *
import cv2
import numpy as np
import glob
import os
song_name = glob.glob("lyrics/song/*.mp3")[0]   #result---- lyrics/song\Future - Jumpin on a Jet.mp3
artist_title = song_name.split('\\')[1].replace('.mp3', '')
folder = song_name.split('-')[1].split('.mp3')[0]
print(song_name)
print(folder)
print(artist_title)

audioclip = AudioFileClip(song_name)

new_audioclip = CompositeAudioClip([audioclip])

size = (1920,1080)
image_folder = f'lyrics/connect/{artist_title}'
img_array = []
image_files = [image_folder+'/'+img for img in os.listdir(image_folder) if img.endswith(".jpg")]
image_sorted = sorted(image_files, key=lambda t: os.stat(t).st_mtime)
print(image_sorted)
clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_sorted, fps=1)
clip.audio = new_audioclip
clip.write_videofile(f'lyrics/videos/{artist_title}.mp4')
