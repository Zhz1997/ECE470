import sys,os
import random
import numpy as np
import copy as copy
import math
from chromosome import Chromosome
from classRoom import ClassRoom
from course import Course
from timeSlot import TimeSlot
from gene import Gene

#print helper functions
#---------------------------------
def printGene(gene):
    print("gene: courseID = " + str(gene.courseID)
    + " roomID = " + str(gene.roomID)
    + " tsID = " + str(gene.tsID)
    + " durationPref = " + str(gene.durationPref))
def printChrom(chrom):
    print("chromosom: ID = " + str(chrom.id)
    + " fitness = " + str(chrom.fitness)
    + " scv = " + str(chrom.scv)
    + " hcv = " + str(chrom.hcv))
def printGeneration(generation):
    for chrom in generation:
        printChrom(chrom)

# store data into list functions
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
        #print(content)
        id = content[0]
        durations = content[1].split("&")
        durationCount = len(durations)
        startTime = content[2].split("&")[0]
        #print(startTime)

        timeSlot = TimeSlot(id,startTime,durationCount,0)
        timeSlots.append(timeSlot)
    return timeSlots
#-------------------------------------------

#GA part
def createGene(gene,courseID):
    gene.courseID = courseID
    gene.roomID = random.randint(1,3)
    gene.tsID = random.randint(1,len(timeSlots))
    gene.durationPref = courses[courseID-1].duration

def createChrom(chrom,id):
    chrom.id = id
    genes = []
    for j in range(0,len(courses)):
        gene = Gene(0,0,0,0)
        createGene(gene,j+1)
        genes.append(gene)
    chrom.genes = genes
    chrom.scv = 0.0000000000001
    chrom.hcv = 0.0000000000001

def createFirstGen(firstGen):
    for i in range(0,genSize):
        chrom = Chromosome(0,0,0,0,0)
        createChrom(chrom,i+1)
        firstGen.append(chrom)


def computeFitness(chrom,out):
    scv = 0
    hcv = 0

    #soft constraints vios
    durationPrefVio = 0
    startTimePrefVio = 0

    #hard constraints
    roomCapVio = 0
    timeConflict = 0
    tsConflictArray = np.empty((3,len(timeSlots)),dtype = object)

    #loop through genes of the chrom to compute violations
    for i in range(0,len(chrom.genes)):
        #compute roomCapVio
        requiredRoomCap = courses[int(chrom.genes[i].courseID)-1].capLevel
        actualRoomCap = rooms[int(chrom.genes[i].roomID)-1].capLevel
        if(requiredRoomCap > actualRoomCap):
            roomCapVio = roomCapVio + 1

        #compute timeConflict
        if(tsConflictArray[int(chrom.genes[i].roomID)-1][int(chrom.genes[i].tsID)-1] != None):
            timeConflict = timeConflict + 1
            tsConflictArray[int(chrom.genes[i].roomID)-1][int(chrom.genes[i].tsID)-1].append(chrom.genes[i].courseID)
        else:
            temL = []
            temL.append(chrom.genes[i].courseID)
            tsConflictArray[int(chrom.genes[i].roomID)-1][int(chrom.genes[i].tsID)-1] = temL

        #compute durationPrefVio
        requiredDuration = chrom.genes[i].durationPref
        actualDuration = timeSlots[int(chrom.genes[i].tsID)-1].durationCount
        if(int(requiredDuration) != (actualDuration)):
            durationPrefVio = durationPrefVio + 1

        #compute startTimePrefVio

    hcv = roomCapVio + timeConflict
    scv = durationPrefVio + startTimePrefVio

    chrom.scv = scv
    chrom.hcv = hcv
    penalty = hcv*21+scv
    chrom.fitness = (1 / penalty) ** 2

    if(out == 1):
        print("roomCapVio = " + str(roomCapVio))
        print("timeConflict = " + str(timeConflict))
        print("durationPrefVio = " + str(durationPrefVio))

        print(tsConflictArray)


def createNextGen(prevGen):
    nextGen = []
    #copy the best chrom from prevGen to nextGen
    prevGenCopy = copy.deepcopy(prevGen)
    prevGenCopy.sort(key=lambda x:x.fitness, reverse=True)
    bestInGen = prevGenCopy[0]
    bestInGen.id = 1
    nextGen.append(bestInGen)

    #----------------------------------------------
    #get total amount of fitness
    fitnessT = 0
    for chrom in prevGen:
        fitnessT = fitnessT + chrom.fitness

    l = []
    for i in range(0,len(prevGen)):
        numOfIns = math.floor((prevGen[i].fitness / fitnessT) * 100)
        #print("at chrom "+str(chrom.id) + " numOfIns is " + str(numOfIns))
        l = l + [i] * (numOfIns+1)

    for i in range(0,genSize-1):
        newChrom = Chromosome(0,0,0,0,0)
        parent1 = prevGen[pickOne(l)]
        parent2 = prevGen[pickOne(l)]

        #do crossOver
        newChrom = crossOver(parent1,parent2,i+2)

        evolve(newChrom)

        #mutate
        ifMutate = random.randint(1,10)
        if(ifMutate <= 1):
            mutate(newChrom)

        nextGen.append(newChrom)

    return nextGen

