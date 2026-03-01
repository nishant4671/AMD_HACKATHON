def calculate_level(xp: int) -> int:
    return min(20, max(1, int(xp / 50) + 1))


def get_badge(xp: int) -> str:
    if xp >= 800:
        return "🏆 Platinum"
    if xp >= 500:
        return "🥈 Gold"
    if xp >= 250:
        return "🥉 Silver"
    return "⬜ Bronze"
