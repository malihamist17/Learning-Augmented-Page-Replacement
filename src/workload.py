import random


def generate_workload(total_references=2000, page_count=20):
    random.seed(42)

    shift_point = total_references // 2

    phase1 = []
    phase2 = []

    # Phase 1: locality-heavy workload
    for _ in range(shift_point):
        page = random.randint(1, 5)
        phase1.append(page)

    # Phase 2: random workload
    for _ in range(total_references - shift_point):
        page = random.randint(1, page_count)
        phase2.append(page)

    reference_string = phase1 + phase2

    return reference_string, shift_point
