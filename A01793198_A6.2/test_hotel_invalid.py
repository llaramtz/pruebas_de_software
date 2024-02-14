"""Pruebas unitarias para Hotel."""
import unittest
import os
import datetime
import sys
from io import StringIO
from unittest.mock import patch
from hotel import Hotel


class TestHotelInvalid(unittest.TestCase):
    """Clase que engloba toas las pruebas
    unitarias necesarias para la clase Hotel."""
    def setUp(self):
        """Setup a test hotel before each test."""
        # Asegurar que la lista de
        # hoteles esté limpia antes de cada prueba
        Hotel.hotels = []
        # Nombre de archivo para pruebas de serialización
        self.filename = "test_hotels.json"
        self.hotel = Hotel.create_hotel("001",
                                        "Test Hotel",
                                        "Test Location")
        self.hotel.add_room("101", 2)

    def test01_load_hotels_with_invalid_data(self):
        """Test loading hotels from
        a file with invalid data."""
        # Crear un archivo de prueba con datos inválidos
        with open("test_invalid_hotels.json", "w", encoding='utf-8') as file:
            file.write('{"invalid_json":')
        captured_output = StringIO()
        sys.stdout = captured_output
        Hotel.load_hotels_from_file("test_invalid_hotels.json")
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        # Verificar que se ha registrado el mensaje de error
        self.assertIn("Error al decodificar JSON", output)
        # Verificar que la lista de hoteles no se modificó
        # Existe solo 1 en la lista de hoteles
        # la que se configura en cada prueba.
        self.assertTrue(len(Hotel.hotels) == 1)
        # Limpiar el archivo de prueba
        os.remove("test_invalid_hotels.json")

    def test_delete_nonexistent_hotel(self):
        """Test deleting a hotel that does
        not exist should raise ValueError."""
        with self.assertRaises(ValueError):
            Hotel.delete_hotel("H999")

    def test_add_duplicate_room(self):
        """Test adding a room with a number
        that already exists should raise ValueError."""
        hotel = Hotel.create_hotel("H003",
                                   "Hotel Three",
                                   "Location Three")
        hotel.add_room("101", 2)
        with self.assertRaises(ValueError):
            hotel.add_room("101", 2)

    def test_reserve_room_unavailable(self):
        """Test reserving a room that is not
        available should raise ValueError."""
        hotel = Hotel.create_hotel("H004",
                                   "Hotel Four",
                                   "Location Four")
        hotel.add_room("102", 2)
        hotel.reserve_room("102", "C001",
                           "2024-02-10", "2024-02-15")
        with self.assertRaises(ValueError):
            hotel.reserve_room("102", "C002",
                               "2024-02-14", "2024-02-16")

    def test_modify_hotel_info_with_no_changes(self):
        """Test modifying hotel information with no changes."""
        original_name = self.hotel.name
        original_location = self.hotel.location
        self.hotel.modify_hotel_info()  # No changes made
        self.assertEqual(original_name, self.hotel.name)
        self.assertEqual(original_location, self.hotel.location)

    def test_add_existing_room_number(self):
        """Test adding a room with an existing
        room number raises ValueError."""
        self.hotel.add_room("1001", 2)
        with self.assertRaises(ValueError):
            self.hotel.add_room("1001", 3)

    def test_reserve_nonexistent_room(self):
        """Test reserving a non-existent
        room raises ValueError."""
        with self.assertRaises(ValueError):
            self.hotel.reserve_room("999", "C001",
                                    "2024-02-10", "2024-02-12")

    def test_cancel_reservation_with_nonexistent_customer_id(self):
        """Test canceling a reservation with a
        nonexistent customer ID raises ValueError."""
        self.hotel.add_room("102", 2)
        self.hotel.reserve_room("102", "C001",
                                "2024-02-10", "2024-02-12")
        with self.assertRaises(ValueError):
            self.hotel.cancel_reservation("102", "C999")

    def test_room_not_available(self):
        """Test the is_room_available method returns
         False when the room is not available."""
        self.hotel.add_room('185', 2)
        start_date = datetime.datetime.now()
        end_date = start_date + datetime.timedelta(days=2)
        # Make a reservation for the current period
        self.hotel.reserve_room('101', 'C001',
                                start_date.strftime('%Y-%m-%d'),
                                end_date.strftime('%Y-%m-%d'))
        # Check availability for the same period
        availability = self.hotel.is_room_available('101',
                                                    start_date,
                                                    end_date)
        self.assertFalse(availability)

    def test_cancel_reservation_with_nonexistent_room(self):
        """Test cancelling a reservation with
        a room number that does not exist."""
        # Assuming self.hotel is an instance of
        # Hotel and no room '999' has been added
        with self.assertRaises(ValueError) as context:
            self.hotel.cancel_reservation('999',
                                          'C001')
        self.assertEqual("Room number does not exist.",
                         str(context.exception))

    def test_load_hotels_with_value_error(self):
        """Test handling of ValueError
        during hotel loading from a file."""
        test_data = '[{"hotel_id": "001", "name": ' \
                    '"Hotel Test", "location": "Test Location"}]'
        with patch('builtins.open',
                   unittest.mock.mock_open(read_data=test_data)):
            with patch('hotel.Hotel.create_hotel') \
                    as mock_create_hotel:
                mock_create_hotel.side_effect = \
                    ValueError("Invalid hotel data")
                with patch('sys.stdout', new_callable=StringIO) \
                        as mock_stdout:
                    Hotel.load_hotels_from_file("test_hotels.json")
                    self.assertIn("Error al cargar hotel: Invalid hotel data",
                                  mock_stdout.getvalue())

    def test_load_hotels_file_not_found(self):
        """Test that a message is printed to the
        console if the hotels file is not found."""
        with patch('builtins.open',
                   side_effect=FileNotFoundError), \
                patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            Hotel.load_hotels_from_file('nonexistent_file.json')
            self.assertIn("Archivo nonexistent_file.json no encontrado",
                          mock_stdout.getvalue())

    def tearDown(self):
        """Clean up after each test."""
        # if os.path.exists(self.filename):
        #    os.remove(self.filename)


if __name__ == '__main__':
    unittest.main()
