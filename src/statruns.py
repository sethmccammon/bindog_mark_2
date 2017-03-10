# File to do stat runs

import matplotlib.pyplot as plt

from simulator import simulator
from coordinator import coordinator
from planner import planner
import time
import numpy as np

def statruns():

    num_runs = 100

    output_file = "../results/tLimited_auction.txt"

    file = open(output_file,'w')

    num_rows = 20
    row_len = 20
    num_bins = 100
    num_workers = 10
    num_bots = 5

    # 0 = greedy, 1 = auction based, 2= replanning
    coord_method = 2

    num_timestep = 100

    writeHeader(file, num_rows, row_len, num_bins, num_workers, num_bots, coord_method, num_timestep)

    file.write("percentage picked, ")
    file.write("time wasted\n")

    percent_picked = []

    for i in range(num_runs):

        sim = simulator(num_rows, row_len, num_bots, num_bins, num_workers)
        coord = coordinator(coord_method)
        plnr = planner(sim)

        for timestep in range(num_timestep):
            plan = coord.cordStep(sim)

            plan = plnr.getPlan(plan, sim)
    
            sim.step()

        percent_picked.append(sim.apples_picked / sim.total_apples * 100)
        file.write(str(sim.apples_picked / sim.total_apples * 100))
        file.write(", ")
        file.write(str(sim.wasted_time))
        file.write("\n")
        print "done running iteration: ", i
    print "mean percent picked: ", np.mean(percent_picked)
    print "std percent picked: ", np.std(percent_picked)

def writeHeader(file, num_rows, row_len, num_bins, num_workers, num_bots, coord_method, num_timestep):
    file.write("parameters\n")
    
    file.write("------------------------------------------------------------------\n")

    file.write("num_rows: ")
    file.write(str(num_rows))
    file.write("\n")

    file.write("row_len: ")
    file.write(str(row_len))
    file.write("\n")

    file.write("num_bins: ")
    file.write(str(num_bins))
    file.write("\n")

    file.write("num_workers: ")
    file.write(str(num_workers))
    file.write("\n")

    file.write("num_bots: ")
    file.write(str(num_bots))
    file.write("\n")

    file.write("coord method: ")
    file.write(str(coord_method))
    file.write("\n")

    file.write("num_timestep: ")
    file.write(str(num_timestep))
    file.write("\n")

    file.write("------------------------------------------------------------------\n")

if __name__ == '__main__':
    statruns()

