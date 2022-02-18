import pytube
import ffmpeg
from pytube import YouTube
import os
import re
from moviepy.editor import *


def combine_video_audio_ff(SAVE_PATH, filename):
    tmp = SAVE_PATH + "/" + filename + "vid.mp4"
    video_stream = ffmpeg.input(tmp)
    tmp = SAVE_PATH + "/" + filename + "aud.mp4"
    audio_stream = ffmpeg.input(tmp)
    tmp = filename + '.mp4'
    ffmpeg.output(audio_stream, video_stream, tmp).run()
# Delete video and audio files

"""
def combine_video_audio_mov(SAVE_PATH, filename):
    path = filename+"vid.mp4"
    print(path)
    clip = VideoFileClip(path)
    path = filename+"aud.mp4"
    print(path)
    audioclip = AudioFileClip(path)

    clip = clip.write_videofile(clip.set_audio(audioclip))

    print("Done")
    videoclip.ipython_display()
"""


SAVE_PATH = "/home/wishes/Downloads/Testsss/5555"
link = 'https://youtu.be/gkzu0IDyYw0'
yt = pytube.YouTube(link)

streams = yt.streams
choice = input("Audio:\n"
               "Press 1 to download mp3 audio:\n"
               "Press 2 to download mp4 audio:\n"
               "Press 3 to download webm audio:\n"
               "______________________________\n")


# TO DOWNLOAD AUDIO____________________
# print("Audio:")
# print("Press 1 to download mp3 audio:")
if choice == '1':
    mp3_stream = streams.filter(only_audio=True).first()
    vid_file = mp3_stream.download(output_path=SAVE_PATH)
    base, ext = os.path.splitext(vid_file)
    new_file = base + '.mp3'
    os.rename(vid_file, new_file)
    print("Done")

elif choice == '2':
    # print("Press 2 to download mp4 audio:")
    # print(yt.streams.filter(only_audio=True, mime_type="audio/mp4"))
    mp4_aud_stream = streams.filter(only_audio=True, mime_type="audio/mp4").first()
    mp4_aud_stream.download(output_path=SAVE_PATH)
    print("Done")

elif choice == '3':
    # print("Press 3 to download webm audio:")
    # print(yt.streams.filter(only_audio=True, mime_type="audio/webm"))
    webm_aud_stream = streams.filter(only_audio=True, mime_type="audio/webm").first()
    webm_aud_stream.download(output_path=SAVE_PATH)
    print("Done")
else:
    print("Meh")
# TO DOWNLOAD VIDEO____________________
print("Video:")
vids = streams.filter(type="video")
videos_string = str(vids)
# print(videos_string)
resolutions_indices = [m.start() for m in re.finditer('res=', videos_string)]
resolutions = []
for i in range(len(resolutions_indices)):
    j = resolutions_indices[i] + 5
    riso = ""
    while videos_string[j] != '"':
        riso = riso+videos_string[j]
        j += 1
    if riso in resolutions:
        continue
    else:
        resolutions.append(riso)

    # print(riso)
while True:
    print(resolutions)
    pref_res = input("Enter your preferable resolution:")
    print(type(pref_res))

    f_video = streams.filter(res=pref_res, progressive=True, mime_type="video/mp4")
    if f_video:  # if not empty, download
        print("progressive=TRUE", f_video)
        f_video.first().download(output_path=SAVE_PATH)
        print("Done")
    else:  # download vid+audio and integrate them
        print(streams)
        f_video = streams.filter(res=pref_res, mime_type="video/mp4").first()
        filename = f_video.title
        f_video.download(output_path=SAVE_PATH, filename=filename+"vid.mp4")
        f_audio = streams.filter(mime_type="audio/mp4").first().download(output_path=SAVE_PATH, filename=filename+"aud.mp4")
        print("Done installing video and audio!")
        # combine_video_audio_ff(SAVE_PATH, filename)
        # print("progressive=False", f_video)
        combine_video_audio_ff(SAVE_PATH, filename)



