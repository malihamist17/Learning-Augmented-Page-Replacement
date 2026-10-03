import csv
import matplotlib.pyplot as plt


def main():

    policies = []
    phase1_ratios = []
    phase2_ratios = []

    with open("results/results.csv", "r") as file:

        reader = csv.DictReader(file)

        for row in reader:

            policies.append(row["Policy"])

            phase1_ratios.append(
                float(row["Phase1_Hit_Ratio"]) * 100
            )

            phase2_ratios.append(
                float(row["Phase2_Hit_Ratio"]) * 100
            )

    x = range(len(policies))

    width = 0.35

    plt.figure(figsize=(8, 5))

    plt.bar(
        [i - width / 2 for i in x],
        phase1_ratios,
        width,
        label="Phase 1: Locality-heavy"
    )

    plt.bar(
        [i + width / 2 for i in x],
        phase2_ratios,
        width,
        label="Phase 2: Random"
    )

    plt.xlabel("Page Replacement Policy")
    plt.ylabel("Hit Ratio (%)")
    plt.title("Hit Ratio Before and After Workload Shift")

    plt.xticks(list(x), policies)

    plt.ylim(0, 100)

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "results/hit_ratio_shift.png",
        dpi=300
    )

    print("Chart saved to: results/hit_ratio_shift.png")


if __name__ == "__main__":
    main()
