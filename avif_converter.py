import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image
import pillow_avif  # Enable AVIF support
import os

def get_unique_folder_path(base_folder):
    folder_path = base_folder
    counter = 0
    while os.path.exists(folder_path):
        folder_path = f"{base_folder}_{counter}"
        counter += 1
    os.makedirs(folder_path)
    return folder_path

def convert_multiple_to_avif():
    input_paths = filedialog.askopenfilenames(
        title="Select images to convert",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.gif")]
    )

    if not input_paths:
        return

    target_base = filedialog.askdirectory(
        title="Select target folder to save converted AVIF images"
    )
    if not target_base:
        return

    output_folder = get_unique_folder_path(os.path.join(target_base, "avif_output"))

    success_count = 0
    quality_value = int(quality_slider.get())

    for input_path in input_paths:
        try:
            filename = os.path.basename(input_path)
            name_without_ext = os.path.splitext(filename)[0]
            output_path = os.path.join(output_folder, name_without_ext + ".avif")

            img = Image.open(input_path)
            img.save(output_path, "AVIF", quality=quality_value)
            success_count += 1

        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert:\n{input_path}\n\n{str(e)}")

    if success_count > 0:
        messagebox.showinfo("Done", f"Successfully converted {success_count} image(s) to:\n{output_folder}")
    else:
        messagebox.showwarning("Nothing converted", "No images were converted successfully.")

def update_quality_label(value):
    quality_value_label.config(text=f"{int(float(value))}")

# GUI setup
root = tk.Tk()
root.title("Convert Images to AVIF")
root.geometry("450x320")

label = tk.Label(root, text="Select multiple images to convert to AVIF format", font=("Arial", 12))
label.pack(pady=15)

# Quality slider
quality_frame = tk.Frame(root)
quality_frame.pack(pady=10)

tk.Label(quality_frame, text="Quality:", font=("Arial", 11)).pack(side=tk.LEFT)

quality_slider = ttk.Scale(quality_frame, from_=0, to=100, orient="horizontal", command=update_quality_label)
quality_slider.set(50)  # Default value
quality_slider.pack(side=tk.LEFT, padx=10)

quality_value_label = tk.Label(quality_frame, text="50", font=("Arial", 11), width=3)
quality_value_label.pack(side=tk.LEFT)

convert_btn = tk.Button(root, text="Select and Convert Images", command=convert_multiple_to_avif, font=("Arial", 12))
convert_btn.pack(pady=20)

root.mainloop()
