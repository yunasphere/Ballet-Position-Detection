import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def select_and_process_image():
    # Open file dialog
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
    )

    if file_path:
        img = cv2.imread(file_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Ensure DATASET folder exists
        output_folder = "DATASET"
        os.makedirs(output_folder, exist_ok=True)

        # Build output file path
        filename = os.path.basename(file_path)
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(output_folder, f"{name}_gray{ext}")

        # Save grayscale image
        cv2.imwrite(output_path, gray)

        # Display grayscale image
        cv2.imshow("Grayscale Image", gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def delete_from_dataset():
    dataset_folder = "DATASET"

    # Ensure folder exists
    if not os.path.exists(dataset_folder):
        messagebox.showerror("Error", "DATASET folder does not exist yet.")
        return

    # File picker limited to DATASET folder
    file_path = filedialog.askopenfilename(
        initialdir=dataset_folder,
        title="Select a file to delete",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
    )

    if file_path:
        try:
            os.remove(file_path)
            messagebox.showinfo("Deleted", f"Deleted:\n{os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete file:\n{e}")

# Create Tkinter window
root = tk.Tk()
root.title("OpenCV Image Loader")
root.geometry("300x200")

# Buttons
btn_load = tk.Button(root, text="Select Image", command=select_and_process_image, height=2, width=20)
btn_load.pack(pady=10)

btn_delete = tk.Button(root, text="Delete From DATASET", command=delete_from_dataset, height=2, width=20)
btn_delete.pack(pady=10)

# Run GUI
root.mainloop()
