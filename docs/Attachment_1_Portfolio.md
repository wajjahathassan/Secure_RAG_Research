# Supplementary Evidence: Secure RAG Prototype

**Applicant:** Wajahat Hassan | **Repo:** [github.com/wajjahathassan/Secure_RAG_Research](https://github.com/wajjahathassan/Secure_RAG_Research) | **Update Date:** Feb 4-6, 2026

---

### 1. Verification of Claims & Setup

**Goal:** Verify the claims of **0.0000 Isometry Error** and **High Retrieval Success** made in the Personal Statement.
**Setup:** Tests run locally on **Synthetic Vectors** (Isometry) and **Real-World MS MARCO Data** (Utility).
**Method:** Orthogonal Matrix Encryption generated via Logistic Map (Chaos Theory).
**Note on Security:** This method is an _obfuscation layer_ for internal privacy. It is not fully secure against an attacker who has many "original vs. encrypted" pairs (Known-Plaintext Attack). It trades partial security for speed.

### 2. Key Results Summary

| Metric                  | Result           | Meaning                                                        |
| :---------------------- | :--------------- | :------------------------------------------------------------- |
| **Mean Isometry Error** | `< 1e-12`        | Distance between vectors is identical before/after encryption. |
| **MS MARCO Accuracy**   | `92.0%` (92/100) | Correctly retrieves real passages despite encryption.          |

### 3. Visual Evidence

<table>
  <tr>
    <td align="center" width="50%">
      <img src="figures/fig2_isometry_proof.png" width="250">
      <br><b>Fig A: Isometry Proof</b><br>
      <i>Vector magnitude and relative positions are unchanged by the rotation.</i>
    </td>
    <td align="center" width="50%">
      <img src="figures/fig3_distance_preservation.png" width="250">
      <br><b>Fig B: Distance Preservation</b><br>
      <i>Target (Blue) stays close (~0.1). Distractors (Red) stay far (>0.6).</i>
    </td>
  </tr>
</table>

### 4. Reproduction Logs (Terminal Output)

**Test 1: Math Verification (`python src/experiment.py`)**

```text
[TEST] Generating 128x128 Orthogonal Matrix using Chaos...
[SUCCESS] Matrix generated. Orthogonality Error: 1.3323e-15
[RESULT] Mean Isometry Error (Distance Difference): 0.0000000000
[VERDICT] Transformation is Isometric.
```

**Test 2: Utility Verification (`python src/search_simulation.py`)**

```text
[SETUP] Database: 100 vectors. Dimensions: 128.
[RUN] Executing 12 search queries on ENCRYPTED index...
Query 1: Match Found (Target ID: 42) - Score: 0.1203
...
[FINAL] Success Rate: 100.0% (12/12)
```

**Test 3: Real-World Validation (`python tools/validate_public.py`)**

```text
[Data] Streaming 100 examples from MS MARCO (v2.1)...
[Model] Loading Sentence-Transformer (all-MiniLM-L6-v2)...
[Security] Encrypting vectors with Chaos Engine...
[Search] Running Nearest Neighbor search on encrypted data...
[Result] Accuracy on Encrypted Data: 92.0% (92/100)
[System Status] PASS
```

---

_Full source code available in the GitHub repository. Algorithms run on standard CPUs (No GPU required)._
