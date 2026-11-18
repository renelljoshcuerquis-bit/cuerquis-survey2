from sqlmodel import Field, SQLModel


class Survey(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    food: str  # was "Food"; the form sends "food", and SQLite column names ignore case
    sports: str
    animals: str
    country: str
    car: str
    brand: str
    games: str
    phone: str
    bike: str


# Table: one row per account. The password column stores "salt$hash", never the plain password.
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str


# Request bodies (not tables)
class UserRegister(SQLModel):
    username: str
    password: str
    confirmed_password: str


class UserLogin(SQLModel):
    username: str
    password: str
