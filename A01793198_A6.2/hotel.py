"""Módulo que representa la gestión de hoteles."""

import datetime
import json


class Hotel:
    """Representa un hotel en el sistema."""
    hotels = []

    def __init__(self, hotel_id, name, location):
        """Inicializa un nuevo hotel."""
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.rooms = {}

    @classmethod
    def create_hotel(cls, hotel_id, name, location):
        """Crea y añade un nuevo hotel a la lista de hoteles."""
        if any(hotel for hotel in cls.hotels if hotel.hotel_id == hotel_id):
            raise ValueError("A hotel with the given ID already exists.")
        hotel = cls(hotel_id, name, location)
        cls.hotels.append(hotel)
        return hotel

    @classmethod
    def delete_hotel(cls, hotel_id):
        """Elimina un hotel de la lista de hoteles."""
        for hotel in cls.hotels:
            if hotel.hotel_id == hotel_id:
                cls.hotels.remove(hotel)
                return True
        raise ValueError("Hotel not found.")

    def display_hotel_info(self):
        """Muestra la información del hotel."""
        print(f"Hotel ID: {self.hotel_id}, Name: {self.name}, "
              f"Location: {self.location}, Rooms: {len(self.rooms)}")

    def modify_hotel_info(self, name=None, location=None):
        """Modifica la información del hotel."""
        if name is not None:
            self.name = name
        if location is not None:
            self.location = location

    def add_room(self, room_number, capacity):
        """Añade una habitación al hotel."""
        if room_number in self.rooms:
            raise ValueError("Room number already exists.")
        self.rooms[room_number] = {'capacity': capacity, 'reservations': []}

    def is_room_available(self, room_number, start_date, end_date):
        """Verifica si una habitación está disponible."""
        for reservation in self.rooms.get(room_number,
                                          {}).get('reservations', []):
            if start_date <= datetime.datetime.strptime(
                    reservation['end_date'], "%Y-%m-%d") \
                    and end_date >= datetime.datetime.strptime(
                    reservation['start_date'], "%Y-%m-%d"):
                return False
        return True

    def reserve_room(self, room_number, customer_id, start_date, end_date):
        """Reserva una habitación en el hotel."""
        if room_number not in self.rooms:
            raise ValueError("Room number does not exist.")
        if not self.is_room_available(room_number, datetime.datetime.strptime(
                start_date, "%Y-%m-%d"),
                                      datetime.datetime.strptime(
                                          end_date, "%Y-%m-%d")):
            raise ValueError("Room is not available for the selected dates.")
        self.rooms[room_number]['reservations'].append(
            {'customer_id': customer_id,
             'start_date': start_date,
             'end_date': end_date})

    def cancel_reservation(self, room_number, customer_id):
        """Cancela una reserva en el hotel."""
        if room_number not in self.rooms:
            raise ValueError("Room number does not exist.")
        for reservation in self.rooms[room_number]['reservations']:
            if reservation['customer_id'] == customer_id:
                self.rooms[room_number]['reservations'].remove(reservation)
                return True
        raise ValueError("Reservation not found for the given customer ID.")

    @classmethod
    def save_hotels_to_file(cls, filename="hotels.json"):
        """Guarda la lista de hoteles en un archivo."""
        with open(filename, "w", encoding="utf-8") as file:
            json.dump([hotel.__dict__ for hotel in cls.hotels], file)

    @classmethod
    def load_hotels_from_file(cls, filename="hotels.json"):
        """Carga hoteles desde un archivo."""
        try:
            with open(filename, 'r', encoding="utf-8") as file:
                hotels_data = json.load(file)
            for hotel_data in hotels_data:
                try:
                    cls.create_hotel(hotel_data['hotel_id'],
                                     hotel_data['name'],
                                     hotel_data['location'])
                except ValueError as error_value:
                    print(f"Error al cargar hotel: {error_value}")
        except FileNotFoundError:
            print(f"Archivo {filename} no encontrado. "
                  f"Se iniciará con una lista vacía de hoteles.")
        except json.JSONDecodeError:
            print(f"Error al decodificar JSON en {filename}.")
