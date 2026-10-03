import csv


def main():

    rows = []

    with open("results/bonus_decisions.csv", "r") as file:

        reader = csv.DictReader(file)

        for row in reader:
            rows.append({
                "confidence": float(row["Confidence"]),
                "correct": row["Correct"] == "True"
            })

    total = len(rows)
    correct = sum(row["correct"] for row in rows)

    high = [
        row for row in rows
        if row["confidence"] >= 0.8
    ]

    low = [
        row for row in rows
        if row["confidence"] < 0.8
    ]

    high_correct = sum(row["correct"] for row in high)
    low_correct = sum(row["correct"] for row in low)

    with open(
        "results/bonus_summary.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Group",
            "Decision_Count",
            "Correct_Count",
            "Accuracy"
        ])

        writer.writerow([
            "Overall",
            total,
            correct,
            correct / total
        ])

        writer.writerow([
            "High_Confidence",
            len(high),
            high_correct,
            high_correct / len(high)
        ])

        writer.writerow([
            "Lower_Confidence",
            len(low),
            low_correct,
            low_correct / len(low)
        ])

    print("Bonus summary saved to: results/bonus_summary.csv")


if __name__ == "__main__":
    main()
