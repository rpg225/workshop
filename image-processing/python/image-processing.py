import requests
from io import BytesIO
from PIL import Image, ImageFilter

image_url = "https://cdn.shopify.com/s/files/1/0736/0941/2851/files/2_474f94f4-d828-4bfe-90a6-2d0b62fccc55.png?v=1739437773"


def apply_filters(image_url, filter):
    if not filter:
        print("Filter is not provided.")
        return
    response = requests.get(image_url)

    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
    else:
        print(f"Failed to fetch image: {response.status_code}")
        print(response.text[:500])
    filtered_img = None
    # Apply filter
    if filter == "blur":
        blurred_img = img.filter(ImageFilter.GaussianBlur(radius=5))
        filtered_img = blurred_img
    elif filter == "grayscale":
        grayscale_img = img.convert("L")
        filtered_img = grayscale_img
    elif filter == "unsharp":
        unsharp_img = img.filter(ImageFilter.UnsharpMask(radius=5))
        filtered_img = unsharp_img
    else:
        print("Unknown filter.")
        return

    return filtered_img

if __name__ == "__main__":
    filtered_img = apply_filters(image_url=image_url, filter="blur") # <--- Changed to blur
    filename = "/data/outputs/filtered_image_blur.png"
    # It's good practice to check if filtered_img is not None before saving
    if filtered_img:
        filtered_img.save(filename)
        print(f"Blur filter applied and image saved successfully as {filename}")
    else:
        print("Image filtering failed. Not saving.")