import numpy as np
import pandas as pd
import json
from Project.methods.old.SolutionClass import SolutionClass

def save_data(sol: SolutionClass, filename: str="_savedata", ret=False):
    """
    Saves the data from a set of solutions into a file
    """

    # Prepares combined dataset
    dataframe = pd.DataFrame(sol.data_list_full[0].keys(), columns=["key"]).set_index("key")

    # Joins every solution into dataframe
    for i, (single_method_dataset, single_method_params) in enumerate(zip(sol.data_list_full, sol.param_list)):
        single_dataset = pd.DataFrame(single_method_dataset.items(), columns=["key", f"data{i}"]).set_index("key")
        dataframe = dataframe.join(single_dataset)

    # Saves to file
    with open(filename + r"/data.json", "w") as file:
        dataframe.to_json(file, double_precision=15)
    
    with open(filename + r"/params.json", "w") as file:
        json.dump(sol.param_list, file)

    if ret:
        return dataframe


def load_data(filename: str="_savedata"):
    """
    Loads data into a solution
    """

    with open(filename + r"/data.json", "r") as file:
        dataframe = pd.read_json(file, precise_float=True)
        dataset = list(dataframe.to_dict().values())

    with open(filename + r"/params.json", "r") as file:
        paramset = json.load(file)
    

    solution = SolutionClass([])
    solution.data_list_full = dataset
    solution.data_list = [full_to_final_solution(i) for i in dataset]
    solution.param_list = paramset

    return solution


def full_to_final_solution(full_sol):
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