import numpy as np


def cosine_similarity(vector1, vector2):
    """
    Calculate cosine similarity between two feature vectors.
    """

    vector1 = np.array(vector1, dtype=np.float32)
    vector2 = np.array(vector2, dtype=np.float32)

    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return float(
        np.dot(vector1, vector2) / (norm1 * norm2)
    )


def find_top_matches(new_vector, saved_vectors, top_k=3):
    """
    Compare a new feature vector with saved product vectors.

    Parameters:
        new_vector:
            Feature vector extracted from a new product image.

        saved_vectors:
            Dictionary containing product names and feature vectors.

        top_k:
            Number of matches to return.

    Returns:
        List of products sorted by similarity.
    """

    results = []

    for product_name, saved_vector in saved_vectors.items():

        score = cosine_similarity(
            new_vector,
            saved_vector
        )

        results.append({
            "product": product_name,
            "similarity": round(score, 4)
        })

    results.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return results[:top_k]


def find_best_match(new_vector, saved_vectors, threshold=0.70):
    """
    Return the best matching product.

    If the similarity is below the threshold,
    return None.
    """

    matches = find_top_matches(
        new_vector,
        saved_vectors,
        top_k=1
    )

    if not matches:
        return None

    best_match = matches[0]

    if best_match["similarity"] < threshold:
        return None

    return best_match
