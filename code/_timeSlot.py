class TimeSlot:
    def __init__(self,id,startTime,durationCount,isOccupied):
        self.id = id
        #self.date = date
        self.startTime = startTime
        self.durationCount = durationCount

    def getId(self):
        return self.id

#    def getDate(self):
#        return self.date

    def getStartTime(self):
        return self.startTime
