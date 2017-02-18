# Coordinator for bindog project

from utils import manhattanDist
from simulator import simulator

import random

class coordinator():

	def __init__ (self, cord_method = 0):
		self.cord_method = cord_method

	def cordStep(self, simulator):
		# Command loop

		if self.cord_method == 0:
			# Use the greedy method of coordination
			return self.greedyCord(simulator)
		elif self.cord_method == 1:
			# Use Yawei's method of coordination
			return self.auctionCord(simulator)
		else:
			pass

	def greedyCord(self, simulator):
		
		print "Starting Greedy Coordination"
		# Greedily choose closest robot to each task needed to be completed

		task_allocation = []
		goals = []

		# Get idle bots, bins needing pickup, locations needing bin delivery
		idle_bots = simulator.getIdleBots()
		goals += simulator.getBinPickupRequests() 
		goals += simulator.getBinDeliveryRequests()

		print goals

		# Loop through all goal locations and assign then
		for loc in goals:
			
			if idle_bots != []:
				c_bot = findClosestBot(loc, idle_bots, simulator)
				if simulator.bots[c_bot].bin != None:
					task_allocation.append([c_bot, [loc]])
				else:
					# Getting a bin then moving to goal location
					r_loc = simulator.bots[c_bot].loc
					r_loc = [r_loc[0],0]
					task_allocation.append([c_bot, [r_loc,loc]])


		return task_allocation

	def auctionCord(self, simulator):
		
		idle_bots = simulator.getIdleBots()
		return None


	def findClosestBot(loc, bots, simulator):
		# Probably need to write different distance function - not manhattan but up and down + sideways
		dist = float('inf')
		c_bot = None

		for item in bots:
			d = manhattanDist(loc, simulator.bots[item])

			if d < dist:
				dist = d
				c_bin = item

if __name__ == '__main__':

	num_rows = 10
  	row_size = 10
  	num_bots = 5
  	num_bins = 0
  	num_wkrs = 15
  	sim = simulator(num_rows, row_size, num_bots, num_bins, num_wkrs)

	cord = coordinator()

	print cord.cordStep(sim)

	sim.drawSimulator()