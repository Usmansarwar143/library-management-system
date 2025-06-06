import re

class Validators:
    @staticmethod
    def validate_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_phone(phone):
        pattern = r'^\+?\d{10,15}$'
        return bool(re.match(pattern, phone)) if phone else True

    @staticmethod
    def validate_quantity(quantity):
        try:
            qty = int(quantity)
            return qty >= 0
        except ValueError:
            return False