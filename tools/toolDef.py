from models.modelDef import Weather, Article, Directions, Time
from geopy.geocoders import Nominatim
from currency_converter import CurrencyConverter
import json
from datetime import datetime
cur_convert = CurrencyConverter()

import requests

def calculate_mortgage_payment(
    loan_amount: int, interest_rate: float, loan_term: int
) -> float:
    """Get the monthly mortgage payment given an interest rate percentage."""
    # Convert annual interest rate to a monthly rate
    monthly_rate = interest_rate / 100 / 12
    
    # Total number of payments
    num_payments = loan_term * 12
    
    # Calculate the monthly payment using the formula
    if monthly_rate == 0:
        # If the interest rate is 0, simply divide the loan amount by the number of payments
        monthly_payment = loan_amount / num_payments
    else:
        monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)
    
    return monthly_payment


def get_article_details(
    title: str,
    authors: list[str],
    short_summary: str,
    date_published: str,
    tags: list[str],
) -> Article:
    '''Get article details from unstructured article text.
    date_published: formatted as "MM/DD/YYYY"'''

    # TODO: you must implement this to actually call it later


def get_weather(city) -> Weather:
    """Get the current weather given a city."""
    if isinstance(city, list):
        cities = city
    else:
        cities = [city]

    results = []
    for city in cities:
        geolocator = Nominatim(user_agent='myapplication')
        location = geolocator.geocode(city)
        response = json.loads(requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={location.latitude}&longitude={location.longitude}&current=temperature_2m").text)
        temperature = response["current"]["temperature_2m"]
        unit = response["current_units"]["temperature_2m"]
        date = response["current"]["time"]

        results.append(Weather(city=city, date=date, temperature=temperature, unit=unit))

    return results



def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """Convert a currency amount to another currency."""

     # doctest: +SKIP
    return f"{amount} {from_currency} = {cur_convert.convert(amount, from_currency, to_currency)} {to_currency}"

def get_directions(start: str, destination: str) -> Directions:
    """Get directions from Google Directions API.
    start: start address as a string including zipcode (if any)
    destination: end address as a string including zipcode (if any)"""

    # TODO: you must implement this to actually call it later
    return [Directions(from_location=start, to_location=destination)]

def get_current_time(*args) -> Time:
    """Get the current time
    """
    time=datetime.now()

    return [Time(time=time)]

def generic_response_no_tool(answer: str) -> str:
    # print(f"Response from generic_response tool {answer}")
    return [answer]