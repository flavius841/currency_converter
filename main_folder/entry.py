import requests
import os
from colorama import init, Fore, Style
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import pandas as pd
from difflib import get_close_matches
from datetime import date, datetime

# url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{base}.json"
commands = ['help', 'exit', 'list', 'dictionary',
            'history_list', 'swap', 'check']

base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "currency_names_full.csv")
df = pd.read_csv(csv_path)
currecny_names_or_code = df["FullName"].tolist()
currecny_names_or_code = currecny_names_or_code + df["Code"].tolist()


csv_path = os.path.join(base_dir, "history_currencies.csv")
df = pd.read_csv(csv_path)
historical_currecny_names = df["Name"].tolist()
historical_currecny_codes = df["Code"].tolist()


command_completer = WordCompleter(commands, ignore_case=True)
currency_completer = WordCompleter(currecny_names_or_code, ignore_case=True)
previous_parts = []


def main():
    global previous_parts
    print(Fore.GREEN + "Welcome to the Currency Converter CLI!" + Style.RESET_ALL)
    print("Type 'help' for instructions or 'exit' to quit.")

    while True:
        message = prompt(">>> ", completer=command_completer).strip()
        parts = message.split()

        if message.lower() == 'exit':
            print(
                Fore.YELLOW + "Exiting the Currency Converter CLI. Goodbye!" + Style.RESET_ALL)
            break
        elif message.lower() == 'help':
            help_menu()

        elif len(parts) == 3 and (parts[0].replace('.', '', 1).isdigit() or parts[0].isnumeric()):
            convert_currency(parts)

        elif len(parts) == 4 and (parts[0].replace('.', '', 1).isdigit() or parts[0].isnumeric()) and parts[3].replace('-', '').isdigit():
            currency_history(parts)

        elif message == 'check':
            list_historical_currencies()

        elif len(parts) == 2 and parts[0].lower() == 'check':
            check_if_historical_currency_supported(parts)

        elif message.lower() == 'list':
            list_currencies()

        elif message.lower() == 'history_list':
            list_historical_currencies()

        elif message.lower() == 'dictionary':
            message = prompt("Enter the full currency name or it's code: ",
                             completer=currency_completer).strip()
            find_currency_code(message.title())

        elif message.lower() == 'swap' and (len(previous_parts) == 3 and (previous_parts[0].replace('.', '', 1).isdigit()
                                                                          or previous_parts[0].isnumeric())):
            previous_parts[1], previous_parts[2] = previous_parts[2], previous_parts[1]
            convert_currency(previous_parts)

        elif message.lower() == 'swap':
            print(Fore.RED + "Invalid previous command." + Style.RESET_ALL)

        else:
            print(
                Fore.RED + "Invalid command or input. Type 'help' for instructions." + Style.RESET_ALL)

        previous_parts = parts


def help_menu():
    help_text = f"""
    {Fore.BLUE}Currency Converter CLI Help:{Style.RESET_ALL}

    - To convert currencies, enter the{Fore.CYAN} amount{Style.RESET_ALL},{Fore.CYAN} source currency code{Style.RESET_ALL}, and{Fore.CYAN} target currency code{Style.RESET_ALL}.
      Example: 100 USD EUR
      
    - To view historical exchange rates, enter the{Fore.CYAN} amount{Style.RESET_ALL},{Fore.CYAN} source currency code{Style.RESET_ALL},{Fore.CYAN} target currency code{Style.RESET_ALL}, and{Fore.CYAN} date (YYYY-MM-DD){Style.RESET_ALL}.
      Example: 100 USD EUR 2022-01-01
      Note: Historical data feature doesn't work for all currencies from the list.

    - Type{Fore.GREEN} 'list'{Style.RESET_ALL} to see all supported currency codes.
    
    - Type{Fore.GREEN} 'exit'{Style.RESET_ALL} to quit the application.
    
    - Type{Fore.GREEN} 'dictionary'{Style.RESET_ALL} to find the currency code by its full name and vice versa.
      Example: If you enter 'United States Dollar', it will return 'USD'.

    - Type{Fore.GREEN} 'history_list'{Style.RESET_ALL} to see all supported currencies for historical data.

    - Type{Fore.GREEN} 'check <CURRENCY_CODE>'{Style.RESET_ALL} to check if a currency code is supported for historical data.
      Example: check USD
      Note: YO=ou can not use cuurrency names with this command, only currency codes.

    - Type {Fore.GREEN} 'swap' {Style.RESET_ALL} to swap the currency codes of your previous input.
      Example: If your previous command was 100 USD EUR, after using swap it will become 100 EUR USD.
      Note: This won't work if your previous command wasn't in the format shown in the example.
    """
    print(help_text)


