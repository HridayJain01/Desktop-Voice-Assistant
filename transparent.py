import tkinter as tk
from PIL import Image, ImageTk

def make_transparent(window, alpha):
    window.attributes("-alpha", alpha)

def main():
    root = tk.Tk()
    root.title("Transparent Frame Example")
    root.geometry("100x100")
    root.attributes('-topmost', True)
    transparent_frame = tk.Frame(root, bg='white')
    transparent_frame.pack(fill=tk.BOTH, expand=True)

    transparency_level = 0.5
    make_transparent(root, transparency_level)

    gif_path = "/Users/hridayjain/Downloads/output-onlinegiftools.gif"
    frames = []

    with Image.open(gif_path) as img:
        for i in range(img.n_frames):
            img.seek(i)
            frame = img.resize((100,100))  # Resize to fit window
            frames.append(ImageTk.PhotoImage(image=frame))

    frame_label = tk.Label(root)
    frame_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def update_gif(frame_index):
        frame_label.config(image=frames[frame_index])
        root.after(100, update_gif, (frame_index + 1) % len(frames))

    update_gif(0)
    root.mainloop()

if __name__ == "__main__":
    main()