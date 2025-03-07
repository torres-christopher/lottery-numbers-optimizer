# Dependencies
import pandas as pd
from collections import Counter
import random

# Define column names
columns = [
    "datum", "rok", "tyden", "den", 
    "1_tah_1", "2_tah_1", "3_tah_1", "4_tah_1", "5_tah_1", "6_tah_1", "dodatkove_1",
    "1_tah_2", "2_tah_2", "3_tah_2", "4_tah_2", "5_tah_2", "6_tah_2", "dodatkove_2"
]

# Load dataset
df = pd.read_csv("sportka.csv", delimiter=";", names=columns, skiprows=1)

# Let user define how far back in history to go
HISTORY_DEPTH = 5  # Adjust to limit how many past draws to analyze (0 = full history)
NUM_TICKETS = 4  # Choose how many tickets to generate (1 to 8)

# Ensure NUM_TICKETS is within the valid range
NUM_TICKETS = max(1, min(NUM_TICKETS, 8))

# Filter data to use only the last X draws
df = df.iloc[:HISTORY_DEPTH] if HISTORY_DEPTH > 0 else df  # If 0, use full history

# Extract all winning numbers (excluding dodatkové) and convert to standard integers
all_numbers = list(map(int, df.iloc[:, 4:10].values.flatten().tolist() + df.iloc[:, 11:17].values.flatten().tolist()))

# Count frequency of each number
number_counts = Counter(all_numbers)

# Identify Hot & Cold numbers
hot_numbers = [num for num, count in number_counts.most_common(12)]  # Top 12 frequent numbers
cold_numbers = [num for num, count in number_counts.most_common()[-12:]]  # Bottom 12 least frequent numbers

# Get the most recent draw numbers (to reuse 1-2 past winners) and convert to integers
last_draw = list(map(int, df.iloc[0, 4:10].tolist())) if not df.empty else []

# Extract all dodatkové numbers from the filtered dataset and convert to integers
all_dodatkove = list(map(int, df["dodatkove_1"].tolist() + df["dodatkove_2"].tolist()))

# Find the most frequently occurring dodatkové číslo
dodatkove_counts = Counter(all_dodatkove)
best_dodatkove = dodatkove_counts.most_common(1)[0][0]  # Select most frequent dodatkové

# Function to generate a unique Sportka number set for each ticket
def generate_lottery_numbers():
    selected_numbers = set()

    # Pick numbers from different groups while ensuring the total is 6
    num_last_draw = random.choice([1, 2]) if last_draw else 0
    num_hot = random.choice([2, 3])
    num_cold = random.choice([1, 2])

    # Adjust selection to ensure exactly 6 numbers in total
    while num_last_draw + num_hot + num_cold > 6:
        num_hot -= 1  # Reduce hot numbers if too many
    
    selected_numbers.update(random.sample(last_draw, k=min(num_last_draw, len(last_draw))))
    selected_numbers.update(random.sample(hot_numbers, k=num_hot))
    selected_numbers.update(random.sample(cold_numbers, k=num_cold))

    # Fill remaining slots, if needed
    while len(selected_numbers) < 6:
        num = random.randint(1, 49)
        if (
            num not in selected_numbers and  # Avoid duplicates
            all(abs(num - x) > 1 for x in selected_numbers)  # Avoid consecutive numbers
        ):
            selected_numbers.add(num)

    # Ensure Even/Odd balance
    even_numbers = [n for n in selected_numbers if n % 2 == 0]
    odd_numbers = [n for n in selected_numbers if n % 2 != 0]

    if len(even_numbers) > 3:  # Too many evens, swap one for an odd
        to_remove = random.choice(even_numbers)
        selected_numbers.remove(to_remove)
        selected_numbers.add(random.choice([x for x in range(1, 50, 2) if x not in selected_numbers]))
    elif len(odd_numbers) > 3:  # Too many odds, swap one for an even
        to_remove = random.choice(odd_numbers)
        selected_numbers.remove(to_remove)
        selected_numbers.add(random.choice([x for x in range(2, 50, 2) if x not in selected_numbers]))

    return sorted(map(int, selected_numbers))  # Ensure output is exactly 6 numbers

# Generate multiple unique tickets
tickets = [generate_lottery_numbers() for _ in range(NUM_TICKETS)]

# Display results
print(f"Generated {NUM_TICKETS} unique tickets:")
for i, ticket in enumerate(tickets, 1):
    print(f"Ticket {i}: {ticket} + Dodatkové Číslo: {best_dodatkove}")
    print("-" * 50)
