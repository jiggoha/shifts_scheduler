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