# Shifts Scheduler
Final project for Automated Decision Systems (CPSC 458)
Project by Amelia Holcomb and Jay Hou.
Hosted at https://github.com/jiggoha/shifts_scheduler

## Goal
The Yale Student Technology Collaborative (STC) hires over a hundred students each semester to staff the library's technology help walk-in office hours. It is important for the office to be supported during the day since students and faculty depend on its service. Therefore, when the STC managers assign shifts to student employees, they must take into account not only the time preferences of the employee, but also the constraint of ensuring that the office is staffed. For our final project, we decided to automate the process of deciding how to assign shifts to students based off of their time preferences.

## Problem Domain
Our algorithm falls within the domain of scheduling problems. Many scheduling problems have been completely optimized by scheduling algorithms, which makes them less of a "decision system" -- there is no choice involved, because a "perfect" solution can be reached. However, we chose a scheduling problem that is more loosely defined. It is not always clear what the optimal solution should be, or if there even is one. Our algorithm tries to reconcile multiple student preferences with manager needs, proceeding at times as a human might when trying to judge the situation.

## Decision Methods Employed
Our algorithm employed a mathematical formulation of value, together with a rule-based system, to decide how to assign shifts. 
For the mathematical formula, we were inspired by the NPV calculations used to determine when to buy and sell stocks. In that decision system, the computer used a specific mathematically derived formula to decide when to buy and sell a stock based on its assessed value. For our project, we needed a way to decide when to assign a shift to a student, based on our assessment of the student's flexibility (likelihood of being able to take another, less popular, shift later on in the algorithm). We created our own mathematical formula to assess this "flexibility score", and it is that formula that governs which student we preference in assigning shifts at any given time. (See Algorithm)
On top of this, we also used a rule-based system to decide which shift (out of many possible preferences) to assign to a given student. We made rules to determine which shift intervals, if assigned, were more likely to lead to a successful solution. (See Algorithm) With more time, we would have added further rule-based heuristics to improve upon our solution. (See Future Steps)

## Constraints
1. Shift schedules are weekly. That is, the schedule recycles after each week.
2. Each student submits time preferences in shifts with a start time and end time for the week. They must input twice the number of hours they would like to work in order to give managers flexibility in assignment.
3. If a student submits one time slot, managers may elect to grant the student the entire time slot, a portion of the time slot, or not at all. 
4. The managers should do their best to meet the number of hours students would like to work. In the case that it is not possible to both meet the hours students would like to work and ensure that the office is always staffed, managers should give preference to students at the expense of the office's open hours.

## Abstractions
1. Instead of working with datetime objects, our algorithm takes in time as absolute, discrete numbers. The period of a schedule is also taken as input.

## Algorithm
#####1. Order of people assignment
We assign an inflexibility score to each student, where
```inflexibility(student) = k * hn / sum(c_i * t_i)```, where ```k``` is a positive constant, ```hn``` is the numbers of hours needed by the student, ```c_i``` is the number of competitors of a time slot the student has requested, and ```t_i``` is the length of time with ```c_i``` number of competitors.

Our algorithm greedily assigns shifts to the most inflexible student. Once it identifies the most inflexible student, it finds the longest continuous times which have the least number of competing students that also requested the same time. In the case of a tie, heuristics are used to assign the "best" time slots.

#####2. Order of time slots assignment
In addition to the main algorithm, the following heuristics are used to assign the time slots to the most inflexible student:
* Select the time slot that minimizes the sum of increased inflexibility scores for all students affected by this assignment
(See also Future Steps)

Once a time slot for the most inflexible student is chosen, recalculate the inflexibility scores of all students who were affected. Repeat choosing most inflexible student to assign a shift to, until either all students have their hours fulfilled or until there are no time slots left which can be assigned.

## Implementation
##### Format of input
Example:
```
Name,HoursNeeded,Start1,End1,...
A,4,1,9
B,2,4,8
C,2,1,3,8,10
D,1,1,3
E,1,8,10
```

##### Sample Input and Output
Requested shifts:
```
0    1    2    3    4    5    6    7    8    9    10    
|----|----|----|----|----|----|----|----|----|----|

     |---------------------------------------|        A
                    |-------------------|             B
     |---------|                        |---------|   C
     |---------|                                      D
                                        |---------|   E

|----|----|----|----|----|----|----|----|----|----|
0    1    2    3    4    5    6    7    8    9    10
```

Assigned shifts:
```
0    1    2    3    4    5    6    7    8    9    10    
|----|----|----|----|----|----|----|----|----|----|

               |----|         |--------------|        A
                    |---------|                       B
     |---------|                                      C
                                                      D
                                             |----|   E

|----|----|----|----|----|----|----|----|----|----|
0    1    2    3    4    5    6    7    8    9    10    

Warning: D still needs 1 more hours.
```

## Future Steps
With more time, there are a couple of additional heuristics/rule-based decisions that we would like to have implemented. 

1. Prefer not to assign students multiple non-continuous shifts within the same five hours whenever possible.
2. If the time slot to be assigned must break up another student's request to two (since the second student cannot work during the hours that will be assigned to the most inflexible student), then choose the time slot such that it breaks up the other student's slot most unevenly.
