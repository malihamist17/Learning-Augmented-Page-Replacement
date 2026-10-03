def simulate_fifo(reference_string, frame_count):
    frames = []
    next_to_replace = 0

    results = []

    for page in reference_string:

        if page in frames:
            results.append(True)   # Hit

        else:
            results.append(False)  # Page fault

            if len(frames) < frame_count:
                frames.append(page)

            else:
                frames[next_to_replace] = page
                next_to_replace = (next_to_replace + 1) % frame_count

    return results


def simulate_lru(reference_string, frame_count):
    frames = []

    results = []

    for page in reference_string:

        if page in frames:
            results.append(True)   # Hit

            # Move recently used page to the end
            frames.remove(page)
            frames.append(page)

        else:
            results.append(False)  # Page fault

            if len(frames) < frame_count:
                frames.append(page)

            else:
                # Remove least recently used page
                frames.pop(0)
                frames.append(page)

    return results

def simulate_optimal(reference_string, frame_count):
    frames = []

    results = []

    for i in range(len(reference_string)):
        page = reference_string[i]

        if page in frames:
            results.append(True)   # Hit

        else:
            results.append(False)  # Page fault

            if len(frames) < frame_count:
                frames.append(page)

            else:
                future = reference_string[i + 1:]

                farthest = -1
                page_to_replace = None

                for frame_page in frames:

                    if frame_page not in future:
                        page_to_replace = frame_page
                        break

                    next_use = future.index(frame_page)

                    if next_use > farthest:
                        farthest = next_use
                        page_to_replace = frame_page

                frames[frames.index(page_to_replace)] = page

    return results

def summarize_results(results, shift_point):
    phase1 = results[:shift_point]
    phase2 = results[shift_point:]

    phase1_hits = sum(phase1)
    phase1_faults = len(phase1) - phase1_hits

    phase2_hits = sum(phase2)
    phase2_faults = len(phase2) - phase2_hits

    total_hits = sum(results)
    total_faults = len(results) - total_hits

    return {
        "phase1_faults": phase1_faults,
        "phase1_hits": phase1_hits,
        "phase1_hit_ratio": phase1_hits / len(phase1),

        "phase2_faults": phase2_faults,
        "phase2_hits": phase2_hits,
        "phase2_hit_ratio": phase2_hits / len(phase2),

        "total_faults": total_faults,
        "total_hits": total_hits,
        "total_hit_ratio": total_hits / len(results)
    }
