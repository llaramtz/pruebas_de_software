"""Módulo que representa la gestión de Reservaciones."""
from dataclasses import dataclass
import json
import datetime


@dataclass
class ReservationData:
    """Clase para encapsular datos de reservación."""
    reservation_id: str
    hotel_id: str
    room_number: int
    customer_id: str
    start_date: datetime.datetime
    end_date: datetime.datetime


class Reservation:
    """Clase para manejar reservaciones."""
    reservations = []

    def __init__(self, reservation_data: ReservationData):
        """Inicializa una nueva reservación."""
        self.reservation_id = reservation_data.reservation_id
        self.hotel_id = reservation_data.hotel_id
        self.room_number = reservation_data.room_number
        self.customer_id = reservation_data.customer_id
        self.start_date = datetime.datetime.strptime(reservation_data.
                                                     start_date,
                                                     "%Y-%m-%d")
        self.end_date = datetime.datetime.strptime(reservation_data.end_date,
                                                   "%Y-%m-%d")
        if self.start_date >= self.end_date:
            raise ValueError("The start date must be before the end date.")

    @classmethod
    def create_reservation(cls, reservation_data: ReservationData):
        """Crea y agrega una nueva reservación a la lista de reservaciones."""
        start_date_dt = datetime.datetime.strptime(reservation_data.
                                                   start_date,
                                                   "%Y-%m-%d")
        end_date_dt = datetime.datetime.strptime(reservation_data.end_date,
                                                 "%Y-%m-%d")

        if any(reservation for reservation in cls.reservations
               if reservation.reservation_id ==
                reservation_data.reservation_id):
            raise ValueError("A reservation with the given ID already exists.")
        if start_date_dt >= end_date_dt:
            raise ValueError("End date must be after start date.")

        for reservation in cls.reservations:
            if reservation.room_number == reservation_data.room_number \
                    and reservation.hotel_id == reservation_data.hotel_id:
                if not (start_date_dt > reservation.end_date
                        or end_date_dt < reservation.start_date):
                    raise ValueError("The room is already booked"
                                     " for the selected dates.")

        reservation = cls(reservation_data)
        cls.reservations.append(reservation)
        return reservation

    @classmethod
    def cancel_reservation(cls, reservation_id):
        """Cancela una reservación existente."""
        reservation = next((res for res in cls.reservations
                            if res.reservation_id == reservation_id), None)
        if reservation:
            cls.reservations.remove(reservation)
        else:
            raise ValueError("Reservation not found.")

    def modify_reservation(self, start_date=None, end_date=None):
        """Modifica las fechas de una reservación existente."""
        if start_date:
            self.start_date = datetime.datetime.strptime(start_date,
                                                         "%Y-%m-%d")
        if end_date:
            self.end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        if self.start_date >= self.end_date:
            raise ValueError("End date must be after start date.")

    def display_reservation_info(self):
        """Muestra la información de la reservación."""
        print(f"Reservation ID: {self.reservation_id}, "
              f"Hotel ID: {self.hotel_id}, "
              f"Room Number: {self.room_number}, "
              f"Customer ID: {self.customer_id}, "
              f"Start Date: {self.start_date.strftime('%Y-%m-%d')}, "
              f"End Date: {self.end_date.strftime('%Y-%m-%d')}")

    @classmethod
    def save_reservations_to_file(cls, filename):
        """Guarda las reservaciones actuales en un archivo."""
        with open(filename, "w", encoding='utf-8') as file:
            data = [{
                'reservation_id': r.reservation_id,
                'hotel_id': r.hotel_id,
                'room_number': r.room_number,
                'customer_id': r.customer_id,
                'start_date': r.start_date.strftime("%Y-%m-%d"),
                'end_date': r.end_date.strftime("%Y-%m-%d")
            } for r in cls.reservations]
            json.dump(data, file, indent=4)

    @classmethod
    def load_reservations_from_file(cls, filename="reservations.json"):
        """Carga reservaciones desde un archivo."""
        try:
            with open(filename, "r", encoding='utf-8') as file:
                reservations_data = json.load(file)
                for data in reservations_data:
                    reservation_data = ReservationData(
                        data['reservation_id'],
                        data['hotel_id'],
                        data['room_number'],
                        data['customer_id'],
                        data['start_date'],
                        data['end_date']
                    )
                    cls.create_reservation(reservation_data)
        except FileNotFoundError:
            print("No previous reservation data found.")
        except json.JSONDecodeError:
            print(f"Error al decodificar JSON en {filename}.")
