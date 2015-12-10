from shifts_scheduler import *

##### TEST 1 ######

pop = Population()
# final_schedule = Times(0, 10)
# times = Times(0, 10)

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

pop.add_person([amelia,jay,alex,frances,shona])

for person in pop.people:
  person.set_score()

pop.sort()

##### TEST 2 ######

pop = Population()
final_schedule = Times(0, 10)
times = Times(0, 10)

a = Person("A", 4)
a.add_group(1, 9)

b = Person("B", 2)
b.add_group(4, 8)

c = Person("C", 2)
c.add_group(1, 3)
c.add_group(8, 10)

d = Person("D", 1)
d.add_group(1, 3)

e = Person("E", 1)
e.add_group(8, 10)

pop.add_person([a,b,c,d,e])

for person in pop.people:
  person.set_score()

pop.sort()