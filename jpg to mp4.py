import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Define color palette
BG_COLOR = "#1e1e1e"
FG_COLOR = "#f0f0f0"
BTN_COLOR = "#0097e6"

def frames_to_video():
    input_folder = folder_entry.get()
    if not input_folder:
        messagebox.showerror("Error", "Please select an input folder.")
        return
    
    frame_rate = frame_rate_entry.get()
    try:
        frame_rate = int(frame_rate)
    except ValueError:
        messagebox.showerror("Error", "Frame rate must be an integer.")
        return

    frame_files = [f for f in os.listdir(input_folder) if f.endswith('.jpg')]
    frame_files.sort()

    if not frame_files:
        messagebox.showerror("Error", "No JPEG frames found in the input folder.")
        return

    # Get dimensions of the first frame
    first_frame = cv2.imread(os.path.join(input_folder, frame_files[0]))
    height, width, _ = first_frame.shape

    # Define output video path
    output_video = os.path.join(os.path.dirname(__file__), "output_video.mp4")

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4 codec
    out = cv2.VideoWriter(output_video, fourcc, frame_rate, (width, height))

    for frame_file in frame_files:
        frame_path = os.path.join(input_folder, frame_file)
        frame = cv2.imread(frame_path)
        out.write(frame)

    # Release the VideoWriter object
    out.release()

    messagebox.showinfo("Success", f"Video created: {output_video}")

# Create the main window
root = tk.Tk()
root.title("Frames to Video")
root.geometry("400x150")
root.configure(bg=BG_COLOR)

# Label and entry for input folder
folder_label = tk.Label(root, text="Input Folder:", fg=FG_COLOR, bg=BG_COLOR)
folder_label.grid(row=0, column=0, padx=10, pady=5)
folder_entry = tk.Entry(root, fg=FG_COLOR, bg=BG_COLOR)
folder_entry.grid(row=0, column=1, padx=10, pady=5)
folder_button = tk.Button(root, text="Browse", fg=FG_COLOR, bg=BTN_COLOR,
                          command=lambda: folder_entry.insert(tk.END, filedialog.askdirectory()))
folder_button.grid(row=0, column=2, padx=10, pady=5)

# Label and entry for frame rate
frame_rate_label = tk.Label(root, text="Frame Rate (fps):", fg=FG_COLOR, bg=BG_COLOR)
frame_rate_label.grid(row=1, column=0, padx=10, pady=5)
frame_rate_entry = tk.Entry(root, fg=FG_COLOR, bg=BG_COLOR)
frame_rate_entry.grid(row=1, column=1, padx=10, pady=5)

# Encode button
encode_button = tk.Button(root, text="Encode", fg=FG_COLOR, bg=BTN_COLOR, command=frames_to_video)
encode_button.grid(row=2, column=1, padx=10, pady=5)

# Start the Tkinter event loop
root.mainloop()
