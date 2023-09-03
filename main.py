import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import time

root = tk.Tk()
original_image = Image.open("template.png")
panel = None
label = None

def get_overlay_image(text_to_add):
    image_with_text = original_image.copy()
    draw = ImageDraw.Draw(image_with_text)
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMonoBoldOblique.ttf", 36, encoding="unic")
    draw.text((100, 200), text_to_add, fill="black", font=font)  
    return image_with_text


def display_image(image_with_text):
    global root
    global label

    root.destroy(); root = tk.Tk()
    photo = ImageTk.PhotoImage(image_with_text)
    label = tk.Label(root, image=photo)
    label.pack()
    label.photo = photo
    root.mainloop()

def update_image(text_to_add):
    overlay = get_overlay_image(text_to_add)
    photo = ImageTk.PhotoImage(overlay)

    label.config(image=photo)
    label.image = photo



display_image(get_overlay_image("Soccer game at 2"))
