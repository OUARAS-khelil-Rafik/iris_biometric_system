import os, cv2, tkinter as tk
from tkinter import filedialog, messagebox, font
from PIL import Image, ImageTk
from preprocessing_image import preprocess_image
from feature_extraction import extract_features
from matching import match_images
from database import load_image_from_database

class ResultWindow:
    def __init__(self, root, iris_id, side, image, matching_rate):
        self.root = root
        self.root.title("Matching Result")

        self.iris_id = iris_id
        self.side = side
        self.image = image
        self.matching_rate = matching_rate

        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack()

        # Vérifier si le taux de correspondance est supérieur à 50%
        if self.matching_rate > 50:
            # Afficher le message de bienvenue avec l'ID
            welcome_label = tk.Label(main_frame, text=f"Welcome, ID \"{self.iris_id}\"", font=("Times", 14, "bold"), foreground="green")
            welcome_label.grid(row=0, column=0, columnspan=2, pady=5)
        else:
            # Fermer automatiquement la fenêtre de résultat
            self.root.destroy()
            # Afficher une boîte de dialogue d'erreur
            messagebox.showerror("Unknown Person", "Unknown person.")
            return

        # ID Entry
        id_label = tk.Label(main_frame, text="ID:", font=("Times", 12, "bold italic"), foreground="black")
        id_label.grid(row=1, column=0, sticky="w")
        self.id_value = tk.Entry(main_frame, font=("Times", 12, font.ITALIC), width=20)
        self.id_value.insert(tk.END, self.iris_id)
        self.id_value.grid(row=1, column=1, pady=5, sticky="w")

        # Side Entry
        side_label = tk.Label(main_frame, text="Side:", font=("Times", 12, "bold italic"), foreground="black")
        side_label.grid(row=2, column=0, sticky="w")
        self.side_value = tk.Entry(main_frame, font=("Times", 12, font.ITALIC), width=20)
        self.side_value.insert(tk.END, self.side)
        self.side_value.grid(row=2, column=1, pady=5, sticky="w")

        # Image
        # Redimensionner l'image pour s'adapter à la fenêtre
        resized_image = cv2.resize(self.image, (300, 300))
        # Convertir l'image en format Tkinter
        tk_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)))
        self.image_label = tk.Label(main_frame, image=tk_image)
        self.image_label.image = tk_image # type: ignore
        self.image_label.grid(row=3, column=0, columnspan=2, pady=5)

        # Matching Rate Entry
        matching_rate_label = tk.Label(main_frame, text="Matching Rate:", font=("Times", 12, "bold italic"), foreground="black")
        matching_rate_label.grid(row=4, column=0, sticky="w")
        self.matching_rate_value = tk.Entry(main_frame, font=("Times", 12, font.ITALIC), width=20)
        self.matching_rate_value.insert(tk.END, f"{self.matching_rate:.2f}%")
        self.matching_rate_value.grid(row=4, column=1, pady=5, sticky="w")

        # Ajouter un bouton "OK"
        ok_button = tk.Button(main_frame, text="OK", font=("Times", 12, "bold"), command=self.ok_clicked)
        ok_button.grid(row=5, column=0, columnspan=2, pady=10)

    def ok_clicked(self):
        # Fermer la fenêtre de résultat
        self.root.destroy()
        
