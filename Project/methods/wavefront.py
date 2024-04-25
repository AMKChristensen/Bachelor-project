import numpy as np
from methods.misc import sgn_change

def get_sign_change_indices(data_full, data_key="ne", offset=0):
    """
    Gets indices where the sign changes in the specified data.
    data_full: Full dataset from a SolutionClass
    data_key: What single set of data to use from the full set
    offset: Offset of all values in the dataset
    """

    changes = []
    for ti, spacial in enumerate(data_full[data_key]):
        changes.append({
            "negatives" : np.where(sgn_change(spacial-offset) == -1)[0],
            "positives" : np.where(sgn_change(spacial-offset) ==  1)[0],
        })
    
    return changes

def get_wavefront_datapoint(data_full, data_key="ne", offset=0, direction="right", change="both", interpolate=True):
    """
    Gets the datapoint on the front of a wavefront by getting points around the zeros of the offset data
    data_full:   SolutionClass.data_full
    data_key:    The specific vector of data to use
    offset:      The vertical position where the fronts are measured
    direction:   Taking the rightmost or leftmost point
    change:      Only looks at the specified slope direction
    interpolate: Whether to interpolate the data. If False the datapoint right after the crossing of 'offset' will be returned.
    """

    # TODO: make a more sophisticated inverse lerp scheme to determine exact x-point

    changes = get_sign_change_indices(data_full, data_key=data_key, offset=offset)

    # We take the positive changes and turn them into datapoints
    data_t = []
    data_y = []
    for ti, c in enumerate(changes):
        if   change == "both":
            sign_changes = np.concatenate((c["positives"], c["negatives"]))
        elif change == "negative":
            sign_changes = c["negatives"]
        elif change == "positive":
            sign_changes = c["positives"]
        else:
            raise ValueError(f"change should be either 'both', 'negative' or 'positive'. Was '{change}'")
        
        # If no points fit the description we append nan and continue to next iteration
        if len(sign_changes) == 0:
            data_t.append(np.nan)
            data_y.append(np.nan)
            continue
        
        # Returns the rightmost or leftmost datapoint
        if   direction == "right":
            yi = np.max(sign_changes) # Rightmost
        elif direction == "left":
            yi = np.min(sign_changes) # Leftmost
        else:
            raise ValueError(f"direction should be either 'right' or 'left'. Was '{direction}'")

        # Linear interpolation of points crossing offset, since points will never perfectly align with the probe height
        if interpolate:
            a = (data_full[data_key][ti,yi] - data_full[data_key][ti,yi-1]) / (data_full["x"][yi] - data_full["x"][yi-1])
            b = data_full[data_key][ti,yi-1] - a * data_full["x"][yi-1]
            x_lerp = (offset - b)/a
            data_y.append(x_lerp)

        else:
            data_y.append(data_full["x"][yi])


        data_t.append(data_full["t"][ti])
        
    return (data_t, data_y)