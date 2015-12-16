# Shifts Scheduler
Final project for Automated Decision Systems (CPSC 458)

## Goal
The Yale Student Technology Collaborative (STC) hires over a hundred students each semester to staff the library's technology help walk-in office hours. It is important for the office to be supported during the day since students and faculty depend on its service. Therefore, when the STC managers assign shifts to student employees, they must take into account not only the time preferences of the employee, but also the constraint of ensuring that the office is staffed. For our final project, we decided to automate the process of deciding how to assign shifts to students based off of their time preferences.

## Constraints
1. Shift schedules are weekly. That is, the schedule recycles after each week.
2. Each student submits time preferences in shifts with a start time and end time for the week. They must input twice the number of hours they would like to work in order to give managers flexibility in assignment.
3. If a student submits one time slot, managers may elect to grant the student the entire time slot, a portion of the time slot, or not at all. ~~The managers should not assign two non-continuous portions of the same original time slot that the student requested.~~
4. The managers should do their best to meet the number of hours students would like to work. In the case that it is not possible to both meet the hours students would like to work and ensure that the office is always staffed, managers should give preference to students at the expense of the office's open hours.

## Abstractions
1. Instead of working with datetime objects, our algorithm takes in time as absolute, discrete numbers. The period of a schedule is also taken as input.

## Algorithm
#####1. Order of people assignment
We assign an inflexibility score to each student, where
```inflexibility(student) = k * hn / sum(c_i * t_i)```, where ```k``` is a positive constant, ```hn``` is the numbers of hours needed by the student, ```c_i``` is the number of competitors of a time slot the student has requested, and ```t_i``` is the length of time with ```c_i``` number of competitors.

Our algorithm greedily assigns shifts to the most inflexible student. Once it identifies the most inflexible student, it finds the longest continuous times which have the least number of competing students that also requested the same time. In the case of a tie, heuristics are used to assign the "best" time slots.

#####2. Order of time slots assignment
The following heuristics are used to assign the time slots to the most inflexible student:
* Select the time slot that minimizes the sum of increased inflexibility scores for all students affected by this assignment
* ~~If the time slot to be assigned must break up another student's request to two (since the second student cannot work during the hours that will be assigned to the most inflexible student), then choose the time slot such that it breaks up the other students slot most unevenness.~~

Once a time slot for the most inflexible student is chosen, recalculate the inflexibility scores of all students who were affected. Repeat choosing most inflexible student to assign a shift to, until either all students have their hours fulfilled or until there are no time slots left which can be assigned.
