import cv2 
import numpy as np


def find_matches(descsA, descsB):
    # Matching of the features from both images 
    method = cv2.NORM_HAMMING2
    matcher = cv2.BFMatcher(method, crossCheck=True)
    matches = matcher.match(descsA, descsB)

    # Sorting of the matches based on the distance. Shorter distance indicates more similarity. 
    matches = sorted(matches, key=lambda x:x.distance)
    return matches

def match_overlay(image, templateGray, kpsB, descsB, orb, overlay_image_path = './assets/model_1.jpg', max_features = 150, top_matches = 18) -> np.array:
    '''Function to match the keypoints of the reference card from the template and video feed, find the homography, 
    transform the overlay image to the homography and overlay image onto the reference card.'''
    
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    output = None

    # Overlay Image
    ov_img = cv2.imread(overlay_image_path)

    # Create the keypoints for the input image
    orb = cv2.ORB_create(max_features)
    (kpsA, descsA) = orb.detectAndCompute(imageGray, None)
     
    # Match the keypoints of template and the frame
    matches = find_matches(descsA, descsB)

    # Return original frame if sufficient matches are not found
    if len(matches) < top_matches:
        print("......returning due to less matches........")
        return image

    # keep only the 'top_matches' no. of matches for better homography estimation
    matches = matches[:top_matches]
    
    # Visualizing the matched keypoints.
    # matched_pt = cv2.drawMatches(imageGray, kpsA, template, kpsB, matches, None)
    # matched_pt = imutils.resize(matched_pt, width=1000)
    # cv2.namedWindow("Matched keypoints", cv2.WINDOW_NORMAL)
    # cv2.resizeWindow("Matched keypoints", 700, 700)
    # cv2.imshow("Matched keypoints", matched_pt)
    # cv2.waitKey(0)
   
    try:
        #Creating the Homography Matrix for alignment of the images using Warp Perspective.
        ptsA = np.zeros((len(matches), 2), dtype="float")
        ptsB = np.zeros((len(matches), 2), dtype="float")

        for (i, m) in enumerate(matches):
            ptsA[i] = kpsA[m.queryIdx].pt
            ptsB[i] = kpsB[m.trainIdx].pt
        ptsA.reshape(-1, 1, 2)
        ptsB.reshape(-1, 1, 2)

        (homography, _) = cv2.findHomography(ptsB, ptsA, method=cv2.RANSAC, ransacReprojThreshold=2)

    except:
        print("......returning due to exception........")
        return image
    
    if homography is None:
        print("......returning due to no homography........")
        return image
    
    (imgH,imgW)= image.shape[:2]
    aligned = cv2.warpPerspective(ov_img, homography, (imgW,imgH))    
    
    templateH, templateW = templateGray.shape
    pts = np.float32([[0, 0], [0, templateH - 1], [templateW - 1, templateH - 1], [templateW - 1, 0]]).reshape(-1, 1, 2)

    # Project the corners into frame
    try:
        dst = cv2.perspectiveTransform(pts, homography)  

        mask = np.zeros((imgH, imgW), dtype="uint8")
        cv2.fillConvexPoly(mask, dst.astype("int32"), (255, 255, 255), cv2.LINE_AA)
        
        # Applying a border to the overlay image
        rect = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        mask = cv2.dilate(mask, rect, iterations=2)

        maskScaled = mask.copy() / 255.0
        maskScaled = np.dstack([maskScaled] * 3)

        # Multiplying the warped image and masked together, multiplying the original
        # input image with the mask, and adding the resulting multiplications together
        warpedMultiplied = cv2.multiply(aligned.astype("float"), maskScaled)
        imageMultiplied = cv2.multiply(image.astype(float), 1.0 - maskScaled)
        output = cv2.add(warpedMultiplied, imageMultiplied)
        output = output.astype("uint8")
        
        print("......returning Normal images........")
        return output
    
    except:
        print("......returning due to exception 2........")
        return image

    