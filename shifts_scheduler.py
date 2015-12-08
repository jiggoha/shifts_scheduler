from __future__ import division
from intervaltree import Interval, IntervalTree

TIME_BLOCKS = 10

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


names = ["a", "b", "c", "d", "e", "c"]
starts = [1, 4, 1, 1, 8, 8]
durations = [8, 4, 2, 2, 2, 2]  
hours_needed = map(lambda x: x/2, durations)
people = make_people(names, hours_needed)
times = get_times(names, starts, durations)
set_scores(times, people)
order = sorted_people(people)