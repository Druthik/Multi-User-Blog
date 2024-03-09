from PIL import Image, ImageTk, ImageDraw, ImageFont

# Function for making round corners
def round_corners(image_path, corner_radius, output_size):
    # Load image using PhotoImage
    original_image = Image.open(image_path).convert("RGBA")
    rounded_image = Image.new("RGBA", original_image.size, (255, 255, 255, 0))

    # Create a mask with rounded corners
    mask = Image.new("L", original_image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), original_image.size], corner_radius, fill=255)
    rounded_image.putalpha(mask)

    # Paste the original image onto the rounded image using the mask
    rounded_image.paste(original_image, (0, 0), mask)

    # Resize the image to the desired output size
    rounded_image = rounded_image.resize(output_size, Image.Resampling.LANCZOS)

    # Convert the rounded image to PhotoImage
    rounded_image_tk = ImageTk.PhotoImage(rounded_image)

    return rounded_image_tk

# Function to create a circular profile picture with the first letter of the username
def create_profile_picture(user_name, size):
    # Create a blank image with an alpha channel (RGBA)
    image = Image.new("RGBA", size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    # Set the font and size
    font_size = int(size[0] * 0.6)
    font = ImageFont.truetype("arial.ttf", font_size)
    # Get the first letter of the username
    first_letter = user_name[0].upper()
    # Calculate the position to center the text
    text_width = draw.textlength(first_letter)
    x = (size[0] - text_width) // 2
    y = (size[1] - text_width) // 2
    # Draw the text on the image
    draw.text((x, y), first_letter, font=font, fill=(255, 255, 255, 255))
    return image