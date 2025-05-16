# Multi-Operation Image Processor

This Python script uses the Pillow (PIL) library to perform a sequence of image processing operations on an image fetched from a URL. It's designed to be flexible, allowing users to define a chain of transformations to be applied.

## Features / Implemented Operations

The script supports the following operations, which are applied in the order they appear in the `operations_list`:

*   **`resize`**: Resizes the image to the specified dimensions.
    *   **Params**: `{"size": (width, height)}` (e.g., `{"size": (300, 300)}`)
*   **`grayscale`**: Converts the image to grayscale (8-bit pixels, black and white).
    *   **Params**: None
*   **`rotate180`**: Rotates the image by 180 degrees.
    *   **Params**: None
*   **`blur`**: Applies a Gaussian blur to the image.
    *   **Params**: `{"radius": integer}` (default: 5, e.g., `{"radius": 10}`)
*   **`unsharp`**: Applies an unsharp mask filter to enhance image sharpness.
    *   **Params**: `{"radius": integer}` (default: 5)
*   **`blue_gradient_overlay`**: Overlays a vertical blue gradient with configurable opacity.
    *   **Params**:
        *   `{"start_color_rgb": (r, g, b)}` (default: `(0, 0, 50)`) - Color at the top.
        *   `{"end_color_rgb": (r, g, b)}` (default: `(0, 100, 200)`) - Color at the bottom.
        *   `{"opacity_percent": integer}` (0-100, default: `50`) - Opacity of the gradient.

## Prerequisites

*   Python 3.x
*   Pillow library: `pip install Pillow`
*   Requests library: `pip install requests`

## Setup

1.  Save the Python script (e.g., as `image_processor.py`).
2.  Ensure the output directory specified in the script (default: `/data/outputs/`) exists. If running locally, you might need to create this directory manually or modify the output path in the script's `if __name__ == "__main__":` block.

## Usage

1.  **Configure Image URL:**
    Modify the `image_url` variable at the top of the script to point to the image you want to process.
    ```python
    image_url = "your_image_url_here.png"
    ```

2.  **Define Operations:**
    The core of the script's behavior is controlled by the `operations_to_perform` list within the `if __name__ == "__main__":` block. This list defines the sequence of image transformations. Each item in the list is a dictionary:
    *   It **must** have a `type` key, specifying the operation to perform (e.g., `"resize"`, `"grayscale"`).
    *   It **may** have a `params` key, which is a dictionary containing parameters specific to that operation. If an operation requires parameters and they are not provided, or if default parameters are defined within the function, those defaults will be used or an error might occur if a required parameter is missing.

    **Example `operations_to_perform` list:**
    ```python
    operations_to_perform = [
        {
            "type": "resize",
            "params": {"size": (300, 300)}
        },
        {
            "type": "grayscale"
        },
        {
            "type": "rotate180"
        },
        {
            "type": "blue_gradient_overlay",
            "params": {
                "start_color_rgb": (0, 0, 80),
                "end_color_rgb": (50, 150, 255),
                "opacity_percent": 30
            }
        }
    ]
    ```

3.  **Run the Script:**
    Execute the script from your terminal:
    ```bash
    python image_processor.py
    ```

4.  **Output:**
    The script will print a log of its actions to the console. The final processed image will be saved to the specified output path (e.g., `/data/outputs/processed_resize_then_grayscale_then_rotate180_image.png`). The filename is dynamically generated to reflect the sequence of operations applied.

## Key Design: Chained Operations

The `apply_operations` function is designed to process a list of operation configurations. It fetches the initial image and then iterates through the `operations_list`. The output image from one operation becomes the input for the next, allowing for a flexible and powerful way to build complex image processing pipelines.

## Notes for Ocean Protocol Integration

*   **Input/Output Paths:** The script uses `/data/outputs/` for saving the processed image. This is a common convention in Ocean Protocol Compute-to-Data environments where algorithms access input data and write outputs to predefined mounted volumes.
*   **Consumer Parameters:** When used as an algorithm in an Ocean compute job:
    *   The `image_url` could be passed as a consumer parameter (e.g., `{"image_url": "http://..."}`).
    *   The `operations_list` itself, or its constituent parts, could also be defined via consumer parameters, allowing users of the algorithm to specify the desired transformations when initiating a compute job. For example, a JSON string representing the `operations_list` could be passed.
*   **Error Handling:** The script includes basic error handling for image fetching and processing steps. In a production Ocean algorithm, more robust error handling and logging would be beneficial.