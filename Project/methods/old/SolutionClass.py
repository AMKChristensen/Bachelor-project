import numpy as np
import itertools
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
    """
    def __init__(self, param_list: list[dict],
                 two_fluid_file = "../temp_plasma",
                 temp_json_file = "temp/temp.json",
                 temp_nc_file   = "temp/temp.nc",
                ):

        # Saves parameter list in case this needs to be pulled out later
        self.param_list = param_list
        self.constants  = make_plasma_input()

        # Simulates the system with the given list of parameters
        self.data_list = []
        self.data_list_full = []

        rep = simplesim.Repeater(two_fluid_file, temp_json_file, temp_nc_file)

        for params in self.param_list:
            rep.clean()
            rep.run(params, error="display", stdout="ignore")
            ncin = Dataset(temp_nc_file, 'r', format="NETCDF4")
            var = ncin.variables

            self.data_list.append(extract_data(var, params=params, only_last=True))
            self.data_list_full.append(extract_data(var, params=params, only_last=False))

            ncin.close()
        
    

    def get_data_keys(self):
        return self.data_list[0].keys()
    
    def get_data_ncin_keys(self):
        return self.data_list_ncin[0].keys()

    def print_diagnostics(self):
        for data in self.data_list:
            print("{}:".format(data["label"]))
            print("Function Calls is {0}. Failed {1}. Took {2:.7f}s".format(data["nsteps"], data["nfailed"], data["duration"]))

    def plot_electrons(self):
        # Prepare plot
        frows, fcols = 1, 3
        plt.rcParams.update({'font.size': 18})
        fig, ax = plt.subplots(frows,fcols,figsize=(fcols*10,frows*8),dpi=80, facecolor='w', edgecolor='k')

        # Plots data
        for data in self.data_list:
            ax[0].plot(data["x"], data["ne"], label=data["label"], lw=4)
            ax[1].plot(data["x"], data["Te"], label=data["label"], lw=4)
            ax[2].plot(data["x"], data["ue"], label=data["label"], lw=4)
        
        ### Plot parameters ###
        ax[0].legend()

        ax[0].grid(True)
        ax[1].grid(True)
        ax[2].grid(True)

        ax[0].set_title("Electron density Nx = {} t = {:.4f}".format(self.param_list[0]['grid']['Nx'], self.data_list[0]["t"]))
        ax[0].set_xlabel("$x$")
        ax[0].set_ylabel("$n_e$")

        ax[1].set_title("Electron Temperature")
        ax[1].set_xlabel("$x$")
        ax[1].set_ylabel("$T_e$")

        ax[2].set_title("Electron Velocity")
        ax[2].set_xlabel("$x$")
        ax[2].set_ylabel("$u_e$")
    
    def plot_ions(self):
        # Prepare plot
        frows, fcols = 1, 3
        plt.rcParams.update({'font.size': 18})
        fig, ax = plt.subplots(frows,fcols,figsize=(fcols*10,frows*8),dpi=80, facecolor='w', edgecolor='k')

        # Plots data
        for data in self.data_list:
            ax[0].plot(data["x"], data["ni"], label=data["label"], lw=4)
            ax[1].plot(data["x"], data["Ti"], label=data["label"], lw=4)
            ax[2].plot(data["x"], data["ui"], label=data["label"], lw=4)
        
        ### Plot parameters ###
        ax[0].legend()

        ax[0].grid(True)
        ax[1].grid(True)
        ax[2].grid(True)

        ax[0].set_title("Ion density Nx = {} t = {:.4f}".format(self.param_list[0]['grid']['Nx'], self.data_list[0]["t"]))
        ax[0].set_xlabel("$x$")
        ax[0].set_ylabel("$n_i$")

        ax[1].set_title("Ion Temperature")
        ax[1].set_xlabel("$x$")
        ax[1].set_ylabel("$T_i$")

        ax[2].set_title("Ion Velocity")
        ax[2].set_xlabel("$x$")
        ax[2].set_ylabel("$u_i$")


    def plot_fields(self):
        # Prepare plot
        frows, fcols = 1, 3
        plt.rcParams.update({'font.size': 18})
        fig, ax = plt.subplots(frows,fcols,figsize=(fcols*10,frows*8),dpi=80, facecolor='w', edgecolor='k')

        ### Plot parameters ###
        ax[0].legend()

        ax[0].grid(True)
        ax[1].grid(True)
        ax[2].grid(True)

        ax[0].set_title("Charge density Nx = {} t = {:.4f}".format(self.param_list[0]['grid']['Nx'], self.data_list[0]["t"]))
        ax[0].set_xlabel("$x$")
        ax[0].set_ylabel("$n_i - n_e$")

        ax[1].set_title("Potential")
        ax[1].set_xlabel("$x$")
        ax[1].set_ylabel(r"$\phi$")

        ax[2].set_title("Electric field")
        ax[2].set_xlabel("$x$")
        ax[2].set_ylabel("$E$")

        # Plots data
        for data in self.data_list:
            ax[0].plot(data["x"], data["charge"], label=data["label"], lw=4)
            ax[1].plot(data["x"], data["potential"], label=data["label"], lw=4)
            ax[2].plot(data["x"], data["electric"], label=data["label"], lw=4)


    def plot_all(self):
        self.plot_electrons()
        self.plot_ions()
        self.plot_fields()


    def animate_all(self, fps=20, filename="testplot.mp4"):
        frows = 3
        fcols = 3

        fig,ax=plt.subplots(frows,fcols,figsize=(fcols*10,frows*8),dpi=300, facecolor='w', edgecolor='k')

        data = self.data_list_full[0]
        params = self.param_list[0]

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
        try: ax[0][0].set_ylim(_find_limits(data["ne"]))
        except: print("ne plot limits failed")
        try: ax[0][1].set_ylim(_find_limits(data["ue"]))
        except: print("ue plot limits failed")
        try: ax[0][2].set_ylim(_find_limits(data["Te"]))
        except: print("Te plot limits failed")
        
        ax[1][0].set_title("Ion density")
        ax[1][1].set_title("Ion velocity")
        ax[1][2].set_title("Ion Temperature")
        ax[1][0].set_ylabel("$n_i$")
        ax[1][1].set_ylabel("$u_i$")
        ax[1][2].set_ylabel("$T_i$")
        try: ax[1][0].set_ylim(_find_limits(data["ni"]))
        except: print("ni plot limits failed")
        try: ax[1][1].set_ylim(_find_limits(data["ui"]))
        except: print("ui plot limits failed")
        try: ax[1][2].set_ylim(_find_limits(data["Ti"]))
        except: print("Ti plot limits failed")

        ax[2][0].set_title("Charge density")
        ax[2][1].set_title("Potential")
        ax[2][2].set_title("Electric field")
        ax[2][0].set_ylabel("$n_i - n_e$")
        ax[2][1].set_ylabel(r"$\phi$")
        ax[2][2].set_ylabel("$E$")
        try: ax[2][0].set_ylim(_find_limits(data["charge"]))
        except: print("charge plot limits failed")
        try: ax[2][1].set_ylim(_find_limits(data["potential"]))
        except: print("potential plot limits failed")
        try: ax[2][2].set_ylim(_find_limits(data["electric"]))
        except: print("electric plot limits failed")


        time = self.data_list_full[0]["t"][:]
        title00 = ax[0][0].get_title()

        ax[0][0].set_title(title00 + " Nx = {} t = {:5.5f}".format(self.param_list[0]['grid']['Nx'], time[0]))
        plots = {}

        plots["ne"] = ax[0][0].plot(data["x"], data["ne"][0], lw=4, label=data["label"])[0]
        plots["ue"] = ax[0][1].plot(data["x"], data["ue"][0], lw=4, label=data["label"])[0]
        plots["Te"] = ax[0][2].plot(data["x"], data["Te"][0], lw=4, label=data["label"])[0]

        plots["ni"] = ax[1][0].plot(data["x"], data["ni"][0], lw=4, label=data["label"])[0]
        plots["ui"] = ax[1][1].plot(data["x"], data["ui"][0], lw=4, label=data["label"])[0]
        plots["Ti"] = ax[1][2].plot(data["x"], data["Ti"][0], lw=4, label=data["label"])[0]

        plots["charge"]    = ax[2][0].plot(data["x"], data["charge"][0], lw=4, label=data["label"])[0]
        plots["potential"] = ax[2][1].plot(data["x"], data["potential"][0], lw=4, label=data["label"])[0]
        plots["electric"]  = ax[2][2].plot(data["x"], data["electric"][0], lw=4, label=data["label"])[0]


        def update_plots(iter):
            ax[0][0].set_title(title00 + " Nx = {} t = {:5.5f}".format(self.param_list[0]['grid']['Nx'], time[iter]))
            plots["ne"].set_data(data["x"], data["ne"][iter])
            plots["ue"].set_data(data["x"], data["ue"][iter])
            plots["Te"].set_data(data["x"], data["Te"][iter])

            plots["ni"].set_data(data["x"], data["ni"][iter])
            plots["ui"].set_data(data["x"], data["ui"][iter])
            plots["Ti"].set_data(data["x"], data["Ti"][iter])

            plots["charge"].set_data(data["x"], data["charge"][iter])
            plots["potential"].set_data(data["x"], data["potential"][iter])
            plots["electric"].set_data(data["x"], data["electric"][iter])

            return plots.values()

        ani = animation.FuncAnimation(fig, update_plots, frames=params["output"]["maxout"], interval=2, blit=True, repeat=True)
        plt.show()
        writer = animation.writers['ffmpeg'](fps=fps)
        writer = animation.FFMpegWriter(fps=20, 
                                        codec='h264')

        ani.save(filename,writer=writer,dpi=300)



####################
# Helper functions #
####################
def _find_limits(data_arr, plottype: str = ""):
    mini = np.min(data_arr)
    maxi = np.max(data_arr)
    r = (maxi - mini)*0.05
    ran = (mini-r, maxi+r)
    return ran