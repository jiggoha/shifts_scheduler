import pdb

from times import *
from people import *

final_schedule = Times(0, TOTAL_HOURS)

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
