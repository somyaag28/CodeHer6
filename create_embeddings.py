"""
create_embeddings.py

This script looks inside the "product_images" folder, generates an
embedding for every image using extract_embedding() from ai_model.py,
and saves everything into one file: product_embeddings.pkl

Folder structure expected:

    product_images/
        101/
            image1.jpg
            image2.jpg
        102/
            image1.jpg
            ...

The folder name (e.g. "101") is the product ID. This MUST match the
product ID used in Sanvi's database.
"""

import os
import pickle
from ai_model import extract_embedding

PRODUCT_IMAGES_FOLDER = "product_images"
OUTPUT_FILE = "product_embeddings.pkl"


def build_embeddings():
    # This dictionary will look like:
    # {
    #   "101": [embedding1, embedding2, embedding3],
    #   "102": [embedding1, embedding2, embedding3],
    # }
    all_embeddings = {}

    # Go through every folder inside product_images/
    # Each folder name is treated as a product ID.
    for product_id in os.listdir(PRODUCT_IMAGES_FOLDER):
        product_folder = os.path.join(PRODUCT_IMAGES_FOLDER, product_id)

        # Skip anything that isn't a folder (like .DS_Store on Mac)
        if not os.path.isdir(product_folder):
            continue

        product_embeddings = []

        # Go through every image inside this product's folder
        for image_name in os.listdir(product_folder):
            image_path = os.path.join(product_folder, image_name)

            # Skip hidden/system files that aren't real images
            if not image_name.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            print(f"Processing {image_path} ...")
            embedding = extract_embedding(image_path)
            product_embeddings.append(embedding)

        all_embeddings[product_id] = product_embeddings

    # Save everything to a single file using pickle.
    # Pickle simply saves a Python object (our dictionary) to disk
    # so it can be loaded back later without redoing all this work.
    with open(OUTPUT_FILE, "wb") as f:
        pickle.dump(all_embeddings, f)

    print(f"\nDone! Saved embeddings for {len(all_embeddings)} products to {OUTPUT_FILE}")


if __name__ == "__main__":
    build_embeddings()
