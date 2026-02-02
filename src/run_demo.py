import numpy as np
from src.secure_rag import SecureVectorEngine
from src.mock_data import MockDataGenerator


def run_demo():
    print("=== Secure RAG Library Demo ===")

    # 1. Setup
    DIMENSION = 128
    DB_SIZE = 100
    SECRET_KEY = 0.459382   # Example User Key

    # 2. Initializing the Secure Engine
    secure_rag = SecureVectorEngine(SECRET_KEY, DIMENSION)

    # 3. Generating Mock Data (Unencrypted)
    print("\n[Data] Generating mock vectors...")
    # Initializing the generator
    # Note: DB_SIZE - 1 because we will add one target manually
    generator = MockDataGenerator(
        dimension=DIMENSION, num_documents=DB_SIZE - 1)

    # Generating the database background noise
    database = generator.generate_embeddings()

    # Generating a specific Query and Target pair
    query_vector, target_vector = generator.create_similar_pair()

    # Inserting target into database at specific index
    target_index = 42
    database = np.insert(database, target_index, target_vector, axis=0)

    print(f"[Data] Database size: {database.shape}")
    print(f"[Data] Target placed at index: {target_index}")

    # 4. ENCRYPTION
    print("\n[Encryption] Encrypting Database and Query...")
    encrypted_db = secure_rag.encrypt_batch(database)
    encrypted_query = secure_rag.encrypt_single(query_vector)

    # 5. BLIND SEARCH
    print("[Search] Performing search on encrypted data...")
    indices, distances = secure_rag.search(
        encrypted_query, encrypted_db, top_k=3)

    # 6. VERIFICATION
    print("\n=== Results ===")
    print(f"Top 3 Indices found: {indices}")
    print(f"Distances (smaller is better): {distances}")

    if indices[0] == target_index:
        print("\n✅ SUCCESS: The system found the hidden target!")
    else:
        print("\n❌ FAILURE: Target missed.")


if __name__ == "__main__":
    run_demo()
