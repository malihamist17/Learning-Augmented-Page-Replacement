def fifo_page_replacement(reference_string, frame_count):
    frames = []
    page_faults = 0
    hits = 0
    next_to_replace = 0

    for page in reference_string:

        if page in frames:
            hits += 1

        else:
            page_faults += 1

            if len(frames) < frame_count:
                frames.append(page)

            else:
                frames[next_to_replace] = page
                next_to_replace = (next_to_replace + 1) % frame_count

    total_references = len(reference_string)
    hit_ratio = hits / total_references

    return page_faults, hits, hit_ratio
