import os


class DriveLetter:
    def __init__(self):
        self.script_directory = os.path.dirname(os.path.abspath(__file__))
        self.drive_letter = self.get_drive_letter()

    def get_drive_letter(self):
        return str(self.script_directory[0]) if self.script_directory else None

    def __str__(self):
        return str(self.drive_letter)
