"""Pruebas unitarias para Customer."""
import unittest
from unittest.mock import patch, mock_open
from customer import Customer


class TestCustomer(unittest.TestCase):
    """Clase que engloba toas las pruebas
    unitarias necesarias para la clase Customer."""
    @classmethod
    def setUpClass(cls):
        """Método llamado al inicio de las pruebas para esta clase."""
        # Limpiar la lista de clientes antes de iniciar las pruebas
        Customer.customers = []

    def test_create_customer(self):
        """Probar la creación de un cliente."""
        customer = Customer.create_customer("C001",
                                            "John Doe",
                                            "johndoe@example.com")
        self.assertEqual(customer.customer_id, "C001")
        self.assertEqual(customer.name, "John Doe")
        self.assertEqual(customer.email, "johndoe@example.com")

    def test_customer_email_validation(self):
        """Probar la validación del correo electrónico del cliente."""
        with self.assertRaises(ValueError):
            Customer.create_customer("C002",
                                     "Jane Doe",
                                     "not-an-email")

    def test_delete_customer(self):
        """Probar la eliminación de un cliente."""
        Customer.create_customer("C003",
                                 "Delete Me",
                                 "deleteme@example.com")
        result = Customer.delete_customer("C003")
        self.assertTrue(result)

    def test_save_and_load_customers(self):
        """Probar guardar y cargar cliente a un archivo."""
        # Crear cleinte de prueba, ya existe 1.
        Customer.create_customer("C002",
                                 "Jane Doe",
                                 "janedoe@example.com")

        # Guardar los clientes en un archivo
        Customer.save_customers_to_file("test_customers.json")

        # Limpiar la lista de clientes y cargar desde el archivo
        Customer.customers = []
        Customer.load_customers_from_file("test_customers.json")

        # Verificar que los clientes se cargaron correctamente
        self.assertEqual(len(Customer.customers), 5)
        self.assertEqual(Customer.customers[0].customer_id, "C001")
        self.assertEqual(Customer.customers[1].customer_id, "C100")
        self.assertEqual(Customer.customers[2].customer_id, "C0002")
        self.assertEqual(Customer.customers[3].customer_id, "C003")
        self.assertEqual(Customer.customers[4].customer_id, "C002")

    def test_create_customer_with_empty_name(self):
        """Probar creacion de cliente sin nombre"""
        with self.assertRaises(ValueError) as context:
            Customer.create_customer("C002", "", "jane@example.com")
        self.assertIn("Name cannot be empty", str(context.exception))

    def test_create_customer_with_duplicate_id(self):
        """Probar creacion de cliente con id duplicado"""
        Customer.create_customer("C100", "John Doe", "john@example.com")
        with self.assertRaises(ValueError) as context:
            Customer.create_customer("C100", "Jane Doe", "jane@example.com")
        self.assertIn("A customer with the given ID already exists",
                      str(context.exception))

    def test_modify_customer_with_invalid_email(self):
        """Probar modificar cliente con email invalido"""
        customer = Customer.create_customer("C003",
                                            "John Doe",
                                            "john@example.com")
        with self.assertRaises(ValueError) as context:
            customer.modify_customer_info(email="invalid_email")
        self.assertIn("Invalid email format",
                      str(context.exception))

    def test_delete_nonexistent_customer(self):
        """Probar eliminar cliente que no existe"""
        with self.assertRaises(ValueError) as context:
            Customer.delete_customer("C099")
        self.assertIn("Customer not found",
                      str(context.exception))

    def test_load_customers_file_not_found(self):
        """Test handling of FileNotFoundError
        during customer loading from a file."""
        with patch('builtins.open', side_effect=FileNotFoundError), \
                patch('logging.error') as mock_log_error:
            Customer.load_customers_from_file("nonexistent_file.json")

            mock_log_error.assert_called_with(
                "Archivo %s no encontrado. Se iniciará con una lista vacía.",
                "nonexistent_file.json"
            )

    def test_load_customers_with_json_decode_error(self):
        """Test handling of JSONDecodeError
        during customer loading from a file."""
        with patch('builtins.open', mock_open(read_data='{"invalid_json":')), \
                patch('logging.error') as mock_log_error:
            Customer.load_customers_from_file("invalid_json.json")

            mock_log_error.assert_called_with(
                "Error al decodificar JSON en %s.",
                "invalid_json.json"
            )

    def test_modify_customer_name_email(self):
        """Test modifying the customer's name."""
        # Crear una instancia de cliente para esta prueba específica
        test_customer = Customer.create_customer("C0002",
                                                 "John Doe",
                                                 "john.doe@example.com")
        # Modificar el nombre del cliente
        test_customer.modify_customer_info(name="Jane Doe")
        test_customer.modify_customer_info(email="john1.doe@example.com")
        # Verificar que el nombre del cliente se ha actualizado correctamente
        self.assertEqual(test_customer.name, "Jane Doe")
        self.assertEqual(test_customer.email, "john1.doe@example.com")

    @classmethod
    def tearDownClass(cls):
        """Método llamado después de todas las pruebas de esta clase."""
        # Resetear la lista de clientes después de las pruebas
        Customer.customers = []
        # Opcional: Eliminar el archivo de prueba si existe
        # if os.path.exists("test_customers.json"):
        #    os.remove("test_customers.json")


if __name__ == '__main__':
    unittest.main()
