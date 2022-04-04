import pytube
import ffmpeg
from pytube import YouTube
import os
import re
from moviepy.editor import *


def combine_video_audio_ff(SAVE_PATH, filename):
    vid_path = SAVE_PATH + "/" + filename + "vid.mp4"
    video_stream = ffmpeg.input(vid_path)

    aud_path = SAVE_PATH + "/" + filename + "aud.mp4"
    audio_stream = ffmpeg.input(aud_path)

    SAVE_PATH = SAVE_PATH + "/" + filename + '.mp4'
    ffmpeg.output(audio_stream, video_stream, SAVE_PATH).run()
    os.remove(vid_path)
    os.remove(aud_path)
    print("Done Integrating.")


SAVE_PATH = "/home/Music"
link = ""

# Making sure the YouTube link is valid.
while True:
    link = input("Enter your link: ")
    try:
        yt = pytube.YouTube(link)
        break
    except:
        # print(sys.exc_info()[0], "occurred.")
        print("Please enter a valid link.")

# Taking the desired download path.
change = input("Your current save path is: %s \nDo you want to change it (y/n):" % SAVE_PATH)
if change == 'y':
    SAVE_PATH = input("Enter your path:")
    print(SAVE_PATH)

print("Collecting Streams...")

streams = yt.streams
choice = input("Would you like to download \n   [1] Audio   [2] Video\n")

if choice == '1':
    audio_choice = input("[1] To download mp3 audio:\n"
                         "[2] To download mp4 audio:\n"
                         "[3] To download webm audio:\n"
                         "______________________________\n")

    if audio_choice == '1':
        mp3_stream = streams.filter(only_audio=True).first()
        print("Downloading '%s'..." % mp3_stream.title)
        vid_file = mp3_stream.download(output_path=SAVE_PATH)
        base, ext = os.path.splitext(vid_file)
        new_file = base + '.mp3'
        os.rename(vid_file, new_file)

    elif audio_choice == '2':
        mp4_aud_stream = streams.filter(only_audio=True, mime_type="audio/mp4").first()
        print("Downloading...")
        mp4_aud_stream.download(output_path=SAVE_PATH)

    elif audio_choice == '3':
        webm_aud_stream = streams.filter(only_audio=True, mime_type="audio/webm").first()
        print("Downloading...")
        webm_aud_stream.download(output_path=SAVE_PATH)

    print("Done")

else:
    vids = streams.filter(type="video")
    videos_string = str(vids)
    resolutions_indices = [m.start() for m in re.finditer('res=', videos_string)]
    resolutions = []
    for i in range(len(resolutions_indices)):
        j = resolutions_indices[i] + 5
        riso = ""
        while videos_string[j] != '"':
            riso = riso + videos_string[j]
            j += 1
        if riso in resolutions:
            continue
        else:
            resolutions.append(riso)

    while True:
        print(resolutions)
        pref_res = input("Enter your preferable resolution: ")
        if pref_res == 't':
            break

        f_video = streams.filter(res=pref_res, progressive=True, mime_type="video/mp4")
        if f_video:  # if not empty, download
            print("progressive=TRUE", f_video)
            f_video.first().download(output_path=SAVE_PATH)
            print("Done")
        else:  # Download video + audio and integrate them.
            # print(streams)
            f_video = streams.filter(res=pref_res, mime_type="video/mp4").first()
            filename = f_video.title
            f_video.download(output_path=SAVE_PATH, filename=filename + "vid.mp4")
            f_audio = streams.filter(mime_type="audio/mp4").first().download(output_path=SAVE_PATH,
                                                                             filename=filename + "aud.mp4")
            print("Done installing video and audio!")
            combine_video_audio_ff(SAVE_PATH, filename)

        print("If you would like to terminate, press [t].")
