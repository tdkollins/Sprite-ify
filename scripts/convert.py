import cv2
import os
import numpy as np
import random
from moviepy.editor import *

# clips: list of objects containing a start time and sentiment score
def make_video(audio_obj):
    length = audio_obj["total_length"]
    clips = audio_obj["segments"]
    sprites = []
    curr_sprite = None
    for i, clip in enumerate(clips):
        if clip["score"] > 0.4 and clip["score"] <= 1.0:
            sprite_type = "happy"
        elif clip["score"] <= 0.4 and clip["score"] >= -0.4:
            sprite_type = "neutral"
        elif clip["score"] < -0.4 and clip["score"] >= -1.0:
            sprite_type = "angry"

        random_file = random.choice(os.listdir(f"../sprites/Kurisu/{sprite_type}/"))
        while random_file == curr_sprite:
            random_file = random.choice(os.listdir(f"../sprites/Kurisu/{sprite_type}/"))
        curr_sprite = random_file

        sprite = f"../sprites/Kurisu/{sprite_type}/{random_file}"

        if clip != clips[-1]:
            duration = clips[i+1]["start_time"] - clip["start_time"]
        else:
            duration = length - clip["start_time"]
        sprites.append(Sprite(sprite_type, sprite, duration, clip["start_time"]))

    video = Video(sprites, 10)
    output = video.render()
    audio = AudioFileClip("../audio_input/potion.wav")
    clip = VideoFileClip(output).set_audio(audio)
    clip.write_videofile("file.mp4", codec="libx264", audio_codec="aac")


# https://stackoverflow.com/questions/44720580/resize-image-canvas-to-maintain-square-aspect-ratio-in-python-opencv
def resizeAndPad(img, size, padColor=0):
    h, w = img.shape[:2]
    sh, sw = size

    # interpolation method
    if h > sh or w > sw: # shrinking image
        interp = cv2.INTER_AREA
    else: # stretching image
        interp = cv2.INTER_CUBIC

    # aspect ratio of image
    aspect = w/h  # if on Python 2, you might need to cast as a float: float(w)/h

    # compute scaling and pad sizing
    if aspect > 1: # horizontal image
        new_w = sw
        new_h = np.round(new_w/aspect).astype(int)
        pad_vert = (sh-new_h)/2
        pad_top, pad_bot = np.floor(pad_vert).astype(int), np.ceil(pad_vert).astype(int)
        pad_left, pad_right = 0, 0
    elif aspect < 1: # vertical image
        new_h = sh
        new_w = np.round(new_h*aspect).astype(int)
        pad_horz = (sw-new_w)/2
        pad_left, pad_right = np.floor(pad_horz).astype(int), np.ceil(pad_horz).astype(int)
        pad_top, pad_bot = 0, 0
    else: # square image
        new_h, new_w = sh, sw
        pad_left, pad_right, pad_top, pad_bot = 0, 0, 0, 0

    # scale and pad
    scaled_img = cv2.resize(img, (new_w, new_h), interpolation=interp)
    scaled_img = cv2.copyMakeBorder(scaled_img, pad_top, pad_bot, pad_left, pad_right, borderType=cv2.BORDER_CONSTANT, value=padColor)

    return scaled_img
    

class Sprite:
    def __init__(self, sprite_type, sprite, duration, start_time):
        self.sprite_type = sprite_type
        self.sprite = sprite
        self.duration = duration
        self.start_time = start_time

class Video:
    def __init__(self, sprites, fps):
        self.sprites = sprites
        self.fps = fps

    def render(self, output_path: str = None):
        if output_path is None:
            if not os.path.exists("audio"):
                os.makedirs("audio")
            random_hash = random.getrandbits(64)
            output_path = f"audio/{random_hash}.mp4"
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        if os.path.isfile(output_path):
            os.remove(output_path)

        img_shape = cv2.imread(self.sprites[0].sprite).shape
        img_size = (1920, 1080)
    
        video = cv2.VideoWriter(output_path, fourcc, self.fps, img_size)
        for s in self.sprites:
            image = cv2.imread(s.sprite)
            print(s.duration)
            for num in range(0, int(s.duration * 10)):
                image = cv2.resize(image, img_size)
                video.write(np.array(image))
        video.release()
        return output_path


obj = {'total_length': 187.26893424036282, 'segments': [{'start_time': 0, 'score': 0.0}, {'start_time': 3.5, 'score': 0.20000000298023224}, {'start_time': 11.7, 'score': -0.6000000238418579}, {'start_time': 19.3, 'score': -0.6000000238418579}, {'start_time': 25.6, 'score': -0.699999988079071}, {'start_time': 32.2, 'score': 0.800000011920929}, {'start_time': 39.8, 'score': -0.8999999761581421}, {'start_time': 46.4, 'score': -0.699999988079071}, {'start_time': 60, 'score': -0.699999988079071}, {'start_time': 64.5, 'score': 0.30000001192092896}, {'start_time': 71, 'score': 0.30000001192092896}, {'start_time': 76.3, 'score': -0.800000011920929}, {'start_time': 81, 'score': -0.800000011920929}, {'start_time': 101, 'score': -0.800000011920929}, {'start_time': 108, 'score': -0.800000011920929}, {'start_time': 119.2, 'score': -0.699999988079071}, {'start_time': 121, 'score': -0.699999988079071}, {'start_time': 125, 'score': -0.699999988079071}, {'start_time': 129, 'score': -0.699999988079071}, {'start_time': 142.9, 'score': 0.30000001192092896}, {'start_time': 145.4, 'score': 0.30000001192092896}, {'start_time': 147.5, 'score': -0.10000000149011612}, {'start_time': 151.9, 'score': -0.699999988079071}, {'start_time': 158.4, 'score': -0.6000000238418579}, {'start_time': 161, 'score': -0.6000000238418579}, {'start_time': 164.3, 'score': 0.30000001192092896}, {'start_time': 168.0, 'score': -0.800000011920929}, {'start_time': 178.3, 'score': 0.30000001192092896}]}
make_video(obj)