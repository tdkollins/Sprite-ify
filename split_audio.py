import sys
from pydub import AudioSegment
from pydub.silence import split_on_silence
from classifier.live_predictions import LivePredictions

def split_audio(file_location: str):
    """
    Split an audio .wav into segements by audio pauses

    Args:
        file_location: the location of the .wav file to load
    """

    try:
        sound_file = AudioSegment.from_wav(file_location)
    except Exception as err:
        print(f"Can not find file at {file_location}")
        raise err

    # Define silence length and threshold
    # silence_length = 200 # (400 ms)
    # silence_threshold = -30 # Consider less than -8 dbfs to be "silent"
    silence_length = 200 # (400 ms)
    silence_threshold = -30 # Consider less than -8 dbfs to be "silent"

    segments = split_on_silence(sound_file, silence_length, silence_threshold)

    for idx, segment in enumerate(segments):
        segment.export(f".//temp//segment{idx}.wav", format="wav")

    serialize_audio(segments)


def serialize_audio(segments):
    total = 0
    serialized_data = []
    for idx, segment in enumerate(segments):
        live_prediction = LivePredictions(file=f".//temp//segment{idx}.wav")
        live_prediction.loaded_model.summary()
        emotion = live_prediction.make_predictions()
        serialized_data.append({
            "start_time": total,
            "emotion": emotion
        })
        total += segment.duration_seconds
    return serialized_data


if __name__ == "__main__":
    split_audio(sys.argv[1])
