import numpy as np
from src.chaos_engine import ChaosEngine


class SecureVectorEngine:
    """
    A high-level API for Secure RAG operations.
    Encapsulates key management, encryption, and search logic.
    """

    def __init__(self, secret_key: float, dimension: int):
        """
        Initialize the engine with a secret key and vector dimension.

        Args:
            secret_key (float): The initial condition for the chaotic map (0 < key < 1).
            dimension (int): The size of the embedding vectors (e.g., 128, 768).
            """

        self.secret_key = secret_key
        self.dimension = dimension

        # Initializing the chaotic crypto-processor
        self.engine = ChaosEngine(r=3.99, x0=self.secret_key)

        # Pre-computing the orthogonal key matrix (This acts as the "Session Key")
        print(
            f"[SecureEngine] Generating Orthogonal Key for dim={dimension}...")
        self.orthogonal_key = self.engine.generate_orthogonal_matrix(dimension)
        print("[SecureEngine] Key Generation Complete.")

    def encrypt_batch(self, vectors: np.ndarray) -> np.ndarray:
        """
        Encrypts a batch of vectors (e.g., the Document Database).

        Args:
            vectors (np.ndarray): Shape (N, dimension)

        Returns:
            np.ndarray: Encrypted vectors of shape (N, dimension)
        """

        # Linear Algebra: Encrypted = Vectors @ Key
        # (Using dot product for rotation)
        return vectors @ self.orthogonal_key

    def encrypt_single(self, vector: np.ndarray) -> np.ndarray:
        """
        Encrypts a single vector (e.g., a User Query).

        Args:
            vector (np.ndarray): Shape (dimension,) or (1, dimension)

        Returns:
            np.ndarray: Encrypted vector
        """

        # Ensuring it's 2D for matrix multiplication
        if vector.ndim == 1:
            vector = vector.reshape(1, -1)

        encrypted = vector @ self.orthogonal_key
        return encrypted.flatten()

    def search(self, encrypted_query: np.ndarray, encrypted_database: np.ndarray, top_k: int = 5):
        """
        Performs a 'Blind Search' on encrypted data.
        Calculates distances without ever decrypting.

        Args:
            encrypted_query (np.ndarray): The encrypted user query.
            encrypted_database (np.ndarray): The encrypted knowledge base.
            top_k (int): Number of results to return.

        Returns:
            indices (np.ndarray): Indices of the nearest neighbors.
            distances (np.ndarray): The distances to those neighbors.
        """

        # Ensuring query is 2D
        if encrypted_query.ndim == 1:
            encrypted_query = encrypted_query.reshape(1, -1)

        # 1. Computing Euclidean Distances (Vectorized)
        # dist = sqrt(sum((db - query)^2))
        diff = encrypted_database - encrypted_query
        sq_dist = np.sum(diff ** 2, axis=1)
        distances = np.sqrt(sq_dist)

        # 2. Sorting and getting Top-K indices
        # argsort gives indices of elements from smallest to largest
        sorted_indices = np.argsort(distances)

        top_indices = sorted_indices[:top_k]
        top_distances = distances[top_indices]

        return top_indices, top_distances
