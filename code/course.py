class Course:
    def __init__(self,id,capLevel,duration,timePref):
        self.id = id
        self.capLevel = capLevel
        self.duration = duration
        self.timePref = timePref

    def getId(self):
        return self.id

    def getCapLevel(self):
        return self.capLevel

    def getDuration(self):
        return self.duration

    def getTimePref(self,id):
        return self.timePref
