import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def find_best_match(
    query_embedding,
    product_embeddings,
    threshold=0.75
):
    """
    Finds the closest registered product to a new
    product image embedding.

    product_embeddings format:

    {
        101: [embedding1, embedding2],
        102: [embedding1],
        103: [embedding1, embedding2, embedding3]
    }

    Returns:

    {
        "product_id": 101,
        "similarity": 0.92
    }

    If no sufficiently good match exists:

    {
        "product_id": None,
        "similarity": 0.42
    }
    """

    # Convert query embedding to NumPy array
    query_embedding = np.asarray(
        query_embedding,
        dtype=np.float32
    ).reshape(1, -1)

    best_product_id = None
    best_similarity = -1.0

    # Compare against every registered product
    for product_id, embeddings in product_embeddings.items():

        # Allow a single embedding or multiple embeddings
        if isinstance(embeddings, np.ndarray):
            embeddings = [embeddings]

        elif not isinstance(embeddings, list):
            embeddings = [embeddings]

        # Compare query with every reference image
        for stored_embedding in embeddings:

            stored_embedding = np.asarray(
                stored_embedding,
                dtype=np.float32
            ).reshape(1, -1)

            similarity = cosine_similarity(
                query_embedding,
                stored_embedding
            )[0][0]

            if similarity > best_similarity:
                best_similarity = float(similarity)
                best_product_id = product_id

    # Reject weak matches
    if best_similarity < threshold:
        return {
            "product_id": None,
            "similarity": best_similarity
        }

    return {
        "product_id": best_product_id,
        "similarity": best_similarity
    }
