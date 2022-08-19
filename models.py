from typing import List, Optional
import datetime
from typing import Optional
from pydantic import BaseModel


class Colour(BaseModel):
    percentage: float
    colour: List[int]


class Cluster(BaseModel):
    date: datetime.datetime
    colours: List[Colour]
