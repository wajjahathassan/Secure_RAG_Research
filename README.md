# Secure RAG: Privacy-Preserving Vector Retrieval via Orthogonal Chaotic Maps

> **Status:** ✅ Verified Prototype (100% Isometry Preservation)
> **Core Tech:** NumPy, Logistic Map (Chaos Theory), QR Decomposition
> **License:** MIT Open Source

**Author:** Wajahat Hassan
**Date:** January 2026

## Abstract

Retrieval-Augmented Generation (RAG) systems rely on vector embeddings that, if leaked, can be inverted to reconstruct the original sensitive text. This research proposes a lightweight encryption method using **Orthogonal Chaotic Maps**. By generating unique orthogonal matrices via the Logistic Map, we rotate embedding vectors in high-dimensional space. This transformation preserves the Euclidean distance between vectors - ensuring retrieval accuracy remains 100%, while rendering the raw vectors unintelligible to attackers without the chaotic initial conditions (keys).

## 1. Introduction

Standard RAG architectures store user data as plaintext vector embeddings. Recent studies (Morris et al., 2023) demonstrate that these embeddings can be inverted to recover private information. Current solutions like Homomorphic Encryption (HE) are often too computationally expensive for real-time chat applications.

**Objective:**
To implement a "Secure RAG" layer that:

1. Encrypts embeddings before storage.
2. Preserves exact distance relationships (Isometry) for search.
3. Operates with negligible latency overhead.

## 2. Architecture Concept

The system enables a "Zero-Knowledge" retrieval workflow. The cloud database stores only chaotic-encrypted vectors and never sees the raw user embeddings.

```text
[Client Side]                               [Cloud Side]
   |                                            |
   +-- 1. Embed("Secret Query") -> v            |
   |                                            |
   +-- 2. ChaosEncrypt(v, key) -> v_encrypted   |
   |      (Rotation via Orthogonal Matrix)      |
   |                                            |
   +------------------------------------------> +-- 3. Search(v_encrypted)
                                                |      (Compute Distances)
                                                |
   +<------------------------------------------ +-- 4. Return Top-K Indices
   |                                            |
   +-- 5. Retrieve & Decrypt (Optional)         |
```

## 3. Methodology

The core engine relies on two mathematical principles: **Chaos Theory** for key generation and **Linear Algebra** for geometric preservation.

### 3.1 The Chaos Engine (Logistic Map)

To avoid storing static encryption keys, we generate pseudo-random sequences using the Logistic Map equation (May, 1976):

`x(n+1) = r * x(n) * (1 - x(n))`

- **r (Control Parameter):** Set to 3.99 to ensure chaotic behavior.

* **x(0) (Initial Condition):** Acts as the private key. A slight change (1e-10) results in a completely different matrix.

### 3.2 Orthogonal Matrix Generation

The chaotic sequence is reshaped into a square matrix. We then apply **QR Decomposition** (`np.linalg.qr`) to orthogonalize this matrix. This produces a rotation matrix `Q` where:

`Q @ Q.T = Identity Matrix`

### 3.3 The Encryption (Rotation)

Data vectors (`v`) are encrypted by projecting them onto the orthogonal matrix (`Q`):

`Encrypted_Vector = Q @ v`

Because `Q` is orthogonal, this operation represents a pure rotation in N-dimensional space. The distance between any two points remains unchanged:

`Distance(v1, v2) == Distance(Encrypted_v1, Encrypted_v2)`

This property allows the RAG system to perform nearest-neighbor searches on encrypted data without ever decrypting it.

## 4. Experimental Results

We conducted two specific experiments to validate the theoretical model using Python.

### 4.1 Isometry Verification

Using `src/experiment.py`, we generated random vectors (dim=128) and encrypted them.

- **Metric:** Difference in Euclidean distance between Original Pair vs. Encrypted Pair.
- **Result:** `0.0000000000`
- **Conclusion:** The transformation is perfectly isometric within standard floating-point precision. The math holds.

### 4.2 Search Utility Simulation

Using `src/search_simulation.py`, we simulated a mini-RAG environment with a "Query" vector and a database of candidates.

- **Setup:** 1 Query, 1 Target Match, 99 Distractors (Total 100 Documents).
- **Procedure:** Encrypt all items, perform Nearest Neighbor search on the encrypted data.
- **Success Rate:** 100% (5/5 trials).
- **Observation:** The system correctly identified the hidden target match every time, solely based on encrypted distances.

## 5. Project Structure

```text
src/
├── chaos_engine.py      # Core Logic: Logistic Map & Matrix Generation
├── mock_data.py         # Utils: Generates normalized test vectors
├── experiment.py        # Proof 1: Verifies distance preservation (Isometry)
└── search_simulation.py # Proof 2: Simulates full RAG retrieval cycle
```

## 6. Usage

### 6.1 Installation

No heavy frameworks are required for the core logic.
`pip install -r requirements.txt`

### 6.2 Reproducing Results

**Experiment 1: Isometry Proof**
Verifies that the distance distortion is effectively zero.
`python src/experiment.py`

**Experiment 2: Search Simulation**
Runs a mock RAG retrieval on encrypted vectors.
`python src/search_simulation.py`

### 6.3 Library Usage (Python API)

You can import the core engine to secure your own vector database.

```python
import numpy as np
from src.secure_rag import SecureVectorEngine

# 1. Initialize
# secret_key (0-1) acts as the chaotic seed
engine = SecureVectorEngine(secret_key=0.45, dimension=128)

# 2. Encrypt Data
# raw_vectors shape: (N, 128)
encrypted_db = engine.encrypt_batch(raw_vectors)

# 3. Encrypt Query
encrypted_query = engine.encrypt_single(user_query)

# 4. Search (Standard Euclidean Distance on Encrypted Data)
indices, distances = engine.search(encrypted_query, encrypted_db, top_k=3)
```

## 7. References

1.  **Morris, J. X., et al. (2023).** _Text Embeddings Reveal (Almost) As Much As Text._ arXiv preprint arXiv:2310.06816.
2.  **May, R. M. (1976).** _Simple mathematical models with very complicated dynamics._ Nature, 261(5560), 459-467.
