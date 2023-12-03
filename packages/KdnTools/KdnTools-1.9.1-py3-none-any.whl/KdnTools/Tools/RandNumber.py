from random import randint
from logging import error


class RandNumber:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2

    @classmethod
    def rand_number(cls, num1, num2):
        try:
            return randint(num1, num2)
        except ValueError as e:
            error(f"Error generating random number: {e}")
            return None

    def __str__(self):
        rand_num = self.rand_number(self.num1, self.num2)
        return str(rand_num) if rand_num is not None else "Error"
