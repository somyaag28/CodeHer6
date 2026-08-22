import json
import math

from ai_model import extract_embedding
from database.inventory import get_all_products


def cosine_similarity(vector_a, vector_b):
    """
    Measures how similar two image embeddings are.

    A value closer to 1 means the images are more similar.
    """

    dot_product = 0
    magnitude_a = 0
    magnitude_b = 0

    for a, b in zip(vector_a, vector_b):
        dot_product += a * b
        magnitude_a += a * a
        magnitude_b += b * b

    if magnitude_a == 0 or magnitude_b == 0:
        return 0

    return dot_product / (
        math.sqrt(magnitude_a) * math.sqrt(magnitude_b)
    )


def match_image(image_path):
    """
    Takes a customer/product image and finds the
    closest product registered by the retailer.
    """

    # Create embedding for the new image
    new_embedding = extract_embedding(image_path)

    # Get all products registered by the retailer
    products = get_all_products()

    best_product = None
    best_similarity = -1

    for product in products:

        product_id = product[0]
        name = product[1]
        price = product[2]
        stock = product[3]
        gst_rate = product[4]
        image_path_saved = product[5]
        embedding_text = product[6]

        # Skip products that don't have an embedding
        if embedding_text is None:
            continue

        # Convert saved text back into a Python list
        saved_embedding = json.loads(embedding_text)

        # Compare the two embeddings
        similarity = cosine_similarity(
            new_embedding,
            saved_embedding
        )

        # Keep the best match
        if similarity > best_similarity:
            best_similarity = similarity

            best_product = {
                "product_id": product_id,
                "name": name,
                "price": price,
                "stock": stock,
                "gst_rate": gst_rate,
                "similarity": similarity
            }

    # Nothing matched
    if best_product is None:
        return {
            "message": "No matching product found"
        }

    return best_product
