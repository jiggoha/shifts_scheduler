class Times:
  def __init__(self, start, end):
    self.start = start
    self.end = end
    self.blocks = []
    self.total_hours = end

    for i in range(end - start):
      b = Block(start + i)
      self.blocks.append(b)

  def __repr__(self):
    return "<start: %d, end: %d>" % (self.start, self.end)

  def pretty_print(self, population):
    for i in range(self.total_hours):
      print("%d    " % (i))
    print("\n")

  def add_request(self, person, start, end):
    for i in range(start, end):
      self.blocks[i].add_request(person)

  def remove_request(self, start, end, person=None):
    if person:
      for i in range(start, end):
        self.blocks[i].remove_request(person)
    else:
      for i in range(start, end):
        self.blocks[i].requested_by = []
        self.blocks[i].num_people = 0


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
