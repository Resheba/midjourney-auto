

def is_intable(val: str) -> int | None:
    try:
        val = int(val)
    except:
        val = None
    return val
