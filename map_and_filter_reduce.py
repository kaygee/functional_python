from copy import copy
from datetime import datetime
from functools import reduce
import json
from operator import attrgetter, itemgetter

class Book:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return self.title

    def __repr__(self):
        return str(self)

def get_books(filename, raw=False):
    try:
        data = json.load(open(filename))
    except FileNotFoundError:
        return []
    else:
        if raw:
            return data['books']
        return [Book(**book) for book in data['books']]

important_list = [5, 3, 1, 2, 4]

# important_list.sort() # Bad idea because it sorts in place.

# returns a sorted copy of the list.
print(sorted(important_list))
print(important_list)

BOOKS = get_books('books.json')
RAW_BOOKS = get_books('books.json', raw=True)

pub_sort = sorted(RAW_BOOKS, key=itemgetter('publish_date'))
print(pub_sort[0]['publish_date'], pub_sort[-1]['publish_date'])

pages_sort = sorted(BOOKS, key=attrgetter('number_of_pages'))
print(pages_sort[0].number_of_pages, pages_sort[-1].number_of_pages)

# https://docs.python.org/2/library/operator.html

a = [1, 2, 3]
def double(n):
    return n * 2

print(list(map(double, a)))

def apply_sales_price(book):
    """Apply a 20 percent discount to the book's price"""
    book = copy(book)
    book.price = round(book.price-book.price*.2, 2)
    return book

# original price
print(BOOKS[0].price)

# using map
sales_books = list(map(apply_sales_price, BOOKS))
print(sales_books[0].price)
# list comprehension
sales_books2 = [apply_sales_price(book) for book in BOOKS]
print(sales_books2[0].price)

backwards = [
    'tac',
    'esuoheerT',
    'htenneK',
    [5, 4, 3, 2, 1],
]

def reverse(iterable):
  return  iterable[::-1]

forwards = map(reverse, backwards)
print(forwards)

dimensions = [
    (5, 5),
    (10, 10),
    (2.2, 2.3),
    (100, 100),
    (8, 70),
]

def area(arg):
  return arg[0] * arg[1]

areas = [area(dimension) for dimension in dimensions]
print(areas)

## FILTER ##
def is_long_book(book):
    return book.number_of_pages >= 600

long_books = list(filter(is_long_book, BOOKS))
print(len(BOOKS))
print(len(long_books))

# list comprehension
long_books_2 = [book for book in BOOKS if book.number_of_pages >= 600]
print(len(long_books_2))

dates = [
    datetime(2012, 12, 15),
    datetime(1987, 8, 20),
    datetime(1965, 2, 28),
    datetime(2015, 4, 29),
    datetime(2012, 6, 30),
]

def is_2012(arg):
  return arg.year == 2012

dt_2012 = filter(is_2012, dates)
print(dt_2012)

words = [
    'yellow',
    'red',
    'yesterday',
    'tomorrow',
    'zucchini',
    'eggplant',
    'year',
    'month',
    'yell',
    'yonder',
]

y_words = [word for word in words if word[0] == 'y']
print(y_words)

#chaining
def has_roland(book):
    return any(["Roland" in subject for subject in book.subjects])

def titlecase(book):
    book = copy(book)
    book.title = book.title.title()
    return book

print(list(map(titlecase, filter(has_roland, BOOKS))))

def is_good_deal(book):
    return book.price <= 5

cheap_books = sorted(
    filter(is_good_deal, map(apply_sales_price, BOOKS)),
    key=attrgetter('price')
)
print("Cheapest book is {} at price of {}".format(cheap_books[0], cheap_books[0].price))

# Create a function named is_over_13 that takes a datetime and returns whether or
# not the difference between that datetime and today is 4745 days or more.
birthdays = [
    datetime(2012, 4, 29),
    datetime(2006, 8, 9),
    datetime(1978, 5, 16),
    datetime(1981, 8, 15),
    datetime(2001, 7, 4),
    datetime(1999, 12, 30)
]

today = datetime.today()

def is_over_13(argument):
    return (argument - today).days

print(is_over_13(birthdays[0]))

# Now create a function named date_string that takes a datetime and returns a
# string like "May 20" using strftime. The format string is "%B %d".
def date_string(argument):
    return argument.strftime("%B %d")

print(date_string(birthdays[0]))

# Finally, make a variable named birth_dates. Use map() and filter(), along
# with your two functions, to create date strings for every datetime in birthdays
# so long as the datetime is more than 13 years old.
birth_dates = map(
    date_string,
    filter(is_over_13, birthdays)
)
print(birth_dates)

# As a dumb American, I don't understand Celsius temperatures. Using c_to_f and
# a list comprehension, create a variable named good_temps. Convert each Celsius
# temperature into Fahrenheit, but only if the Celsius temperature is between 9 and 32.6.
temperatures = [
    37,
    0,
    25,
    100,
    13.2,
    29.9,
    18.6,
    32.8
]

def c_to_f(temp):
    """Returns Celsius temperature as Fahrenheit"""
    return temp * (9/5) + 32

good_temps = [c_to_f(temperature) for temperature in temperatures if 9 <= temperature <= 32.6]
print(good_temps)

def product(x, y):
    return (x * y)

print(reduce(product, [1, 2, 3, 4, 5]))

def add_book_prices(book1, book2):
    return book1 + book2

total = reduce(add_book_prices, [b.price for b in BOOKS])
print("total price {}".format(total))
