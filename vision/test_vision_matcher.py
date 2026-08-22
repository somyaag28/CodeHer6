from vision_matcher import find_best_match


# Dummy embeddings representing retailer-registered products

maggi_1 = [1.0, 0.0, 0.0, 0.0]
maggi_2 = [0.98, 0.02, 0.0, 0.0]

coke_1 = [0.0, 1.0, 0.0, 0.0]


# Simulated product embeddings from the database

product_embeddings = {
    101: [maggi_1, maggi_2],
    102: [coke_1]
}


# Customer scans Maggi

customer_embedding = [
    0.99,
    0.01,
    0.0,
    0.0
]


result = find_best_match(
    customer_embedding,
    product_embeddings,
    threshold=0.75
)

print("Maggi test:")
print(result)


# Customer scans an unknown product

unknown_embedding = [
    0.0,
    0.0,
    1.0,
    0.0
]


unknown_result = find_best_match(
    unknown_embedding,
    product_embeddings,
    threshold=0.75
)

print("\nUnknown product test:")
print(unknown_result)
