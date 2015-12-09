class Times:
  def __init__(self, start, end):
    self.start = start
    self.end = end
    self.blocks = []

    for i in range(end - start):
      b = Block(start + i)
      self.blocks.append(b)

  def __repr__(self):
    return "<start: %d, end: %d>" % (self.start, self.end)

  def add_request(self, person, start, end):
    for i in range(start, end):
      self.blocks[i].add_request(person)

  def remove_request(self, person, start, end):
    for i in range(start, end):
      self.blocks[i].remove_request(person)

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
    # TODO: update people?

  def remove_request(self, person):
    self.requested_by.remove(person)
    self.num_people -= 1
    # TODO: update people?