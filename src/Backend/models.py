from enum import Enum
from dataclasses import dataclass
from typing import Tuple

#fixed some values for health state using Enum
class HealthState(Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"
@dataclass

#graph node
class Node:
    id:int
    state:HealthState
    postion:tuple[float,float]
    day_infected :int =0

@dataclass
#define how simulation will run
class simulation_config:
    infection_rate:float=0.2
    recovery_days:int=14
    initial_infected:int=5
