## Project overview

The goal of this project is to build a robust recommendation system that handles large-scale book data. By blending user-item interaction history with semantic book features (titles, authors, and subjects), the engine overcomes common challenges like the "cold start" problem and high-dimensional data noise.

## Key features

* **Hybrid ensemble engine**: A 3-way weighted blend of User-to-User, Item-to-Item, and AI-driven Content-based filtering.
* **Memory-efficient processing**: Utilizes `scipy.sparse` (CSR matrices) and batched predictions to handle large datasets within limited RAM environments (like Google Colab).
* **Personalized time decay**: Applies a decay formula to interaction weights, ensuring that a user's recent interests carry more weight than older clicks.
* **Semantic NLP**: Uses the `paraphrase-multilingual-mpnet-base-v2` Sentence Transformer model to understand the context of book titles and subjects across multiple languages.
* **Popularity fallback**: Automatically provides top global items for "cold-start" users who have no prior interaction history.

## Technical methodology

### 1. Data preprocessing and temporal splitting

The project implements two types of data splitting:

* **Global temporal split**: Ranks all interactions by time across the entire dataset to simulate a realistic production environment.
* **Time-weighted matrix**: Instead of binary 1s and 0s, interactions are weighted based on a **personalized time rank** (0.2 to 1.0), prioritizing recent activity.

### 2. Similarity algorithms

* **Collaborative filtering**: Computes similarity using Cosine Similarity on interaction vectors.
* **KNN noise filtering**: To keep similarity matrices efficient and accurate, we apply a K-Nearest Neighbors filter, keeping only the top 50–100 strongest relationships per item or user and zeroing out the "static noise."
* **Content-based filtering**: Transforms book metadata into 768-dimensional embeddings to find books with similar "meanings" rather than just shared keywords.

### 3. The ensemble model

The final recommendation is calculated by blending three different "brains":

$$Final\_Score = (W_{u2u} \times Score_{u2u}) + (W_{i2i} \times Score_{i2i}) + (W_{content} \times Score_{content})$$

*The optimal weights identified during testing were approximately 40% User-to-User, 40% Item-to-Item, and 20% Content-based.*

## Installation and usage

### Requirements

* `numpy`
* `pandas`
* `scipy`
* `scikit-learn`
* `sentence-transformers`

### Running the notebook

1. **Data loading**: The notebook fetches the `interactions_train.csv` and `items.csv` directly from the Team Geneva GitHub repository.
2. **Matrix building**: Run the cells under "Data matrix" to generate the sparse interaction structures.
3. **Model execution**: You can run individual models (U2U, I2I) or jump straight to the **ultimate 3-way ensemble** cell to generate a submission-ready CSV.


## Performance and optimization

To prevent "Out of Memory" (OOM) errors, the project includes an **aggressive RAM cleanup** protocol:

* Deletion of dense matrices immediately after sparsification.
* Explicit `gc.collect()` calls within batch loops.
* Pre-normalization of vectors to use Dot Product as a faster alternative to standard Cosine Similarity.
