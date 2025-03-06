# Sportka Number Generator

This Python script generates **multiple unique Sportka tickets** while optimizing number selection using **historical data analysis**. The script ensures:numbers. The script allows you to:
- **A mix of even/odd and high/low numbers** for better balance.
- **Avoiding consecutive numbers** for a more spread-out selection.
- **Including 1-2 past winners** from the most recent draw.
- **A selectable number of tickets (1-8)**.
- **The most frequently drawn dodatkové číslo**.

## 🎯 Features
- 📊 **Hot & Cold Number Analysis** – Picks numbers based on their historical frequency.
- 🔄 **Even/Odd & High/Low Balance** – Ensures an optimal number mix.
- 🚫 **Avoids Consecutive Numbers** – Ensures better spread.
- ♻ **Includes Past Winners** – Adds 1-2 numbers from the last draw.
- 🔢 **Dodatkové Číslo Prediction** – Finds the most frequently drawn dodatkové číslo.
- 🎟️ **Custom Number of Tickets** – Choose between **1 to 8 tickets**.

## 🛠️ Installation
Ensure you have Python installed (version 3.x recommended) and install the required libraries:
```bash
pip install pandas
```

## Usage
1. Save your Sportka historical data as sportka.csv in the same directory.
2. Adjust the HISTORY_DEPTH variable in the script:
  - HISTORY_DEPTH = 100 → Uses the last 100 draws.
  - HISTORY_DEPTH = 0 → Uses all available history.
  - NUM_TICKETS = 3 → Creates three ticket variations
3. Run the script:

```bash
python predictor.py
```

## CSV File Format
Your sportka.csv file should be formatted as per official [downloadable file](https://www.sazka.cz/loterie/historie-cisel?game=sportka):

```markdown
datum;rok;tyden;den;1. cislo 1. tah;2. cislo 1. tah;3. cislo 1. tah;4. cislo 1. tah;5. cislo 1. tah;6. cislo 1. tah;dodatkove cislo 1. tah;1. cislo 2. tah;2. cislo 2. tah;3. cislo 2. tah;4. cislo 2. tah;5. cislo 2. tah;6. cislo 2. tah;dodatkove cislo 2. tah;
5. 3. 2025;2025;10;3;44;32;11;3;17;33;24;39;49;41;31;33;23;3
2. 3. 2025;2025;09;7;26;24;25;27;44;17;16;34;32;43;41;25;35;5
```

## Example output
```less
Generated 3 tickets using this fixed set:
Ticket 1: [3, 17, 22, 31, 41, 49] + Dodatkové Číslo: 23
Ticket 2: [3, 17, 22, 31, 41, 49] + Dodatkové Číslo: 23
Ticket 3: [3, 17, 22, 31, 41, 49] + Dodatkové Číslo: 23
```

## How It Works
1. Loads past Sportka draw results from sportka.csv.
2. Counts how often each number has appeared.
3. Selects:
  - 2-3 hot numbers (most frequent).
  - 1-2 cold numbers (least frequent).
  - Remaining numbers to ensure a balance.
4. Finds the most frequently drawn dodatkové číslo.
5. Outputs a single "sloupeček" (6 numbers) + dodatkové číslo.

## Notes
- This program does not predict future results with certainty! It is a statistical tool that helps optimize number selection based on past trends.
- The lottery is still random, so results will vary.

## Licence
This project is open-source and can be freely modified and shared.

---
📝 Created for personal use & fun. Good luck with Sportka! 🎰