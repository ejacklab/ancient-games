def total(prices):
    """Sum of prices in cents."""
    out = 0
    for p in prices:
        out += p
    return out
