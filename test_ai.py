"""
test_ai.py

A very simple sanity check for ai_model.py.

This does NOT test accuracy (whether it recognizes the "right"
product) — that is Sionna's job once matching is added. This just
checks that our part of the pipeline works: image in, embedding out.
"""

import os
from ai_model import extract_embedding

PRODUCT_IMAGES_FOLDER = "product_images"


def find_one_test_image():
    """Finds the first available image inside product_images/ to test with."""
    for product_id in os.listdir(PRODUCT_IMAGES_FOLDER):
        product_folder = os.path.join(PRODUCT_IMAGES_FOLDER, product_id)

        if not os.path.isdir(product_folder):
            continue

        for image_name in os.listdir(product_folder):
            if image_name.lower().endswith((".jpg", ".jpeg", ".png")):
                return os.path.join(product_folder, image_name)

    return None


def run_test():
    print("Looking for a test image...")
    image_path = find_one_test_image()

    if image_path is None:
        print("No test image found. Please add an image inside product_images/<product_id>/")
        return

    print(f"Using test image: {image_path}")
    print("Running it through MobileNetV3...")

    embedding = extract_embedding(image_path)

    # Check 1: Did we actually get something back?
    if embedding is None or len(embedding) == 0:
        print("FAILED: No embedding was produced.")
        return

    print("SUCCESS: Embedding was created.")

    # Check 2: How big is the embedding?
    print(f"Embedding length: {len(embedding)} numbers")

    # Check 3: Print only the first 5 values (not all 576!)
    # so we can eyeball that they look like normal numbers.
    print(f"First 5 values: {embedding[:5]}")


if __name__ == "__main__":
    run_test()
