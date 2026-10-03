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

    # High-confidence decisions
    high_confidence = [
        row for row in rows
        if row["confidence"] >= 0.8
    ]

    high_correct = sum(
        row["correct"]
        for row in high_confidence
    )

    # Low-confidence decisions
    low_confidence = [
        row for row in rows
        if row["confidence"] < 0.8
    ]

    low_correct = sum(
        row["correct"]
        for row in low_confidence
    )

    print("Bonus Confidence Analysis")
    print("-------------------------")
    print("Total decisions:", total)
    print("Overall accuracy:", correct / total)
    print()

    print("High-confidence decisions (>= 0.8)")
    print("Count:", len(high_confidence))

    if high_confidence:
        print(
            "Accuracy:",
            high_correct / len(high_confidence)
        )

    print()

    print("Lower-confidence decisions (< 0.8)")
    print("Count:", len(low_confidence))

    if low_confidence:
        print(
            "Accuracy:",
            low_correct / len(low_confidence)
        )


if __name__ == "__main__":
    main()