def convert_currency(parts):
    amount = float(parts[0])
    from_currency = parts[1].lower()
    to_currency = parts[2].lower()
    url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{from_currency}.json"
    try:
        response = requests.get(url)
        if response.status_code == 404:
            print(
                Fore.RED + f"Error: Unsupported source currency code '{from_currency.upper()}'." + Style.RESET_ALL)
            return
        data = response.json()
        if to_currency in data[from_currency]:
            rate = data[from_currency][to_currency]
            converted_amount = amount * rate
            print(
                Fore.CYAN + f"{amount} {from_currency.upper()} = {converted_amount:.2f} {to_currency.upper()}" + Style.RESET_ALL)
        else:
            print(
                Fore.RED + f"Error: Unsupported target currency code '{to_currency.upper()}'." + Style.RESET_ALL)
    except requests.exceptions.RequestException as e:
        print(Fore.RED + "Error: Could not reach the currency API. "
              "The website may be down or your internet may be offline." + Style.RESET_ALL)


def list_currencies():
    url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/usd.json"
    try:
        response = requests.get(url)
        data = response.json()
        for currency_code in data['usd']:
            print(currency_code.upper())
    except requests.exceptions.RequestException as e:
        print(Fore.RED + "Error: Could not reach the currency API. "
              "The website may be down or your internet may be offline." + Style.RESET_ALL)


def find_currency_code(currency_name_or_code):
    full_name_matches = df.loc[df["FullName"].str.lower()
                               == currency_name_or_code.lower()]

    if not full_name_matches.empty:
        code = full_name_matches["Code"].values[0]
        print(
            Fore.CYAN + f"The currency code for '{currency_name_or_code}' is: {code}" + Style.RESET_ALL)
        return

    code_matches = df.loc[df["Code"].str.lower() ==
                          currency_name_or_code.lower()]

    if not code_matches.empty:
        code = code_matches["FullName"].values[0]
        print(
            Fore.CYAN + f"The code name for '{currency_name_or_code}' is: {code}" + Style.RESET_ALL)
        return

    suggestions = get_close_matches(
        currency_name_or_code, currecny_names_or_code, n=3, cutoff=0.6)

    if suggestions:
        print(Fore.YELLOW + f"Did you mean one of these?" + Style.RESET_ALL)
        for suggestion in suggestions:
            print(Fore.YELLOW + f"- {suggestion}" + Style.RESET_ALL)
        return

    else:
        print(
            Fore.RED + f"Error: Currency name '{currency_name_or_code}' not found." + Style.RESET_ALL)


def currency_history(parts):
    amount = float(parts[0])
    from_currency = parts[1].upper()
    to_currency = parts[2].upper()
    if not is_valid_date(parts[3]):
        print(Fore.RED + "Error: Please enter a valid date" + Style.RESET_ALL)
        return
    input_date = datetime.strptime(parts[3], "%Y-%m-%d").date()
    today = date.today()
    earliest_date = date(2007, 1, 1)
    if input_date < earliest_date:
        print(Fore.RED + "Error: The date cannot be earlier than January 1, 2007." + Style.RESET_ALL)
        return
    if input_date > today:
        print(Fore.RED + "Error: The date cannot be in the future." + Style.RESET_ALL)
        return
    rates = "rates"
    if from_currency not in historical_currecny_codes:
        print(
            Fore.RED + f"Error: The currency code '{from_currency}' is not supported for historical data." + Style.RESET_ALL)
        return
    if to_currency not in historical_currecny_codes:
        print(
            Fore.RED + f"Error: The currency code '{to_currency}' is not supported for historical data." + Style.RESET_ALL)
        return
    url = f"https://api.frankfurter.app/{input_date}?from={from_currency}&to={to_currency}"
    try:
        response = requests.get(url, timeout=5)

        data = response.json()
        rate = data[rates][to_currency]
        converted_amount = amount * rate
        print(
            Fore.CYAN + f"On {input_date}: {amount} {from_currency.upper()} = {converted_amount:.2f} {to_currency.upper()}" + Style.RESET_ALL)

    except requests.exceptions.RequestException as e:
        print(Fore.RED + "Error: Could not reach the currency API. "
              "The website may be down or your internet may be offline." + Style.RESET_ALL)


def list_historical_currencies():
    print(Fore.CYAN + "Supported currencies for historical data:" + Style.RESET_ALL)
    for currency_name in historical_currecny_names:
        print(currency_name)


def check_if_historical_currency_supported(parts):

    if parts[1].upper() in historical_currecny_codes:
        print(
            Fore.CYAN + f"The currency code '{parts[1]}' is supported for historical data." + Style.RESET_ALL)
    else:
        print(
            Fore.RED + f"The currency code '{parts[1]}' is NOT supported for historical data." + Style.RESET_ALL)


def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True

    except ValueError:
        return False


# def swap_function():
