from typing import List

def flatten_list(original_list: List[List]) -> List:
    """
    Flatten a list of lists by extracting the first element from each sublist.

    Args:
        original_list (List[List]): The original list of lists.

    Returns:
        List: The flattened list containing the first element from each sublist.
    """
    flat_list = []
    for element in original_list:
        flat_list.append(element[0])

    return flat_list
