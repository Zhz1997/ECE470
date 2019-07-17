import sys,os
import random
import numpy as np
from chromosome import Chromosome
from classRoom import ClassRoom
from course import Course
from timeSlot import TimeSlot
from gene import Gene

#print helper functions
def debug1():
    #print statement for debug purpose
    print("rooms:")
    for i in range(0,len(rooms)):
        print("id: "+rooms[i].id+" "+"capLevel: "+rooms[i].capLevel)

    print("courses:")
    for i in range(0,len(courses)):
        print("id: "+courses[i].getId()+" "+"capLevel: "+courses[i].getCapLevel()+" duration: "+courses[i].getDuration()+" timePref: "+courses[i].getTimePref())

    print("timeSlots:")
    for i in range(0,len(timeSlots)):
        print("id: "+timeSlots[i].getId()+" "+"date: "+timeSlots[i].getDate()+" startTime: "+timeSlots[i].getStartTime())
def printGene(gene):
    print("gene: courseID = " + str(gene.courseID)
    + " roomID = " + str(gene.roomID)
    + " date = " + str(gene.date)
    + " tsID = " + str(gene.tsID))
def printChrom(chrom):
    print("chromosom: ID = " + str(chrom.id)
    + " fitness = " + str(chrom.fitness)
    + " scv = " + str(chrom.scv)
    + " hcv = " + str(chrom.hcv))

#------------------------------------
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

def createFirstGen(firstGen,rooms,courses,timeSlots):
    for i in range (0,10):
        genes = []
        for c in courses:
            roomID = random.randint(1,len(rooms))
            dates = [1,2,3,4,5]
            courseDates = []
            ts = []
            if(c.duration == "2"):
                random.shuffle(dates)
                courseDates.append(dates[0])
                courseDates.append(dates[1])
                courseDates.append(dates[2])

                ts_ini = random.randint(1,10)
                if(ts_ini % 2 == 0):
                    ts.append(ts_ini-1)
                    ts.append(ts_ini)
                else:
                    ts.append(ts_ini)
                    ts.append(ts_ini+1)

            elif(c.duration == "3"):
                random.shuffle(dates)
                courseDates.append(dates[0])
                courseDates.append(dates[1])

                ts_ini = random.randint(1,10)
                if(ts_ini == 1):
                    ts.append(ts_ini)
                    ts.append(ts_ini+1)
                    ts.append(ts_ini+2)
                elif(ts_ini == 10):
                    ts.append(ts_ini-2)
                    ts.append(ts_ini-1)
                    ts.append(ts_ini)
                else:
                    ts.append(ts_ini-1)
                    ts.append(ts_ini)
                    ts.append(ts_ini+1)

            curGene = Gene(c.id,roomID,courseDates,ts)
            genes.append(curGene)
            #printGene(curGene)
        chrom = Chromosome(i+1,genes,float('inf'),0,0)
        firstGen.append(chrom)

def computeFitness(chrom,courses,rooms):
    #define the 3d array for checking time conflict(days,rooms,ts)
    checkTF = np.empty((5,3,10),dtype = object)

    timeConflict = 0
    roomCapVio = 0
    timePrefVio = 0

    scv = 0
    hcv = 0
    for i in range(0,len(chrom.genes)):
        #check timePref
        actualTime = 0
        if(chrom.genes[i].tsID[0] <= 5):
            actualTime = 0
        elif(chrom.genes[i].tsID[0] > 5):
            actualTime = 1
        if(int(courses[i].timePref) != int(actualTime)):
            timePrefVio = timePrefVio + 1

        #check roomCap
        requiredRoomCap = int(courses[i].capLevel)
        actualRoomCap = int(rooms[chrom.genes[i].roomID-1].capLevel)
        if(requiredRoomCap>actualRoomCap):
            roomCapVio = roomCapVio + 1

        #check time conflict
        for date in chrom.genes[i].date:
            for tsID in chrom.genes[i].tsID:
                if(checkTF[date-1][chrom.genes[i].roomID-1][tsID-1] != None):
                    timeConflict = timeConflict + 1
                    checkTF[date-1][chrom.genes[i].roomID-1][tsID-1].append(chrom.genes[i].courseID)

                else:
                    temL = []
                    temL.append(chrom.genes[i].courseID)
                    checkTF[date-1][chrom.genes[i].roomID-1][tsID-1] = temL

    hcv = roomCapVio + timeConflict
    scv = timePrefVio
    fitness = hcv*21+scv
    chrom.fitness = fitness
    chrom.scv = scv
    chrom.hcv = hcv




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

    #create initial generation
    firstGen = []
    createFirstGen(firstGen,rooms,courses,timeSlots)

    #calculate fitness values of chroms in first generation
    for chrom in firstGen:
        computeFitness(chrom,courses,rooms)
    #computeFitness(firstGen[0],courses,rooms)
    for chrom in firstGen:
        printChrom(chrom)

    nextGen = []
    



if __name__ == '__main__':
    main()
