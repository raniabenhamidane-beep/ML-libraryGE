# Building a hybrid book recommendation engine for a student library

This project is an iterative exploration into building a recommendation system that balances historical borrowing habits with the semantic meaning of book metadata. Rather than relying on a single algorithm, we developed a **3-way hybrid model** that blends collaborative and content-based filtering.

## Deliverables

**Video link**: https://youtu.be/zs9qtUctSA8?si=aB6sI7gUVBU_WzW3 
**Ranking**: 4th place
**Final Score**: 0.174

## The winning formula: weights and tuning

After extensive testing and grid searches, we identified a specific configuration that outperformed all other variations:

* **The blend weights**: 10% user-to-user (U2U), 15% item-to-item (I2I), and **75% content-based similarity**.
* **KNN filter**: Setting **k=20** for the nearest-neighbor filters proved to be the most effective for stripping away noise without losing relevant recommendations.
* **Dominance of content**: The high weight assigned to the content model (75%) suggests that for this library dataset, the semantic relationships between books are the strongest predictors of future interest.

--- 

## The foundation: temporal decay and data handling

We didn't treat all data as equal; we accounted for the fact that user interests evolve over time.

* **Global temporal split**: Interactions were sorted chronologically to ensure the model respects the sequence of borrowings.
* **User time decay**: We mapped each user’s timeline on a 0.0 to 1.0 scale, applying a decay formula that keeps a minimum weight of **0.2** for older interactions.
---

## Technical evolution and upgrades

### From TF-IDF to multilingual AI

Our initial model used a standard TF-IDF approach, which focused on keyword matching. To better handle the French-heavy catalog, we upgraded to the **SentenceTransformers 'paraphrase-multilingual-mpnet-base-v2'** model. This allowed the engine to understand the *meaning* of titles and subjects across multiple languages.

### Choosing dot product over cosine similarity

A major breakthrough occurred when we replaced standard cosine similarity with **raw dot products**.

* Unlike cosine similarity, which normalizes for the number of interactions, the dot product allows for a natural **popularity bias**.
* This weighting helps active users and popular books act as more "informative" anchors for the recommendation engine.

---

## Efficiency and RAM management

Building these models in an environment like Google Colab required strict memory discipline:

* **Sparsification**: We converted dense similarity matrices into `csr_matrix` format immediately to save RAM.
* **In-place filtering**: Custom functions were written to zero-out non-Top-K neighbors without creating massive duplicate arrays.
* **Garbage collection**: We implemented manual `gc.collect()` calls throughout the batch processing loops to prevent kernel crashes during heavy matrix multiplication.

---

## Future directions

* **Richer metadata**: We believe that tapping into a broader API for full book descriptions (rather than just titles/subjects) would further enhance the content model.
* **4-way hybridization**: Exploring a fourth dimension, such as a dedicated popularity-only model or a graph-based approach, could push accuracy even further.
* **Finer tuning of parameters**: Further sensitivity analysis could refine the accuracy of the model.
