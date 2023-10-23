def term_transformer(term):
    if term > 12:
        return "Long Term"
    else:
        return "Short Term"


def years_in_current_job_transformer(years):
    if years < 1:
        return "less than 1 year"
    if years >= 10:
        return "10 years or more"
    else:
        return f"{years} years"
