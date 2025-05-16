import requests
from io import BytesIO
from PIL import Image, ImageFilter, ImageDraw

image_url = "https://cdn.shopify.com/s/files/1/0736/0941/2851/files/2_474f94f4-d828-4bfe-90a6-2d0b62fccc55.png?v=1739437773"

def apply_operations(image_url, operations_list): # Renamed for clarity
    if not operations_list:
        print("No operations provided.")
        return None

    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        current_img = Image.open(BytesIO(response.content))
        print(f"Initial image loaded. Mode: {current_img.mode}, Size: {current_img.size}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch image: {e}")
        return None
    except Exception as e:
        print(f"Failed to open initial image: {e}")
        return None

    for operation_config in operations_list:
        op_type = operation_config.get("type")
        op_params = operation_config.get("params", {}) # Get params or an empty dict

        if not op_type:
            print("Operation type missing in config:", operation_config)
            continue # Skip this malformed operation

        print(f"\nApplying operation: {op_type} with params: {op_params}")

        # Ensure current_img is not None from a previous failed operation (though we return early now)
        if current_img is None:
            print("Previous operation failed, cannot continue.")
            return None

        temp_img = None # To store result of current operation

        if op_type == "blur":
            radius = op_params.get("radius", 5)
            temp_img = current_img.filter(ImageFilter.GaussianBlur(radius=radius))
        elif op_type == "grayscale":
            # Grayscale can be applied to RGB or RGBA. If already L, it does nothing.
            if current_img.mode != "L":
                temp_img = current_img.convert("L")
            else:
                temp_img = current_img # No change needed
        elif op_type == "unsharp":
            radius = op_params.get("radius", 5)
            temp_img = current_img.filter(ImageFilter.UnsharpMask(radius=radius))
        elif op_type == "rotate180":
            temp_img = current_img.transpose(Image.ROTATE_180)
        elif op_type == "resize":
            size = op_params.get("size")
            if size and isinstance(size, tuple) and len(size) == 2:
                print(f"Resizing image to {size[0]}x{size[1]}")
                try:
                    temp_img = current_img.resize(size, Image.Resampling.LANCZOS)
                except AttributeError:
                    temp_img = current_img.resize(size, Image.LANCZOS)
            else:
                print("Invalid or no size provided for resize. Expected 'size': (width, height) in params.")
                return None # Critical error for this operation
        elif op_type == "blue_gradient_overlay":
            # Ensure base image is RGBA for compositing
            if current_img.mode != "RGBA":
                base_img_rgba = current_img.convert("RGBA")
            else:
                base_img_rgba = current_img

            width, height = base_img_rgba.size
            gradient_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(gradient_layer)

            start_color_rgb = op_params.get("start_color_rgb", (0, 0, 50))
            end_color_rgb = op_params.get("end_color_rgb", (0, 100, 200))
            opacity_percent = op_params.get("opacity_percent", 50)
            alpha = int((opacity_percent / 100) * 255)

            print(f"Applying blue gradient from {start_color_rgb} to {end_color_rgb} with {opacity_percent}% opacity.")
            for y in range(height):
                ratio = y / (height - 1 if height > 1 else 1)
                r = int(start_color_rgb[0] * (1 - ratio) + end_color_rgb[0] * ratio)
                g = int(start_color_rgb[1] * (1 - ratio) + end_color_rgb[1] * ratio)
                b = int(start_color_rgb[2] * (1 - ratio) + end_color_rgb[2] * ratio)
                draw.line([(0, y), (width, y)], fill=(r, g, b, alpha))
            temp_img = Image.alpha_composite(base_img_rgba, gradient_layer)
        else:
            print(f"Unknown operation type: {op_type}")
            return None # Unknown operation, stop processing

        if temp_img is None and op_type not in ["grayscale"]: # Grayscale might not change if already L
             print(f"Operation {op_type} did not produce an image.")
             # return None # Decide if this should be a fatal error

        current_img = temp_img
        if current_img:
            print(f"After {op_type}: Mode: {current_img.mode}, Size: {current_img.size}")
        else: # Should ideally not happen if logic above is correct
            print(f"Error: current_img became None after {op_type}")
            return None


    return current_img

if __name__ == "__main__":
    # Define the sequence of operations you want to apply
    # 1. Resize to 300x300
    # 2. Convert to grayscale
    # 3. Rotate 180 degrees
    operations_to_perform = [
        {
            "type": "resize",
            "params": {"size": (300, 300)}
        },
        {
            "type": "grayscale"
            # No extra params needed for grayscale
        },
        {
            "type": "rotate180"
            # No extra params needed for rotate180
        }
        # Example: You could add more, like the gradient afterwards
        # {
        #     "type": "blue_gradient_overlay",
        #     "params": {
        #         "start_color_rgb": (0, 0, 80),
        #         "end_color_rgb": (50, 150, 255),
        #         "opacity_percent": 30
        #     }
        # }
    ]

    print(f"Starting image processing with {len(operations_to_perform)} operations...")
    final_image = apply_operations(image_url=image_url, operations_list=operations_to_perform)

    if final_image:
        # Construct a filename based on the operations
        op_names = "_then_".join([op.get("type","unknown") for op in operations_to_perform])
        filename = f"/data/outputs/processed_{op_names}_image.png"
        try:
            # If the final image is RGBA (e.g., after gradient) and saving as PNG, it's fine.
            # If it's 'L' (grayscale), PNG is also fine.
            # If you intend to save as JPG, and it's RGBA, convert to "RGB".
            # if final_image.mode == 'RGBA':
            #     final_image.convert('RGB').save(filename_jpg)
            final_image.save(filename)
            print(f"\nAll operations applied. Final image saved successfully as {filename}")
            print(f"Final image mode: {final_image.mode}, size: {final_image.size}")
        except Exception as e:
            print(f"Failed to save final image {filename}: {e}")
    else:
        print("\nImage processing failed. No final image produced.")