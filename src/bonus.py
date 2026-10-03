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

    if page in last_access:
        recency = current_index - last_access[page]
    else:
        recency = current_index + 1

    window_start = max(0, current_index - 20)
    recent_window = reference_string[window_start:current_index]

    recent_frequency = recent_window.count(page)

    return [recency, recent_frequency]


def run_bonus_experiment(reference_string, frame_count):

    frames = []
    last_access = {}

    training_features = []
    training_labels = []

    model = None

    decisions = []

    for i, page in enumerate(reference_string):

        # Page hit
        if page in frames:
            last_access[page] = i
            continue

        # Empty frame
        if len(frames) < frame_count:
            frames.append(page)
            last_access[page] = i
            continue

        # Find the actual Optimal decision
        optimal_candidate = get_optimal_candidate(
            reference_string,
            i,
            frames
        )

        candidate = None
        confidence = 0.0

        # Use learned model
        if model is not None and len(model.classes_) >= 2:

            candidate_scores = []

            for frame_page in frames:

                features = get_features(
                    reference_string,
                    i,
                    frame_page,
                    last_access
                )

                probabilities = model.predict_proba([features])[0]

                if 1 in model.classes_:
                    score = probabilities[
                        list(model.classes_).index(1)
                    ]
                else:
                    score = 0.0

                candidate_scores.append(
                    (score, frame_page)
                )

            confidence, candidate = max(
                candidate_scores,
                key=lambda x: x[0]
            )

        # Fallback: LRU
        if candidate is None:

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

            confidence = 0.0

        # Check correctness
        correct = candidate == optimal_candidate

        # Generate explanation
        if correct:
            explanation = (
                "The learned model selected the same "
                "eviction candidate as Optimal."
            )
        else:
            explanation = (
                "The learned model selected a different "
                "candidate from Optimal."
            )

        decisions.append({
            "step": i,
            "requested_page": page,
            "evicted_page": candidate,
            "optimal_page": optimal_candidate,
            "confidence": confidence,
            "correct": correct,
            "explanation": explanation
        })

        # Learn from the current eviction
        for frame_page in frames:

            features = get_features(
                reference_string,
                i,
                frame_page,
                last_access
            )

            label = (
                1 if frame_page == optimal_candidate
                else 0
            )

            training_features.append(features)
            training_labels.append(label)

        # Retrain using recent examples
        if len(training_features) >= 12:

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

        # Perform the selected eviction
        frames[frames.index(candidate)] = page
        last_access[page] = i

    return decisions
