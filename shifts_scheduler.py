#!/usr/bin/python
from __future__ import division
from __future__ import print_function

import pdb
import csv
import sys

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

####################################  intervals.py  #############################################################
####################################  intervals.py  #############################################################
####################################  intervals.py  #############################################################
####################################  intervals.py  #############################################################

class Group:
  def __init__(self, start, end, person):
    self.start = start
    self.end = end
    self.person = person
    self.intervals = [Interval(start, end, self)]

  def __repr__(self):
    return "<start: %d, end: %d, num intervals: %d>" % (self.start, self.end, len(self.intervals))

  def add_interval(self, start, end):
    self.intervals.append(Interval(start, end, self))

  def delete_interval(self, interval):
    self.intervals.remove(interval)
    if (len(self.intervals) == 0):
      self.person.delete_group(self)

  def delete(self):
    self.person.remove_group(self)

  def slice(self, start, end):
    for interval in self.intervals:
      if start >= interval.start and end <= interval.end:
        interval.slice(start, end)
        return
    raise Exception("Not within interval.")

class Interval:
  def __init__(self, start, end, group):

    self.start = start
    self.end = end
    self.group = group
    self.blocks = []

    for i in range(start, end):
      self.blocks.append(times.blocks[i])

  def __repr__(self):
    return "<start: %d, end: %d>" % (self.start, self.end)

  def delete(self):
    self.group.delete_interval(self)

  def slice(self, start, end):
    # slice the whole thing:
    if start == self.start and end == self.end:
      self.delete()

    # slice in the middle
    elif start > self.start and end < self.end:
      # create second one as a result of slice
      self.group.add_interval(end, self.end)
      # cut the interval to create first one
      self.end = start
    
    # slice lines up in the beginning
    elif start == self.start:
      # update group's start
      if self.group.start == self.start:
        self.group.start = end
      self.start = end

    # slice lines up at the end
    elif end == self.end:
      # update group's end
      if self.group.end == self.end:
        self.group.end = start
      self.end = start
    else:
      raise Exception("Not within interval.")

    to_remove = []
    for b in self.blocks:
      if b.start >= start and b.end <= end:
        b.remove_request(self.group.person)
        to_remove.append(b)

    for b in to_remove:
      self.remove_block(b)

  def remove_block(self, block):
    self.blocks.remove(block)

####################################  people.py  #############################################################
####################################  people.py  #############################################################
####################################  people.py  #############################################################
####################################  people.py  #############################################################

class Population:
  def __init__(self):
    self.num_people = 0
    self.people = []

  def __repr__(self):
    return "<num people: %d>" % (self.num_people)

  def add_person(self, new_people):
    self.num_people += len(new_people)
    self.people.extend(new_people)

    for new_person in new_people:
      new_person.population = self

  def sort(self):
    return sorted(self.people, key=lambda person: person.score, reverse=True)

class Person:
  def __init__(self, name, hours_needed):
    self.name = name
    self.hours_needed = hours_needed
    self.adj_hours_avail = 0
    self.score = 0
    self.groups = []
    self.population = None
    self.final = []

  def __repr__(self):
    return "<name: %s, hours_needed: %d, score: %f, num groups: %d>" % (self.name, self.hours_needed, self.score, len(self.groups))

  def set_score(self):
    self.set_adj_hours_avail()
    if self.adj_hours_avail != 0:
      self.score = self.hours_needed / self.adj_hours_avail
    else:
      self.score = 0

  def set_adj_hours_avail(self):
    self.adj_hours_avail = 0

    for group in self.groups:
      for interval in group.intervals:
        for block in interval.blocks:
          self.adj_hours_avail += block.num_people

  def add_group(self, start, end):
    self.groups.append(Group(start, end, self))

  def delete_group(self, group):
    self.groups.remove(group)

  def slice(self, start, end):
    for group in self.groups:
      if start >= group.start and end <= group.end:
        group.slice(start, end)
        return
    raise Exception("Not within group.")

  def find_intervals_to_assign(self):
    min_conflict = self.population.num_people + 1
    curr_int_start = curr_int_end = 0
    max_int_len = 0
    interval_list = []

    for group in self.groups:
      for interval in group.intervals:
        for block in interval.blocks:
          if block.num_people < min_conflict:                   ## new minimum conflict
            interval_list = []
            min_conflict = block.num_people
            curr_int_start = block.start
            curr_int_end = block.end
          elif block.num_people == min_conflict:                ## same minimum conflict
            if block.start == curr_int_end:                       ## still part of current interval
              curr_int_end = block.end
            else:                                                 ## new interval
              curr_int_len = curr_int_end - curr_int_start
              if curr_int_len > max_int_len:       ## new maximum length
                interval_list = [(curr_int_start, curr_int_end)]
              elif curr_int_len == max_int_len:    ## same maximum length
                interval_list.append((curr_int_start, curr_int_end))
              curr_int_start = block.start
              curr_int_end = block.end
    interval_list.append((curr_int_start, curr_int_end))

    return interval_list

####################################  times.py  #############################################################
####################################  times.py  #############################################################
####################################  times.py  #############################################################
####################################  times.py  #############################################################

