#!/usr/bin/python
from __future__ import division

import pdb
import csv
import sys

from times import *
from intervals import *
from groups import *
from people import *


if __name__ == '__main__':

  TOTAL_HOURS = int(sys.argv[2])
  times = Times(0, TOTAL_HOURS)
  final_schedule = Times(0, TOTAL_HOURS)

  pop = Population()

  filepath = sys.argv[1]
  with open(filepath, 'rb') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',')
    next(filereader, None)  #skip header
    for row in filereader:
      (name, hours_needed), starts_ends = row[:2], row[2:]
      person = Person(name, int(hours_needed))
      pop.add_person([person])
      for i in range(0, len(starts_ends), 2):
        person.add_group(int(starts_ends[i]), int(starts_ends[i+1]))

  for person in pop.people:
    print(person)

  schedule_shifts()


def schedule_shifts():

    order = pop.sort()
    while(order[0].hours_needed != 0):
      intervals = order[0].find_intervals_to_assign()

      #interval choice heuristics
      interval = intervals[0]

      assign_shift(interval, person)
      order = pop.sort()


def assign_shift(shift, person):

  start = shift[0]
  end = shift[1]
  dur = end - start

  final_schedule.add_request(person, start, end)
  person.hours_needed -= dur
  if person.hours_needed == 0:
    to_remove = person.groups
    for group in to_remove:
      person.delete_group(group)

  affected_persons = []
  for block in times.blocks[start:end]:
    to_slice = block.requested_by
    for person in to_slice:
      person.slice(block.start, block.end)
    affected_persons = list(set(affected_persons)|set(to_slice))

  for person in affected_persons:
    person.set_score
