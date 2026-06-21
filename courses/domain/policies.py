def next_order(current_maximum: int | None) -> int:
    return (current_maximum or 0) + 1


def current_course_rule(rules, *, date):
    active_rules = [
        rule
        for rule in rules
        if rule.data_inicio <= date and (rule.data_fim is None or rule.data_fim >= date)
    ]

    if not active_rules:
        return None

    return max(active_rules, key=lambda rule: rule.data_inicio)
