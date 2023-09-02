import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont

def display_image(image_path):
    root = tk.Tk()
    root.title("Ambiance")

    original_image = Image.open(image_path)
    
    # Create a copy of the original image to add text
    image_with_text = original_image.copy()
    
    text_to_add = "Soccer game at 2"
    
    # Create a drawing context for adding text to the image
    draw = ImageDraw.Draw(image_with_text)
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMonoBoldOblique.ttf", 36, encoding="unic")
    draw.text((200, 200), text_to_add, fill="black", font=font)  

    # Convert the modified image to a PhotoImage
    photo = ImageTk.PhotoImage(image_with_text)
    
    label = tk.Label(root, image=photo)
    label.pack()
    label.photo = photo

    root.mainloop()

# Example usage:
image_path = "template.png"  # Replace with the path to your image
display_image(image_path)
