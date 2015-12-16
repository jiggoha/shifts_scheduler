from intervals import *

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