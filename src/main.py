import matplotlib.pyplot as plt

from simulator import simulator
from coordinator import coordinator
from planner import planner

def main():
  num_rows = 5
  row_len = 5
  num_bins = 30
  num_workers = 4
  num_bots = 2

  coord_method = 1

  num_timestep = 10000


  sim = simulator(num_rows, row_len, num_bots, num_bins, num_workers)
  coord = coordinator(coord_method)
  plnr = planner(sim)
  sim.drawSimulator()

  for timestep in range(num_timestep):
    plan = coord.cordStep(sim)

    for item in plan:
      print "Robot: ", item.robot_id
      print "Goals: ", item.locations

    plan = plnr.getPlan(plan, sim)
    # print "Planner Plan", plan
    sim.drawSimulator()


    for key in sim.bots.keys():
      print key, sim.bots[key].plan
    raw_input()
    sim.step()
  plt.show()
  return 0

if __name__ == '__main__':
	main()