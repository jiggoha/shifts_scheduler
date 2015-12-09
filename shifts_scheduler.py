from __future__ import division
from times import *

TIME_BLOCKS = 10
times = Times(0, 10)

class Person:
  def __init__(self, name, hours_needed):
    self.name = name
    self.hours_needed = hours_needed
    self.adj_hours_avail = 0
    self.groups = []

  def __repr__(self):
    return "<name: %s, hours_needed: %d, adj_hours_avail: %d, num groups: %d>" % (self.name, self.hours_needed, self.adj_hours_avail, len(self.groups))

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


# names = ["a", "b", "c", "d", "e", "c"]
# starts = [1, 4, 1, 1, 8, 8]
# durations = [8, 4, 2, 2, 2, 2]  
# hours_needed = map(lambda x: x/2, durations)
# people = make_people(names, hours_needed)
# times = get_times(names, starts, durations)
# set_scores(times, people)
# order = sorted_people(people)