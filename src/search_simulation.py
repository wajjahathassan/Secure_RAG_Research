import numpy as np
from chaos_engine import ChaosEngine
from mock_data import MockDataGenerator


def calculate_cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2)


def run_search_simulation():
    print("---------------------------------------------------------")
    print("Simulation: Encrypted Search in Vector Database")
    print("---------------------------------------------------------\n")

    # 1. Setup
    DIMENSION = 128
    NUM_DOCS = 100
    print(f"[Setup] Database Size: {NUM_DOCS} documents")
    print(f"[Setup] Vector Dimension: {DIMENSION}")

    # 2. Preparing Data (Plaintext)
    print("\n[Step 1] Creating Plaintext Database...")
    gen = MockDataGenerator(dimension=DIMENSION, num_documents=NUM_DOCS)
    database_plaintext = gen.generate_embeddings()

    # Selecting a "Target" document (in this case, index 42) to search for
    target_index = 42
    target_vector = database_plaintext[target_index]

    # Creates a Query that is similar to the Target (simulating a user search)
    # Adding noise to the target to make the query
    noise = np.random.normal(0, 0.05, DIMENSION)
    query_plaintext = target_vector + noise

    # Normalize
    query_plaintext = query_plaintext / np.linalg.norm(query_plaintext)

    print(f" • Target Document Index: {target_index}")
    print(
        f" • Plaintext Similarity (Query vs Target): {calculate_cosine_similarity(query_plaintext, target_vector):.4f}")

    # 3. Generating Key
    print("\n[Step 2] Generating Keys...")
    chaos = ChaosEngine(r=3.99, x0=0.555)
    key_matrix = chaos.generate_orthogonal_matrix(DIMENSION)

    # 4. Encrypting Everything
    print("\n[Step 3] Encrypting Database and Query...")
    # Encrypting all documents in the database
    # (Matrix multiplication across the entire list)
    database_encrypted = np.dot(database_plaintext, key_matrix.T)

    # Encrypting the query
    query_encrypted = np.dot(key_matrix, query_plaintext)
    print(" • Encryption Complete.")

    # 5. Performing Search (on Encrypted Data ONLY)
    print("\n[Step 4] Searching Encrypted Database...")

    # Calculated similarity between Encrypted Query and ALL Encrypted Docs
    similarities = []
    for idx, doc_vector in enumerate(database_encrypted):
        sim = calculate_cosine_similarity(query_encrypted, doc_vector)
        similarities.append(sim)

    # Finds the index of the highest similarity
    best_match_index = np.argmax(similarities)
    best_match_score = similarities[best_match_index]

    # 6. The Results
    print(f"\n[Result] Best Match Found At Index: {best_match_index}")
    print(f"[Result] Similarity Score: {best_match_score:.4f}")

    if best_match_index == target_index:
        print("\nSUCCESS: The search correctly identified the target document in the encrypted domain!")
    else:
        print(
            f"\nFAILURE: Retrieved index {best_match_index}, expected {target_index}.")


if __name__ == "__main__":
    run_search_simulation()
