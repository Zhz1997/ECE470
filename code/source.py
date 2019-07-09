import sys,os
from classRoom import ClassRoom
from course import Course
from timeSlot import TimeSlot


def getRooms(rooms,roomsFile):
    lines = [line.rstrip('\n') for line in roomsFile]

    for i in range(1,len(lines)):
        content = lines[i].split(",")
        room = ClassRoom(content[0],content[1])
        rooms.append(room)
    return rooms

def getCourses(courses,courseFile):
    lines = [line.rstrip('\n') for line in courseFile]

    for i in range(1,len(lines)):
        content = lines[i].split(",")
        course = Course(content[0],content[1],content[2],content[3])
        courses.append(course)
    return courses

def getTimeSlots(timeSlots,timeSlotFile):
    lines = [line.rstrip('\n') for line in timeSlotFile]

    for i in range(1,len(lines)):
        content = lines[i].split(",")
        timeSlot = TimeSlot(content[0],content[1],content[2])
        timeSlots.append(timeSlot)
    return timeSlots


def main():
    #get path to data folder
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/data/data_1"
    roomsPath = path + "/rooms.csv"
    timeSlotPath = path + "/timeSlot.csv"
    coursePath = path+"/courses.csv"

    #open files
    roomsFile = open(roomsPath,encoding = 'utf-8')
    timeSlotFile = open(timeSlotPath,encoding = 'utf-8')
    courseFile = open(coursePath,encoding = 'utf-8')

    #create lists to store rooms,courses,timeSlots
    rooms = []
    courses = []
    timeSlots = []

    #store values into the lists
    rooms = getRooms(rooms,roomsFile)
    courses = getCourses(courses,courseFile)
    timeSlots = getTimeSlots(timeSlots,timeSlotFile)


    #print statement for debug purpose
    print("rooms:")
    for i in range(0,len(rooms)):
        print("id: "+rooms[i].getId()+" "+"capLevel: "+rooms[i].getCapLevel())

    print("courses:")
    for i in range(0,len(courses)):
        print("id: "+courses[i].getId()+" "+"capLevel: "+courses[i].getCapLevel()+" duration: "+courses[i].getDuration()+" timePref: "+courses[i].getTimePref())

    print("timeSlots:")
    for i in range(0,len(timeSlots)):
        print("id: "+timeSlots[i].getId()+" "+"date: "+timeSlots[i].getDate()+" startTime: "+timeSlots[i].getStartTime())


if __name__ == '__main__':
    main()
