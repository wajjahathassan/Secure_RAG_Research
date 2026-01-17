import numpy as np


class ChaosEngine:
    """
    Handles the generation of chaotic sequences for vector masking.
    Currently uses the Logistic Map.
    """

    def __init__(self, r=3.99, x0=0.5):
        # The control parameter. Needs to be close to 4.0 for true chaos.
        # If it's too low, the system just... stops behaving chaotically.
        self.r = r

        # Initial condition. The 'seed'.
        # A tiny change here changes everything later.
        self.x0 = x0

    def generate_sequence(self, length):
        """
        Generates a sequence of chaotic values between 0 and 1.

        Args:
            length(int): How many numbers we need. usually matches vector dimension.

        Returns:
            np.array: The chaotic sequence.
        """

        # Holds the values.
        sequence = np.zeros(length)

        # Start with the seed.
        current_x = self.x0

        # We iterate. Standard logistic map equation.
        # x_next = r * x * (1 - x)
        for i in range(length):
            current_x = self.r * current_x * (1 - current_x)
            sequence[i] = current_x

        return sequence

    def generate_orthogonal_matrix(self, size):
        """
        Attempting to create a quasi-orthogonal matrix using the chaos.
        We need this to rotate the embeddings securely.
        """

        # Create a random matrix first using the chaotic sequence.
        # Flattening it out to fill the grid.
        total_elements = size * size
        raw_chaos = self.generate_sequence(total_elements)

        # Reshape into a square matrix.
        matrix = raw_chaos.reshape((size, size))

        # QR decomposition.
        # This is the standard linear algebra trick to force orthogonality.
        # Q will be our orthogonal matrix. R is discarded.
        Q, _ = np.linalg.qr(matrix)

        return Q


if __name__ == "__main__":
    # Just a quick test.
    # Seeing if the numbers look random enough.
    engine = ChaosEngine(r=3.99, x0=0.4)
    seq = engine.generate_sequence(5)
    print("Test Sequence:", seq)
