import tictoc

tic0 = tictoc.tic()
import emcpy.stats.obspace
from emcpy.plots.plots import LinePlot, HorizontalLine
from emcpy.plots.create_plots import CreatePlot, CreateFigure
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# import emcpy.utils
# lsdict=emcpy.utils.advanced_linestyles()

expt_names = []
# ********************************************************************
#                        USER SPECIFIED PARAMETERS                  *
# ********************************************************************
n_mem = 30
expt_names.append("rrfs_a_conus")
# expt_names.append("rrfs_b_test")
# expt_names.append("just uncomment for a second experiment")

date1 = "2022122000"
date2 = "2022123023"  # will skip 00-18
skip_enkf_hours = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]  # right now rrfs only runs EnKF at 18-23Z

datapath = "/lfs/h2/emc/da/noscrub/donald.e.lippi/rrfs_mon/diags/"  # rrfs_a_conus/"

# Filtering parameters
hem = None  # GL, NH, TR, SH, CONUS, or None. Overrides lat/lon max/mins filter options.

p_max = 1050.0  # maximum pressure (mb) for including observation in calculations
p_min = 100.0  # minimum pressure (mb) for including observation in calculations

lat_max = 90.0  # maximum latitude (deg N) for including observation in calculations
lat_min = 0.0  # minimum latitude (deg N) for including observation in calculations

lon_max = 360.0  # maximum latitude (deg E) for including observation in calculations
lon_min = 0.0  # minimum latitude (deg E) for including observation in calculations

error_max = 40.0  # maximum error standard deviation for including observation in calculations
error_min = 0.000001  # minimum error standard deviation for including observation in calculations

ob_types = ["u", "v", "t", "q"]
codes_uv = [280, 281, 282, 220, 221, 230, 231, 232, 233, 234, 235]
codes_tq = [180, 181, 182, 120, 130, 131, 132, 133, 134, 135]

# Plotting parameters
plot_bias = True  # mean of (forecast - observation)
plot_rms = True  # rms of (F-O)
plot_std_dev = True  # standard deviation of (F-O)
plot_total_spread = True  # total spread (standard deviation)
plot_spread = True  # ensemble spread (standard deviation)
plot_ob_error = True  # observation error standard deviation
plot_rmse = True  # rms of (O-Omf) = rmse of ensemble mean fcst
plot_cr = True  # consistency ratio (total spread/rmsi)**2
plot_ser = True  # spread error ratio (intraensemble std_dev/ rmse of ensemble mean fcst)
plot_zero_line = True  # horizontal line on zero
plot_one_line = True  # horizontal line on one

# Figure settings
suptitle_fontsize = 15  # super title fontsize
title_fontsize = 9  # subplot title fontsizes
xy_label_fontsize = 13  # xy-axes label fontsized
tick_label_fontsize = 10  # xy-axes tick label fontsizes
lw = 1.5  # linewidth
ms = 4  # markersize
ls = ["-", "--", ":", ".-"]  # linestyles: solid, dashed, dotted, dash-dotted
# ls=["solid","dashed","dotted","dashdot"]
# ls=["solid",lsdict["densely dotted"],lsdict[""],"dashdot"]

scale_fig_size = 1.2  # =1.2 --> 8*1.2x6*1.2=9.6x7.2 sized fig (1.44 times bigger fig)

# Debug settings
validate = False
debug = False
# validate=True
debug = True

if debug:
    codes_uv = [287]
    codes_tq = [187]
    codes_uv = [280, 281, 282, 220, 221, 230, 231, 232, 233, 234, 235]
    codes_tq = [180, 181, 182, 120, 130, 131, 132, 133, 134, 135]
    # date1="2022113019"; date2="2022113023"
    date1 = "2022121619"
    date2 = "2022121623"  # 1 day
    date1 = "2022121619"
    date2 = "2022121723"  # 2 day
    ob_types = ["u"]
#  ob_types=["q"]
#  date1="2022122000"; date2="2022122200" #will skip 00-18
#  ob_types=["u","q"]

# ********************************************************************
#                   END OF USER SPECIFIED PARAMETERS                *
# ********************************************************************

# Calculate all observation space statistics
dates, bias, rms, std_dev, rmse, spread, ob_error, total_spread, num_obs_total, num_obs_assim, cr, ser = \
emcpy.stats.obspace.obspace_stats(
#_stats.netCDF_obspace_diag.obspace_stats(
    datapath,
    date1,
    date2,
    expt_names,
    n_mem,
    skip_enkf_hours,
    ob_types,
    codes_uv,
    codes_tq,
    hem,
    p_max,
    p_min,
    lat_max,
    lat_min,
    lon_max,
    lon_min,
    error_max,
    error_min,
)

