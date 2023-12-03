# KdnTools

## Description

KdnTools is a Python package that provides a collection of useful tools for common tasks in Python development. Whether
you"re working with databases, handling user interactions, or performing various operations, KdnTools aims to simplify
and enhance your coding experience.

## Features

- **User Interaction Tools**: Includes a user class with methods for colored text output and a choice menu for user-friendly interactions.

- **Database Management**: Simplifies common SQLite database operations, such as creating tables, inserting data, viewing data, and more.

- **Random Number Generation**: Provides a tool for generating random numbers within a specified range.

- **Word Count**: Allows you to count the number of words in a given string.

- **Drive Letter**: Retrieves the drive letter of the script"s directory.

- **Tasks Management (Example)**: An example module showcasing how to use KdnTools for managing tasks with a SQLite database.

# Documentation

## DataFetcher

The DataFetcher class is designed for making HTTP requests. It supports GET, POST, PUT, and DELETE operations.

### Example Usage:

fetcher = DataFetcher(base_url="https://api.example.com", api_key="your_api_key")

### Fetch data

data = fetcher.fetch_data(endpoint="users", params={"page": 1})

### Post data

new_user = {"name": "John Doe", "email": "john@example.com"}
response = fetcher.post_data(endpoint="users", data=new_user)


## DbManage

The DbManage class simplifies SQLite database operations.

### Example Usage:

db_manager = DbManage(db_location="example.db")

### Create a table

columns = {"id": "INTEGER", "name": "TEXT", "age": "INTEGER"}
db_manager.create_table(table_name="users", columns=columns)

### Insert data

user_data = {"name": "John Doe", "age": 25}
db_manager.insert_data(table_name="users", data=user_data)

### View data

db_manager.view_data(table_name="users")

### Remove data

db_manager.remove_data(table_name="users", condition="age > 30")

## DriveLetter

The DriveLetter class retrieves the drive letter of the script"s directory.

print(f"Drive Letter: {DriveLetter()}")


## Files

The Files class provides methods for writing, reading, and appending data to files.

### Write to a file

Files.write(file_name, data_to_write)

### Read from a file

read_data = Files.read_file(file_name)

print(f"Read Data: {read_data}")

### Append to a file

data_to_append = "\nAppended Data!"

Files.append(file_name, data_to_append)


## RandNumber

The RandNumber class generates a random number within a specified range.

### Example Usage:
rand_num_generator = RandNumber(num1=1, num2=100)

random_number = str(rand_num_generator)

print(f"Random Number: {random_number}")


## String
The String class provides various string manipulation tools.

### ReverseString 

input_str = "KdnTools"

reversed_str = str(String.ReverseString(input_str))

print(f"Reversed String: {reversed_str}")

### Uppercase

input_str = "KdnTools"

uppercase_str = str(String.Uppercase(input_str))

print(f"Uppercase String: {uppercase_str}")

### Lowercase

input_str = "KdnTools"
lowercase_str = str(String.Lowercase(input_str))
print(f"Lowercase String: {lowercase_str}")

### Capitalize

input_str = "KdnTools"

capitalized_str = str(String.Capitalize(input_str))

print(f"Capitalized String: {capitalized_str}")

### Palindrome

input_str = "KdnTools"

palindrome_check = str(String.Palindrome(input_str))

print(f"Is Palindrome: {palindrome_check}")

### SubstringCount

input_str = "KdnTools"

substring = "Kdn"

count_substring = str(String.SubstringCount(input_str, substring))

print(f"Occurrences of "{substring}": {count_substring}")

### ReverseWords

input_str = "KdnTools is awesome"

reversed_words = str(String.ReverseWords(input_str))

print(f"Reversed Words: {reversed_words}")

## User
The User class provides methods for user interaction, including colored text output and a choice menu.

### Example Usage:
user = User()

### Colored Text Output
user.Ctext(user.green, "Welcome to KdnTools!")

### Choice Menu
choices = ["Option 1", "Option 2", "Option 3"]

selected_option = user.Choice("Please select an option:", choices)

### Displaying the selected option
user.Ctext(user.blue, f"Selected Option: {choices[selected_option - 1]}")


### Methods
Ctext(colour, text)
Displays colored text in the console.

Parameters:

colour (str): Color code for the text (e.g., user.green).

text (str): The text to be displayed.

Choice(text, options)

Provides a user-friendly choice menu.


Parameters:


text (str): The prompt or question to be displayed.

options (list): List of options for the user to choose from.

Returns:

int: The index of the selected option in the provided list.


# Installation

```bash
pip install KdnTools
```
