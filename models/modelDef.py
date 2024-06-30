from pydantic import BaseModel, Field
from datetime import datetime

class Article:
    pass


class Weather(BaseModel):
    city: str =Field(description="City name")
    date: str
    temperature: float
    unit: str

    def __repr__(self) -> str:
        return f"As of {self.date}, the weather in {self.city} is {self.temperature} {self.unit}"


class Directions(BaseModel):
    from_location: str
    to_location: str

    def __repr__(self) -> str:
        return f"The direction from {self.from_location} to {self.to_location} is via ..."

class Time(BaseModel):
    time: datetime

    def __repr__(self) -> str:
        return f"The current time is {self.time.strftime('%Y-%B-%d %H-%M')}"