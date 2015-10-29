from copy import copy
from datetime import datetime
from functools import reduce, partial
import json
from operator import attrgetter, itemgetter
from operator import add

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

#Example that reduce uses recursion
def long_total(a=None, b=None, books=None):
    if a is None and b is None and books is None:
        return None
    if a is None and b is None and books is not None:
        a = books.pop(0)
        b = books.pop(0)
        return long_total(a, b, books)
    if a is not None and books and books is not None and b is None:
        b = books.pop(0)
        return long_total(a, b, books)
    if a is not None and b is not None and books is not None:
        return long_total(a+b, None, books)
    if a is not None and b is not None and not books:
        return long_total(a+b, None, None)
    if a is not None and b is None and not books or books is None:
        return a
# Keep recursion going until no elements are left.
print(long_total(None, None, [b.price for b in BOOKS]))

def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n - 1)
print("factorial {}".format((5)))

# We have a bunch of prices and sales numbers and we need to find out our total earnings.
# Let's start by writing a function named product_sales that takes a single
# two-member tuple made up of a price and a number of units sold. product_sales
# should return the product of the price and the number of units.
prices = [
    (6.99, 5),
    (2.94, 15),
    (156.99, 2),
    (99.99, 4),
    (1.82, 102)
]

def product_sales(price_and_number_of_units_sold):
    return price_and_number_of_units_sold[0] * price_and_number_of_units_sold[1]

print(product_sales((20, 4.99)))

# We need to add two numbers together. We could write a function that does this but that seems silly.
# Import add from the operator module.
# Alright, one more import. Import reduce() from functools.

# Finally, we're ready to find our totals. Create a variable named total.
# Use map() to find the per-product totals for each item in prices, then use
# reduce (and add) to find the total value.
total = reduce(add, map(product_sales, prices))

print(total)

# Finish the prereqs function so that it recursively finds all of the prerequisite
# course titles in courses (like "Object-Oriented Python" is a prerequisite for
# "Django Basics"). You should add() the title of the prerequisite to the pres set
# and then call prereqs again with the child courses.
# In the end, return the prereqs set.
courses = {'count': 2,
           'title': 'Django Basics',
           'prereqs': [{'count': 3,
                     'title': 'Object-Oriented Python',
                     'prereqs': [{'count': 1,
                               'title': 'Python Collections',
                               'prereqs': [{'count':0,
                                         'title': 'Python Basics',
                                         'prereqs': []}]},
                              {'count': 0,
                               'title': 'Python Basics',
                               'prereqs': []},
                              {'count': 0,
                               'title': 'Setting Up a Local Python Environment',
                               'prereqs': []}]},
                     {'count': 0,
                      'title': 'Flask Basics',
                      'prereqs': []}]}


def prereqs(data, pres=None):
    pres = pres or set()
    # for each prereq in this courses' prereqs...
    for prereq in data['prereqs']:
        # add title of this prereq course, then...
        pres.add(prereq['title'])
        # use recursive call to find further prerequisites of this
        # course, if any
        prereqs(prereq, pres)
    # return current
    return pres

print(prereqs(courses))

# anonymous functions / lambdas
total = reduce(lambda x, y: x + y, [b.price for b in BOOKS])
print(total)
long_books = filter(lambda book: book.number_of_pages >= 600, BOOKS)
print(len(list(long_books)))
good_deals = filter(lambda book: book.price <= 6, BOOKS)
print(len(list(good_deals)))

meals = [
    {'name': 'cheeseburger',
     'calories': 750},
    {'name': 'cobb salad',
     'calories': 250},
    {'name': 'large pizza',
     'calories': 1500},
    {'name': 'burrito',
     'calories': 1050},
    {'name': 'stir fry',
     'calories': 625}
]

high_cal = filter(lambda meal: meal['calories'] > 1000, meals)
print(list(high_cal))

# Use reduce() and a lambda to find the longest string in strings. Save this
# value in the variable longest.
# Remember, reduce() takes two arguments and you can write an if statement like:
# give_me_this if this_thing > that_thing else give_me_that.
strings = [
    "Do not take life too seriously. You will never get out of it alive.",
    "My fake plants died because I did not pretend to water them.",
    "A day without sunshine is like, you know, night.",
    "Get your facts first, then you can distort them as you please.",
    "My grandmother started walking five miles a day when she was sixty. She's ninety-seven know and we don't know where she is.",
    "Life is hard. After all, it kills you.",
    "All my life, I always wanted to be somebody. Now I see that I should have been more specific.",
    "Everyone's like, 'overnight sensation.' It's not overnight. It's years of hard work.",
]
longest = reduce(lambda x, y: x if len(x) > len(y) else y, strings)
print("The longest string is \"{}\"".format(longest))

#Partials
def mark_down(book, discount):
    book = copy(book)
    book.price = round(book.price - book.price * discount, 2)
    return book

standard = partial(mark_down, discount=.2)
print(standard(BOOKS[0]).price)

half = partial(mark_down, discount=.5)
print(standard(BOOKS[5]).price)

half_price_books = map(half, filter(is_long_book, BOOKS))
print(list(half_price_books))

# Now, use partial to make a version of discount that applies a 10% discount.
# Name this partial function discount_10.
partial_prices = [
    10.50,
    9.99,
    0.25,
    1.50,
    8.79,
    101.25,
    8.00
]

def discount(price, amount):
    return price - price * (amount/100)
discount_10 = partial(discount, amount=10)
# Great! Follow that same pattern to make discount_25 and discount_50 with 25%
# and 50% discounts each.
discount_25 = partial(discount, amount=25)
discount_50 = partial(discount, amount=50)
# Finally, I need to see all of our prices with each discount applied. Use map()
# to create prices_10, prices_25, and prices_50 where you discount all of the prices
# with the appropriate discount.
prices_10 = map(discount_10, partial_prices)
print(list(prices_10))
prices_25 = map(discount_25, partial_prices)
print(list(prices_25))
prices_50 = map(discount_50, partial_prices)
print(list(prices_50))

#currying
def curried_f(x, y=None, z=None):
    def f(x, y, z):
        return x**3 + y**2 + z
    if y is not None and z is not None:
        return f(x, y, z)
    if y is not None:
        return lambda z: f(x, y, z)
    return lambda y, z=None: (
        f(x, y, z) if (y is not None and z is not None)
        else (lambda z: f(x, y, z)))

print(curried_f(2, 3, 4))
g = curried_f(2)
print(g)
h = g(3)
print(h)
i = h(4)
print(i)
