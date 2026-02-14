def rank_candidates(matches):

    ranked = sorted(
        matches,
        key=lambda x: x.score,
        reverse=True
    )

    return ranked
