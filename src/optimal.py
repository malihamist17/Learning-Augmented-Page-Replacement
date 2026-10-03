def optimal_page_replacement(reference_string, frame_count):
    frames = []
    page_faults = 0
    hits = 0

    for i in range(len(reference_string)):
        page = reference_string[i]

        if page in frames:
            hits += 1

        else:
            page_faults += 1

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

    total_references = len(reference_string)
    hit_ratio = hits / total_references

    return page_faults, hits, hit_ratio
