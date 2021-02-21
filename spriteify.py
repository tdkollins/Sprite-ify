from scripts.convert import make_video_from_audio_data
from split_audio import split_audio
import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: spriteify <audio_path> <char_name>")
        raise Exception
    if sys.argv[2] not in ["Kurisu", "Hajime"]:
        print("Character must be Kurisu or Hajime")
        raise Exception
    make_video_from_audio_data(split_audio(sys.argv[1]), sys.argv[1], sys.argv[2])
