from sklearn.tree import DecisionTreeClassifier


def get_optimal_candidate(reference_string, current_index, frames):
    future = reference_string[current_index + 1:]

    farthest = -1
    candidate = None

    for page in frames:

        if page not in future:
            return page

        next_use = future.index(page)

        if next_use > farthest:
            farthest = next_use
            candidate = page

    return candidate


def get_features(reference_string, current_index, page, last_access):
    # Recency: how many steps since this page was last accessed
    if page in last_access:
        recency = current_index - last_access[page]
    else:
        recency = current_index + 1

    # Frequency in the recent access window
    window_start = max(0, current_index - 20)
    recent_window = reference_string[window_start:current_index]
    recent_frequency = recent_window.count(page)

    return [recency, recent_frequency]


def simulate_learned(reference_string, frame_count):
    frames = []
    last_access = {}

    # Training data
    training_features = []
    training_labels = []

    model = None

    results = []

    # Counters for checking whether the model is actually being used
    model_decisions = 0
    fallback_decisions = 0

    for i, page in enumerate(reference_string):

        # -------------------------
        # Page hit
        # -------------------------
        if page in frames:
            results.append(True)
            last_access[page] = i
            continue

        # -------------------------
        # Page fault
        # -------------------------
        results.append(False)

        # Empty frame available
        if len(frames) < frame_count:
            frames.append(page)
            last_access[page] = i
            continue

        # -------------------------
        # Choose eviction candidate
        # -------------------------
        candidate = None

        if model is not None and len(model.classes_) >= 2:

            model_decisions += 1

            candidate_scores = []

            for frame_page in frames:

                features = get_features(
                    reference_string,
                    i,
                    frame_page,
                    last_access
                )

                probability = model.predict_proba([features])[0]

                # Probability that this page is the
                # page Optimal would evict.
                if 1 in model.classes_:
                    score = probability[
                        list(model.classes_).index(1)
                    ]
                else:
                    score = 0

                candidate_scores.append(
                    (score, frame_page)
                )

            candidate = max(
                candidate_scores,
                key=lambda x: x[0]
            )[1]

        # -------------------------
        # Fallback before model
        # has enough training data
        # -------------------------
        if candidate is None:

            fallback_decisions += 1

            oldest_page = None
            oldest_time = -1

            for frame_page in frames:

                if frame_page in last_access:
                    age = i - last_access[frame_page]
                else:
                    age = i + 1

                if age > oldest_time:
                    oldest_time = age
                    oldest_page = frame_page

            candidate = oldest_page

        # -------------------------
        # Learn from this eviction
        # -------------------------
        optimal_candidate = get_optimal_candidate(
            reference_string,
            i,
            frames
        )

        for frame_page in frames:

            features = get_features(
                reference_string,
                i,
                frame_page,
                last_access
            )

            if frame_page == optimal_candidate:
                label = 1
            else:
                label = 0

            training_features.append(features)
            training_labels.append(label)

        # -------------------------
        # Train/retrain model
        # -------------------------
        if len(training_features) >= 12:

            # Keep only recent training examples.
            # This allows the model to adapt when
            # the workload pattern changes.
            recent_features = training_features[-60:]
            recent_labels = training_labels[-60:]

            model = DecisionTreeClassifier(
                max_depth=3,
                random_state=42,
                class_weight="balanced"
            )

            model.fit(
                recent_features,
                recent_labels
            )

        # -------------------------
        # Replace selected page
        # -------------------------
        frames[frames.index(candidate)] = page
        last_access[page] = i

    return results, model_decisions, fallback_decisions
