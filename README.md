# ECE470
Course timetable


data/data_1/ts:
	time slots 

data/data_1/courses:
	duration: prefered duration (2 hour or 3 hour)
	capacityLevel represent the maximun # of students
	duration: number of time slots that need to occupy for each class (Each course needs to have 6 hours of class each week)
	timePref: prefered time slot. 0 for any timeSlots startTime <= 12; 1 for >12

data/data_1/rooms:
	capLevel: amount of student it can have, rooms can be used for classes that have a lower or equal capacityLevel.
