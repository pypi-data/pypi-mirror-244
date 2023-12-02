import fortune  # type: ignore


def get_fortune() -> str:
    """Get random fortune"""
    return fortune.fortune()
