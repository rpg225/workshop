import requests
from io import BytesIO
from PIL import Image, ImageFilter

image_url = "https://cdn.shopify.com/s/files/1/0736/0941/2851/files/2_474f94f4-d828-4bfe-90a6-2d0b62fccc55.png?v=1739437773"


def apply_filters(image_url, filter_type):
    if not filter_type:
        print("Filter type is not provided.")
        return None
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch image: {e}")
        return None

    try:
        img = Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"Failed to open image from response: {e}")
        return None

    processed_img = None # Renamed from filtered_img for clarity as rotation isn't strictly a "filter"
    # Apply operation
    if filter_type == "blur":
        processed_img = img.filter(ImageFilter.GaussianBlur(radius=5))
    elif filter_type == "grayscale":
        processed_img = img.convert("L")
    elif filter_type == "unsharp":
        processed_img = img.filter(ImageFilter.UnsharpMask(radius=5))
    elif filter_type == "rotate180":
        # Option 1: Using transpose (often preferred for standard rotations)
        processed_img = img.transpose(Image.ROTATE_180)
        # Option 2: Using rotate (rotates counter-clockwise, but 180 is same either way)
        # processed_img = img.rotate(180)
    else:
        print(f"Unknown operation/filter: {filter_type}")
        return None

    return processed_img

if __name__ == "__main__":
    # To output a 180-degree rotated image, set chosen_operation to "rotate180"
    chosen_operation = "rotate180" # CHANGED HERE
    output_img = apply_filters(image_url=image_url, filter_type=chosen_operation)

    if output_img:
        filename = f"/data/outputs/processed_{chosen_operation}_image.png" # Updated filename
        try:
            output_img.save(filename)
            print(f"Operation '{chosen_operation}' applied and image saved successfully as {filename}")
        except Exception as e:
            print(f"Failed to save image {filename}: {e}")
    else:
        print(f"Image processing with '{chosen_operation}' failed. Image not saved.")