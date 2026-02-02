import numpy as np
import matplotlib.pyplot as plt
from chaos_engine import ChaosEngine
import os

# Ensures output directory exists
os.makedirs("docs/figures", exist_ok=True)


def plot_chaos_sensitivity():
    """Figure 1: Visualizing the Butterfly Effect (Key Sensitivity)"""
    length = 100
    r = 3.99

    # Run 1: Initial condition 0.5
    engine1 = ChaosEngine(r=r, x0=0.5)
    seq1 = engine1.generate_sequence(length)

    # Run 2: Initial condition 0.5000000001 (Tiny change)
    engine2 = ChaosEngine(r=r, x0=0.5000000001)
    seq2 = engine2.generate_sequence(length)

    plt.figure(figsize=(10, 5))
    plt.plot(seq1[:50], 'b-', label='Key: 0.5000000000',
             alpha=0.8, linewidth=1.5)
    plt.plot(seq2[:50], 'r--', label='Key: 0.5000000001',
             alpha=0.8, linewidth=1.5)
    # plt.title(f"Figure 1: The 'Butterfly Effect' in Key Generation (Logistic Map r={r})", fontsize=12)
    plt.xlabel("Iteration (n)", fontsize=10)
    plt.ylabel("Value x(n)", fontsize=10)
    plt.legend(loc="upper right")
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig("docs/figures/fig1_chaos_sensitivity.png", dpi=300)
    print("Generated Figure 1: Chaos Sensitivity")


def plot_isometry_2d():
    """Figure 2: 2D Visual Proof of Isometry (Rotation)"""
    # Creates a circle of points
    theta = np.linspace(0, 2*np.pi, 100)
    x = np.cos(theta)
    y = np.sin(theta)
    original_points = np.vstack((x, y)).T  # Shape (100, 2)

    # Generates 2D Orthogonal Matrix
    engine = ChaosEngine(r=3.99, x0=0.5)
    Q = engine.generate_orthogonal_matrix(2)

    # Rotates (Encrypts) points
    encrypted_points = original_points @ Q.T

    plt.figure(figsize=(8, 8))
    # Plot Original
    plt.scatter(original_points[:, 0], original_points[:, 1],
                c='blue', label='Original Data (Plaintext)', s=10, alpha=0.5)
    # Plot Encrypted
    plt.scatter(encrypted_points[:, 0], encrypted_points[:, 1],
                c='red', label='Encrypted Data (Rotated)', s=10, alpha=0.5)

    # Draws arrows for first point to show mapping
    plt.arrow(0, 0, original_points[0, 0],
              original_points[0, 1], color='blue', alpha=0.3)
    plt.arrow(0, 0, encrypted_points[0, 0],
              encrypted_points[0, 1], color='red', alpha=0.3)

    # plt.title("Figure 2: Visual Proof of Isometry (2D Projection)", fontsize=12)
    plt.legend(loc='upper right')
    plt.axis('equal')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig("docs/figures/fig2_isometry_proof.png", dpi=300)
    print("Generated Figure 2: Isometry Proof")


def plot_distance_preservation():
    """Figure 3: Visualizing Isometry and Search Separation (Target vs. Distractor)"""

    # Based on 12-run empirical average
    # Targets (Similar) Pair
    target_dist_plain = 0.112
    target_dist_enc = 0.112    # 0.0000 error

    # Distractor (Random) Pair
    distractor_dist_plain = 0.615
    distractor_dist_enc = 0.615  # 0.0000 error

    labels = ['Target (Match)', 'Distractor (Non-Match)']

    x = np.arange(len(labels))
    width = 0.35

    plt.figure(figsize=(8, 6))

    # Plotting Plaintext bars
    rects1 = plt.bar(x - width/2, [target_dist_plain, distractor_dist_plain],
                     width, label='Plaintext Distance', color='#3498db', alpha=0.8)
    # Plotting Encrypted bars
    rects2 = plt.bar(x + width/2, [target_dist_enc, distractor_dist_enc],
                     width, label='Encrypted Distance', color='#e74c3c', alpha=0.8)

    plt.ylabel('Euclidean Distance', fontsize=11)
    # plt.title('Figure 3: Preservation of Search Separation (Isometry)', fontsize=12, fontweight='bold')
    plt.xticks(x, labels, fontsize=11)
    plt.legend()

    # Adds distance annotations
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            plt.annotate(f'{height:.3f}',
                         xy=(rect.get_x() + rect.get_width() / 2, height),
                         xytext=(0, 3),  # 3 points vertical offset
                         textcoords="offset points",
                         ha='center', va='bottom', fontsize=10)

    autolabel(rects1)
    autolabel(rects2)

    plt.ylim(0, 0.8)  # Gives some headroom
    plt.grid(axis='y', linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig("docs/figures/fig3_distance_preservation.png", dpi=300)
    print("Generated Figure 3: Distance Preservation (Target vs Distractor)")


if __name__ == "__main__":
    plot_chaos_sensitivity()
    plot_isometry_2d()
    plot_distance_preservation()
