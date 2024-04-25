import numpy as np

def extract_data(var, params: dict, only_last: bool=True):
    """
    Gives more usable aliases to the data from the temp-two-fluid simulation
    var: netCDF4 Dataset.variables
    params: dictionary of parameters for simulation
    only_last: Whether to return just the data for just the final time. Else the complete set for every point in time and space is returned
    """

    last_idx = var["time"].shape[0]-1

    if params["physical"]["type"] == "adiabatic":
        electrons = np.exp( var["potential"][:,:])
    else:
        electrons = var["electrons"][:,:]

    # Prepares fields
    charge    = np.ma.getdata(var["ions"][:,:]) - np.ma.getdata(electrons[:,:])
    potential = np.ma.getdata(var["potential"][:,:])
    electric  = -np.gradient(np.ma.getdata(var["potential"][:,:]), np.ma.getdata(var['x'][:]), axis=1)

    # Prepares labels too
    label = f"{params['advection']['type']}"
    if "variant" in params["advection"].keys():
        if (params['advection']['variant'] == "original"): 
            label += " semi-implicit"
        else: 
            label += f" {params['advection']['variant']}"

    # For old system without temperature fields
    try:
        Te = var["te"]
        Ti = var["ti"]
    except:
        print("Error: No temperature fields found. Setting to constant")
        Te = Ti = params["physical"]["tau"]*np.ones(electrons.shape)

    if only_last:

        data = {
            # metadata
            "label"    : label,
            "last_idx" : last_idx,
            "nsteps"   : int(np.ma.getdata(var["nsteps"][last_idx])),
            "nfailed"  : int(np.ma.getdata(var["failed"][last_idx])),
            "duration" : float(np.ma.getdata(var["duration"][last_idx])),

            # Time and space
            "t"       : float(np.ma.getdata(var["time"][last_idx])),
            "x"       : np.ma.getdata(var['x'][:]),

            # Electrons
            "ne"      : np.ma.getdata(electrons[last_idx,:]),
            "ue"      : np.ma.getdata(var["ue"][last_idx,:]),
            "Te"      : np.ma.getdata(Te[last_idx,:]),
            "norm_ne" : np.linalg.norm( electrons, ord=1), # type: ignore
            "norm_ue" : np.linalg.norm( var["ue"][last_idx,:], ord=1), # type: ignore
            "norm_Te" : np.linalg.norm( Te[last_idx,:], ord=1), # type: ignore

            # Ions
            "ni"      : np.ma.getdata(var["ions"][last_idx,:]),
            "ui"      : np.ma.getdata(var["ui"][last_idx,:]),
            "Ti"      : np.ma.getdata(Ti[last_idx,:]),
            "norm_ni" : np.linalg.norm( var["ions"][last_idx,:], ord=1), # type: ignore
            "norm_ui" : np.linalg.norm( var["ui"][last_idx,:], ord=1), # type: ignore
            "norm_Ti" : np.linalg.norm( Ti[last_idx,:], ord=1), # type: ignore

            # Fields
            "charge"         : charge[last_idx,:],
            "potential"      : potential[last_idx,:],
            "electric"       : electric[last_idx,:],
            "norm_charge"    : np.linalg.norm( charge[last_idx,:], ord=1),
            "norm_potential" : np.linalg.norm( potential[last_idx,:], ord=1),
            "norm_electric"  : np.linalg.norm( electric[last_idx,:], ord=1),

            #"m"      : total_mass,
            #"p"      : total_momentum,
            #"E"      : total_energy,
        }
    
    
    else:  # Data for every saved timestep

        data = {
            # metadata
            "label"    : label,
            "last_idx" : last_idx,
            "nsteps"   : np.array(np.ma.getdata(var["nsteps"][:]), dtype=int),
            "nfailed"  : np.array(np.ma.getdata(var["failed"][:]), dtype=int),
            "duration" : np.ma.getdata(var["duration"][:]),

            # Time and space
            "t"       : np.array(np.ma.getdata(var["time"][:])),
            "x"       : np.array(np.ma.getdata(var['x'][:])),

            # Electrons
            "ne"      : np.ma.getdata(electrons[:,:]),
            "ue"      : np.ma.getdata(var["ue"][:,:]),
            "Te"      : np.ma.getdata(Te[:,:]),
            "norm_ne" : np.linalg.norm( electrons, ord=1, axis=1), # type: ignore
            "norm_ue" : np.linalg.norm( var["ue"][:,:], ord=1, axis=1), # type: ignore
            "norm_Te" : np.linalg.norm( Te[:,:], ord=1, axis=1), # type: ignore

            # Ions
            "ni"      : np.ma.getdata(var["ions"][:,:]),
            "ui"      : np.ma.getdata(var["ui"][:,:]),
            "Ti"      : np.ma.getdata(Ti[:,:]),
            "norm_ni" : np.linalg.norm( var["ions"][:,:], ord=1, axis=1), # type: ignore
            "norm_ui" : np.linalg.norm( var["ui"][:,:], ord=1, axis=1), # type: ignore
            "norm_Ti" : np.linalg.norm( Ti[:,:], ord=1, axis=1), # type: ignore

            # Fields
            "charge"         : charge,
            "potential"      : potential,
            "electric"       : electric,
            "norm_charge"    : np.linalg.norm( charge, ord=1, axis=1),
            "norm_potential" : np.linalg.norm( potential, ord=1, axis=1),
            "norm_electric"  : np.linalg.norm( electric, ord=1, axis=1),


            #"m"      : total_mass,
            #"p"      : total_momentum,
            #"E"      : total_energy,
        }

        #data["Te"] = np.where(np.isnan(data["Te"]), 0.0, data["Te"])
        #data["norm_Te"] = np.where(np.isnan(data["norm_Te"]), 0.0, data["norm_Te"])

        #print(data["Te"])
        #print(data["norm_Te"])
            

    return data