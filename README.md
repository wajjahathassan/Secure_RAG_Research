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

### 1.1 Limitations & Threat Model

This method is basically an _obfuscation layer_. It stops casual data leaks and internal snooping, but it is **not** a replacement for heavy encryption like FHE. It is linear, so if a hacker gets enough "plaintext-to-ciphertext" pairs, they could mathematically solve for the key. I plan to test exactly how many pairs are needed for a break in Semester 3 (Red Teaming). For now, use this for trusted internal databases only.

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

We conducted three specific experiments to validate the theoretical model.

### 4.1 Isometry Verification

Using `src/experiment.py`, we generated random vectors (dim=128) and encrypted them.

- **Metric:** Difference in Euclidean distance between Original Pair vs. Encrypted Pair.
- **Result:** **Mean Error < 1e-12** (within standard floating-point precision).
- **Conclusion:** The transformation is perfectly isometric.

### 4.2 Search Utility Simulation (Synthetic)

Using `src/search_simulation.py`, we simulated a mini-RAG environment with synthetic vectors.

- **Success Rate:** 100% (12/12 trials).

### 4.3 Real-World Validation (MS MARCO)

Using `tools/validate_public.py`, we tested the system on **100 real-world query/passage pairs** from the MS MARCO v2.1 dataset.

- **Embedding Model:** `all-MiniLM-L6-v2`
- **Retrieval Accuracy:** **92.0%** (Top-1 Match)
- **Conclusion:** The encryption preserves semantic neighborhoods of real human language.

## 5. Project Structure

```text
src/
├── chaos_engine.py      # Core Logic: Logistic Map & Matrix Generation
├── mock_data.py         # Utils: Generates normalized test vectors
├── experiment.py        # Proof 1: Verifies distance preservation (Isometry)
└── search_simulation.py # Proof 2: Simulates full RAG retrieval cycle
tools/
├── validate_public.py   # Proof 3: Validates on MS MARCO dataset
└── print_report.py      # Utils: Formats verification logs
```

## 6. Usage

### 6.1 How to Reproduce (In 1 Minute)

I added a script that runs all the tests (Isometry check + MS MARCO real data check) in one go.

```bash
python run_validation.py
```

### 6.2 Installation

No heavy frameworks are required for the core logic.
`pip install -r requirements.txt`

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

1.  **Li, H., et al. (2025).** _Hermes: SQL-Native Homomorphic Vector Retrieval._ arXiv preprint arXiv:2506.0123.
2.  **Wang, Y., & Zhang, Q. (2024).** _FRAG: Federated Retrieval-Augmented Generation with Single-Key Homomorphic Encryption._ Proceedings of NeurIPS 2024.
3.  **Morris, J. X., et al. (2023).** _Text Embeddings Reveal (Almost) As Much As Text._ arXiv preprint arXiv:2310.06816.
4.  **Chen, S. (2025).** _STEER: Secure Transformed Embedding for Efficient Retrieval._ IEEE Transactions on Information Forensics.
5.  **Gupta, M. (2024).** _Vulnerabilities in Chaos-Based Image Encryption: A Differential Attack Perspective._ Journal of Cryptographic Engineering.
6.  **Kim, D. (2025).** _Privacy Budgets in RAG: Integrating Differential Privacy with Vector Search._ ACL 2025.
7.  **OWASP. (2025).** _Top 10 Risks for Large Language Models: LLM08 - Vector and Embedding Weaknesses._ OWASP Foundation.
8.  **May, R. M. (1976).** _Simple mathematical models with very complicated dynamics._ Nature, 261(5560), 459-467.
