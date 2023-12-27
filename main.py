import tkinter as tk
from tkinter import filedialog, simpledialog, Label, Button
from PIL import Image, ImageTk
import os
import shutil
import hashlib

class ImageOrganizer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Image Organizer")
        self.selected_folders = []
        self.destination_folder = None

        self.init_ui()

    def init_ui(self):
        # Adjusting the main window size and background color
        self.root.geometry("400x400")
        self.root.configure(bg='#f0f0f0')  # Light grey background

        # Font and color configurations
        label_font = ("Helvetica", 16)
        button_font = ("Helvetica", 12)
        label_color = "#333333"  # Dark grey
        button_color = "#4a7abc"  # Blue color matching the logo

        self.label = Label(self.root, text="Image Organizer", font=label_font, bg='#f0f0f0', fg=label_color)
        self.label.pack(pady=10)

        # Load, resize, and display the logo
        original_image = Image.open("Image_Combiner.png")  # Replace with the path to the downloaded logo
        resized_image = original_image.resize((150, 150), Image.Resampling.LANCZOS)
        self.logo_image = ImageTk.PhotoImage(resized_image)
        self.logo_label = Label(self.root, image=self.logo_image, bg='#f0f0f0')
        self.logo_label.pack(pady=10)

        self.add_folder_button = Button(self.root, text="Add Folder", command=self.select_folder,
                                        font=button_font, bg=button_color, fg='white')
        self.add_folder_button.pack(pady=5)

        self.submit_button = Button(self.root, text="Submit", command=self.copy_and_remove_duplicates,
                                    font=button_font, bg=button_color, fg='white')
        self.submit_button.pack(pady=5)

    def select_folder(self):
        if len(self.selected_folders) < 5:
            folder = filedialog.askdirectory(title="Select Folder")
            if folder:
                self.selected_folders.append(folder)

    def get_file_hash(self, file_path):
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def copy_and_remove_duplicates(self):
        if not self.selected_folders:
            return

        self.destination_folder = filedialog.askdirectory(title="Select Destination Folder")
        testing_images_folder = os.path.join(self.destination_folder, "Testing_Images")
        os.makedirs(testing_images_folder, exist_ok=True)

        hashes = {}
        for folder in self.selected_folders:
            for filename in os.listdir(folder):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    file_path = os.path.join(folder, filename)
                    file_hash = self.get_file_hash(file_path)

                    if file_hash not in hashes:
                        hashes[file_hash] = filename
                        shutil.copy(file_path, os.path.join(testing_images_folder, filename))

        self.rename_folder(testing_images_folder)

    def rename_folder(self, original_folder):
        new_name = simpledialog.askstring("Rename Folder", "Enter new folder name:", initialvalue="Testing_Images")
        if new_name:
            new_folder_path = os.path.join(self.destination_folder, new_name)
            os.rename(original_folder, new_folder_path)

    def run(self):
        self.root.mainloop()

def main():
    app = ImageOrganizer()
    app.run()

if __name__ == "__main__":
    main()
