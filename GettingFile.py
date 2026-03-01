import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(
    title="Select a file",
    initialdir="/",
    filetypes=(
        ("All Image Files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff *.webp"),
        ("PNG files", "*.png"),
        ("JPEG files", "*.jpg *.jpeg"),
        ("GIF files", "*.gif"),
        ("BMP files", "*.bmp"),
        ("TIFF files", "*.tiff"),
        ("WEBP files", "*.webp"),
        ("All files", "*.*")
    )
)


def Save_Root():
    Path = file_path
    return Path

Save_Root()