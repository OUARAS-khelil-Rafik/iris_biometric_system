import os
import cv2
import sqlite3
import re

# Chemin vers le répertoire contenant les images
base_path = "./iris_images"

# Créer une connexion à la base de données SQLite
conn = sqlite3.connect("iris_database.db")
cursor = conn.cursor()

# Créer une table pour stocker les données si elle n'existe pas déjà
cursor.execute('''CREATE TABLE IF NOT EXISTS iris_data
                (iris_id TEXT, side TEXT, n_pos TEXT, image_name TEXT, image_path TEXT)''')

# Parcourir les répertoires et les fichiers
for folder_name in os.listdir(base_path):
    if os.path.isdir(os.path.join(base_path, folder_name)):
        for subfolder_name in os.listdir(os.path.join(base_path, folder_name)):
            if os.path.isdir(os.path.join(base_path, folder_name, subfolder_name)):
                for file_name in os.listdir(os.path.join(base_path, folder_name, subfolder_name)):
                    # Créer le chemin complet de l'image
                    image_path = os.path.join(base_path, folder_name, subfolder_name, file_name)
                    
                    # Utiliser une expression régulière pour extraire des informations du nom de fichier
                    match = re.match(r"(\d+)([LR])_(\d+)\.png", file_name)
                    if match:
                        iris_id, side, position = match.groups()
                        
                        # Vérifier si les données existent déjà dans la base de données
                        cursor.execute('''SELECT * FROM iris_data WHERE iris_id=? AND side=? AND n_pos=?''',
                                       (iris_id, "left" if side == "L" else "right", position))
                        existing_data = cursor.fetchone()
                        
                        # Si les données n'existent pas déjà, les ajouter à la base de données
                        if not existing_data:
                            cursor.execute('''INSERT INTO iris_data VALUES (?, ?, ?, ?, ?)''',
                                           (iris_id, "left" if side == "L" else "right", position, file_name, image_path))

# Commit des modifications et fermeture de la connexion
conn.commit()
conn.close()

print("Données insérées dans la base de données SQLite.")

def load_image_from_database(iris_id, side, n_pos):
    """Charger une image à partir de la base de données."""
    conn = sqlite3.connect("iris_database.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT image_path FROM iris_data WHERE iris_id=? AND side=? AND n_pos=?''', (iris_id, "left" if side == "L" else "right", n_pos))
    row = cursor.fetchone()
    if row:
        image_path = row[0]
        image = cv2.imread(image_path)
        conn.close()
        return image
    else:
        print("Aucune image correspondante trouvée dans la base de données.")
        conn.close()
        return None