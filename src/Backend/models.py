from enum import Enum
from dataclasses import dataclass
from typing import Tuple

#fixed some values for health state using Enum
class HealthState(Enum):
    SUSCEPTIBLE = "susceptible"
    INFECTED = "infected"
    RECOVERED = "recovered"
@dataclass

#graph node
class Node:
    id:int
    state:HealthState
    position:tuple[float,float]
    day_infected :int =0

@dataclass
#define how simulation will run
class SimulationConfig:
    infection_rate:float=0.2
    recovery_days:int=14
    initial_infected:int=5
