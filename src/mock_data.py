import numpy as np


class MockDataGenerator:
    """
    Generates fake vector embeddings for testing encryption.
    Real embeddings are just lists of floats, so I simulate that here.
    """

    def __init__(self, dimension=128, num_documents=10):
        # dimension: The size of the vector (e.g., Gemini is 768, I used 128 for speed).
        # num_documents: How many fake 'files' to generate.
        self.dimension = dimension
        self.num_documents = num_documents

    def generate_embeddings(self):
        """
        Creates a list of random vectors.
        In a real app, these would come from 'model.encode("text")'.
        """

        # Create a matrix of random numbers [10 rows, 128 columns]
        # I normalized them so they look like real unit vectors (length = 1).
        # Real embeddings usually have a magnitude of 1.
        raw_data = np.random.rand(self.num_documents, self.dimension)

        # L2 Normalization (making sure the arrow length is 1)
        # axis=1 means, process row by row.
        norms = np.linalg.norm(raw_data, axis=1, keepdims=True)
        normalized_data = raw_data / norms

        return normalized_data

    def create_similar_pair(self):
        """
        Creates two vectors that are remarkably similar (close to each other).
        I need this to prove that my encryption scheme PRESERVES similarity.
        """

        # 1. Creates a random vector (Vector A)
        vec_a = np.random.rand(self.dimension)
        vec_a = vec_a / np.linalg.norm(vec_a)

        # 2. Creates Vector B by adding a tiny bit of noise to A.
        # 0.01 is very small noise
        noise = np.random.normal(0, 0.01, self.dimension)
        vec_b = vec_a + noise
        vec_b = vec_b / np.linalg.norm(vec_b)

        return vec_a, vec_b


if __name__ == "__main__":
    # Testing the generator
    # Small dimension for readable output
    gen = MockDataGenerator(dimension=5)

    print("- Single Batch Test -")
    print(gen.generate_embeddings())

    print("\n- Similarity Test -")
    v1, v2 = gen.create_similar_pair()
    # Dot product = Cosine Similarity (since they are normalized)
    similarity = np.dot(v1, v2)
    print(f"Similarity between pair: {similarity:.4f}")
    # Should be close to 1.0 (e.g., 0.99)
