# 🖼️ Image Captioning AI (VGG16 + Transformer)

An image captioning system that combines **computer vision** and **natural language processing**: a frozen, pre-trained **VGG16** network extracts visual features from an image, and a **Transformer decoder** generates a natural-language caption describing it.

Built with **TensorFlow / Keras**.

---

## 📌 Features

- 🧠 **VGG16** (ImageNet pre-trained, frozen) as the CNN feature extractor
- 🔀 **Transformer decoder** with masked self-attention + cross-attention over image features (no RNN/LSTM — fully attention-based, like a mini "Show, Attend and Tell" but Transformer-based)
- 🧵 Custom tokenizer/vocabulary built with `TextVectorization`
- 📦 Caches CNN features to disk so you only run the CNN once, not on every training epoch
- 🖨️ Greedy decoding for inference on new, unseen images
- 🧩 Modular code: preprocessing, model, training, and inference are all separate, reusable files

---

## 🧩 How It Works

1. **Feature extraction (`feature_extractor.py`)**
   Every training image is resized to 224×224 and passed through VGG16 (with the classification head removed). The last convolutional block outputs a 7×7×512 feature map, which is reshaped into a sequence of **49 visual tokens**, each a 512-dim vector. VGG16's weights stay frozen — we only use it as a fixed feature extractor.

2. **Caption preprocessing (`data_preprocessing.py`)**
   Captions are lowercased, stripped of punctuation, and wrapped with `<start>` / `<end>` tokens. A `TextVectorization` layer builds the vocabulary and turns captions into integer token sequences.

3. **Transformer decoder (`transformer_model.py`)**
   For each caption, the decoder:
   - Embeds the tokens generated so far + adds positional encoding
   - Applies **causal (masked) self-attention** so it can only look at *previous* words, not future ones
   - Applies **cross-attention** where caption tokens attend to the 49 visual tokens from VGG16 — this is how the model "looks at" the image while writing the caption
   - Predicts a probability distribution over the vocabulary for the next word

   This is trained with **teacher forcing**: the model is shown the correct previous words and learns to predict the next one.

4. **Inference (`generate_caption.py`)**
   For a new image, VGG16 extracts features, then the decoder generates the caption **one word at a time** (greedy decoding), feeding each predicted word back in as input for the next step, until it predicts `<end>` or hits the max length.

---

## 📁 Project Structure

```
image_captioning/
│
├── config.py               # All hyperparameters and file paths
├── feature_extractor.py    # VGG16 CNN feature extraction
├── data_preprocessing.py   # Caption cleaning, tokenizer, tf.data pipeline
├── transformer_model.py    # Transformer decoder architecture
├── train.py                 # Training script
├── generate_caption.py      # Inference script (caption a new image)
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Download a dataset

This project is built for the **Flickr8k dataset** (8,000 images, 5 captions each — small enough to train on a single GPU or even Colab).

- Download from Kaggle: [Flickr8k Dataset](https://www.kaggle.com/datasets/adityajn105/flickr8k)
- After downloading, arrange the files like this:

```
dataset/
├── Images/              # all .jpg files
└── captions.txt         # format: image,caption (header row included)
```

> `captions.txt` should look like:
> ```
> image,caption
> 1000268201_693b08cb0e.jpg,A child in a pink dress is climbing up a set of stairs .
> 1000268201_693b08cb0e.jpg,A girl going into a wooden building .
> ...
> ```

*(You can also use Flickr30k or MS-COCO — just make sure the captions file matches this `image,caption` CSV format, or adjust `load_captions()` in `data_preprocessing.py`.)*

### 3. Extract image features (run once)

```bash
python feature_extractor.py
```

This creates `features.pkl`, caching VGG16 features for every image so you don't need to re-run the CNN on every training epoch.

### 4. Train the model

```bash
python train.py
```

This builds the vocabulary, trains the Transformer decoder, and saves:
- `tokenizer_vocab.json` — the vocabulary
- `checkpoints/final_model.weights.h5` — the trained weights

Training progress (loss/accuracy) prints each epoch. Early stopping and learning-rate reduction are enabled by default (see `config.py` to tune epochs, batch size, model size, etc.).

### 5. Generate a caption for a new image

```bash
python generate_caption.py --image path/to/your/image.jpg
```

Example output:
```
Predicted caption:
  a dog running through the grass
```

---

## ⚙️ Configuration

All key hyperparameters live in `config.py`:

| Parameter | Default | Description |
|---|---|---|
| `EMBED_DIM` | 512 | Transformer embedding dimension |
| `NUM_HEADS` | 8 | Attention heads |
| `NUM_DECODER_LAYERS` | 2 | Stacked decoder blocks |
| `FF_DIM` | 1024 | Feed-forward hidden size |
| `MAX_CAPTION_LEN` | 40 | Max tokens per caption |
| `VOCAB_SIZE` | 10000 | Max vocabulary size |
| `BATCH_SIZE` | 64 | Training batch size |
| `EPOCHS` | 30 | Training epochs (early stopping may end sooner) |

---

## 🛠️ Possible Extensions

- Swap VGG16 for **ResNet50** or **EfficientNet** for stronger features
- Add **beam search** decoding instead of greedy decoding for better captions
- Evaluate with **BLEU / METEOR / CIDEr** scores against reference captions
- Fine-tune the last few VGG16 layers instead of freezing the whole CNN
- Deploy as a web app (Flask/Streamlit) with drag-and-drop image upload
- Visualize cross-attention weights to see *where* the model is "looking" for each generated word

---

## 📚 Concepts Demonstrated

- Transfer learning with a pre-trained CNN
- Transformer architecture: self-attention, cross-attention, positional encoding
- Sequence-to-sequence generation with teacher forcing
- Multimodal learning (combining vision and language)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙌 Acknowledgements

Built as part of an AI/ML learning task on combining computer vision and NLP for image captioning.
