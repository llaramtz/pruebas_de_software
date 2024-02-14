"""Pruebas unitarias para Hotel."""
import unittest
import os
from io import StringIO
from unittest.mock import patch
from hotel import Hotel


class TestHotel(unittest.TestCase):
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

    def test_create_hotel(self):
        """Test hotel creation."""
        self.assertEqual(self.hotel.name, "Test Hotel")
        self.assertEqual(self.hotel.location, "Test Location")

    def test_add_room(self):
        """Test adding a room to the hotel."""
        self.hotel.add_room("102", 4)
        self.assertIn("102", self.hotel.rooms)

    def test_reserve_room(self):
        """Test reserving a room."""
        try:
            self.hotel.reserve_room("101",
                                    "C001",
                                    "2024-02-10",
                                    "2024-02-12")
            reservation_made = any(reservation for reservation in
                                   self.hotel.rooms["101"]['reservations']
                                   if reservation['customer_id'] == "C001")
            self.assertTrue(reservation_made)
        except ValueError as error:
            self.fail(f"Reserve room raised an exception: {error}")

    def test_cancel_reservation(self):
        """Test canceling a reservation."""
        self.hotel.reserve_room("101", "C001",
                                "2024-02-10",
                                "2024-02-12")
        self.hotel.cancel_reservation("101", "C001")
        reservation_cancelled = not any(reservation for reservation in
                                        self.hotel.rooms["101"]['reservations']
                                        if reservation['customer_id']
                                        == "C001")
        self.assertTrue(reservation_cancelled)

    def test_save_and_load_hotel(self):
        """Test saving and loading hotels from a file."""
        Hotel.save_hotels_to_file(self.filename)
        # Verificar la existencia del archivo
        self.assertTrue(os.path.exists(self.filename))
        # Limpiar la lista de hoteles y cargar desde el archivo
        Hotel.hotels = []
        Hotel.load_hotels_from_file(self.filename)
        loaded_hotel = Hotel.hotels[0]
        self.assertEqual(loaded_hotel.hotel_id, self.hotel.hotel_id)
        self.assertEqual(loaded_hotel.name, self.hotel.name)
        self.assertEqual(loaded_hotel.location, self.hotel.location)

    def test_create_duplicate_hotel(self):
        """Test creating a hotel with a
         duplicate ID should raise ValueError."""
        Hotel.create_hotel("H001",
                           "Hotel One",
                           "Location One")
        with self.assertRaises(ValueError):
            Hotel.create_hotel("H001",
                               "Hotel Duplicate",
                               "Location Duplicate")

    def test_modify_hotel_info(self):
        """Test modifying hotel information."""
        hotel = Hotel.create_hotel("H002",
                                   "Hotel Two",
                                   "Location Two")
        hotel.modify_hotel_info(name="Hotel Two Updated",
                                location="Location Updated")
        self.assertEqual(hotel.name, "Hotel Two Updated")
        self.assertEqual(hotel.location, "Location Updated")

    def test_display_hotel_info(self):
        """Test that the hotel info
        is printed correctly."""
        with unittest.mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.hotel.display_hotel_info()
            self.assertIn(self.hotel.name, fake_out.getvalue())

    def test_display_hotel_info_output(self):
        """Test the output of the display_hotel_info method."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.hotel.display_hotel_info()
            output = fake_out.getvalue()
            self.assertIn(self.hotel.hotel_id, output)
            self.assertIn(self.hotel.name, output)
            self.assertIn(self.hotel.location, output)

    def test_delete_existing_hotel(self):
        """Test deleting an existing
        hotel returns True."""
        # Assume self.hotel is an instance of Hotel with hotel_id="001"
        result = Hotel.delete_hotel("001")
        self.assertTrue(result)
        # Verify that the hotel with hotel_id="001" is no longer in the list
        self.assertNotIn("001", [hotel.hotel_id for hotel in Hotel.hotels])

    def tearDown(self):
        """Clean up after each test."""
        # if os.path.exists(self.filename):
        #    os.remove(self.filename)


if __name__ == '__main__':
    unittest.main()
