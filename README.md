# ECE470
Course timetable


data/data_1/timeSlot: 
	date represent monday,tuesday.....; 
	startTime represent the start time of the time slot, each time slot has a duration of 1 hour.

data/data_1/courses:
	capacityLevel represent the maximun # of students
	duration: number of time slots that need to occupy for each class (Each course needs to have 6 hours of class each week)
	timePref: prefered time slot. 0 for any timeSlots startTime <= 12; 1 for >12

data/data_1/rooms:
	capLevel: amount of student it can have, rooms can be used for classes that have a lower or equal capacityLevel. 
 
