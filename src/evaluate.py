def evaluate_policy(policy_function, reference_string, shift_point, frame_count):
    phase1 = reference_string[:shift_point]
    phase2 = reference_string[shift_point:]

    # Run the complete trace once.
    total_faults, total_hits, total_ratio = policy_function(
        reference_string, frame_count
    )

    # Run each phase separately only to measure phase-specific behavior.
    phase1_faults, phase1_hits, phase1_ratio = policy_function(
        phase1, frame_count
    )

    phase2_faults, phase2_hits, phase2_ratio = policy_function(
        phase2, frame_count
    )

    return {
        "phase1_faults": phase1_faults,
        "phase1_hits": phase1_hits,
        "phase1_hit_ratio": phase1_ratio,

        "phase2_faults": phase2_faults,
        "phase2_hits": phase2_hits,
        "phase2_hit_ratio": phase2_ratio,

        "total_faults": total_faults,
        "total_hits": total_hits,
        "total_hit_ratio": total_ratio
    }















