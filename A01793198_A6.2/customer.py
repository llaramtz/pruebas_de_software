"""Module for managing customer data."""
import json
import re
import logging


class Customer:
    """Manages customer information."""

    customers = []

    def __init__(self, customer_id, name, email):
        """Initialize a new customer object."""
        self.customer_id = customer_id
        self.name = name
        self.email = email

    @classmethod
    def create_customer(cls, customer_id, name, email):
        """Create and return a new customer."""
        if not cls.is_valid_email(email):
            raise ValueError("Invalid email format.")
        if any(customer for customer in cls.customers
               if customer.customer_id == customer_id):
            raise ValueError("A customer with the given ID already exists.")
        if not name:
            raise ValueError("Name cannot be empty.")
        new_customer = cls(customer_id, name, email)
        cls.customers.append(new_customer)
        return new_customer

    @classmethod
    def delete_customer(cls, customer_id):
        """Delete a customer by ID."""
        for existing_customer in cls.customers:
            if existing_customer.customer_id == customer_id:
                cls.customers.remove(existing_customer)
                return True
        raise ValueError("Customer not found.")

    def modify_customer_info(self, name=None, email=None):
        """Modify customer's name and/or email."""
        if name:
            self.name = name
        if email:
            if not self.is_valid_email(email):
                raise ValueError("Invalid email format.")
            self.email = email

    @staticmethod
    def is_valid_email(email):
        """Validate email format."""
        email_pattern = (
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        )
        return re.match(email_pattern, email) is not None

    @classmethod
    def save_customers_to_file(cls, filename="customers.json"):
        """Save all customers to a file."""
        with open(filename, "w", encoding="utf-8") as file_handle:
            json.dump([cust.__dict__ for cust in cls.customers],
                      file_handle, indent=4)

    @classmethod
    def load_customers_from_file(cls, filename="customers.json"):
        """Load customers from a file."""
        try:
            with open(filename, "r", encoding="utf-8") as file_handle:
                customers_data = json.load(file_handle)
            for customer_data in customers_data:
                try:
                    cls.create_customer(**customer_data)
                except ValueError as value_error:
                    logging.error("Error al cargar cliente: %s", value_error)
        except FileNotFoundError:
            logging.error("Archivo %s no encontrado. "
                          "Se iniciará con una lista vacía.", filename)
        except json.JSONDecodeError:
            logging.error("Error al decodificar JSON en %s.", filename)
        else:
            logging.info("Customers loaded successfully.")
