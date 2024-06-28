import cv2
import imutils
# import numpy as np

from utils.utils import match_overlay


if __name__ == "__main__":
    maxFeatures = 300
    template = cv2.imread('./assets/ref.jpg')       # Reference Marker

    # Initialize Video Capture
    cap = cv2.VideoCapture(1)

    # Convert the template to grayscale
    templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # create the ORB feature detector and detect features of the template
    orb = cv2.ORB_create(maxFeatures)
    (kpsB, descsB) = orb.detectAndCompute(templateGray, None)

    while True:
        _, frame = cap.read()
        # frame = cv2.flip(frame,1)

        output = match_overlay(image=frame, templateGray=templateGray, kpsB=kpsB, descsB=descsB, orb=orb)
        print(f"######## output = {output.shape}")
        cv2.imshow("AR Overlay", output)

        # cv2.imshow("Overlay of the Aligned Images", overlay)
        
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

    # After the loop release the cap object 
    cap.release() 
    # Destroy all the windows 
    cv2.destroyAllWindows() 
