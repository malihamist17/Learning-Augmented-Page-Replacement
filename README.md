# CSE-307 Track 1 — Learning-Augmented Page Replacement

**Learning-Augmented OS Heuristics: Classical Algorithms Meet Adaptive Prediction**

This project compares classical page replacement algorithms with a lightweight learned page replacement policy under a deliberate workload shift.

## 1. Algorithms Implemented

### FIFO

First-In, First-Out replaces the page that has been in memory for the longest time.

### LRU

Least Recently Used replaces the page that has not been accessed for the longest time.

### Optimal

Optimal (Belady's) replaces the page whose next future use is farthest away. If a page will not be used again, it is selected first.

Optimal is used as a theoretical benchmark because it requires future knowledge.

### Learned Policy

The learned policy uses a Decision Tree classifier.

For each page currently in memory, the model uses:

* **Recency:** number of references since the page was last accessed.
* **Recent frequency:** number of times the page appeared in the previous 20 references.

The model predicts which page should be evicted.

Recent training examples are kept so that the model can adapt when the workload changes.

## 2. Workload Design

A synthetic reference string containing **2,000 page references** is used.

| Phase   | References | Access Pattern            |
| ------- | ---------: | ------------------------- |
| Phase 1 |      1,000 | Locality-heavy, pages 1–5 |
| Phase 2 |      1,000 | Random, pages 1–20        |

The workload uses a fixed random seed (`42`) for reproducibility.

All policies use the same reference string and **3 page frames**.

The learned policy is trained online. When the frames are full, Optimal is used as a teacher to identify the correct eviction candidate. The learned decision is made before the new teacher label is added to the training data.

## 3. Results

| Policy  | Phase 1 Hit Ratio | Phase 2 Hit Ratio | Total Faults | Total Hit Ratio |
| ------- | ----------------: | ----------------: | -----------: | --------------: |
| FIFO    |             61.5% |             15.6% |         1229 |          38.55% |
| LRU     |             62.2% |             15.1% |         1227 |          38.65% |
| Optimal |             77.9% |             35.4% |          867 |          56.65% |
| Learned |             60.0% |             17.0% |         1230 |          38.50% |

The workload shift reduced the hit ratio of all policies. LRU had the largest drop, while Optimal remained the strongest policy because it has future-reference knowledge.

The learned policy achieved a **17.0% Phase 2 hit ratio**. Using recent training examples improved it compared with the earlier version, reducing total faults from **1260 to 1230**.

Detailed results are available in:

`results/results.csv`

The main comparison chart is:

`results/hit_ratio_shift.png`

## 4. Bonus: Decision Explanation and Confidence

The optional bonus component generates a short explanation for each learned eviction decision.

For each decision, it records:

* requested page
* selected eviction page
* Optimal eviction page
* model-reported prediction probability
* whether the decision matched Optimal
* short explanation

### Bonus Results

| Group                    | Decisions | Correct | Accuracy |
| ------------------------ | --------: | ------: | -------: |
| Overall                  |      1227 |     448 |   36.51% |
| High confidence (≥ 0.8)  |       271 |     100 |   36.90% |
| Lower confidence (< 0.8) |       956 |     348 |   36.40% |

The small difference between the two confidence groups suggests that the model-reported prediction probability had only a weak relationship with actual decision correctness.

The confidence value is the probability reported by the Decision Tree. It is **not** a calibrated probability that the decision itself is correct.

Detailed bonus results:

`results/bonus_decisions.csv`

Bonus summary:

`results/bonus_summary.csv`

## 5. Repository Structure

```text
learning-augmented-page-replacement/
├── src/
│   ├── fifo.py
│   ├── lru.py
│   ├── optimal.py
│   ├── learned.py
│   ├── workload.py
│   ├── simulation.py
│   ├── evaluate.py
│   ├── main.py
│   ├── plot_results.py
│   ├── bonus.py
│   ├── run_bonus.py
│   ├── analyze_bonus.py
│   └── save_bonus_summary.py
│
├── results/
│   ├── results.csv
│   ├── hit_ratio_shift.png
│   ├── bonus_decisions.csv
│   └── bonus_summary.csv
│
└── README.md
```

## 6. How to Run

From the project root:

```bash
python3 src/main.py
```

This runs FIFO, LRU, Optimal, and the learned policy and generates:

```text
results/results.csv
```

Generate the main figure:

```bash
python3 src/plot_results.py
```

Run the bonus experiment:

```bash
python3 src/run_bonus.py
```

Analyze bonus confidence:

```bash
python3 src/analyze_bonus.py
```

Save the bonus summary:

```bash
python3 src/save_bonus_summary.py
```

## 7. Requirements

* Python 3
* scikit-learn
* NumPy
* Matplotlib

The classical algorithms use standard Python functionality.

## 8. AI Assistance Disclosure

AI assistance was used during development for:

* explaining operating-system concepts
* debugging code
* suggesting implementation structure
* reviewing experimental logic
* helping prepare project documentation

The workload design, experimental configuration, execution of experiments, recorded results, and interpretation of the results were reviewed and verified by the student.
