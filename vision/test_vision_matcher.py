from vision_matcher import find_top_matches, find_best_match


# Dummy saved product vectors
saved_vectors = {

    "Maggi": [
        0.20,
        0.40,
        0.10,
        0.70
    ],

    "Parle-G": [
        0.80,
        0.10,
        0.30,
        0.20
    ],

    "Coca-Cola": [
        0.10,
        0.90,
        0.20,
        0.30
    ]
}


# Dummy feature vector of a new product
new_vector = [
    0.21,
    0.39,
    0.12,
    0.69
]


print("TOP MATCHES")
print("-----------")

matches = find_top_matches(
    new_vector,
    saved_vectors,
    top_k=3
)

for match in matches:
    print(
        match["product"],
        "->",
        match["similarity"]
    )


print("\nBEST MATCH")
print("----------")

best = find_best_match(
    new_vector,
    saved_vectors
)

if best:
    print("Product:", best["product"])
    print("Similarity:", best["similarity"])
else:
    print("No reliable match found.")
