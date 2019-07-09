class TimeSlot:
    def __init__(self,id,date,startTime):
        self.id = id
        self.date = date
        self.startTime = startTime

    def getId(self):
        return self.id

    def getDate(self):
        return self.date

    def getStartTime(self):
        return self.startTime
