"""
ai_model.py

This file has ONE job: turn a product image into a list of numbers
(called an "embedding" or "feature vector") using a pre-trained
MobileNetV3 Small model.

Sionna will import extract_embedding() from this file and use the
numbers it returns to compare products. We do NOT do any comparison
or matching here — that is Sionna's part.
"""

import torch
from torchvision import models, transforms
from PIL import Image

# ---------------------------------------------------------------
# STEP 1: Load the pre-trained MobileNetV3 Small model (once)
# ---------------------------------------------------------------
# "weights" here means the model has already been trained by other
# researchers on a huge dataset called ImageNet (1000 object types).
# We are NOT training this ourselves. We are reusing what it already
# learned about edges, shapes, colors and textures.
weights = models.MobileNet_V3_Small_Weights.DEFAULT
model = models.mobilenet_v3_small(weights=weights)

# ---------------------------------------------------------------
# STEP 2: Remove the final classification layer
# ---------------------------------------------------------------
# Normally, MobileNetV3 ends by predicting one of 1000 ImageNet
# classes (like "dog", "car", "banana"). We don't want a class
# prediction — we want the raw feature vector that comes just
# BEFORE that final decision. Replacing the classifier with
# "Identity" means "just pass the features through unchanged."
model.classifier = torch.nn.Identity()

# ---------------------------------------------------------------
# STEP 3: Put the model in evaluation mode
# ---------------------------------------------------------------
# Some layers (like Dropout, used only during training to prevent
# overfitting) behave differently during training vs. actual use.
# model.eval() tells PyTorch: "we are only using this model to make
# predictions, not training it." This keeps results consistent.
model.eval()

# ---------------------------------------------------------------
# STEP 4: Get the correct preprocessing steps for this model
# ---------------------------------------------------------------
# Every pre-trained model expects images prepared in a specific way
# (specific resize size, and specific pixel normalization numbers).
# weights.transforms() gives us the EXACT preprocessing that was
# used when this model was originally trained, so we don't have to
# guess or hardcode numbers ourselves.
transform = weights.transforms()


def extract_embedding(image_path):
    """
    Takes the file path of a product image and returns its
    embedding (a list of numbers describing the image's features).

    Example:
        embedding = extract_embedding("product_images/101/image1.jpg")
    """

    # Open the image and make sure it has 3 color channels (RGB).
    # Some images (like PNGs) can be in different formats (e.g. RGBA),
    # so we force RGB to avoid errors.
    image = Image.open(image_path).convert("RGB")

    # Apply the model's required preprocessing (resize, crop,
    # normalize pixel values, etc.)
    image = transform(image)

    # The model expects a "batch" of images, even if it's just one.
    # unsqueeze(0) adds an extra dimension so the shape becomes
    # [1, 3, height, width] instead of [3, height, width].
    image = image.unsqueeze(0)

    # torch.no_grad() tells PyTorch not to track gradients.
    # Gradients are only needed for TRAINING a model. Since we are
    # only using the model (not training it), turning this off
    # makes things faster and uses less memory.
    with torch.no_grad():
        embedding = model(image)

    # The output is a PyTorch tensor of shape [1, 576].
    # We remove the extra batch dimension and convert it into a
    # plain Python list of numbers, which is much easier for
    # Sionna to store, save, and compare later.
    embedding = embedding.squeeze(0).tolist()

    return embedding
