from dataclasses import dataclass
from typing import Protocol
from datetime import date, datetime
from dateutil.parser import parse

class RoomType(Protocol):
    @property
    def multiplicator(self) -> float: ...

class RoomStandard:
    @property
    def multiplicator(self):
        return 1.0

class RoomLux:
    @property
    def multiplicator(self):
        return 1.2


class Room:
    def __init__(self, number: int, basePrice: float, roomType: RoomType) -> None:
        self.number = number
        self.basePrice = basePrice
        self.roomType = roomType
        self.booked = []

    @property
    def price(self) -> float:
        return self.basePrice * self.roomType.multiplicator
    
    def is_booked(self, book_date: date) -> bool:
        if book_date in self.booked:
            return True
        return False
    
    def reservation_on(self, book_date: date) -> None:
        if self.is_booked(book_date):
            raise ValueError("Комната на эту дату уже забронирована")
        self.booked.append(book_date)

    def reservation_off(self, book_date: date) -> None:
        if not self.is_booked(book_date):
            raise ValueError("Комната на эту дату не имеет брони")
        self.booked.remove(book_date)

@dataclass
class Booking:
    room_num: int
    book_start: date
    book_end: date
    canceled: bool = False


class Hotel:
    def __init__(self) -> None:
        self.rooms: dict = {}
        self.book: list[Booking] = []

    def add_room(self, room:Room) -> None:
        self.rooms[room.number] = room

    def get_room_by_num(self, room_num: int):
        """Возвращает объект класса Room по номеру номера"""
        return self.rooms[room_num]
    
    def new_booking(self, room_num: int, book_start: date, book_end:date):
        """Бронирование номер по его номеру"""
        if book_start > book_end:
            raise ValueError("некорректно заданы даты начала и конца бронирования")
        if self.is_booked(room_num, book_start) or self.is_booked(room_num, book_end):
            raise ValueError("На эти даты комната уже забронирована")
        for book in self.book:
            if book.canceled: 
                continue
            if book.room_num != room_num:
                continue
            if book_start < book.book_start < book_end:
                raise ValueError("На эти даты комната уже забронирована")
            if book_start < book.book_end < book_end:
                raise ValueError("На эти даты комната уже забронирована")
        print(f"Номер {room_num} забронирован на c {book_start} по {book_end}")
        self.book.append(Booking(room_num, book_start, book_end))
    
    def cancel_booking(self, room_num: int, book_start: date, book_end:date):
        """Отмена бронирования"""
        try:
            i = self.book.index(Booking(room_num, book_start, book_end))
            book = self.book[i]
            book.canceled = True
            print(f"Бронирование номера {room_num} успешно снято")
            return True
        except ValueError:
            print(f"Бронирование номера {room_num} отсуствует")
            return False
    
    @property
    def room_list(self) -> list:
        result: list = []
        for element in self.rooms:
            result.append(element)
        return result
    
    def is_booked(self, room_num: int, chk_date: date = date.today()) -> bool:
        for book in self.book:
            if book.canceled: 
                continue
            if book.room_num != room_num:
                continue
            if book.book_start <= chk_date <= book.book_end:
                return True
        return False

    def get_available_rooms(self, chk_date: date = date.today()) -> list:
        booked_list = []
        for book in self.book:
            if book.canceled: 
                continue
            if self.is_booked(book.room_num, chk_date):
                booked_list.append(book.room_num)
        return [x for x in self.room_list if x not in booked_list] 
    
    def get_booked_rooms(self) -> list:
        result = []
        for book in self.book:
            if book.canceled:
                continue
            result.append([book.room_num, book.book_start.strftime("%d.%m.%Y"), book.book_end.strftime("%d.%m.%Y")])
        return result
    
        

    
date_start = parse('2026-01-23').date()
date_end = parse('2026-01-26').date()
date_check = parse('2026-01-24').date()


myHotel = Hotel()
myHotel.add_room(Room(101, 1200.0, RoomStandard()))
myHotel.add_room(Room(102, 1200.0, RoomStandard()))
myHotel.add_room(Room(103, 1200.0, RoomStandard()))
myHotel.add_room(Room(201, 1200.0, RoomLux()))
myHotel.add_room(Room(202, 1200.0, RoomLux()))

print(myHotel.get_available_rooms())
myHotel.new_booking(102,date_start,date_end)
print(myHotel.get_available_rooms(date_check))

print(myHotel.get_booked_rooms())
myHotel.cancel_booking(102,date_start,date_end)
print(myHotel.get_available_rooms(date_check))
print(myHotel.get_available_rooms(date_check))