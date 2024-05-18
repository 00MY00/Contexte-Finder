
def Find_Partial_Match(value, lst):
    for item in lst:
        if value in item:
            return item
    return None


