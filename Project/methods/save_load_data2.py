import numpy as np
import pandas as pd
import json
from methods.SolutionClass2 import SolutionClass
from methods.misc import *


def save_data(sol: SolutionClass, filename: str="_savedata"):
    """
    Saves the data from a SolutionClass to the specified file as JSON
    """
    
    # Saves to file
    with open(filename + r".json", "w") as file:
        meta = {"data_full": sol.data_full, "params": sol.params, "constants": sol.constants}

        # Changes the array type throughout the dictionary to lists instead of ndarrays
        dict_ndarr_to_list(meta)

        json.dump(meta, file)


def load_data(filename: str="_savedata"):
    """
    Loads data into a SolutionClass from a file
    """

    sol = SolutionClass()

    with open(filename + r".json", "r") as file:
        load = json.load(file)

        sol.data_full = load["data_full"]
        dict_list_to_ndarr(sol.data_full) # Transforms into ndarrays for more convenience
        sol.data      = full_to_final_solution(sol.data_full)
        sol.params    = load["params"]
        sol.constants = load["constants"]

        # Changes the array type throughout the dictionary to ndarrays instead of lists

        del load  # probably not necessary, but who cares.

    return sol


def full_to_final_solution(full_sol):
    """
    Transforms a dataset for every time into a dataset for only the final time.
    """

    # For old system without temperature fields
    try:
        Te = full_sol["te"]
        Ti = full_sol["ti"]
    except:
        print("Error: No temperature fields found. Setting to zero")
        Te = Ti = np.zeros(full_sol["x"].shape)

    last_idx = full_sol["last_idx"]
    return {
        # metadata
        "label"    : full_sol["label"],
        "last_idx" : last_idx,
        "nsteps"   : full_sol["nsteps"][last_idx],
        "nfailed"  : full_sol["nfailed"][last_idx],
        "duration" : full_sol["duration"][last_idx],

        # Time and space
        "t"       : full_sol["t"][last_idx],
        "x"       : full_sol["x"],

        # Electrons
        "ne"      : full_sol["ne"][last_idx],
        "ue"      : full_sol["ue"][last_idx],
        "Te"      : full_sol["Te"][last_idx],
        "norm_ne" : full_sol["norm_ne"][last_idx],
        "norm_ue" : full_sol["norm_ue"][last_idx],
        "norm_Te" : full_sol["norm_Te"][last_idx],

        # Ions
        "ni"      : full_sol["ni"][last_idx],
        "ui"      : full_sol["ui"][last_idx],
        "Ti"      : full_sol["Ti"][last_idx],
        "norm_ni" : full_sol["norm_ni"][last_idx],
        "norm_ui" : full_sol["norm_ui"][last_idx],
        "norm_Ti" : full_sol["norm_Ti"][last_idx],

        # System
        "charge"    : full_sol["charge"][last_idx],
        "potential" : full_sol["potential"][last_idx],
        "electric"  : full_sol["electric"][last_idx],

        #"m"      : total_mass,
        #"p"      : total_momentum,
        #"E"      : total_energy,
    }