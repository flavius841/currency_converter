import requests
import os
from colorama import init, Fore, Style
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import pandas as pd

# url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{base}.json"
commands = ['help', 'exit', 'list', 'dictionary']


command_completer = WordCompleter(commands, ignore_case=True)


def main():
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

        elif message.lower() == 'list':
            list_currencies()

        elif message.lower() == 'dictionary':
            message = input("Enter the full currency name: ")
            find_currency_code(message)


def help_menu():
    help_text = """
    Currency Converter CLI Help:
    - To convert currencies, enter the amount, source currency code, and target currency code.
      Example: 100 USD EUR
    - Type 'list' to see all supported currency codes.
    - Type 'exit' to quit the application.
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


def find_currency_code(currency_name):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "currency_names_full.csv")
    df = pd.read_csv(csv_path)
    matches = df.loc[df["FullName"] == currency_name]

    if not matches.empty:
        code = matches["Code"].values[0]
        print(
            Fore.CYAN + f"The currency code for '{currency_name}' is: {code}" + Style.RESET_ALL)
    else:
        print(
            Fore.RED + f"Error: Currency name '{currency_name}' not found." + Style.RESET_ALL)
