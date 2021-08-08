from abc import ABC
from datetime import datetime, date, time


class BaseModel(ABC):
    id: int
    table_name: str


class BaseUser(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: str
    password: str
    type: str


class BaseTable(BaseModel):
    number: int
    position: str
    status: int


class BaseCategory(BaseModel):
    name: str


class BaseMenuItem(BaseModel):
    name: str
    price: int
    category: BaseCategory
    discount: float
    serving_time_period: int
    estimated_cooking_time: int


class BaseOrder(BaseModel):
    table: BaseTable
    menu_items: list
    number: int
    status: int
    date_time_stamp: date
    time_time_stamp: time


class BaseReceipt(BaseModel):
    order: BaseOrder
    total_price: int
    final_price: int
    date_time_stamp: date
    time_time_stamp: time
