import pandas as pd
from collections import Counter
import random

# Define column names
columns = [
    "datum", "rok", "tyden", "den", 
    "1_tah_1", "2_tah_1", "3_tah_1", "4_tah_1", "5_tah_1", "6_tah_1", "dodatkove_1",
    "1_tah_2", "2_tah_2", "3_tah_2", "4_tah_2", "5_tah_2", "6_tah_2", "dodatkove_2"
]

df = pd.read_csv("sportka.csv", delimiter=";", names=columns, skiprows=1)

HISTORY_DEPTH = 1000
NUM_TICKETS = 4
NUM_TICKETS = max(1, min(NUM_TICKETS, 8))
df = df.iloc[:HISTORY_DEPTH] if HISTORY_DEPTH > 0 else df

# Extract all winning numbers
all_numbers = list(map(int, df.iloc[:, 4:10].values.flatten().tolist() + df.iloc[:, 11:17].values.flatten().tolist()))

# Count frequency
number_counts = Counter(all_numbers)

# Split to low and high halves
low_half = [n for n in all_numbers if n <= 24]
high_half = [n for n in all_numbers if n >= 25]

low_counts = Counter(low_half)
high_counts = Counter(high_half)

# Get hot/cold from each half
hot_low = [num for num, _ in low_counts.most_common(6)]
hot_high = [num for num, _ in high_counts.most_common(6)]
cold_low = [num for num, _ in low_counts.most_common()[-6:]]
cold_high = [num for num, _ in high_counts.most_common()[-6:]]

# Define last_draw properly
last_draw = list(map(int, df.iloc[0, 4:10].tolist())) if not df.empty else []

# Get best dodatkove
all_dodatkove = list(map(int, df["dodatkove_1"].tolist() + df["dodatkove_2"].tolist()))
dodatkove_counts = Counter(all_dodatkove)
best_dodatkove = dodatkove_counts.most_common(1)[0][0] if dodatkove_counts else 0

def generate_lottery_numbers():
    selected_numbers = set()
    pool = []

    # Last draw reuse
    num_last_draw = random.choice([1, 2]) if last_draw else 0
    pool += random.sample(last_draw, k=min(num_last_draw, len(last_draw)))

    # Hot/cold selections
    hot_each = random.choice([1, 2])
    cold_each = 1  # always 1 from each side

    pool += random.sample(hot_low, k=min(hot_each, len(hot_low)))
    pool += random.sample(hot_high, k=min(hot_each, len(hot_high)))
    pool += random.sample(cold_low, k=min(cold_each, len(cold_low)))
    pool += random.sample(cold_high, k=min(cold_each, len(cold_high)))

    # Shuffle and trim to 6 unique values
    random.shuffle(pool)
    for num in pool:
        if len(selected_numbers) < 6 and num not in selected_numbers and all(abs(num - x) > 1 for x in selected_numbers):
            selected_numbers.add(num)

    # Fill if still under 6
    while len(selected_numbers) < 6:
        num = random.randint(1, 49)
        if (
            num not in selected_numbers and
            all(abs(num - x) > 1 for x in selected_numbers)
        ):
            selected_numbers.add(num)

    # Even/odd balance adjustment
    even = [n for n in selected_numbers if n % 2 == 0]
    odd = [n for n in selected_numbers if n % 2 != 0]
    if len(even) > 4:
        to_remove = random.choice(even)
        selected_numbers.remove(to_remove)
        replacement = random.choice([x for x in range(1, 50, 2) if x not in selected_numbers])
        selected_numbers.add(replacement)
    elif len(odd) > 4:
        to_remove = random.choice(odd)
        selected_numbers.remove(to_remove)
        replacement = random.choice([x for x in range(2, 50, 2) if x not in selected_numbers])
        selected_numbers.add(replacement)

    return sorted(selected_numbers)

# Generate tickets
tickets = [generate_lottery_numbers() for _ in range(NUM_TICKETS)]

# Display
print(f"Generated {NUM_TICKETS} unique tickets:")
for i, ticket in enumerate(tickets, 1):
    print(f"Ticket {i}: {ticket} + Dodatkové Číslo: {best_dodatkove}")
    print("-" * 50)
