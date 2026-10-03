import csv

from workload import generate_workload
from fifo import fifo_page_replacement
from lru import lru_page_replacement
from optimal import optimal_page_replacement
from simulation import (
    simulate_fifo,
    simulate_lru,
    simulate_optimal,
    summarize_results
)
from learned import simulate_learned


def main():

    # -------------------------
    # Experiment settings
    # -------------------------
    frame_count = 3

    reference_string, shift_point = generate_workload()

    # -------------------------
    # Run classical policies
    # -------------------------
    fifo_results = summarize_results(
        simulate_fifo(reference_string, frame_count),
        shift_point
    )

    lru_results = summarize_results(
        simulate_lru(reference_string, frame_count),
        shift_point
    )

    optimal_results = summarize_results(
        simulate_optimal(reference_string, frame_count),
        shift_point
    )

    # -------------------------
    # Run learned policy
    # -------------------------
    learned_history, model_decisions, fallback_decisions = (
        simulate_learned(reference_string, frame_count)
    )

    learned_results = summarize_results(
        learned_history,
        shift_point
    )

    # -------------------------
    # Store results
    # -------------------------
    policies = [
        ("FIFO", fifo_results),
        ("LRU", lru_results),
        ("Optimal", optimal_results),
        ("Learned", learned_results)
    ]

    output_file = "results/results.csv"

    with open(output_file, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Policy",
            "Phase1_Faults",
            "Phase1_Hits",
            "Phase1_Hit_Ratio",
            "Phase2_Faults",
            "Phase2_Hits",
            "Phase2_Hit_Ratio",
            "Total_Faults",
            "Total_Hits",
            "Total_Hit_Ratio"
        ])

        for policy, result in policies:

            writer.writerow([
                policy,
                result["phase1_faults"],
                result["phase1_hits"],
                result["phase1_hit_ratio"],
                result["phase2_faults"],
                result["phase2_hits"],
                result["phase2_hit_ratio"],
                result["total_faults"],
                result["total_hits"],
                result["total_hit_ratio"]
            ])

    # -------------------------
    # Print results
    # -------------------------
    print("CSE-307 Track 1 Experiment")
    print("--------------------------")
    print("References:", len(reference_string))
    print("Shift point:", shift_point)
    print("Frame count:", frame_count)
    print()

    for policy, result in policies:

        print(policy)
        print("  Phase 1 faults:", result["phase1_faults"])
        print("  Phase 1 hit ratio:", result["phase1_hit_ratio"])
        print("  Phase 2 faults:", result["phase2_faults"])
        print("  Phase 2 hit ratio:", result["phase2_hit_ratio"])
        print("  Total faults:", result["total_faults"])
        print("  Total hit ratio:", result["total_hit_ratio"])
        print()

    print("Learned model decisions:", model_decisions)
    print("Learned fallback decisions:", fallback_decisions)
    print()
    print("Results saved to:", output_file)


if __name__ == "__main__":
    main()
