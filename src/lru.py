def lru_page_replacement(reference_string, frame_count):
    frames = []
    page_faults = 0
    hits = 0

    for page in reference_string:

        if page in frames:
            hits += 1

            # Move the recently used page to the end
            frames.remove(page)
            frames.append(page)

        else:
            page_faults += 1

            if len(frames) < frame_count:
                frames.append(page)

            else:
                # Remove the least recently used page
                frames.pop(0)
                frames.append(page)

    total_references = len(reference_string)
    hit_ratio = hits / total_references

    return page_faults, hits, hit_ratio