def pickOne(l):
    index = random.randint(1,len(l))
    return l[index-1]

def crossOver(parent1,parent2,id):
    midPoint = 0
    midPoint = random.randint(1,21)
    newGenes = []
    for i in range(0,midPoint):
        newGenes.append(parent1.genes[i])
    for i in range(midPoint,21):
        newGenes.append(parent2.genes[i])

    newChrom = Chromosome(id,newGenes,0.00000001,100,100)
    return newChrom

def mutate(chrom):
    chrom = createChrom(chrom,chrom.id)

def evolve(chrom):
    #evolve RoomCap
    if(chrom.hcv>0):
        for gene in chrom.genes:
            #printGene(gene)
            if(courses[int(gene.courseID)-1].capLevel > rooms[int(gene.roomID)-1].capLevel):
                gene.roomID = gene.roomID + 1

    #evolve DurationPref
    else:
        firstDPV = gene(0,0,0,0)
        secondDPV = gene(0,0,0,0)
        firstDPVFound = 0
        firstDPVIndex = 0
        secondDPVFound = 0
        secondDPVIndex = 0
        geneIndex = 0
        while(fistDPVFound != 1 or secondDPVFound != 1):
            if(fistDPVFound == 0):
                #find the fist duration prefer violation
                if(chrom.genes[geneIndex].durationPref != timeSlots[int(chrom.genes[geneIndex].tsID)-1]):
                    firstDPV = chrom.genes[geneIndex]
                    firstDPVFound = 1
                    firstDPVIndex = geneIndex
            else:
                #find the second duration prefer violation
                if(chrom.genes[geneIndex].durationPref != timeSlots[int(chrom.genes[geneIndex].tsID)-1]):
                    secondDPV = chrom.genes[geneIndex]
                    secondDPVFound = 1
                    secondDPVIndex = geneIndex


            #increase geneIndex
            geneIndex = geneIndex + 1
            #reset index
            if(geneIndex == len(chrom.genes)):
                geneIndex = 0

        if(firstDPVIndex == secondDPVIndex):
            return
        #swap first DPV and second DPV
        tempGene = copy.deepcopy(secondDPV)
        secondDPV = copy.deepcopy(firstDPV)
        firstDPV = copy.deepcopy(tempGene)



#-------------------------------------------------------
def main():
    #generate first generation
    firstGen = []
    createFirstGen(firstGen)
    printGeneration(firstGen)


    #compute fitness for all chroms in first Gen
    bestFitValue = 0
    bestChromId = 0
    for chrom in firstGen:
        computeFitness(chrom,0)
        if chrom.fitness > bestFitValue:
            bestFitValue = chrom.fitness
            bestChromId = chrom.id

    print("-----------------------------")
    printGeneration(firstGen)
    print("bestFitValue in initial generation is " + str(bestFitValue) + " chrom id is " + str(bestChromId))

    #body part
    prevGen = copy.deepcopy(firstGen)
    for i in range(0,numberOfGen):
        bestChrom = firstGen[0]
        bestFitValue = 0
        lowestHcv = 100
        lowestScv = 100
        nextGen = []
        nextGen = createNextGen(prevGen)
        #compute fitness of chromes in new generation
        for chrom in nextGen:
            computeFitness(chrom,0)
            #printChrom(chrom)
            if chrom.fitness > bestFitValue:
                #solution = chrom
                bestFitValue = chrom.fitness
                lowestHcv = chrom.hcv
                lowestScv = chrom.scv
                bestChrom = chrom
            #if chrom.hcv < lowestHcv:
                #lowestHcv = chrom.hcv
        print("best fitness value at generation " + str(i) + " is "+ str(bestFitValue) + " scv: " + str(lowestScv) + " hcv: " + str(lowestHcv))
        prevGen = nextGen

    #for i in prevGen:
    computeFitness(bestChrom,1)









#-------------------------------------------
if __name__ == '__main__':
    #global variables
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/data/data_1"
    roomsPath = path + "/rooms.csv"
    timeSlotPath = path + "/tss.csv"
    #timeSlotPath = path + "/timeSlot.csv"
    coursePath = path + "/courses.csv"

    roomsFile = open(roomsPath,encoding = 'utf-8')
    timeSlotFile = open(timeSlotPath,encoding = 'utf-8')
    courseFile = open(coursePath,encoding = 'utf-8')


    rooms = []
    courses = []
    timeSlots = []

    rooms = getRooms(rooms,roomsFile)
    courses = getCourses(courses,courseFile)
    timeSlots = getTimeSlots(timeSlots,timeSlotFile)

    genSize = 100
    numberOfGen = 1500

    #call main
    main()