class Times:
  def __init__(self, start, end):
    self.start = start
    self.end = end
    self.blocks = []
    self.total_hours = end

    for i in range(end - start):
      b = Block(start + i)
      self.blocks.append(b)

  def __repr__(self):
    return "<start: %d, end: %d>" % (self.start, self.end)

  def pretty_print_assigned(self, population):
    # print "timeline"
    for i in range(self.total_hours + 1):
      print("%d    " % (i), end = "")
    print("\n", end = "")

    for i in range(self.total_hours):
      print("|----", end = "")
    print("|\n")

    # print people's shifts
    for person in population.people:
      shifts = sorted(person.final)
      
      in_shift = False
      print_four = False
      for i in range(self.total_hours):
        if person in self.blocks[i].requested_by:
          if not in_shift:
            print("|----", end = "")
          else:
            print("-----", end = "")
          in_shift = True
        else:
          if print_four:
            print("    ", end = "")
            print_four = False
          else:
            print("     ", end = "")
    
        # end of a shift
        if (i + 1) < self.total_hours and in_shift and person not in self.blocks[i + 1].requested_by:
          print("|", end = "")
          in_shift = False
          print_four = True

      if in_shift:
        print("|  ", person.name)
      else:
        print("   ", person.name)

    # print "timeline"
    print("\n", end = "")
    for i in range(self.total_hours):
      print("|----", end = "")
    print("|")

    for i in range(self.total_hours + 1):
      print("%d    " % (i), end = "")
    print("\n", end = "")

  def add_request(self, person, start, end):
    for i in range(start, end):
      self.blocks[i].add_request(person)

  def remove_request(self, start, end, person=None):
    if person:
      for i in range(start, end):
        self.blocks[i].remove_request(person)
    else:
      for i in range(start, end):
        self.blocks[i].requested_by = []
        self.blocks[i].num_people = 0


class Block:
  def __init__(self, start):
    self.start = start
    self.end = start + 1
    self.requested_by = []
    self.num_people = 0

  def __repr__(self):
    return "<start: %d, requested by %d>" % (self.start, self.num_people)

  def add_request(self, person):
    self.requested_by.append(person)
    self.num_people += 1

  def remove_request(self, person):
    self.requested_by.remove(person)
    self.num_people -= 1

############################################# main ########################################################
############################################# main ########################################################
############################################# main ########################################################
############################################# main ########################################################

def schedule_shifts():
  for person in pop.people:
    person.set_score()
  order = pop.sort()
  person = order[0]

  while(person.hours_needed != 0):
    print(bcolors.WARNING + "Current requests schedule:" + bcolors.ENDC)
    times.pretty_print_assigned(pop)
    print("\n")

    print("\n")
    print(bcolors.OKGREEN + "Since " + person.name + " is most inflexible person with a score of " + str(person.score) + ", they will be assigned hours next." + bcolors.ENDC)

    intervals = person.find_intervals_to_assign()

    # interval choice heuristics
    interval = intervals[0]
    start, end = interval
    duration = person.hours_needed
    if(end - start > duration):
      minimum = sys.maxint
      minimum_start = start
      
      for possible_start in range(start, end - duration + 1):
        effect = 0
        for i in range(possible_start, possible_start + duration):
          people_affected = times.blocks[i].requested_by
          for person_affected in people_affected:
            effect += person_affected.score
        if effect < minimum:
          minimum = effect
          minimum_start = possible_start
      interval = (minimum_start, minimum_start + duration)

    print("\t" + person.name + " has been assigned a shift from " + str(start) + " to " + str(end) + ", which is least likely to conflict with another student later on.")
    assign_shift(interval, person)

    order = pop.sort()
    person = order[0]



def assign_shift(shift, person):
  start = shift[0]
  end = shift[1]
  duration = end - start

  final_schedule.add_request(person, start, end)
  person.final.append((start, end))
  person.hours_needed -= duration

  if person.hours_needed == 0:
    print("\t" + person.name + "'s requested time has been satifised by being assigned " + str(duration) + " more hours.")

    to_remove = list(person.groups)
    for group in to_remove:
      person.delete_group(group)
    for block in times.blocks:
      if person in block.requested_by:
        block.requested_by.remove(person)
  else:
    print("\t%s has been assigned %d more hours, and still needs %d hours." %  (person.name, duration, person.hours_needed))
    

  for block in times.blocks[start:end]:
    to_slice = list(block.requested_by)
    for person in to_slice:
      person.slice(block.start, block.end)

  for p in pop.people:
    p.set_score()


if __name__ == '__main__':
  if len(sys.argv) != 3:
    sys.exit("Usage: shifts_scheduler input_path num_blocks")

  TOTAL_HOURS = int(sys.argv[2])
  times = Times(0, TOTAL_HOURS)
  final_schedule = Times(0, TOTAL_HOURS)

  pop = Population()

  filepath = sys.argv[1]
  with open(filepath, 'rb') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',')
    next(filereader, None)  # skip header
    
    for row in filereader:
      (name, hours_needed), starts_ends = row[:2], row[2:]
      person = Person(name, int(hours_needed))
      pop.add_person([person])
      for i in range(0, len(starts_ends), 2):
        start = int(starts_ends[i])
        end = int(starts_ends[i+1])

        person.add_group(start, end)
        for j in range(start, end):
          times.blocks[j].add_request(person)

  print(bcolors.FAIL + bcolors.BOLD + "This log explains each step in the decision process. For a larger overview of the problem and our approach, please see the README.md.")
  print("\n", end = "")
  print("Project hosted at https://github.com/jiggoha/shifts_scheduler" + bcolors.ENDC)
  print("\n")

  schedule_shifts()

  print("\n")
  print(bcolors.OKBLUE + "Final schedule:\n" + bcolors.ENDC)
  final_schedule.pretty_print_assigned(pop)

  print("\n")
  for person in pop.people:
    if person.hours_needed != 0:
      print(bcolors.WARNING + "Warning: " + person.name + " still needs " + str(person.hours_needed) + " more hours." + bcolors.ENDC)

  print("\n")
  print(bcolors.FAIL + bcolors.BOLD + "This log explains each step in the decision process. For a larger overview of the problem and our approach, please see the README.md.")
  print("\n", end = "")
  print("Project hosted at https://github.com/jiggoha/shifts_scheduler" + bcolors.ENDC)