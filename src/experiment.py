import numpy as np
from chaos_engine import ChaosEngine
from mock_data import MockDataGenerator


def calculate_cosine_similarity(vec1, vec2):
    """
    Calculates the cosine similarity between two vectors.
    Since the vectors are normalized, this is just the dot product.
    """

    return np.dot(vec1, vec2)


def run_experiment():
    print("---------------------------------------------------------")
    print("Experiment: Secure RAG - Orthogonal Encryption Verification")
    print("---------------------------------------------------------\n")

    # 1. Setup
    DIMENSION = 128
    print(f"[Setup] Vector Dimension: {DIMENSION}")

    # 2. Generating Data
    print("[Step 1] Generating Mock Data Pairs...")
    data_gen = MockDataGenerator(dimension=DIMENSION)
    vec_original_a, vec_original_b = data_gen.create_similar_pair()

    sim_original = calculate_cosine_similarity(vec_original_a, vec_original_b)
    print(f" • Original Similarity (Plaintext): {sim_original:.6f}")

    # 3. Generating Key (Chaos)
    print("\n[Step 2] Generating Orthogonal Key (Chaotic Matrix)...")

    # Using a specific seed (simulating a private key)
    chaos_engine = ChaosEngine(r=3.99, x0=0.742)
    key_matrix = chaos_engine.generate_orthogonal_matrix(DIMENSION)
    print(" • Key Matrix Generated using Logistic Map Chaos.")

    # 4. Encryption
    # The core operation: Encrypted_Vector = Matrix * Original_Vector
    print("\n[Step 3] Encrypting Vectors (Rotation)...")
    vec_encrypted_a = np.dot(key_matrix, vec_original_a)
    vec_encrypted_b = np.dot(key_matrix, vec_original_b)

    # 5. Verifying Results
    print("\n[Step 4] Verifying Similarity Preservation...")
    sim_encrypted = calculate_cosine_similarity(
        vec_encrypted_a, vec_encrypted_b)
    print(f" • Encrypted Similarity (Ciphertext): {sim_encrypted:.6f}")

    # 6. Conclusion
    diff = abs(sim_original - sim_encrypted)
    print(f"\n[Result] Difference: {diff:.10f}")

    if diff < 1e-9:
        print("\nSUCCESS: Similarity is preserved perfectly via orthogonal rotation.")
        print("Hypothesis Confirmed: The distances between points remain unchanged in the encrypted space.")
    else:
        print("\nWARNING: Significant deviation present. Check floating point precision or orthogonality.")


if __name__ == "__main__":
    run_experiment()
