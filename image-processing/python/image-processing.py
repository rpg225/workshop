import requests
from io import BytesIO
from PIL import Image, ImageFilter

image_url = "https://cdn.shopify.com/s/files/1/0736/0941/2851/files/2_474f94f4-d828-4bfe-90a6-2d0b62fccc55.png?v=1739437773"


def apply_filters(image_url, operation_type, size=None): # Added 'size' parameter
    if not operation_type:
        print("Operation type is not provided.")
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

    processed_img = None
    # Apply operation
    if operation_type == "blur":
        processed_img = img.filter(ImageFilter.GaussianBlur(radius=5))
    elif operation_type == "grayscale":
        processed_img = img.convert("L")
    elif operation_type == "unsharp":
        processed_img = img.filter(ImageFilter.UnsharpMask(radius=5))
    elif operation_type == "rotate180":
        processed_img = img.transpose(Image.ROTATE_180)
    elif operation_type == "resize": # NEW OPERATION
        if size and isinstance(size, tuple) and len(size) == 2:
            print(f"Resizing image to {size[0]}x{size[1]}")
            # The resize method takes a tuple (width, height)
            try: # Check for Pillow version for resampling argument
                processed_img = img.resize(size, Image.Resampling.LANCZOS)
            except AttributeError: # Older Pillow versions
                processed_img = img.resize(size, Image.LANCZOS)
        else:
            print("Invalid or no size provided for resize operation. Expected (width, height) tuple.")
            return None
    else:
        print(f"Unknown operation/filter: {operation_type}")
        return None

    return processed_img

if __name__ == "__main__":
    # --- To output a RESIZED image ---
    chosen_operation = "resize"
    target_size = (300, 300) # Define the target dimensions (width, height)
    output_img = apply_filters(image_url=image_url, operation_type=chosen_operation, size=target_size) # Pass the size


    if output_img:
        # Make filename more descriptive for resize
        if chosen_operation == "resize" and target_size:
            filename = f"/data/outputs/processed_{chosen_operation}_{target_size[0]}x{target_size[1]}_image.png"
        else:
            filename = f"/data/outputs/processed_{chosen_operation}_image.png"
        try:
            output_img.save(filename)
            print(f"Operation '{chosen_operation}' applied and image saved successfully as {filename}")
        except Exception as e:
            print(f"Failed to save image {filename}: {e}")
    else:
        print(f"Image processing with '{chosen_operation}' failed. Image not saved.")