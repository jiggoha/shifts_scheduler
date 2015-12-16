
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