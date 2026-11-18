from sqlmodel import Field, SQLModel


class Survey(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    food: str  
    sports: str
    animals: str
    country: str
    car: str
    brand: str
    games: str
    phone: str
    bike: str



class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str 
    password: str



class UserRegister(SQLModel):
    username: str
    password: str
    confirmed_password: str


class UserLogin(SQLModel):
    username: str
    password: str
