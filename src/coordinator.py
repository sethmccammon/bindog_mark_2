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

		# Get idle bots, bins needing pickup, locations needing bin delivery
		idle_bots = simulator.getIdleBots()
		
		#bins = simulator.bins # We consider all bins
		pickups = simulator.getBinPickupRequests() 
		delivery = simulator.getBinDeliveryRequests()

		# Loop through all pickup locations and assign then
		for loc in pickups:
			
			if idle_bots != []:
				c_bot = self.findClosestBot(loc, idle_bots, simulator)
				print simulator.bots[c_bot].loc
				print loc
				if simulator.bots[c_bot].hasBin():
					task_allocation.append([c_bot, [loc], ['get']])
				else:
					# Getting a bin then moving to goal location
					r_loc = simulator.bots[c_bot].loc
					r_loc = [r_loc[0],0]
					task_allocation.append([c_bot, [r_loc,loc],['get', 'get']])

				idle_bots.remove(c_bot)

		# Loop through all non-full bins
		for bot in idle_bots:
			goal = findBestBin(bot, pickups, simulator)

			if goal is not None:
				loc = simulator.bins[goal].loc
				simulator.bins[goal].bot_assigned = True
				if simulator.bots[bot].hasBin():
					task_allocation.append([c_bot, [loc], ['get']])
				else:
					# Getting a bin then moving to goal location
					r_loc = simulator.bots[c_bot].loc
					r_loc = [r_loc[0],0]
					task_allocation.append([c_bot, [r_loc,loc],['get', 'get']])

		# Loop through all delivery locations and assign then
		for loc in delivery:
			
			if idle_bots != []:
				c_bot = self.findClosestBot(loc, idle_bots, simulator)
				print simulator.bots[c_bot].loc
				print loc
				if simulator.bots[c_bot].hasBin():
					task_allocation.append([c_bot, [loc], ['drop']])
				else:
					# Getting a bin then moving to goal location
					r_loc = simulator.bots[c_bot].loc
					r_loc = [r_loc[0],0]
					task_allocation.append([c_bot, [r_loc,loc],['get', 'drop']])

				idle_bots.remove(c_bot)


		return task_allocation

	def findBestBin(self, bot, exclude_bins, simulator):
		bins = simulator.bins # get the dictionary of bins
		best_bin = None
		best_score = float('inf')

		for bin in bins:
			if not(bins[bin].loc in exclude_bins) and not(bins[bin].bot_assigned):
				if binScore(bot, bin, simulator) < best_score:
					best_bin = bin
					best_score = binScore(bot, bin, simulator)

		return best_bin



	def binScore(self, bot, bin, simulator):
		score = manhattanDist(simulator.bins[bin].loc, simulator.bots[bot].loc)

		score += simulator.bins[bin].estimateTimeToFull()

		return score


	def auctionCord(self, simulator):
		
		idle_bots = simulator.getIdleBots()

		#Get idle bots, bins needing pickup, locations needing bin delivery
		idle_bots = simulator.getIdleBots()
		goals += simulator.getBinPickupRequests() 
		goals += simulator.getBinDeliveryRequests() 

		# While still robots without plans
		while idle_bots != []:
			plans = []
			for bot in idle_bots:
				plans.append(getRobotPlan(bot, goals, simulator))

			plans = findNonConflictPlan(plans)

			for plan in plans:
				idle_bots.remove(plan[0])

		# All robots without plan calculate preferred plan
		# Check conflict - if it exists, then auction
		# Loop with robots that don't have a plan

		return None


	def getRobotPlan(self, bot, goals, simulator):
		# score each plan by travel and wait time

		return []

	def findNonConflictPlan(self, plans):
		return []


	def findClosestBot(self, loc, bots, simulator):
		# Probably need to write different distance function - not manhattan but up and down + sideways
		dist = float('inf')
		c_bot = None

		for item in bots:

			d = manhattanDist(loc, simulator.bots[item].loc)

			if d < dist:
				dist = d
				c_bot = item

		return c_bot

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