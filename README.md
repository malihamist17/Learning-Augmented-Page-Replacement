# CSE-307 Track 1 — Learning-Augmented Page Replacement

## Project Title

**Learning-Augmented OS Heuristics: Classical Algorithms Meet Adaptive Prediction**

This project implements classical page replacement algorithms and compares them with a lightweight learned page replacement policy under a deliberate workload shift.

## 1. Problem Statement

Operating systems use page replacement algorithms to decide which page should be removed from memory when a page fault occurs and all available frames are occupied.

Classical policies such as FIFO and LRU use fixed rules. The Optimal (Belady's) algorithm provides a theoretical benchmark because it uses knowledge of future page references.

This project investigates whether a lightweight learned predictor can adapt when the workload changes from a locality-heavy pattern to a random pattern.

### Research Question

> How does a workload shift from locality-heavy access to random access affect classical page replacement policies, and can a lightweight learned predictor adapt to the change?

---

## 2. Algorithms Implemented

### FIFO

First-In, First-Out replaces the page that has been in memory for the longest time.

### LRU

Least Recently Used replaces the page that has not been accessed for the longest time.

### Optimal

Optimal page replacement replaces the page whose next future use is farthest away. If a page will never be used again, it is selected first.

Optimal is used as a theoretical benchmark because it requires future knowledge.

### Learned Policy

The learned policy uses a Decision Tree classifier.

The model uses two features for each page currently in memory:

- **Recency:** number of references since the page was last accessed.
- **Recent frequency:** number of times the page appeared in the previous 20 references.

The model predicts which candidate page should be evicted.

The learned component is retrained using a recent window of training examples so that it can adapt when the workload changes.

---

## 3. Workload Design

A synthetic reference string containing **2,000 page references** was generated.

The workload contains two phases:

### Phase 1 — Locality-heavy

- 1,000 references
- Pages are selected from pages 1–5
- This creates strong locality because the same small set of pages is accessed repeatedly.

### Phase 2 — Random

- 1,000 references
- Pages are selected from pages 1–20
- This creates a much broader and more random access pattern.

The random generator uses a fixed seed (`42`) so that the experiment is reproducible.

The system uses **3 page frames** for all policies.

The same reference string and frame count are used for every policy.

---

## 4. Learned Training Method

The learned policy is trained online while the reference string is being processed.

When a page fault occurs and the frames are full, the Optimal algorithm is used as a teacher to identify which current page should be evicted.

This teacher decision is used as the training label for the model.

The learned policy makes its eviction decision **before** adding the new teacher label to its training data. Therefore, the model does not use the current Optimal answer to make the same decision.

The model keeps only recent training examples. This helps it adjust when the workload changes from locality-heavy access to random access.

---

## 5. Experimental Results

### Page Replacement Results

| Policy | Phase 1 Faults | Phase 1 Hit Ratio | Phase 2 Faults | Phase 2 Hit Ratio | Total Faults | Total Hit Ratio |
|---|---:|---:|---:|---:|---:|---:|
| FIFO | 385 | 61.5% | 844 | 15.6% | 1229 | 38.55% |
| LRU | 378 | 62.2% | 849 | 15.1% | 1227 | 38.65% |
| Optimal | 221 | 77.9% | 646 | 35.4% | 867 | 56.65% |
| Learned | 400 | 60.0% | 830 | 17.0% | 1230 | 38.50% |

The detailed raw results are stored in:

`results/results.csv`

The figure showing the change in hit ratio is stored in:

`results/hit_ratio_shift.png`

---
## 6. Analysis

All four policies had lower hit ratios after the workload changed from locality-heavy access to random access.

FIFO decreased from 61.5% to 15.6%, which is a drop of 45.9 percentage points.

LRU decreased from 62.2% to 15.1%, which is the largest drop of 47.1 percentage points. LRU depends on recent page usage. When the access pattern becomes random, recent usage is less useful for predicting which page will be needed next.

Optimal decreased from 77.9% to 35.4%. It still performed much better because it knows the future page references and can choose the page that will be needed farthest in the future.

The learned policy decreased from 60.0% to 17.0%. However, the version using recent training examples performed better than the earlier version.

Compared with the earlier version, the recent-training-window approach reduced total faults from 1260 to 1230 and increased the Phase 2 hit ratio from 14.8% to 17.0%.

This shows that recent training data can help the learned policy adjust to a workload change. However, in this experiment, it was still far from the performance of the Optimal policy.

---

## 7. Bonus: Decision Explanation and Confidence

The optional bonus part generates a short explanation for each learned eviction decision.

For each decision, we record:

* requested page
* selected eviction page
* Optimal eviction page
* model-reported prediction probability
* whether the learned decision matched Optimal
* short explanation of the decision

The detailed results are stored in:

`results/bonus_decisions.csv`

The summary is stored in:

`results/bonus_summary.csv`

### Bonus Results

| Group                    | Decisions | Correct | Accuracy |
| ------------------------ | --------: | ------: | -------: |
| Overall                  |      1227 |     448 |   36.51% |
| High confidence (≥ 0.8)  |       271 |     100 |   36.90% |
| Lower confidence (< 0.8) |       956 |     348 |   36.40% |

The accuracy difference between the two confidence groups is small.

This means that, in this experiment, the model-reported prediction probability had only a weak relationship with whether the decision was actually correct.

The confidence value is the probability reported by the Decision Tree. It is not a calibrated probability that the decision itself is correct.

## 8. Repository Structure

```
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
```

---

## 9. How to Run

From the project root:

```bash
python3 src/main.py
```

This runs FIFO, LRU, Optimal, and the learned policy and creates:

```text
results/results.csv
```

To generate the main figure:

```bash
python3 src/plot_results.py
```

To run the bonus experiment:

```bash
python3 src/run_bonus.py
```

To analyze bonus confidence:

```bash
python3 src/analyze_bonus.py
```

To save the bonus summary:

```bash
python3 src/save_bonus_summary.py
```

---

## 10. Requirements

The project uses Python 3 and the following libraries:

* scikit-learn
* NumPy
* Matplotlib

The classical page replacement algorithms use standard Python functionality.

---

## 11. Reproducibility

The workload generator uses:

```python
random.seed(42)
```

Therefore, the same reference string can be regenerated.

All policies use the same:

* reference string
* workload shift point
* number of frames

This makes the comparison consistent.


## 12. AI Assistance Disclosure

AI assistance was used during development for:

* explaining operating-system concepts
* debugging code
* suggesting implementation structure
* reviewing experimental logic

The workload design, experimental configuration, execution of experiments, recorded results, and interpretation of the results were reviewed and verified by the student.

## 13. Conclusion

This project demonstrates how classical page replacement policies behave when the workload changes significantly.

The experiment shows a substantial performance drop after the workload shifts from a locality-heavy pattern to a random pattern.

The learned policy uses recent access behavior and a Decision Tree to make eviction predictions. Using a recent training window provided some adaptation to the workload change, although the learned policy remained far from the theoretical Optimal benchmark.

The experiment illustrates the potential and limitations of lightweight learning-augmented heuristics in operating-system resource management.
