import cv2
import imageio

def extract_features(image1, image2):
    # Initialiser le détecteur SIFT
    sift = cv2.SIFT_create() # type: ignore

    # Trouver les points clés et les descripteurs avec SIFT
    keypoints1, descriptors1 = sift.detectAndCompute(image1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(image2, None)

    # Dessiner les points clés
    img_with_keypoints1 = cv2.drawKeypoints(image1, keypoints1, None) # type: ignore
    img_with_keypoints2 = cv2.drawKeypoints(image2, keypoints2, None) # type: ignore

    # Sauvegarder l'image résultante
    imageio.imwrite('DetectedSIFT1.png', img_with_keypoints1)
    imageio.imwrite('DetectedSIFT2.png', img_with_keypoints2)
    
    return keypoints1, descriptors1, keypoints2, descriptors2
