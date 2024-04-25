import numpy as np

def dict_list_to_ndarr(input: dict):
    """
    Changes the array type throughout the dictionary to ndarrays instead of lists
    Does not need to return anything since the input dict is modified directly, as mutable types are passed by reference.
    """

    # If input is dict: loops through entries
    for sub_input, sub_key in zip(input.values(), input.keys()):

        # If entry is dict: Recursively goes through nested dicts
        if isinstance(sub_input, dict):
            dict_list_to_ndarr(sub_input)
        
        # If entry is dict: changes numpy array to list
        if isinstance(sub_input, list):
            input[sub_key] = np.array(sub_input)


def dict_ndarr_to_list(input: dict):
    """
    Changes the array type throughout the dictionary to lists instead of ndarrays
    Does not need to return anything since the input dict is modified directly, as mutable types are passed by reference.
    """

    # If input is dict: loops through entries
    for sub_input, sub_key in zip(input.values(), input.keys()):

        # If entry is dict: Recursively goes through nested dicts
        if isinstance(sub_input, dict):
            dict_ndarr_to_list(sub_input)
        
        # If entry is dict: changes numpy array to list
        if isinstance(sub_input, np.ndarray):
            input[sub_key] = sub_input.tolist()


def sgn_change(arr, looping=False):
    """
    Returns an array with the following values
    0: No change in sign from last value
    1: Sign changed to positive from negative
    -1: Sign changes to negative from positive

    Optional kwargs:
    looping: 
        True:  Records sign change from last to first index
        False: First index always 0 since there is no index before first to compare to
    """
    sign_arr = np.sign(arr)
    sign_change_arr = ((sign_arr - np.roll(sign_arr, 1))/2).astype(int)
    if not looping: 
        sign_change_arr[0] = 0
    return sign_change_arr