# Augmented Reality Marker Image Overlay 

## Description
This project demonstrates a fundamental Augmented Reality (AR) application built using Python and OpenCV. It enables you to overlay an image onto a reference marker detected in a video stream.

## Functionality
1. Marker Detection: The project uses the ORB algorithm to detect key features from the reference marker ('./assets/ref.png). Similarly, the feaures from each frame of the video are detected for identifying the marker in the video.

2. Marker Localization: Brute force matching is used to find the matches between the detected features from both the images (marker as well as the video frame). Further, out of all the matches found, only a few matches are retained to neglect matches with lower distances. 

3. Homography Calculation and Perspective Wrapping: Once sufficient number of matches are found, the homography matrix is calculated to estimate the rotation, translation, and scaling of the marker in the video. Further, the overlay image is then wraped according to the calculated homography. 

4. Overlaying the image over the marker:  the overlay image is overlayed onto the marker in the video frame with proper masking. 

## Demo:
https://github.com/SuyashMali/augmented-reality-marker-overlay/assets/69067427/fc3d362e-57c0-4839-87d1-31769982e0e2


## Usage:
* Clone/Download the repository to your device
* change to the directory *'augmented-reality-marker-overlay'*
```bash
cd augmented-reality-marker-overlay 
```
* It is recommended to setup a virtual environment (however, not necessary). 
* Install the dependencies from the requirements.txt file. 
```bash
pip install -r requirements.txt
```
* Take out a small printout of the marker image (<a href=https://github.com/SuyashMali/augmented-reality-marker-overlay/blob/main/assets/ref.jpg>'./assets/ref.jpg'</a>), or replace the marker image with your marker. 
* Run the ***app.py*** file
```bash
python app.py
```

