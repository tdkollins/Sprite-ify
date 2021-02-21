import sys
from scipy.io import wavfile
from pydub import AudioSegment
from classifier.live_predictions import LivePredictions
from google.cloud import speech, storage

bucket_name = "sizu_audio"

def upload_file(file_location: str, file_name: str):
    print("Uploading file to GCP bucket... This might take a minute...")
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_filename(file_location)


def split_audio(file_location: str):
    file_name = file_location.split("\\")[-1].split("/")[-1]
    client = speech.SpeechClient()
    upload_file(file_location, file_name)
    gcs_uri = f"gs://{bucket_name}/{file_name}"
    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        audio_channel_count=2,
        language_code="en-US",
        enable_word_time_offsets=True,
    )
    timestamps = []
    speakers = []
    print("Running speech to text... This might take a couple minutes...")
    response = client.long_running_recognize(config=config, audio=audio).result(timeout=300)
    for result in response.results:
        words = result.alternatives[0].words
        timestamps.append(words[0].start_time.total_seconds())
        if len(words) >= 15:
            for word in words[10:-5:10]:
                timestamps.append(word.start_time.seconds)
        print("Transcript: {}".format(result.alternatives[0].transcript))
    print(timestamps)

    rate, data = wavfile.read(file_location)
    timestamps = timestamps[1::]
    start = 0
    for idx, time in enumerate(timestamps):
        end = int((rate * time))
        print(start, end)
        segment = data[start:end-1]
        wavfile.write(f".//temp//segment{idx}.wav", rate, segment)
        if (idx == len(timestamps) - 1):
            wavfile.write(f".//temp//segment{idx}.wav", rate, data[end:])
        start = end

    serialize_audio(len(timestamps), timestamps, speakers)


def serialize_audio(num_files, timestamps, speakers):
    timestamps = [0] + timestamps[:-1:]
    serialized_data = []
    for idx in range(num_files):
        print(f".//temp//segment{idx}.wav")
        live_prediction = LivePredictions(file=f".//temp//segment{idx}.wav")
        live_prediction.loaded_model.summary()
        emotion = live_prediction.make_predictions()
        serialized_data.append({
            "start_time": timestamps[idx],
            "emotion": emotion,
            "speaker": speakers[idx]
        })
    print(serialized_data)
    return serialized_data


if __name__ == "__main__":
    split_audio(sys.argv[1])
