import cv2
import numpy as np

def match_images(image1, keypoints1, descriptors1, image2, keypoints2, descriptors2):
    # Initialiser la correspondance Brute Force avec la distance euclidienne
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

    # Matcher les descripteurs
    matches = bf.match(descriptors1, descriptors2)

    # Trier les correspondances
    matches = sorted(matches, key=lambda match: match.distance)

    # Dessiner les correspondances
    matched_image = cv2.drawMatches(image1, keypoints1, image2, keypoints2, matches[:100], None) # type: ignore

    # Calculer le taux de correspondance en pourcentage
    matching_rate = len(matches) / min(len(keypoints1), len(keypoints2)) * 100

    return matching_rate, matched_image

def display_matched_image(matched_image, matching_rate):
    # Afficher le résultat de la correspondance
    if matching_rate < 50:
        print("Images do not match.")
    else:
        print("Images match.")
    
    # Redimensionner l'image pour la rendre plus petite
    scale_percent = 50  # pour une réduction de 50%
    width = int(matched_image.shape[1] * scale_percent / 100)
    height = int(matched_image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_image = cv2.resize(matched_image, dim, interpolation=cv2.INTER_AREA)

    # Define text parameters
    text = f"Matching Rate: {matching_rate:.2f}%"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.4
    font_thickness = 1
    text_color = (255, 255, 255)  # White color

    # Get text size
    text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]

    # Calculate text position
    text_x = (resized_image.shape[1] - text_size[0]) // 2  # Center horizontally
    text_y = resized_image.shape[0] - 20  # 20 pixels above the bottom

    # Add text to the image
    cv2.putText(resized_image, text, (text_x, text_y), font, font_scale, text_color, font_thickness)

    # Show the image
    cv2.imshow("Matching Images", resized_image)
    cv2.waitKey(0)