# Coordinator for bindog project

from utils import manhattanDist
from simulator import simulator
import copy

import random



class robotTask(object):
  """docstring for robotTask"""
  def __init__(self, robot_id, locations, tasks):
    self.robot_id = robot_id
    self.locations = locations
    self.tasks = tasks
 
    



class coordinator():

  def __init__ (self, cord_method = 0):
    if cord_method == 0:
      print "Starting Greedy Coord"
    elif cord_method == 1:
      print "Starting Auction Coord"
    else:
      print "Invalid ID"
      return 0
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
    #print "Starting Greedy Coordination"

    task_allocation = []

    idle_bots = simulator.getIdleBots()
    assigned_bots = []

    random.shuffle(idle_bots)

    for bot in idle_bots:
      goal = self.findBestBin(bot, [], simulator)
      # print goal
      if goal is not None:
        loc = simulator.bins[goal].loc
        simulator.bins[goal].bot_assigned = True

        if simulator.bots[bot].hasBin():
          #task_allocation.append([bot, [loc], ['get']])
          task_allocation.append(robotTask(bot, [loc], ['get']))
        else:
          # Getting a bin then moving to goal location
          r_loc = simulator.bots[bot].loc
          r_loc = [r_loc[0],0]
          #task_allocation.append([bot, [r_loc,loc],['get', 'get']])
          task_allocation.append(robotTask(bot, [r_loc,loc], ['get', 'get']))
        assigned_bots.append(bot)

    for bot in assigned_bots:
      idle_bots.remove(bot)

    deliverys = simulator.getBinDeliveryRequests()

    for loc in deliverys:
      if idle_bots != []:
        c_bot = self.findClosestBot(loc, idle_bots, simulator)
        if simulator.bots[c_bot].hasBin():
          task_allocation.append([c_bot, [loc], ['drop']])
        else:
          # Getting a bin then moving to goal location
          r_loc = simulator.bots[c_bot].loc
          r_loc = [r_loc[0],0]
          task_allocation.append(robotTask(c_bot, [r_loc,loc],['get', 'drop']))
        idle_bots.remove(c_bot)

    return task_allocation

  def findBestBin(self, bot, exclude_bins, simulator):
    bins = simulator.bins # get the dictionary of bins
    best_bin = None
    best_score = float('inf')

    for bin in bins:
      if not(bins[bin].loc in exclude_bins) and not(bins[bin].bot_assigned):
        if self.binScore(bot, bin, simulator) < best_score:
          best_bin = bin
          best_score = self.binScore(bot, bin, simulator)

    return best_bin



  def binScore(self, bot, bin, simulator):
    score = manhattanDist(simulator.bins[bin].loc, simulator.bots[bot].loc)

    score += simulator.bins[bin].estimateTimeToFull()

    return score


  def auctionCord(self, simulator):
    task_allocation = []

    #Get idle bots, bins needing pickup, locations needing bin delivery
    idle_bots = simulator.getIdleBots() 
    deliverys = simulator.getBinDeliveryRequests() 

    # While still robots without plans
    still_planning = True
    prev_idle = copy.deepcopy(idle_bots)

    while still_planning:
      
      plans = []
      for bot in idle_bots:
        plans.append(self.getRobotPlan(bot, simulator))

      plans = self.findNonConflictPlan(plans)

      for plan in plans:
        if plan != []:
          c_bot = plan[0]
          loc = simulator.bins[plan[1]].loc
          simulator.bins[plan[1]].bot_assigned = True
          idle_bots.remove(c_bot)
          if simulator.bots[c_bot].hasBin():
            task_allocation.append(robotTask(c_bot, [loc], ['drop']))
          else:
            # Getting a bin then moving to goal location
            r_loc = simulator.bots[c_bot].loc
            r_loc = [r_loc[0],0]
            task_allocation.append(robotTask(c_bot, [r_loc,loc],['get', 'drop']))


      still_planning = not(idle_bots == [] or prev_idle == idle_bots)
      prev_idle = copy.deepcopy(idle_bots)

    for loc in deliverys:
      if idle_bots != []:
        c_bot = self.findClosestBot(loc, idle_bots, simulator)
        if simulator.bots[c_bot].hasBin():
          task_allocation.append(robotTask(c_bot, [loc], ['drop']))
        else:
          # Getting a bin then moving to goal location
          r_loc = simulator.bots[c_bot].loc
          r_loc = [r_loc[0],0]
          task_allocation.append(robotTask(c_bot, [r_loc,loc],['get', 'drop']))

        idle_bots.remove(c_bot)



    return task_allocation


  def getRobotPlan(self, bot, simulator):
    # score each plan by travel and wait time

    best_bin = self.findBestBin(bot, [], simulator)
    if best_bin is not None:
      return [bot, best_bin, self.binScore(bot, best_bin, simulator)]
    else:
      return []

  def findNonConflictPlan(self, plans):
    
    to_remove = []

    for i, plan in enumerate(plans):
      for j in range(i+1,len(plans)):
        if plan[1] == plans[j][1]: 
          if plan[2] <= plans[j][2]:
            to_remove.append(plans[j])
          else:
            to_remove.append(plan)
    
    for item in to_remove:
      if item in plans:
        plans.remove(item)

    return plans


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
  num_wkrs = 4
  sim = simulator(num_rows, row_size, num_bots, num_bins, num_wkrs)

  sim.wkrs[0].delivery = True

  cord = coordinator(cord_method=1)

  plans = cord.cordStep(sim)

  print "displaying the plans for the robots"
  for plan in plans:
    print plan

  sim.drawSimulator()

    # def greedyCord(self, simulator):
    
  #   print "Starting Greedy Coordination"
  #   # Greedily choose closest robot to each task needed to be completed

  #   task_allocation = []

  #   # Get idle bots, bins needing pickup, locations needing bin delivery
  #   idle_bots = simulator.getIdleBots()
  #   print idle_bots
  #   #bins = simulator.bins # We consider all bins
  #   pickups = simulator.getBinPickupRequests() 
  #   deliverys = simulator.getBinDeliveryRequests()

  #   # Loop through all pickup locations and assign then
  #   for loc in pickups:
      
  #     if idle_bots != []:
  #       c_bot = self.findClosestBot(loc, idle_bots, simulator)
  #       print simulator.bots[c_bot].loc
  #       print loc
  #       if simulator.bots[c_bot].hasBin():
  #         task_allocation.append([c_bot, [loc], ['get']])
  #       else:
  #         # Getting a bin then moving to goal location
  #         r_loc = simulator.bots[c_bot].loc
  #         r_loc = [r_loc[0],0]
  #         task_allocation.append([c_bot, [r_loc,loc],['get', 'get']])
  #       print "removing bot ", c_bot
  #       idle_bots.remove(c_bot)
  #       print idle_bots

  #   # Loop through all idle bots and find bins to go to
  #   random.shuffle(idle_bots)
  #   for bot in idle_bots:
  #     goal = self.findBestBin(bot, pickups, simulator)
  #     print goal
  #     if goal is not None:
  #       loc = simulator.bins[goal].loc
  #       simulator.bins[goal].bot_assigned = True
  #       if simulator.bots[bot].hasBin():
  #         task_allocation.append([c_bot, [loc], ['get']])
  #       else:
  #         # Getting a bin then moving to goal location
  #         r_loc = simulator.bots[c_bot].loc
  #         r_loc = [r_loc[0],0]
  #         task_allocation.append([c_bot, [r_loc,loc],['get', 'get']])
  #       print "removing bot ", bot
  #       idle_bots.remove(bot)
  #       print idle_bots

  #   # Loop through all delivery locations and assign then
  #   for loc in deliverys:
      
  #     if idle_bots != []:
  #       c_bot = self.findClosestBot(loc, idle_bots, simulator)
  #       print simulator.bots[c_bot].loc
  #       print loc
  #       if simulator.bots[c_bot].hasBin():
  #         task_allocation.append([c_bot, [loc], ['drop']])
  #       else:
  #         # Getting a bin then moving to goal location
  #         r_loc = simulator.bots[c_bot].loc
  #         r_loc = [r_loc[0],0]
  #         task_allocation.append([c_bot, [r_loc,loc],['get', 'drop']])
  #       print "removing bot ", c_bot
  #       idle_bots.remove(c_bot)
  #       print idle_bots


  #   return task_allocation