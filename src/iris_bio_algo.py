import cv2
import imageio
from matplotlib import pyplot as plt
import numpy as np
from database import load_image_from_database

# Charger les images à partir de la base de données
iris_id1 = "030"
side1 = "R"
n_pos1 = "1"
image1 = load_image_from_database(iris_id1, side1, n_pos1)

iris_id2 = "030"
side2 = "R"
n_pos2 = "2"
image2 = load_image_from_database(iris_id2, side2, n_pos2)

# Check if images are not None
if image1 is not None and image2 is not None:
    # Redimensionner les images pour qu'elles aient la même dimension
    height = min(image1.shape[0], image2.shape[0])
    width = min(image1.shape[1], image2.shape[1])
    image1 = cv2.resize(image1, (width, height))
    image2 = cv2.resize(image2, (width, height))

    # Convertir en niveaux de gris
    gray_scale1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_scale2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
else:
    print("One or both images are None.")

# Calculer les histogrammes
hist_image1 = cv2.calcHist([gray_scale1], [0], None, [256], [0, 256])
hist_image2 = cv2.calcHist([gray_scale2], [0], None, [256], [0, 256])

# Tracer les histogrammes
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.bar(np.arange(256), hist_image1.squeeze(), color='b')
plt.title('Histogramme de l\'image 1')
plt.xlabel('Intensité de pixel')
plt.ylabel('Nombre de pixels')

plt.subplot(1, 2, 2)
plt.bar(np.arange(256), hist_image2.squeeze(), color='r')
plt.title('Histogramme de l\'image 2')
plt.xlabel('Intensité de pixel')
plt.ylabel('Nombre de pixels')

plt.tight_layout()
plt.show()

# Redimensionner les images
gray_scale1 = cv2.resize(gray_scale1, (500, 500))
gray_scale2 = cv2.resize(gray_scale2, (500, 500))

# Appliquer la suppression du bruit
gray_scale1 = cv2.GaussianBlur(gray_scale1, (9, 9), 1)
gray_scale2 = cv2.GaussianBlur(gray_scale2, (9, 9), 1)

# Égalisation de l'histogramme pour améliorer le contraste
gray_scale1 = cv2.equalizeHist(gray_scale1)
gray_scale2 = cv2.equalizeHist(gray_scale2)

# Filtrage de la morphologie mathématique pour supprimer les petits éléments
kernel = np.ones((5,5),np.uint8)
gray_scale1 = cv2.morphologyEx(gray_scale1, cv2.MORPH_OPEN, kernel)
gray_scale2 = cv2.morphologyEx(gray_scale2, cv2.MORPH_OPEN, kernel)

# Initialiser le détecteur SIFT
sift = cv2.SIFT_create() # type: ignore

# Trouver les points clés et les descripteurs avec SIFT
keypoints1, descriptors1 = sift.detectAndCompute(gray_scale1, None)
keypoints2, descriptors2 = sift.detectAndCompute(gray_scale2, None)

# Dessiner les points clés
img_with_keypoints1 = cv2.drawKeypoints(gray_scale1, keypoints1, None) # type: ignore
img_with_keypoints2 = cv2.drawKeypoints(gray_scale2, keypoints2, None) # type: ignore

# Sauvegarder l'image résultante
imageio.imwrite('DetectedSIFT1.png', img_with_keypoints1)
imageio.imwrite('DetectedSIFT2.png', img_with_keypoints2)

# Afficher les images
cv2.imshow("Detected SIFT 1", img_with_keypoints1)
cv2.waitKey(0) # maintenir la fenêtre

cv2.imshow("Detected SIFT 2", img_with_keypoints2)
cv2.waitKey(0) # maintenir la fenêtre

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

# Si le taux de correspondance est inférieur à 50%, considérez-le comme non correspondant
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