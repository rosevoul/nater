from numpy import mean
ROUND_FLOAT = 3


def compute_PrecisionRecallF1(ground_truth, ranked_recommendations):
    if not isinstance(ground_truth, list):
        ground_truth = [ground_truth]
    relevant_items_retrieved = list(
        set(ground_truth) & set(ranked_recommendations))
    precision = len(relevant_items_retrieved) / len(ranked_recommendations)
    recall = len(relevant_items_retrieved) / len(ground_truth)
    if not precision and not recall:
        return (0.0, 0.0, 0.0)
    f1 = 2 * ((precision * recall) / (precision + recall))

    return (round(precision, ROUND_FLOAT), round(recall, ROUND_FLOAT), round(f1, ROUND_FLOAT))


def computeReciprocalRank(single_ground_truth, ranked_recommendations):
    try:
        rr = 1.0 / (ranked_recommendations.index(single_ground_truth) + 1)
        return round(rr, ROUND_FLOAT)

    except ValueError:
        return 0.0


def computeMeanReciprocalRank(single_ground_truth_list, ranked_recommendations_lists):
    rr = []
    for i, single_ground_truth in enumerate(single_ground_truth_list):
        rr.append(computeReciprocalRank(
            single_ground_truth, ranked_recommendations_lists[i]))

    return round(mean(rr), ROUND_FLOAT)


def computeAveragePrecision(ground_truth, ranked_recommendations):

    if not isinstance(ground_truth, list):
        ground_truth = [ground_truth]
    i = 1
    hits = 0
    p_at_k = [0.0] * len(ranked_recommendations)
    for item in ranked_recommendations:
        try:
            hit = ground_truth.index(item) + 1
            hits += 1
            p = hits / float(i)
            p_at_k[i - 1] = hits / float(i)
        except:
            pass
        i += 1

    try:
        return round(sum(p_at_k) / hits, ROUND_FLOAT)

    except ZeroDivisionError:
        return 0.0


def computeMeanAveragePrecision(ground_truth_list, ranked_recommendations_list):
    ap = []
    for i, ground_truth in enumerate(ground_truth_list):
        ap.append(computeAveragePrecision(
            ground_truth, ranked_recommendations_list[i]))

    return round(mean(ap), ROUND_FLOAT)
