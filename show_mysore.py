from pathlib import Path
import tkinter as tk

from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageTk

image_path = Path(
    r"C:\Users\madhu\OneDrive\Desktop\Mysore_palace_illuminated.jpg"
)
output_path = Path(__file__).parent / "mysore_dasara_titled.png"

LOADING_TITLE = "KARNATAKA IN GOLD"
LOADING_SUBTITLE = "A ROYAL NIGHT AT MYSURU PALACE"

# Open the image
image = Image.open(image_path).convert("RGB")
image_width, image_height = image.size

# Add a dark title panel to the bottom of the photo
overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)
draw.rectangle(
    (0, image_height - 110, image_width, image_height),
    fill=(0, 0, 0, 165)
)

try:
    title_font = ImageFont.truetype("arial.ttf", 30)
    subtitle_font = ImageFont.truetype("arial.ttf", 18)
except OSError:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()

# Center the title on the photo
photo_title = "KARNATAKA IN GOLD"
title_box = draw.textbbox((0, 0), photo_title, font=title_font)
title_x = (image_width - (title_box[2] - title_box[0])) // 2
draw.text(
    (title_x, image_height - 91),
    photo_title,
    font=title_font,
    fill="#FFD166"
)

# Center the subtitle below the title
photo_subtitle = "MYSURU DASARA • THE PALACE OF LIGHTS"
subtitle_box = draw.textbbox((0, 0), photo_subtitle, font=subtitle_font)
subtitle_x = (image_width - (subtitle_box[2] - subtitle_box[0])) // 2
draw.text(
    (subtitle_x, image_height - 50),
    photo_subtitle,
    font=subtitle_font,
    fill="white"
)

# Combine the title panel and photo, then save a PNG copy
titled_image = Image.alpha_composite(
    image.convert("RGBA"),
    overlay
).convert("RGB")
titled_image.save(output_path)
print(f"Titled image saved: {output_path}")

# Fit the complete image in the display window without cropping it
window_width = 1100
window_height = 700
display_image = ImageOps.contain(
    titled_image,
    (1040, 620),
    Image.Resampling.LANCZOS
)
dark_image = Image.new("RGB", display_image.size, "black")

# Create the display window
root = tk.Tk()
root.title("Karnataka in Gold")
root.geometry(f"{window_width}x{window_height}")
root.resizable(False, False)

canvas = tk.Canvas(
    root,
    width=window_width,
    height=window_height,
    bg="black",
    highlightthickness=0
)
canvas.pack()

# Loading title and subtitle
title_item = canvas.create_text(
    window_width // 2,
    285,
    text="",
    fill="#FFD166",
    font=("Arial", 30, "bold")
)

canvas.create_text(
    window_width // 2,
    330,
    text=LOADING_SUBTITLE,
    fill="#E8D9B5",
    font=("Arial", 14)
)

# Loading progress line
bar_left = window_width // 2 - 180
bar_right = window_width // 2 + 180
bar_y = 390

canvas.create_line(
    bar_left, bar_y, bar_right, bar_y,
    fill="#493917",
    width=3
)
progress_line = canvas.create_line(
    bar_left, bar_y, bar_left, bar_y,
    fill="#FFD166",
    width=4
)


def show_photo(step=0):
    total_steps = 12

    if step <= total_steps:
        amount = step / total_steps
        frame = Image.blend(dark_image, display_image, amount)
        preview = ImageTk.PhotoImage(frame, master=root)
        root.current_photo = preview

        if step == 0:
            root.image_item = canvas.create_image(
                window_width // 2,
                window_height // 2,
                image=preview,
                anchor="center"
            )
        else:
            canvas.itemconfigure(root.image_item, image=preview)

        root.after(65, show_photo, step + 1)


def finish_loading():
    # Show the full title, including the final letter, before the photo
    canvas.itemconfigure(
        title_item,
        text=LOADING_TITLE,
        fill="#FFE8A3",
        font=("Arial", 36, "bold")
    )
    canvas.delete("title_sparkle")

    # Hold the finished title briefly, then show the image
    root.after(900, start_photo)


def start_photo():
    canvas.delete("all")
    show_photo()


def show_loading(step=0):
    total_steps = 50
    progress = step / total_steps
    letters = round(len(LOADING_TITLE) * progress)

    # Pulse the title size and gold color
    pulse = step % 12
    if pulse > 6:
        pulse = 12 - pulse

    font_size = 30 + pulse
    gold_colors = ["#FFD166", "#FFE8A3", "#F5B942"]

    canvas.itemconfigure(
        title_item,
        text=LOADING_TITLE[:letters],
        fill=gold_colors[(step // 4) % len(gold_colors)],
        font=("Arial", font_size, "bold")
    )

    # Add small sparkles beside the title
    canvas.delete("title_sparkle")
    bounds = canvas.bbox(title_item)

    if bounds:
        sparkle_y = (bounds[1] + bounds[3]) // 2
        size = 2 + step % 3

        for sparkle_x in (bounds[0] - 18, bounds[2] + 18):
            canvas.create_oval(
                sparkle_x - size,
                sparkle_y - size,
                sparkle_x + size,
                sparkle_y + size,
                fill="#FFD166",
                outline="",
                tags="title_sparkle"
            )

    # Animate the progress line and its gold highlight
    current_x = bar_left + int((bar_right - bar_left) * progress)
    canvas.coords(progress_line, bar_left, bar_y, current_x, bar_y)

    canvas.delete("glow")
    canvas.create_oval(
        current_x - 5, bar_y - 5,
        current_x + 5, bar_y + 5,
        fill="#FFF1B8",
        outline="",
        tags="glow"
    )

    if step < total_steps:
        root.after(55, show_loading, step + 1)
    else:
        finish_loading()


# Start the loading animation and keep the window open
show_loading()
root.mainloop()