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
HISTORY_DEPTH = 0  # Adjust to limit how many past draws to analyze (0 = full history)
NUM_TICKETS = 1  # Choose how many tickets to generate (1 to 8)

# Ensure NUM_TICKETS is within the valid range
NUM_TICKETS = max(1, min(NUM_TICKETS, 8))

# Filter data to use only the last X draws
df = df.iloc[:HISTORY_DEPTH] if HISTORY_DEPTH > 0 else df  # If 0, use full history

# Extract all winning numbers (excluding dodatkové)
all_numbers = df.iloc[:, 4:10].values.flatten().tolist() + df.iloc[:, 11:17].values.flatten().tolist()

# Count frequency of each number
number_counts = Counter(all_numbers)

# Identify Hot & Cold numbers
hot_numbers = [num for num, count in number_counts.most_common(12)]  # Top 12 frequent numbers
cold_numbers = [num for num, count in number_counts.most_common()[-12:]]  # Bottom 12 least frequent numbers

# Function to generate a unique Sportka number set for each ticket
def generate_lottery_numbers():
    selected_numbers = set()
    
    # Pick 2-3 hot numbers
    selected_numbers.update(random.sample(hot_numbers, k=random.choice([2, 3])))
    
    # Pick 1-2 cold numbers
    selected_numbers.update(random.sample(cold_numbers, k=random.choice([1, 2])))
    
    # Fill remaining numbers ensuring balance
    while len(selected_numbers) < 6:
        num = random.randint(1, 49)
        if num not in selected_numbers:
            selected_numbers.add(num)
    
    return sorted(selected_numbers)

# Extract all dodatkové numbers from the filtered dataset
all_dodatkove = df["dodatkove_1"].tolist() + df["dodatkove_2"].tolist()

# Find the most frequently occurring dodatkové číslo
dodatkove_counts = Counter(all_dodatkove)
best_dodatkove = dodatkove_counts.most_common(1)[0][0]  # Select most frequent dodatkové

# Generate multiple unique tickets
tickets = [generate_lottery_numbers() for _ in range(NUM_TICKETS)]

# Display results
print(f"Generated {NUM_TICKETS} unique tickets:")
for i, ticket in enumerate(tickets, 1):
    print(f"Ticket {i}: {ticket} + Dodatkové Číslo: {best_dodatkove}\n- - - - - - - - - - - - - - - - - - - - - - - - - - - -")
