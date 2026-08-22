# AI Module — Product Feature Extraction

**Author:** Aanya
**Part of:** SIH 2026 — Image-Based Product Recognition for Barcode-Free Retail Billing (Team CodeHer6)

## What does my module do?

My module takes a photo of a product and turns it into a list of numbers
(called an **embedding**). It does NOT decide what the product is — it
just describes the image mathematically so that Sionna's code can compare
it to other product photos later.

Think of it like this: I turn a picture into a "fingerprint" of numbers.
Sionna compares fingerprints to find the closest match.

```
Product image → my code (ai_model.py) → embedding (list of numbers) → Sionna compares it
```

## What is PyTorch?

PyTorch is a Python library for building and running neural networks.
It is NOT the AI model itself — it's the toolkit we use to load and run
one. Think of PyTorch as the engine, and MobileNetV3 as the specific
car built using that engine.

**TorchVision** is a companion library to PyTorch that comes with
ready-to-use pre-trained models (like MobileNetV3) and image
preprocessing tools, so we don't have to build a CNN from scratch.

## What is MobileNetV3?

MobileNetV3 is a type of **CNN (Convolutional Neural Network)** —
a neural network designed specifically to understand images. It was
designed to be small and fast enough to run on phones and low-end
hardware, which is exactly what our project needs since vendors will
use smartphone cameras.

We use the **"Small"** version because it's the lightest variant —
perfect for a prototype and for devices that aren't very powerful.

## Why a pre-trained model instead of training our own?

**Pre-trained** means someone else already trained this model on a
huge dataset called ImageNet (1.2 million images, 1000 categories)
so it already knows how to recognize edges, shapes, colors, and
textures in images.

Training a CNN from scratch requires:
- Tens of thousands of labelled images
- Powerful GPUs and a lot of time
- Deep expertise in tuning neural networks

We have none of that for a hackathon prototype, so we **reuse**
(this is called **transfer learning**) the general visual knowledge
MobileNetV3 already has, instead of starting from zero.

**Important limitation:** MobileNetV3 was trained on general
ImageNet objects (dogs, cars, chairs, etc.), not specifically on
grocery products. So it may see two similar-looking products (like
two chip packets) as very close to each other. That's expected —
our system handles this by having Sionna return the **top matches**
so the vendor can confirm the right one, instead of assuming 100%
accuracy.

A future improvement (not required now) would be to **fine-tune**
MobileNetV3 on our own labelled product photos if we collect enough
data later.

## Why do we remove the final classification layer?

By default, MobileNetV3 ends by predicting one of 1000 ImageNet
classes (e.g., "banana", "backpack"). We don't want a class name —
we want the raw numbers computed just before that final decision.
Those numbers are the embedding. So we replace the classifier with
`torch.nn.Identity()`, which just means "pass the data through
unchanged, don't classify it."

## What is an embedding / feature vector?

An embedding is a list of numbers that represents the important
visual characteristics of an image (shapes, colors, patterns) in a
compact form. Similar-looking products will have embeddings that are
mathematically close to each other. Very different products will have
embeddings that are far apart.

We don't return "this is product 101" directly, because deciding the
best match is Sionna's job (comparing embeddings). My job stops at
turning the image into numbers.

## Installation

From inside the `AI/` folder, run:

```bash
pip install -r requirements.txt
```

This installs:
- `torch` — the PyTorch library
- `torchvision` — pre-trained models + image preprocessing
- `pillow` — for opening and reading image files

## How to arrange product images

```
product_images/
    101/
        image1.jpg
        image2.jpg
        image3.jpg
    102/
        image1.jpg
        image2.jpg
    103/
        image1.jpg
```

The **folder name is the product ID**, and it must match the same
product ID used in Sanvi's database (e.g., product 101 in my folder =
product 101 in the database).

We keep 3–5 images per product because the same product can look
slightly different depending on the angle, lighting, or how it's
placed in front of the camera. Having multiple images means we get
multiple embeddings per product, which gives Sionna more reference
points to compare against — this makes matching more reliable than
relying on just one photo.

## How to run the test

```bash
python test_ai.py
```

This finds one sample image, runs it through `extract_embedding()`,
and prints:
- Whether it succeeded
- How many numbers are in the embedding
- The first 5 numbers (just as a sanity check, not the full vector)

## How to generate product_embeddings.pkl

```bash
python create_embeddings.py
```

This goes through every folder inside `product_images/`, creates
embeddings for every image, and saves them all into
`product_embeddings.pkl` — grouped by product ID.

## What does Sionna receive from my module?

Two things:

1. **The function** `extract_embedding(image_path)` from `ai_model.py`,
   which she can call on a new, unknown product photo taken during
   billing.
2. **The file** `product_embeddings.pkl`, which contains the saved
   reference embeddings for every known product (101, 102, 103, ...).

Sionna's job is to take the new embedding from step 1, compare it
against all the saved embeddings in step 2 (using something like
cosine similarity), and return the best matching product ID(s).

## How my module connects to the rest of the team

```
Somya (camera/UI)
        ↓ captures image
Aanya (me): ai_model.py → extract_embedding()
        ↓ returns embedding (numbers)
Sionna: compares embedding against product_embeddings.pkl
        ↓ returns best matching product ID
Sanvi: looks up that product ID in the database (name, price, stock)
        ↓
San: calculates billing + GST
        ↓
Saanch: FastAPI ties all of this together into one working app
```

My part only covers: **image → embedding**. Everything after that
(matching, database, billing, API, UI) belongs to my teammates.
