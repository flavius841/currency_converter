import requests
import os
from colorama import init, Fore, Style
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

# url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{base}.json"
commands = ['help', 'exit', 'list']


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
