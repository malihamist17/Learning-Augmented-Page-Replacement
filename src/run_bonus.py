import csv

from workload import generate_workload
from bonus import run_bonus_experiment


def main():

    frame_count = 3

    reference_string, shift_point = generate_workload()

    decisions = run_bonus_experiment(
        reference_string,
        frame_count
    )

    output_file = "results/bonus_decisions.csv"

    with open(output_file, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Step",
            "Requested_Page",
            "Evicted_Page",
            "Optimal_Page",
            "Confidence",
            "Correct",
            "Explanation"
        ])

        for decision in decisions:

            writer.writerow([
                decision["step"],
                decision["requested_page"],
                decision["evicted_page"],
                decision["optimal_page"],
                decision["confidence"],
                decision["correct"],
                decision["explanation"]
            ])

    # Summary
    total = len(decisions)

    correct = sum(
        decision["correct"]
        for decision in decisions
    )

    incorrect = total - correct

    accuracy = correct / total

    print("CSE-307 Track 1 Bonus Experiment")
    print("--------------------------------")
    print("Total learned decisions:", total)
    print("Correct decisions:", correct)
    print("Incorrect decisions:", incorrect)
    print("Decision accuracy:", accuracy)
    print()
    print("Results saved to:", output_file)


if __name__ == "__main__":
    main()