if validate:

    def check(t, test):
        testmin = np.min(test)
        testmax = np.max(test)
        if testmin == 0 and testmax == 0:
            print("%s....GOOD" % (t))
        else:
            print("%s: min=%.2f max=%.2f" % (t, testmin, testmax))

        test = ["bias", "rms", "std_dev", "rmse", "spread", "ob_error", "total_spread", "cr", "ser"]
        for t in test:
            if t == "bias":
                test = bias[0, 0, :] - bias[0, 1, :]
                check(t, test)
            if t == "rms":
                test = rms[0, 0, :] - rms[0, 1, :]
                check(t, test)
            if t == "std_dev":
                test = std_dev[0, 0, :] - std_dev[0, 1, :]
                check(t, test)
            if t == "rmse":
                test = rmse[0, 0, :] - rmse[0, 1, :]
                check(t, test)
            if t == "spread":
                test = spread[0, 0, :] - spread[0, 1, :]
                check(t, test)
            if t == "ob_error":
                test = ob_error[0, 0, :] - ob_error[0, 1, :]
                check(t, test)
            if t == "total_spread":
                test = total_spread[0, 0, :] - total_spread[0, 1, :]
                check(t, test)
            if t == "cr":
                test = cr[0, 0, :] - cr[0, 1, :]
                check(t, test)
            if t == "ser":
                test = ser[0, 0, :] - ser[0, 1, :]
                check(t, test)
        exit()


# ****************************************************************************

# Define the x-axis (time UTC)
x_str = [str(item).zfill(4) for item in range(0, 2400, 100)]
x = [int(item) for item in x_str]

