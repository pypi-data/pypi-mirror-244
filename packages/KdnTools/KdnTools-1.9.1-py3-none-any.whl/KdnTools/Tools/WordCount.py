class WordCount:
    def __init__(self, input_string):
        self.input_string = input_string

    @classmethod
    def count_words(cls, input_string):
        word_count = len(input_string.split())
        return word_count

    def __str__(self):
        return str(self.count_words(self.input_string))
