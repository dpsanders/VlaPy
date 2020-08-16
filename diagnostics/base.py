# MIT License
#
# Copyright (c) 2020 Archis Joglekar
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import time

import numpy as np
from matplotlib import pyplot as plt


def __get_figure_and_plot__():
    this_fig = plt.figure(figsize=(8, 4))
    this_plt = this_fig.add_subplot(111)

    return this_fig, this_plt


def plot_health(health_dir, storage_manager):
    # t = storage_manager.overall_arrs["e"].coords["time"].data
    #
    # for metric, vals in storage_manager.health.items():
    #     this_fig, this_plt = __get_figure_and_plot__()
    #     this_plt.plot(t[-vals.size :], vals)
    #     this_plt.grid()
    #     this_plt.set_xlabel(r"Time ($\omega_p^{-1}$)", fontsize=12)
    #     this_plt.set_ylabel(metric, fontsize=12)
    #     this_plt.set_title(metric + " vs Time", fontsize=14)
    #     this_fig.savefig(
    #         os.path.join(health_dir, metric + ".png"), bbox_inches="tight",
    #     )
    #     plt.close(this_fig)
    pass


def plot_e_vs_t(plots_dir, t, e, title):
    this_fig, this_plt = __get_figure_and_plot__()
    this_plt.plot(t, e)
    this_plt.set_xlabel(r"Time ($\omega_p^{-1}$)", fontsize=12)
    this_plt.set_ylabel(r"$\hat{E}_{k=1}$", fontsize=12)
    this_plt.set_title(title, fontsize=14)
    this_plt.grid()
    this_fig.savefig(
        os.path.join(plots_dir, "E_vs_time.png"), bbox_inches="tight",
    )
    plt.close(this_fig)


def plot_e_vs_w(plots_dir, w, e, title):
    this_fig, this_plt = __get_figure_and_plot__()
    this_plt.semilogy(np.fft.fftshift(w), np.fft.fftshift(e), "-x")
    this_plt.set_xlabel(r"Frequency ($\omega_p$)", fontsize=12)
    this_plt.set_ylabel(r"$\hat{\hat{E}}_{k=1}$", fontsize=12)
    this_plt.set_title(title, fontsize=14)
    this_plt.grid()
    this_plt.set_xlim(-5, 5)
    this_plt.set_ylim(0.001 * np.amax(e), 1.5 * np.amax(e))
    this_fig.savefig(
        os.path.join(plots_dir, "E_vs_frequency.png"), bbox_inches="tight",
    )
    plt.close(this_fig)


def plot_dw_vs_t(plots_dir, t, ek1_shift, title):
    lower_bound = int(0.25 * t.size)
    upper_bound = int(0.7 * t.size)

    this_fig, this_plt = __get_figure_and_plot__()
    this_plt.plot(t[lower_bound:upper_bound], ek1_shift[lower_bound:upper_bound])
    this_plt.set_xlabel(r"Time ($\omega_p^{-1}$)", fontsize=12)
    this_plt.set_ylabel(r"$\Delta \Phi$", fontsize=12)
    this_plt.set_title(title, fontsize=14)
    this_plt.grid()
    this_fig.savefig(
        os.path.join(plots_dir, "nl_frequency_shift_vs_time.png"), bbox_inches="tight",
    )
    plt.close(this_fig)


def plot_fhat0(plots_dir, f, v, title):
    this_fig, this_plt = __get_figure_and_plot__()

    this_plt.plot(v, f[0], label="initial")
    this_plt.plot(v, f[-1], label="final")
    this_plt.legend()
    this_plt.grid()
    this_plt.set_xlabel(r"$(v - v_{ph}) / v_{th}$", fontsize=12)
    this_plt.set_ylabel(r"$\hat{f}^{0}$", fontsize=12)
    this_plt.set_title(title, fontsize=14)
    this_fig.savefig(
        os.path.join(plots_dir, "fk0.png"), bbox_inches="tight",
    )
    plt.close(this_fig)


class BaseDiagnostic:
    def __init__(self):
        self.plots_dir = ""
        self.health_dir = ""

    def _make_dirs_(self, storage_manager):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        self.plots_dir = os.path.join(
            storage_manager.paths["long_term"], "plots", timestr
        )
        self.health_dir = os.path.join(
            storage_manager.paths["long_term"], "plots", timestr, "health"
        )
        os.makedirs(self.plots_dir, exist_ok=True)
        os.makedirs(self.health_dir, exist_ok=True)

    def _make_health_dict_(self, storage_manager):
        health = {}
        for key, val in storage_manager.health.items():
            if "(" in key:
                mod_key = key.replace("(", "_")
                mod_key = mod_key.replace(")", "_")
            else:
                mod_key = key

            health[mod_key] = val[-1]

        return health
