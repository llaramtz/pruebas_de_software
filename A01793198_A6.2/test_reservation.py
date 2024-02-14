"""Pruebas unitarias para Reservaciones."""
import unittest
import datetime
import os
from io import StringIO
from unittest.mock import patch, mock_open
from reservation import Reservation, ReservationData


class TestReservation(unittest.TestCase):
    """Clase que engloba toas las pruebas
    unitarias necesarias para la clase reservación."""
    @classmethod
    def setUpClass(cls):
        """Preparar el entorno de prueba antes
        de ejecutar las pruebas de esta clase."""
        Reservation.reservations = []

    def test_create_reservation(self):
        """Probar la creación de una reservación."""
        reservation_data = ReservationData("R001", "H001", 101,
                                           "C001", "2024-02-10", "2024-02-15")
        reservation = Reservation.create_reservation(reservation_data)
        self.assertEqual(reservation.start_date,
                         datetime.datetime.strptime("2024-02-10",
                                                    "%Y-%m-%d"))
        self.assertEqual(reservation.end_date,
                         datetime.datetime.strptime("2024-02-15",
                                                    "%Y-%m-%d"))

    def test_cancel_reservation(self):
        """Probar la cancelación de una reservación."""
        reservation_data = ReservationData("R003", "H001", 102, "C002",
                                           "2024-03-10", "2024-03-15")
        Reservation.create_reservation(reservation_data)
        result = Reservation.cancel_reservation("R003")
        self.assertIsNone(result)

    def test_modify_reservation(self):
        """Probar la modificación de una reservación."""
        reservation_data = ReservationData("R004", "H001", 103, "C003",
                                           "2024-04-10", "2024-04-15")
        reservation = Reservation.create_reservation(reservation_data)
        reservation.modify_reservation(start_date="2024-04-12")
        self.assertEqual(reservation.start_date,
                         datetime.datetime.strptime("2024-04-12",
                                                    "%Y-%m-%d"))

    def test_save_and_load_reservations(self):
        """Test para guardar y cargar reservaciones desde un archivo."""
        Reservation.reservations = []
        reservation_data_1 = ReservationData("XCV", "H001", 101, "C001",
                                             "2025-02-10", "2025-02-15")
        reservation_data_2 = ReservationData("QWE", "H001", 102, "C002",
                                             "2025-03-10", "2025-03-15")
        Reservation.create_reservation(reservation_data_1)
        Reservation.create_reservation(reservation_data_2)
        Reservation.save_reservations_to_file("test_reservations.json")
        self.assertTrue(os.path.exists("test_reservations.json"))
        Reservation.reservations = []
        Reservation.load_reservations_from_file("test_reservations.json")
        self.assertEqual(len(Reservation.reservations), 2)
        loaded_reservation_data_1 = Reservation.reservations[0]
        self.assertEqual(loaded_reservation_data_1.reservation_id, "XCV")
        loaded_reservation_data_2 = Reservation.reservations[1]
        self.assertEqual(loaded_reservation_data_2.reservation_id, "QWE")

    def test_reservation_conflict(self):
        """Probar que no se pueden hacer
        reservaciones que se solapen en las mismas fechas."""
        Reservation.reservations = []
        reservation_data_1 = ReservationData("R100", "H001", 101, "C001",
                                             "2028-02-10", "2028-02-15")
        Reservation.create_reservation(reservation_data_1)
        reservation_data_2 = ReservationData("R101", "H001", 101, "C002",
                                             "2028-02-14", "2028-02-20")
        with self.assertRaises(ValueError):
            Reservation.create_reservation(reservation_data_2)

    def test_create_reservation_with_end_date_before_start_date(self):
        """Probar que se lanza un ValueError si la fecha de
        inicio es igual o posterior a la fecha de fin."""
        reservation_data = ReservationData("R005", "H001", 102, "C001",
                                           "2024-02-15", "2024-02-10")
        with self.assertRaises(ValueError):
            Reservation.create_reservation(reservation_data)

    def test_create_reservation_with_existing_id(self):
        """Probar que se lanza un ValueError
        si el ID de la reservación ya existe."""
        Reservation.reservations = []
        reservation_data_1 = ReservationData("R006", "H001", 103, "C001",
                                             "2024-03-15", "2024-03-20")
        Reservation.create_reservation(reservation_data_1)
        reservation_data_2 = ReservationData("R006", "H001", 103, "C002",
                                             "2024-03-21", "2024-03-25")
        with self.assertRaises(ValueError):
            Reservation.create_reservation(reservation_data_2)

    def test_cancel_nonexistent_reservation(self):
        """Test that a ValueError is raised when trying to
        cancel a reservation that does not exist."""
        with self.assertRaises(ValueError):
            Reservation.cancel_reservation("R999")

    def test_display_reservation_info(self):
        """Test that display_reservation_info
        method prints the correct output."""
        reservation_data = ReservationData("R00300", "H003", 303, "C003",
                                           "2024-04-10", "2024-04-15")
        reservation = Reservation.create_reservation(reservation_data)
        expected_output = f"Reservation ID: {reservation.reservation_id}, " \
            f"Hotel ID: {reservation.hotel_id}, " \
            f"Room Number: {reservation.room_number}, " \
            f"Customer ID: {reservation.customer_id}, " \
            f"Start Date: {reservation.start_date.strftime('%Y-%m-%d')}, " \
            f"End Date: {reservation.end_date.strftime('%Y-%m-%d')}\n"
        with patch('sys.stdout', new_callable=StringIO) as fake_out:
            reservation.display_reservation_info()
            self.assertEqual(fake_out.getvalue(), expected_output)

    @patch('builtins.open', new_callable=mock_open)
    def test_load_reservations_file_not_found(self, mock_file):
        """Test loading reservations from a
        non-existent file logs the correct message."""
        mock_file.side_effect = FileNotFoundError
        with patch('sys.stdout', new_callable=StringIO) as fake_out:
            Reservation.load_reservations_from_file("nonexistent_file.json")
            self.assertIn("No previous reservation data found.",
                          fake_out.getvalue())

    @classmethod
    def tearDownClass(cls):
        """Limpiar después de todas las pruebas de esta clase."""
        Reservation.reservations = []
        if os.path.exists("test_reservations.json"):
            os.remove("test_reservations.json")


if __name__ == '__main__':
    unittest.main()
