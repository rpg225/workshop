# Image Processing Algorithm for Ocean Protocol Workshop

This Python script demonstrates various image processing operations using the Pillow (PIL) library. It's designed to be used as an algorithm, potentially within the Ocean Protocol ecosystem, to transform images fetched from a URL. The script has evolved to support multiple chained operations.

## Features / Implemented Operations

The script can perform the following operations, which can be chained in any desired order:

*   **`resize`**: Resizes the image to specified dimensions.
    *   Params: `{"size": (width, height)}`
*   **`grayscale`**: Converts the image to grayscale.
    *   Params: None
*   **`rotate180`**: Rotates the image by 180 degrees.
    *   Params: None
*   **`blur`**: Applies a Gaussian blur.
    *   Params: `{"radius": integer}` (default: 5)
*   **`unsharp`**: Applies an unsharp mask filter.
    *   Params: `{"radius": integer}` (default: 5)
*   **`blue_gradient_overlay`**: Overlays a customizable blue gradient with opacity.
    *   Params:
        *   `{"start_color_rgb": (r, g, b)}` (default: (0, 0, 50))
        *   `{"end_color_rgb": (r, g, b)}` (default: (0, 100, 200))
        *   `{"opacity_percent": integer}` (0-100, default: 50)

## Prerequisites

*   Python 3.x
*   Pillow library: `pip install Pillow`
*   Requests library: `pip install requests`

## Setup

1.  Save the final Python script (provided in the previous interactions) as a `.py` file (e.g., `image_processor.py`).
2.  Ensure the output directory (e.g., `/data/outputs/` as used in the script) exists if running in an environment that requires it (like Ocean Compute). If running locally, you might need to create it or modify the output path in the script.

## Usage (Current Version - Chained Operations)

To use the script:

1.  Modify the `image_url` variable at the top of the script if you wish to process a different default image.
2.  The core of the script's flexibility lies in the `operations_to_perform` list within the `if __name__ == "__main__":` block. This list defines the sequence of operations to be applied.
3.  Each item in `operations_to_perform` is a dictionary:
    *   It **must** have a `type` key specifying the operation (e.g., `"resize"`, `"grayscale"`).
    *   It **may** have a `params` key, which is itself a dictionary containing parameters for that operation (e.g., `{"size": (300, 300)}` for resize).

**Example `operations_to_perform` list:**

```python
operations_to_perform = [
    {
        "type": "resize",
        "params": {"size": (300, 300)}  # Resizes to 300x300 pixels
    },
    {
        "type": "grayscale"
        # No params needed for grayscale
    },
    {
        "type": "rotate180"
        # No params needed for rotate180
    },
    {
        "type": "blue_gradient_overlay",
        "params": {
            "start_color_rgb": (0, 0, 80),    # A custom dark blue
            "end_color_rgb": (50, 150, 255), # A custom lighter blue
            "opacity_percent": 30             # 30% opacity
        }
    }
]
