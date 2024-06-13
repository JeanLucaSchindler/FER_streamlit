import streamlit as st

import numpy as np
import pandas as pd
import random
# import time
from PIL import Image
#import matplotlib.pyplot as plt
import base64
# import cv2
# import ffmpeg
import tempfile
import requests
import os
from io import BytesIO
import subprocess



# Set the background image
def set_background(image_path, opacity=0.5):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    css = f"""
    <style>
    .stApp {{
        background-image: url(data:image/png;base64,{encoded_string});
        background-size: cover;
        background-blend-mode: multiply;
        opacity: {opacity}; /* Adjust opacity level */
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Path to your background image
background_image_path = 'inside-out-rileys-headquarters.jpeg'

# Set the background with increased transparency (adjust opacity as needed)
set_background(background_image_path, opacity=1)


# Display the title
st.markdown('<h1 style="color: white; font-weight: bold; text-align: center;">Facial Emotion Recognition model</h1>', unsafe_allow_html=True)

df = pd.read_csv('raw-data-clean-CLEAN.csv', sep=';')
# my_random = random.randrange(0,len(df['pth']))


labels_df = list(df['label'].unique())


def emotions_1672():

    placeholder = st.empty()

    button = st.button('Random emotions generator')

    new_images = []
    new_captions = []

    for i, label in enumerate(labels_df):
            emotion = df[df['label'] == label].reset_index()
            my_random_emotion = random.choice(emotion.index)
            image_path = '1672-data-set/' + emotion.loc[my_random_emotion, 'pth']
            image = Image.open(image_path)
            new_images.append(image)
            new_captions.append(label)

    placeholder.image(new_images, caption=new_captions, width=150)

# Call the function to start displaying images
# emotions_1672()


#Old def emotions_1672

#Have pictures from batch #1672 appear on screen
# def emotions_1672():

#     # Create a placeholder for images
#     placeholder = st.empty()

#     # Initialize current images and captions
#     current_images = []
#     current_captions = []

#     # Initialize images for the first time
#     for label in labels_df:
#         emotion = df[df['label'] == label].reset_index()
#         my_random_emotion = random.choice(emotion.index)
#         image_path = '1672-data-set/' + emotion.loc[my_random_emotion, 'pth']
#         image = Image.open(image_path)
#         current_images.append(image)
#         current_captions.append(label)

#     button = st.button('Click to predict your emotions')
#     while button == False:
#         new_images = []
#         new_captions = []

#         for i, label in enumerate(labels_df):
#             # Decide whether to change the image
#             if random.random() < 0.5 and current_images[i] is not None:  # 50% chance to change the image
#                 emotion = df[df['label'] == label].reset_index()
#                 my_random_emotion = random.choice(emotion.index)
#                 image_path = '1672-data-set/' + emotion.loc[my_random_emotion, 'pth']
#                 image = Image.open(image_path)
#                 new_images.append(image)
#                 new_captions.append(label)
#             else:
#                 new_images.append(current_images[i])
#                 new_captions.append(current_captions[i])

#         # Update the current images and captions
#         current_images = new_images
#         current_captions = new_captions

#         # Update the images in the placeholder
#         placeholder.image(current_images, caption=current_captions, width=150)

#         # Wait for 2 seconds before updating again
#         #time.sleep(2)



def get_my_images_and_their_label(labels):
    """
    Create a function that couples all emotions into 1 big block and
    returns a list of images (for different emotions) along with their
    associated label
    Attention: it does the same thing as emotions()
    """
    my_images = []
    my_labels = []

    for label in labels:
        image, label = function_emotion(label)
        my_images.append(image)
        my_labels.append(label)

    return my_images, my_labels





#Uploading image to the streamlit
uploaded_image = st.file_uploader(label ="Choose a photo 📷",type=["jpg", "jpeg", "png"])

if uploaded_image is not None:

    image_bytes = uploaded_image.read()

    # Prepare the files dictionary for the request
    files = {'img': (image_bytes)}

    # Define the FastAPI endpoint URL
    url = "https://ferimagev5-3fpq7qou5q-ew.a.run.app/upload_image"

    # Make the POST request to the FastAPI endpoint
    response = requests.post(url, files=files)

    # Display the response from the FastAPI endpoint
    if response.status_code == 200:
        # Read the response image
        response_image = Image.open(BytesIO(response.content))

        # Display the response image
        st.image(response_image, caption='Processed Image.', width=200)
    else:
        st.write("Failed to get response from the server.")



#Uploading video to the streamlit
uploaded_video = st.file_uploader(label ="Choose a video 🎞️", type=["mp4"])

if uploaded_video is not None:

    # Prepare the files dictionary for the request
    files = {'vid': ("uploaded_video.mp4", uploaded_video, 'video/mp4')}

    # Define the FastAPI endpoint URL
    url = 'https://ferimagev5-3fpq7qou5q-ew.a.run.app/upload_video'
    # Make the POST request to the FastAPI endpoint
    response = requests.post(url, files=files)

    #
    bytesio_object = BytesIO(response.content)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        temp_file.write(bytesio_object.getbuffer())
        temp_file_path = temp_file.name

    input_file_xvid = temp_file_path


    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file_output:
        temp_file_output_path = temp_file_output.name

    output_file_h264 = temp_file_output_path


    # Run FFmpeg command to convert the video to H.264
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-i", input_file_xvid,
        "-c:v", "libx264",  # H.264 codec
        "-crf", "23",       # Constant Rate Factor (0-51), lower values mean better quality (23 is default)
        "-preset", "medium", # Preset for encoding speed and compression efficiency (options: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow)
        "-c:a", "aac",      # AAC audio codec
        "-b:a", "128k",     # Audio bitrate
        "-strict", "experimental",  # Needed for some FFmpeg versions to enable AAC codec
        output_file_h264
    ]

    # Run FFmpeg command
    subprocess.run(ffmpeg_cmd)
    # print('convertion done to h264')

    st.video(output_file_h264, format="video/mp4")

    #removing temporary filess
    os.remove(input_file_xvid)
    os.remove(output_file_h264)





    # bytesio_object = BytesIO(response.content)
    # with open("output.mp4", "wb") as f:
    #     f.write(bytesio_object.getbuffer())


    # # Input and output file paths
    # input_file = "output.mp4"
    # output_file = "output_h264.mp4"

    # # Run FFmpeg command to convert the video to H.264
    # ffmpeg_cmd = [
    #     "ffmpeg",
    #     "-i", input_file,
    #     "-c:v", "libx264",  # H.264 codec
    #     "-crf", "23",       # Constant Rate Factor (0-51), lower values mean better quality (23 is default)
    #     "-preset", "medium", # Preset for encoding speed and compression efficiency (options: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow)
    #     "-c:a", "aac",      # AAC audio codec
    #     "-b:a", "128k",     # Audio bitrate
    #     "-strict", "experimental",  # Needed for some FFmpeg versions to enable AAC codec
    #     output_file
    # ]

    # # Run FFmpeg command
    # subprocess.run(ffmpeg_cmd)
    # print('convertion done to h264')

    # st.video('output_h264.mp4', format="video/mp4")



#allow webcam --> to take a photo

st.markdown("**Take picture with your webcam if you want**", unsafe_allow_html=False)
if 'webcam_active' not in st.session_state:
    st.session_state.webcam_active = False

# Button to activate the webcam
if st.button('Activate webcam'):
    st.session_state.webcam_active = True

# Button to deactivate the webcam
if st.button('Deactivate webcam'):
    st.session_state.webcam_active = False

# Display the webcam input if activated
if st.session_state.webcam_active:
    st.camera_input(label='Take a picture')
