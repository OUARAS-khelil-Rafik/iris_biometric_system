import sqlite3
import random
import os

# Connexion à la base de données
conn = sqlite3.connect('iris_database.db')
cursor = conn.cursor()

# Chemin vers le dossier contenant les images d'iris
image_folder = 'iris_images'

# Création des tables pour data les ensembles d'enrôlement et de reconnaissance
cursor.execute('''CREATE TABLE IF NOT EXISTS data (
                    id INTEGER PRIMARY KEY,
                    subject_id TEXT,
                    eye_side TEXT,
                    image_path TEXT
                  )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS enrollment_data (
                    id INTEGER PRIMARY KEY,
                    subject_id TEXT,
                    eye_side TEXT,
                    image_path TEXT
                  )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS recognition_data (
                    id INTEGER PRIMARY KEY,
                    subject_id TEXT,
                    eye_side TEXT,
                    image_path TEXT
                  )''')

# Supprimer les données existantes dans les tables d'enrôlement et de reconnaissance
cursor.execute('''DELETE FROM data''')
cursor.execute('''DELETE FROM enrollment_data''')
cursor.execute('''DELETE FROM recognition_data''')

# Fonction pour insérer des données dans la table data
def insert_data(subject_id, eye_side, image_path):
    cursor.execute('''INSERT INTO data (subject_id, eye_side, image_path)
                      VALUES (?, ?, ?)''', (subject_id, eye_side, image_path))
    conn.commit()

# Fonction pour insérer des données dans la table d'enrôlement
def insert_enrollment_data(subject_id, eye_side, image_path):
    cursor.execute('''INSERT INTO enrollment_data (subject_id, eye_side, image_path)
                      VALUES (?, ?, ?)''', (subject_id, eye_side, image_path))
    conn.commit()

# Fonction pour insérer des données dans la table de reconnaissance
def insert_recognition_data(subject_id, eye_side, image_path):
    cursor.execute('''INSERT INTO recognition_data (subject_id, eye_side, image_path)
                      VALUES (?, ?, ?)''', (subject_id, eye_side, image_path))
    conn.commit()

# Insérer les données
for folder_name in os.listdir(image_folder):
    if os.path.isdir(os.path.join(image_folder, folder_name)):
        for side in ['left', 'right']:
            for image_name in os.listdir(os.path.join(image_folder, folder_name, side)):
                insert_data(folder_name, side, os.path.join(image_folder, folder_name, side, image_name))

# Récupération du nombre total d'enregistrements dans la table data
cursor.execute('''SELECT COUNT(*) FROM data''')
data_count = cursor.fetchone()[0]

# Division des données en ensembles d'enrôlement et de reconnaissance
enrollment_count = int(data_count * 0.7)  # 70% pour l'enrôlement
recognition_count = data_count - enrollment_count  # 30% pour la reconnaissance

# Récupération des données d'enrôlement et de reconnaissance
cursor.execute('''SELECT * FROM data''')
data = cursor.fetchall()

# Séparation des ensembles
random.shuffle(data)
enrollment_set = data[:enrollment_count]
recognition_set = data[enrollment_count:]

# Insertion des données d'enrôlement
for enrollment_data in enrollment_set:
    insert_enrollment_data(enrollment_data[1], enrollment_data[2], enrollment_data[3])

# Insertion des données de reconnaissance
for recognition_data in recognition_set:
    insert_recognition_data(recognition_data[1], recognition_data[2], recognition_data[3])

# Fermer la connexion à la base de données
conn.close()