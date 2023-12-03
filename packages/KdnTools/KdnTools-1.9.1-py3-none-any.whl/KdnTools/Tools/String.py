class String:
    class ReverseString:
        def __init__(self, input_string):
            self.input_string = input_string

        @staticmethod
        def reverse(input_string):
            return input_string[::-1]

        def __str__(self):
            return self.reverse(self.input_string)

    class Uppercase:
        def __init__(self, input_string):
            self.input_string = input_string

        @staticmethod
        def to_uppercase(input_string):
            return input_string.upper()

        def __str__(self):
            return self.to_uppercase(self.input_string)

    class Lowercase:
        def __init__(self, input_string):
            self.input_string = input_string

        @staticmethod
        def to_lowercase(input_string):
            return input_string.lower()

        def __str__(self):
            return self.to_lowercase(self.input_string)

    class Capitalize:
        def __init__(self, input_string):
            self.input_string = input_string

        @staticmethod
        def capitalize_first(input_string):
            return input_string.capitalize()

        def __str__(self):
            return self.capitalize_first(self.input_string)

    class Palindrome:
        def __init__(self, input_string):
            self.input_string = input_string

        @staticmethod
        def is_palindrome(input_string):
            cleaned_str = "".join(char.lower() for char in input_string if char.isalnum())
            return cleaned_str == cleaned_str[::-1]

        def __str__(self):
            return f"Is Palindrome: {self.is_palindrome(self.input_string)}"

    class SubstringCount:
        def __init__(self, input_string, substring):
            self.input_string = input_string
            self.substring = substring

        @staticmethod
        def count_substring(input_string, substring):
            return input_string.count(substring)

        def __str__(self):
            return f"Occurrences of "
            {self.substring}
            ": {self.count_substring(self.input_string, self.substring)}"

    class ReverseWords:
        def __init__(self, input_string):
            self.input_string = input_string

        @staticmethod
        def reverse_words(input_string):
            words = input_string.split()
            reversed_words = " ".join(word[::-1] for word in words)
            return reversed_words

        def __str__(self):
            return f"Reversed Words: {self.reverse_words(self.input_string)}"
