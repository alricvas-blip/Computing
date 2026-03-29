
from dataclasses import dataclass, field

@dataclass
class Monsters:
    age: int
    gender : str
    countryOfBirth : str

    def print (self):
        print(f"Age: {self.age}, Gender: {self.gender}, Country of Birth: {self.countryOfBirth}")

@dataclass
class Dragon:
    ScaleColour : str
    TailLength : float
    ColourofFireBreath : str
    NumberOfLegs : int
    

    def print (self):
        print(f"Scale Colour: {self.ScaleColour}, Tail Length: {self.TailLength}, Colour of Fire Breath: {self.ColourofFireBreath}, Number of Legs: {self.NumberOfLegs}")

@dataclass
class TRex
    sizeInM :float
    weightInKg : float
    numberOfTeeth : int
    
    def print (self):
        print(f"Size in M: {self.sizeInM}, Weight in Kg: {self.weightInKg}, Number of Teeth: {self.numberOfTeeth}")

@dataclass
class Minmi
    ScaleColour : str
    TailLength : float
    FootDiameterinCm : float

    def print (self):
        print(f"Scale Colour: {self.ScaleColour}, Tail Length: {self.TailLength}, Foot Diameter in Cm: {self.FootDiameterinCm}")