class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Iris Matching App")

        # Canvas pour afficher l'image d'arrière-plan
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        # Charger l'image d'arrière-plan
        bg_image = Image.open("./images/BG.png")
        bg_image = bg_image.resize((800, 600))
        self.root.resizable(False, False)
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)
        
        self.upload_icon = tk.PhotoImage(file="./images/upload.png")
        self.upload_icon = self.upload_icon.subsample(27)  # Réduire de moitié la taille de l'icône convert_icon
        self.upload_button = tk.Button(self.canvas, text="Upload Iris", image=self.upload_icon, compound=tk.LEFT, command=self.upload_image, takefocus=0, background="white", foreground='black', font=('Times', 15, 'bold'), border=5, activebackground="gray", activeforeground='black', relief='raised', cursor='hand1', anchor='center', padx=5, pady=5, justify='center', wraplength=150, bd=2, highlightthickness=0, default='active', disabledforeground='black', highlightbackground='white', highlightcolor='white')
        self.canvas.create_window(400, 500, anchor=tk.N, window=self.upload_button)
        
        self.processed_images = []  # Liste pour stocker les noms d'images déjà traitées

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            # Extraire l'iris_id et le côté (side) à partir du nom de l'image uploadée
            file_name = os.path.basename(file_path)
            iris_id = file_name[:3]
            side = file_name[3]
            
            # Obtenez les dimensions de la fenêtre principale
            main_window_width = self.root.winfo_width()
            main_window_height = self.root.winfo_height()
            
            # Calculez la position x et y pour centrer la fenêtre de dialogue
            x = self.root.winfo_x() + main_window_width // 2 - 125  # 250/2 = 125 (la moitié de la largeur de la fenêtre de dialogue)
            y = self.root.winfo_y() + main_window_height // 2 - 25  # 50/2 = 25 (la moitié de la hauteur de la fenêtre de dialogue)
            
            # Afficher la boîte de dialogue de traitement centrée
            processing_dialog = tk.Toplevel(self.root)
            processing_dialog.title("Processing")
            processing_dialog.geometry("250x50+{}+{}".format(x, y))  # Positionner la fenêtre de dialogue centrée
            processing_dialog.iconbitmap("./images/logo.ico")
            processing_dialog.resizable(False, False)
            processing_dialog.grab_set()
            
            # Label pour afficher le message de traitement
            processing_label = tk.Label(processing_dialog, text="Processing results...", font=("Times", 15, "bold italic"))
            processing_label.pack(pady=10)

            # Mettre à jour l'interface utilisateur après un court délai (simulé ici par une fonction de temporisation)
            self.root.after(10000, lambda: self.process_uploaded_image(file_path, processing_dialog))

    def process_uploaded_image(self, file_path, processing_dialog):
        # Continuer le traitement de l'image téléchargée
        uploaded_image = cv2.imread(file_path)
        file_name = os.path.basename(file_path)
        iris_id = file_name[:3]
        side = file_name[3]

        # Charger les images à partir de la base de données
        highest_matching_rate, matched_iris_id, matched_image, matched_side = self.match_uploaded_image(uploaded_image, iris_id, side)
        
        # Obtenez les dimensions de la fenêtre principale
        main_window_width = self.root.winfo_width()
        main_window_height = self.root.winfo_height()
        # Calculez la position x et y pour centrer la fenêtre de dialogue
        x = self.root.winfo_x() + main_window_width // 2 - 165  # 330/2 = 165 (la moitié de la largeur de la fenêtre de dialogue)
        y = self.root.winfo_y() + main_window_height // 2 - 255  # 510/2 = 215 (la moitié de la hauteur de la fenêtre de dialogue)
        
        # Afficher le résultat dans une nouvelle fenêtre
        result_window = tk.Toplevel(self.root)
        result_window.geometry("330x510+{}+{}".format(x, y))
        result_window.resizable(False, False)
        result_window.iconbitmap("./images/logo.ico")  # Définition de l'icône pour la nouvelle fenêtre
        ResultWindow(result_window, matched_iris_id, matched_side, matched_image, highest_matching_rate)
        # Fermer la boîte de dialogue de traitement
        processing_dialog.destroy()

    def match_uploaded_image(self, uploaded_image, iris_id, side):
        highest_matching_rate = 0
        matched_iris_id = None
        matched_image = None
        matched_side = None

        for n_pos in range(1, 3):
            image_from_db = load_image_from_database(iris_id, side, str(n_pos))
            if image_from_db is not None and image_from_db.shape == uploaded_image.shape and not (image_from_db == uploaded_image).all():  # Comparer seulement si l'image est différente de l'image téléchargée
                gray_scale_uploaded, gray_scale_db = preprocess_image(uploaded_image, image_from_db)
                keypoints_uploaded, descriptors_uploaded, keypoints_db, descriptors_db = extract_features(gray_scale_uploaded, gray_scale_db)
                matching_rate, _ = match_images(uploaded_image, keypoints_uploaded, descriptors_uploaded, image_from_db, keypoints_db, descriptors_db)

                if matching_rate > highest_matching_rate:
                    highest_matching_rate = matching_rate
                    matched_iris_id = iris_id
                    matched_image = image_from_db
                    matched_side = side

        return highest_matching_rate, matched_iris_id, matched_image, matched_side
