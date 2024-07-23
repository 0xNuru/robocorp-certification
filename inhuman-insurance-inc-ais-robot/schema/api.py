from pydantic import BaseModel, Field

class Payload(BaseModel):
    year: int = Field(gt=999, lt=10000, description="the year must be a four digit number")
    country: str = Field(min_length=3, max_length=3, description="the country name has to be three characters")
    rate: float = Field(lt=5.0, description="the rate must be a positive number that's less than 5")