from __future__ import division
from times import *

times = Times(0, 10)

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

  def __repr__(self):
    return "<name: %s, hours_needed: %d, adj_hours_avail: %d, num groups: %d>" % (self.name, self.hours_needed, self.adj_hours_avail, len(self.groups))

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

  def intervals_to_assign(self):
    min_conflict = self.population.num_people + 1
    curr_int_start = curr_int_end = min_int_start = min_int_end = 0
    max_int_len = 0
    interval_list = []

    for group in person.groups:
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

    return interval_list

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
    global times

    self.start = start
    self.end = end
    self.group = group
    self.blocks = []

    for i in range(start, end):
      self.blocks.append(times.blocks[i])
      times.blocks[i].add_request(group.person)

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
      if self.group.start == self.start:
        self.group.start = end
      self.start = end

    # slice lines up at the end
    elif end == self.end:
      if self.group.end == self.end:
        self.group.end = start
      self.end = start
    else:
      raise Exception("Not within interval.")

    for b in blocks:
      if start >= b.start and end <= b.end:
        b.remove_request(self.group.person)

pop = Population()

times = Times(0, 10)
amelia = Person("Amelia", 2)
amelia.add_group(0, 3)
amelia.add_group(5, 6)

jay = Person("Jay", 3)
jay.add_group(2, 8)

alex = Person("Alex", 2)
alex.add_group(6, 10)

frances = Person("Frances", 2)
frances.add_group(1, 3)
frances.add_group(8, 10)

shona = Person("Shona", 1)
shona.add_group(5, 7)

pop.add_person([amelia, jay, alex, frances, shona])

for person in pop.people:
  person.set_score()