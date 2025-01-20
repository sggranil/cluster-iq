def chart_count_formatter(labels, counts):
    result = []

    for label, count in zip(labels, counts):
        result.append({
            "label": label,
            "count": count
        })

    return result
