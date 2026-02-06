from sentence_transformers import SentenceTransformer
from datasets import load_dataset
import numpy as np
import argparse
import json

import os
import sys

# Getting the path to 'Secure_RAG_Research(the root folder)' (One level up from 'tools')
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

# Adding root to sys.path to find 'src'
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Importing my existing engine directly to test it
try:
    from src.secure_rag import SecureVectorEngine
except ImportError:
    # Fallback: explicit source path append
    sys.path.append(os.path.join(project_root, 'src'))
    from secure_rag import SecureVectorEngine


def run_validation(output_path):
    print("--- Starting Public Data Validation (MS MARCO) ---")

    # 1. Loads Data (Streaming mode to avoid downloading 5GB+)
    # Only taking the first 100 examples from the validation set.
    print("[Data] Streaming 100 examples from MS MARCO (v2.1)...")
    dataset = load_dataset(
        "ms_marco", "v2.1", split="validation", streaming=True)

    queries = []
    passages = []

    # Iterating and collecting 100 pairs
    # Each 'example' has a query and a list of passages. Taking the first passage as the "target".
    counter = 0
    for example in dataset:
        if counter >= 100:
            break

        q_text = example['query']
        # Extracting the first passage text safely
        p_text = example['passages']['passage_text'][0]

        queries.append(q_text)
        passages.append(p_text)
        counter += 1

    print(f"[Data] Collected {len(queries)} query-passage pairs.")

    # 2. Encoding Text to Vectors (The "Real" Embeddings)
    # Using a small, standard model. First run will download it (~200MB).
    print("[Model] Loading Sentence-Transformer (all-MiniLM-L6-v2)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    print("[Embed] Converting text to vectors...")
    query_vectors = model.encode(queries)
    passage_vectors = model.encode(passages)

    # 3. Encrypting Everything (The Test)
    print("[Security] Encrypting vectors with Chaos Engine...")
    # Initializing engine with a fixed key for reproducibility
    engine = SecureVectorEngine(
        secret_key=0.42, dimension=384)  # MiniLM is 384-dim

    encrypted_queries = engine.encrypt_batch(query_vectors)
    encrypted_passages = engine.encrypt_batch(passage_vectors)

    # 4. Verifying Retrieval (Can it find the right passage?)
    print("[Search] Running Nearest Neighbor search on encrypted data...")

    hits = 0
    total = len(queries)

    for i in range(total):
        # Current encrypted query
        q_vec = encrypted_queries[i]

        # Searching against ALL encrypted passages
        # Assuming the engine has a 'search' method
        # If not, doing a manual dot product here for transparency

        # Calculating distances to all passages
        # dist = ||q - p||
        diff = encrypted_passages - q_vec
        dists = np.linalg.norm(diff, axis=1)

        # Finding index of closest match
        best_idx = np.argmin(dists)

        # Did it find the correct index(i)?
        if best_idx == i:
            hits += 1

    accuracy = (hits / total) * 100
    print(
        f"[Result] Accuracy on Encrypted Data: {accuracy:.1f}% ({hits}/{total})")

    # 5. Saving Report
    report = {"dataset": "ms_marco_v2.1_subset", "samples": total, "accuracy": accuracy,
              "model": "all-MiniLM-L6-v2", "status": "PASS" if accuracy > 90 else "FAIL"}

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"[Log] Report saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True,
                        help="Path to save JSON report")
    args = parser.parse_args()

    run_validation(args.out)
