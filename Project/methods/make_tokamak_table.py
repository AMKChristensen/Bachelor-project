import numpy as np
import feltorutilities as fp

def make_tokamak_table():
    """
    Makes table of relavent constants for the tokamak.
    """

    # These parameters are for a Tokamak
    show = ["name", "mu", "R_0", "a_0", "beta", "resistivity",
            "T_e", "n_0", "B_0", "CFL_diff", "epsilon_D",
            "omega_0_inv", "viscosity_i", "viscosity_e", "rho_s","c_s"]
    physical={"name" : "Compass",
        "beta" : 1e-4, "resistivity": 1e-4, #change both to change n_0
        "tau" : 1,
        "m_i" : fp.deuteron_mass, "R_0" : 545, "R": 0.545,
        "a": 0.175, "q":2, "scaleR" : 1.45, "Nz" : 32}
    fp.numerical2physical( physical, physical)
    table = dict()
    for s in show + list(physical.keys()):
        table[s] = fp.parameters2quantity( physical, s)

    table["lx"] = 2*np.pi*table["R_0"]*3

    return table