# Prepare for plotting
for ob_type in ob_types:  # make a new figure for each observation type
    if ob_type == "u" or ob_type == "v":
        codes = codes_uv
    elif ob_type == "t" or ob_type == "q":
        codes = codes_tq

    plot1 = CreatePlot()
    plt_list = []

    # Plot mean,sd,totalspread,etc.
    for expt_name in expt_names:  # all experiments go on the same figure
        i_o = ob_types.index(ob_type)
        i_e = expt_names.index(expt_name)

        if plot_bias:
            y = bias[i_o, i_e, :]
            lp = LinePlot(x, y)
            lp.color = "green"
            lp.linestyle = ls[i_e]
            lp.linewidth = lw
            lp.marker = "o"
            lp.markersize = ms
            lp.markerfacecolor = None
            lp.alpha = None
            lp.label = "bias of F-O (%s)" % (expt_name)
            plt_list.append(lp)

        if plot_rms:
            y = rms[i_o, i_e, :]
            lp = LinePlot(x, y)
            lp.color = "red"
            lp.linestyle = ls[i_e]
            lp.linewidth = lw  # *1.4
            lp.marker = "o"
            lp.markersize = ms
            lp.alpha = None
            lp.label = "rms of F-O (%s)" % (expt_name)
            plt_list.append(lp)

        if plot_std_dev:
            y = std_dev[i_o, i_e, :]
            lp = LinePlot(x, y)
            lp.color = "magenta"
            lp.linestyle = ls[i_e]
            lp.linewidth = lw
            lp.marker = "o"
            lp.markersize = ms
            lp.alpha = None
            lp.label = "std_dev of F-O (%s)" % (expt_name)
            plt_list.append(lp)

        if plot_rmse:
            y = rmse[i_o, i_e, :]
            lp = LinePlot(x, y)
            lp.color = "blue"
            lp.linestyle = ls[i_e]
            lp.linewidth = lw  # *1.4
            lp.marker = "o"
            lp.markersize = ms
            lp.alpha = None
            lp.label = "rms of ensemble fcst (%s)" % (expt_name)
            plt_list.append(lp)

        if plot_spread:
            y = spread[i_o, i_e, :]
            lp = LinePlot(x, y)
            lp.color = "cyan"
            lp.linestyle = ls[i_e]
            lp.linewidth = lw
            lp.marker = "o"
            lp.markersize = ms
            lp.alpha = None
            lp.label = "spread (std_dev) (%s)" % (expt_name)
            plt_list.append(lp)

        if plot_ob_error:
            y = ob_error[i_o, i_e, :]
            lp = LinePlot(x, y)
            lp.color = "orange"
            lp.linestyle = ls[i_e]
            lp.linewidth = lw
            lp.marker = "o"
            lp.markersize = ms
            lp.alpha = None
            lp.label = "ob_error (std_dev) (%s)" % (expt_name)
            plt_list.append(lp)

        if plot_total_spread:
            y = total_spread[i_o, i_e, :]
            lp = LinePlot(x, y)
            lp.color = "navy"
            lp.linestyle = ls[i_e]
            lp.linewidth = lw
            lp.marker = "o"
            lp.markersize = ms
            lp.alpha = None
            lp.label = "total spread (std_dev) (%s)" % (expt_name)
            plt_list.append(lp)

        if plot_cr:
            y = cr[i_o, i_e, :]
            lp = LinePlot(x, y)
            lp.color = "gray"
            lp.linestyle = ls[i_e]
            lp.linewidth = lw
            lp.marker = "o"
            lp.markersize = ms
            lp.alpha = None
            lp.label = "consistency ratio (%s)" % (expt_name)
            plt_list.append(lp)

        if plot_ser:
            y = ser[i_o, i_e, :]
            lp = LinePlot(x, y)
            lp.color = "black"
            lp.linestyle = ls[i_e]
            lp.linewidth = lw
            lp.marker = "o"
            lp.markersize = ms
            lp.alpha = None
            lp.label = "spread error ratio (%s)" % (expt_name)
            plt_list.append(lp)

        if plot_zero_line:
            lp = HorizontalLine(0)
            lp.color = "black"
            lp.linestyle = "-"
            lp.linewidth = 1
            lp.label = None
            plt_list.append(lp)

        if plot_one_line:
            lp = HorizontalLine(1)
            lp.color = "black"
            lp.linestyle = "-"
            lp.linewidth = 1
            lp.label = None
            plt_list.append(lp)

    # Plot number of obs
    plot2 = CreatePlot()
    plt_list2 = []
    for expt_name in expt_names:
        # Total number of observations
        i_e = expt_names.index(expt_name)
        y = num_obs_total[i_o, i_e, :]
        lp = LinePlot(x, y)
        lp.color = "black"
        lp.linestyle = ls[i_e]
        lp.linewidth = lw
        lp.marker = "o"
        lp.markersize = ms
        lp.alpha = None
        lp.label = "total (%s)" % (expt_name)
        plt_list2.append(lp)

        # Number of observations assimilated
        y = num_obs_assim[i_o, i_e, :]
        lp = LinePlot(x, y)
        lp.color = "gray"
        lp.linestyle = ls[i_e]
        lp.linewidth = lw
        lp.marker = "o"
        lp.markersize = ms
        lp.alpha = None
        lp.label = "assim (%s)" % (expt_name)
        plt_list2.append(lp)

    # Plot 1
    plot1.plot_layers = plt_list
    title = "Filtered by:\n%s%s,  %.1f-%.1f hPa,  %.1f-%.1f degN,  %.1f-%.1f degE,  %.6f-%.1f err" % (
        ob_type,
        codes,
        p_max,
        p_min,
        lat_min,
        lat_max,
        lon_min,
        lon_max,
        error_min,
        error_max,
    )
    plot1.add_title(title, loc="left", fontsize=title_fontsize, color="red", style="italic")
    plot1.add_ylabel("stats", fontsize=xy_label_fontsize)
    plot1.add_grid()
    plot1.set_xticks(x)
    plot1.set_xticklabels(x_str, rotation=90)
    plot1.add_legend(loc="upper left", fancybox=True, framealpha=0.80, ncols=len(expt_names))

    # Plot 2
    plot2.plot_layers = plt_list2
    plot2.add_xlabel("Time (UTC)", fontsize=xy_label_fontsize)
    plot2.add_ylabel("Number of Observations", fontsize=xy_label_fontsize)
    plot2.add_grid()
    plot2.set_xticks(x)
    plot2.set_xticklabels(x_str, rotation=90)
    plot2.add_legend(loc="upper left", fancybox=True, framealpha=0.80, ncols=len(expt_names))

    # Figure
    fig = CreateFigure(nrows=2, ncols=1, figsize=(8 * scale_fig_size, 6 * scale_fig_size))
    fig.plot_list = [plot1, plot2]
    fig.create_figure()  # must go before add_suptitle
    fig.add_suptitle("Obs Space Diagnostics (%s-%s)" % (dates[0], dates[-1]), ha="center", fontsize=suptitle_fontsize)
    fig.tight_layout()  # must go after add_suptitle
    fig.save_figure("obs_diag_%s.png" % (ob_type))

# Calculate time to run script
tictoc.toc(tic0, "End. ")
