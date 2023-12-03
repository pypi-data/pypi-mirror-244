class List:
    def __init__(self, text):
        self.text = text
        self.list = self.make_list()

    def make_list(self):
        return self.text.split()

    def add_item(self, item):
        self.list.append(item)

    def remove_item(self, item):
        if item in self.list:
            self.list.remove(item)
            print(f"{item} removed from the list.")
        else:
            print(f"{item} not found in the list.")

    def display_list(self):
        print("Current List:")
        for i, item in enumerate(self.list, start=1):
            print(f"{i}. {item}")

    def clear_list(self):
        self.list = []
        print("List cleared.")

    def sort_list(self):
        self.list.sort()
        print("List sorted.")

    def reverse_list(self):
        self.list.reverse()
        print("List reversed.")

    def search_item(self, item):
        if item in self.list:
            print(f"{item} found in the list.")
        else:
            print(f"{item} not found in the list.")

    def count_elements(self):
        count = len(self.list)
        print(f"Number of elements in the list: {count}")

    def get_unique_elements(self):
        unique_elements = list(set(self.list))
        print("Unique Elements:", unique_elements)

    def get_duplicates(self):
        seen = set()
        duplicates = set(x for x in self.list if x in seen or seen.add(x))
        print("Duplicate Elements:", list(duplicates))
