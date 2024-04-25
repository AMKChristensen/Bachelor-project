import numpy as np
import itertools
import copy
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import simplesimdb as simplesim
from methods.extract_data import extract_data
from methods.make_input import make_plasma_input

class SolutionClass:
    """
    This class solves a navier-stokes problem for a list of parameters describing different problems and solution methods.
    The solution is only evaluated once per parameter set for optimization and the results may be plotted with a list of built-in functions

    params/self.params: dict of simulation parameters
    self.constants: dict of constants used for the simulation
    self.data: Dict of the data for the last time of the simulation
    self.data_full: The data for every outputted time of the simulation
    """

    def __init__(self, params: dict = None,
                 two_fluid_file = "../temp_plasma",
                 temp_json_file = "temp/temp.json",
                 temp_nc_file   = "temp/temp.nc",
                 updates = False,
                ):

        # Initializes class fields for manual setting after empty input
        self.params    = {}
        self.constants = {}
        self.data      = {}
        self.data_full = {}

        if params != None:
            # Saves parameter list in case this needs to be pulled out later
            if updates: print("copying params")
            self.params = copy.deepcopy(params)

            if updates: print("making plasma input")
            self.constants = make_plasma_input()

            # Simulates the system with the given list of parameters
            if updates: print("setting up repeater")
            rep = simplesim.Repeater(two_fluid_file, temp_json_file, temp_nc_file)
            rep.clean()
            if updates: print("runs repeater")
            rep.run(params, error="display", stdout="ignore")
            if updates: print("extracts data")
            ncin = Dataset(temp_nc_file, 'r', format="NETCDF4")

            self.data      = extract_data(ncin.variables, params=params, only_last=True)
            self.data_full = extract_data(ncin.variables, params=params, only_last=False)

            if updates: print("closing ncin")
            ncin.close()
            if updates: print("Done!")

    # Getters for certain mutable data so they wont be changed elsewhere in code
    def get_params(self):
        return copy.deepcopy(self.params)
    
    def get_constants(self):
        return copy.deepcopy(self.constants)
    
    def get_data(self):
        return copy.deepcopy(self.data)
    
    def get_data_full(self):
        return copy.deepcopy(self.data_full)

    def print_diagnostics(self):
        """
        Prints simple diagnostics for the simulation
        """
        print("{}:".format(self.data["label"]))
        print("Function Calls is {0}. Failed {1}. Took {2:.7f}s".format(self.data["nsteps"], self.data["nfailed"], self.data["duration"]))

    def plot_electrons(self):
        """
        Plots the final iteration state for the electron density, velocity, and temperature
        """

        # Prepare plot
        frows, fcols = 1, 3
        plt.rcParams.update({'font.size': 18})
        fig, ax = plt.subplots(frows,fcols,figsize=(fcols*10,frows*8),dpi=80, facecolor='w', edgecolor='k')

        # Plots data
        ax[0].plot(self.data["x"], self.data["ne"], label=self.data["label"], lw=4)
        ax[1].plot(self.data["x"], self.data["Te"], label=self.data["label"], lw=4)
        ax[2].plot(self.data["x"], self.data["ue"], label=self.data["label"], lw=4)
        
        ### Plot parameters ###
        ax[0].legend()

        ax[0].grid(True)
        ax[1].grid(True)
        ax[2].grid(True)

        ax[0].set_title("Electron density Nx = {} t = {:.4f}".format(self.params['grid']['Nx'], self.data["t"]))
        ax[0].set_xlabel("$x$")
        ax[0].set_ylabel("$n_e$")

        ax[1].set_title("Electron Temperature")
        ax[1].set_xlabel("$x$")
        ax[1].set_ylabel("$T_e$")

        ax[2].set_title("Electron Velocity")
        ax[2].set_xlabel("$x$")
        ax[2].set_ylabel("$u_e$")
    
    def plot_ions(self):
        """
        Plots the final iteration state for the ion density, velocity, and temperature
        """

        # Prepare plot
        frows, fcols = 1, 3
        plt.rcParams.update({'font.size': 18})
        fig, ax = plt.subplots(frows,fcols,figsize=(fcols*10,frows*8),dpi=80, facecolor='w', edgecolor='k')

        # Plots data
        ax[0].plot(self.data["x"], self.data["ni"], label=self.data["label"], lw=4)
        ax[1].plot(self.data["x"], self.data["Ti"], label=self.data["label"], lw=4)
        ax[2].plot(self.data["x"], self.data["ui"], label=self.data["label"], lw=4)
        
        ### Plot parameters ###
        ax[0].legend()

        ax[0].grid(True)
        ax[1].grid(True)
        ax[2].grid(True)

        ax[0].set_title("Ion density Nx = {} t = {:.4f}".format(self.params['grid']['Nx'], self.data["t"]))
        ax[0].set_xlabel("$x$")
        ax[0].set_ylabel("$n_i$")

        ax[1].set_title("Ion Temperature")
        ax[1].set_xlabel("$x$")
        ax[1].set_ylabel("$T_i$")

        ax[2].set_title("Ion Velocity")
        ax[2].set_xlabel("$x$")
        ax[2].set_ylabel("$u_i$")

    def plot_fields(self):
        """
        Plots the final iteration state for the charge density, potential and electric field
        """

        # Prepare plot
        frows, fcols = 1, 3
        plt.rcParams.update({'font.size': 18})
        fig, ax = plt.subplots(frows,fcols,figsize=(fcols*10,frows*8),dpi=80, facecolor='w', edgecolor='k')

        ### Plot parameters ###
        ax[0].legend()

        ax[0].grid(True)
        ax[1].grid(True)
        ax[2].grid(True)

        ax[0].set_title("Charge density Nx = {} t = {:.4f}".format(self.params['grid']['Nx'], self.data["t"]))
        ax[0].set_xlabel("$x$")
        ax[0].set_ylabel("$n_i - n_e$")

        ax[1].set_title("Potential")
        ax[1].set_xlabel("$x$")
        ax[1].set_ylabel(r"$\phi$")

        ax[2].set_title("Electric field")
        ax[2].set_xlabel("$x$")
        ax[2].set_ylabel("$E$")

        # Plots data
        ax[0].plot(self.data["x"], self.data["charge"],    label=self.data["label"], lw=4)
        ax[1].plot(self.data["x"], self.data["potential"], label=self.data["label"], lw=4)
        ax[2].plot(self.data["x"], self.data["electric"],  label=self.data["label"], lw=4)

    def plot_all(self):
        """
        Plots all of the most important data serially
        """

        self.plot_electrons()
        self.plot_ions()
        self.plot_fields()

    def animate_all(self, filename="testplot.mp4", fps=20):
        """
        animates all of the plots for every time. Can take a while for moderately large datasets
        """

        frows = 3
        fcols = 3

        fig,ax=plt.subplots(frows,fcols,figsize=(fcols*10,frows*8),dpi=300, facecolor='w', edgecolor='k')

        # Common plot options
        for ax_single in itertools.chain.from_iterable(zip(*ax)):
            ax_single.set_xlabel("$x$")
            ax_single.grid(True)

        #ax[0][0].legend()
        ax[0][0].set_title("Electron density")
        ax[0][1].set_title("Electron velocity")
        ax[0][2].set_title("Electron Temperature")
        ax[0][0].set_ylabel("$n_e$")
        ax[0][1].set_ylabel("$u_e$")
        ax[0][2].set_ylabel("$T_e$")
        try: ax[0][0].set_ylim(_find_limits(self.data_full["ne"]))
        except: print("ne plot limits failed")
        try: ax[0][1].set_ylim(_find_limits(self.data_full["ue"]))
        except: print("ue plot limits failed")
        try: ax[0][2].set_ylim(_find_limits(self.data_full["Te"]))
        except: print("Te plot limits failed")
        
        ax[1][0].set_title("Ion density")
        ax[1][1].set_title("Ion velocity")
        ax[1][2].set_title("Ion Temperature")
        ax[1][0].set_ylabel("$n_i$")
        ax[1][1].set_ylabel("$u_i$")
        ax[1][2].set_ylabel("$T_i$")
        try: ax[1][0].set_ylim(_find_limits(self.data_full["ni"]))
        except: print("ni plot limits failed")
        try: ax[1][1].set_ylim(_find_limits(self.data_full["ui"]))
        except: print("ui plot limits failed")
        try: ax[1][2].set_ylim(_find_limits(self.data_full["Ti"]))
        except: print("Ti plot limits failed")

        ax[2][0].set_title("Charge density")
        ax[2][1].set_title("Potential")
        ax[2][2].set_title("Electric field")
        ax[2][0].set_ylabel("$n_i - n_e$")
        ax[2][1].set_ylabel(r"$\phi$")
        ax[2][2].set_ylabel("$E$")
        try: ax[2][0].set_ylim(_find_limits(self.data_full["charge"]))
        except: print("charge plot limits failed")
        try: ax[2][1].set_ylim(_find_limits(self.data_full["potential"]))
        except: print("potential plot limits failed")
        try: ax[2][2].set_ylim(_find_limits(self.data_full["electric"]))
        except: print("electric plot limits failed")


        title00 = ax[0][0].get_title()
        ax[0][0].set_title(title00 + " Nx = {} t = {:5.5f}".format(self.params['grid']['Nx'], self.data_full["t"][0]))
        plots = {}

        plots["ne"], = ax[0][0].plot(self.data_full["x"], self.data_full["ne"][0], lw=4, label=self.data_full["label"])
        plots["ue"], = ax[0][1].plot(self.data_full["x"], self.data_full["ue"][0], lw=4, label=self.data_full["label"])
        plots["Te"], = ax[0][2].plot(self.data_full["x"], self.data_full["Te"][0], lw=4, label=self.data_full["label"])

        plots["ni"], = ax[1][0].plot(self.data_full["x"], self.data_full["ni"][0], lw=4, label=self.data_full["label"])
        plots["ui"], = ax[1][1].plot(self.data_full["x"], self.data_full["ui"][0], lw=4, label=self.data_full["label"])
        plots["Ti"], = ax[1][2].plot(self.data_full["x"], self.data_full["Ti"][0], lw=4, label=self.data_full["label"])

        plots["charge"],    = ax[2][0].plot(self.data_full["x"], self.data_full["charge"][0], lw=4, label=self.data_full["label"])
        plots["potential"], = ax[2][1].plot(self.data_full["x"], self.data_full["potential"][0], lw=4, label=self.data_full["label"])
        plots["electric"],  = ax[2][2].plot(self.data_full["x"], self.data_full["electric"][0], lw=4, label=self.data_full["label"])


        def update_plots(iter):
            ax[0][0].set_title(title00 + " Nx = {} t = {:5.5f}".format(self.params['grid']['Nx'], self.data_full["t"][iter]))
            plots["ne"].set_data(self.data_full["x"], self.data_full["ne"][iter])
            plots["ue"].set_data(self.data_full["x"], self.data_full["ue"][iter])
            plots["Te"].set_data(self.data_full["x"], self.data_full["Te"][iter])

            plots["ni"].set_data(self.data_full["x"], self.data_full["ni"][iter])
            plots["ui"].set_data(self.data_full["x"], self.data_full["ui"][iter])
            plots["Ti"].set_data(self.data_full["x"], self.data_full["Ti"][iter])

            plots["charge"].set_data(self.data_full["x"], self.data_full["charge"][iter])
            plots["potential"].set_data(self.data_full["x"], self.data_full["potential"][iter])
            plots["electric"].set_data(self.data_full["x"], self.data_full["electric"][iter])

            return plots.values()

        ani = animation.FuncAnimation(fig, 
                                      update_plots, 
                                      frames=self.params["output"]["maxout"], 
                                      interval=2, 
                                      blit=True, 
                                      repeat=True)
        writer = animation.FFMpegWriter(fps=20, codec='h264')

        ani.save(filename, writer=writer, dpi=150)


####################
# Helper functions #
####################
def _find_limits(data_arr, plottype: str = ""):
    """
    Finds limits for certain plots
    """
    mini = np.min(data_arr)
    maxi = np.max(data_arr)
    r_temp = (maxi - mini)*0.05
    r = (mini-r_temp, maxi+r_temp)

    return r