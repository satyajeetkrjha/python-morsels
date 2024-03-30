

def all_same(sequence):
    first_item = next(iter(sequence),None)
    return all(first_item == item for item in sequence)



