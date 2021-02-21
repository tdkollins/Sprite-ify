# Sprite-ify

Trevor Kollins and Nicole Danuwidjaja

## What it does
Sprite-ify takes in an audio clip and converts it into a full-fledged sprite animation. 

## How we built it
Sprite-ify uses Google Cloud Platform to utilize their Natural Language API and Speech to Text API for text analysis with machine learning, along with Google Cloud Storage for computing and storing results. We used this to serialize audio chunks based off of sentence breaks and obtain sentiment scores. 

Using this, we selected sprites for each chunk with the corresponding sentiment (e.g. happy, sad, neutral, embarrassed) and used OpenCV to create a video based on the sprites and chunk durations. We programmatically combined the original audio with the newly created video and return the output as an animation!
