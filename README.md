# currency_converter

This is a **CLI (Command Line Interface) project** that allows you to: 
1. convert currencies
2. view historical exchange rates
3. find the currency code by its full name and vice versa


## Prerequisites

To run this project, you need to have **Python** and **Git** installed on your system.

---
If you already have Python and Git, you can jump to the Running the CLI section.

---

## Installing Python

### **macOS**

1. Go to the official site: [https://www.python.org/downloads/macos/](https://www.python.org/downloads/macos/)
2. Download the `.pkg` installer.
3. Open it and follow the instructions.

Then, install **pipx**:

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

Restart your terminal after running `ensurepath`.

---

### **Linux (Ubuntu/Debian)**

Install Python:

```bash
sudo apt update
sudo apt install python3
```

Then, install pip and pipx:

```bash
sudo apt install python3-pip
sudo apt update
sudo apt install pipx
```

---

### **Windows**

1. Download Python from: [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
2. Run the installer.
   **Important:** Check the box **“Add Python to PATH”** before clicking “Install Now.”
3. After installation, install pipx:

```cmd
python -m pip install --user pipx
python -m pipx ensurepath
```

Restart Command Prompt after running `ensurepath`.

---

## Installing Git

### **macOS**

If you have Homebrew:

```bash
brew install git
```

### **Linux (Ubuntu/Debian)**

```bash
sudo apt update
sudo apt install git
```

### **Windows**

1. Go to: [https://git-scm.com/download/win](https://git-scm.com/download/win)
2. Download the installer and follow the prompts (default options are fine).

---

## Running the CLI

After installing Python, pipx, and Git, you can install the CLI project:

```bash
pipx install git+https://github.com/flavius841/currency_converter
```

Now, you can run the CLI by typing:

```bash
convert_currency
```

in your terminal or Command Prompt.

---

## Notes
* Make sure Python, pipx, and Git are installed correctly before running the CLI.

---

## How to use it

1. To convert currencies, enter the amount, source currency code, and target currency code.
      * Example: 100 USD EUR
      
2. To view historical exchange rates, enter the amount, source currency code, target currency code, and date (YYYY-MM-DD).
      * Example: 100 USD EUR 2022-01-01
      * Note: Historical data feature doesn't work for all currencies from the list.

3. Type 'list' to see all supported currency codes.
    
4. Type 'exit' to quit the application.
    
5. Type 'dictionary' to find the currency code by its full name and vice versa.
      * Example: If you enter 'United States Dollar', it will return 'USD'.

6. Type'history_list' to see all supported currencies for historical data.

7. Type 'check <CURRENCY_CODE>' to check if a currency code is supported for historical data.
      * Example: check USD
      * Note: YO=ou can not use cuurrency names with this command, only currency codes.

8. Type 'swap' to swap the currency codes of your previous input.
      * Example: If your previous command was 100 USD EUR, after using swap it will become 100 EUR USD.
      * Note: This won't work if your previous command wasn't in the format shown in the example.