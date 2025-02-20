import os
from PIL import Image, ImageStat

INPUT_DIR = "default_image_folder"
OUTPUT_DIR = "default_output_folder"


def calculate_brightness(image_path):
    img = Image.open(image_path).convert("L")
    stat = ImageStat.Stat(img)
    return stat.mean[0]


def main(
    image_folder=INPUT_DIR,
    output_folder=OUTPUT_DIR,
    dark_threshold=100,
    bright_threshold=150,
):
    if not os.path.exists(image_folder):
        print("Image folder not found.")
        return
    os.makedirs(output_folder, exist_ok=True)

    dark_folder = os.path.join(output_folder, "dark")
    medium_folder = os.path.join(output_folder, "medium")
    bright_folder = os.path.join(output_folder, "bright")
    os.makedirs(dark_folder, exist_ok=True)
    os.makedirs(medium_folder, exist_ok=True)
    os.makedirs(bright_folder, exist_ok=True)

    try:
        image_files = [
            f
            for f in os.listdir(image_folder)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]
    except FileNotFoundError:
        print("No images found in the given path.")
        return

    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        brightness = calculate_brightness(image_path)

        if brightness < dark_threshold:
            target_folder = dark_folder
        elif brightness > bright_threshold:
            target_folder = bright_folder
        else:
            target_folder = medium_folder

        dst = os.path.join(target_folder, image_file)
        os.rename(image_path, dst)

    print("Images classified by brightness.")


if __name__ == "__main__":
    main()
