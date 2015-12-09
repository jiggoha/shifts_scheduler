from __future__ import division
#from intervaltree import Interval, IntervalTree

TIME_BLOCKS = 10    #total number of time blocks
NUM_PEOPLE = 10     #number of people who submitted shift requests

class Person:
  def __init__(self, name, hours_needed):
    self.name = name
    self.hours_needed = hours_needed
    self.adj_hours_avail = 0
    self.groups = []

  def __repr__(self):
    return "name: %s, hours_needed: %d, adj_hours_avail: %d, num groups: %d" % (self.name, self.hours_needed, self.adj_hours_avail, len(self.groups))

  def add_group(self, start, end):
    self.groups.append(Group(start, end, self))

  def remove_group(self, group):
    self.groups.remove(group)

class Group:
  def __init__(self, start, end, person):
    self.start = start
    self.end = end
    self.intervals = [Interval(start, end, self)]
    self.person = person

  def __repr__(self):
    return "(start: %d, end: %d)" % (self.start, self.end)

  def add_interval(self, start, end):
    self.intervals.append(Interval(start, end, group))

  def remove_interval(self, interval):
    self.intervals.remove(interval)
    if (len(self.intervals) == 0):
      self.person.remove_group(self)

  def remove(self):
    self.person.remove_group(self)

class Interval:
  def __init__(self, start, end, group):
    self.start = start
    self.end = end
    self.group = group

  def __repr__(self):
    return "(start: %d, end: %d)" % (self.start, self.end)

  def remove(self):
    self.group.remove_interval(self)

def get_times(names, starts, durations):
  times = [[] for i in range(TIME_BLOCKS)]

  for i in range(len(names)):
    for j in range(starts[i], starts[i] + durations[i]):
      times[j].append(names[i])

  return times

def make_people(names, hours_needed):
  people = {}
  for i in range(len(names)):
    people[names[i]] = Person(names[i], hours_needed[i])
  return people

def set_scores(times, people):
  for person in people.values():
    person.adj_hours_avail = 0

  for names_list in times:
    for name in names_list:
      people[name].adj_hours_avail += len(names_list)

  for name, person in people.items():
    if person.adj_hours_avail == 0:
      person.score = 0
    else:
      person.score = person.hours_needed / person.adj_hours_avail

def sorted_people(people):
  return sorted(people.items(), key=lambda person: person[1].score, reverse=True)

def next_person(people):
  max_score = -1
  max_person = people[0]

  for person in people:
    if person.score > max_score:
      max_score = person.score
      max_person = person

  return person

def find_block(person):
  min_conflict = NUM_PEOPLE + 1
  curr_int_start = curr_int_end = min_int_start = min_int_end
  max_int_len = 0
  interval_list = []

  for group in person.groups:
    for interval in group.intervals:
      for block in interval:
        if block.num_people < min_conflict:                   ## new minimum conflict
          interval_list = []
          min_conflict = block.num_people
        elif block.num_people == min_conflict:                ## same minimum conflict
          if block.start == curr_int_end:                       ## still part of current interval
            curr_int_end = block.end
          else:                                                 ## new interval
            if curr_int_end - curr_int_start > max_int_len:       ## new maximum length
              interval_list = [(curr_int_start, curr_int_end)]
            elif curr_int_end - curr_int_start == max_int_len:    ## same maximum length
              interval_list.append((curr_int_start, curr_int_end))
            curr_int_start = curr_int_end = block.end

  return interval_list








