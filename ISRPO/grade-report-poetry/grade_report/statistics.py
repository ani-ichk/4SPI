def calculate(students):
    scores = [s["score"] for s in students]

    # собираем баллы по группам
    groups = {}
    for s in students:
        groups.setdefault(s["group"], []).append(s["score"])

    return {
        "count": len(scores),
        "average": round(sum(scores) / len(scores), 2),
        "min": min(scores),
        "max": max(scores),
        "groups": {g: round(sum(v) / len(v), 2) for g, v in groups.items()},
    }