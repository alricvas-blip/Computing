
from dataclasses import dataclass, field

@dataclass
class Artist:
    name: str
    dob : str
    countryOfBirth : str

    def print (self):
        print(f"Name: {self.name}, Date of Birth: {self.dob}, Country of Birth: {self.countryOfBirth}")

@dataclass
class CD:
    artist : Artist
    title : str
    numTracks : int
    cost : float

    def print (self):
        self.artist.print()
        print(f"Title: {self.title}, Number of Tracks: {self.numTracks}, Cost: {self.cost}")

Kanye = Artist("Kanye West", "June 8, 1977", "United States")
CD1 = CD(Kanye, "Graduation", 13, 9.99)
CD1.print()

JayZ = Artist("Jay-Z", "December 4, 1969", "United States")
CD2 = CD(JayZ, "The Blueprint", 8, 12.99)
CD2.print()

@dataclass
class CDCollection:
    collection : list[CD] = field(default_factory=list)
    count : int = 0
    totalCost : float = 0

    def addCD(self, cd ):
        pass
    def remCD(self, index):
        pass
    def getCD(self, index):
        pass
    def findCD(self, title):
        pass
    def printCDs(self, index):
        pass
    def printCollection(self):
        pass


