import pandas as pd
from collections import Counter
import random

# Define column names based on your dataset structure
columns = [
    "datum", "rok", "tyden", "den", 
    "1_tah_1", "2_tah_1", "3_tah_1", "4_tah_1", "5_tah_1", "6_tah_1", "dodatkove_1",
    "1_tah_2", "2_tah_2", "3_tah_2", "4_tah_2", "5_tah_2", "6_tah_2", "dodatkove_2"
]

# Load your Sportka CSV file
df = pd.read_csv("sportka.csv", delimiter=";", names=columns, skiprows=1)

# Extract all winning numbers (excluding dodatkové numbers)
all_numbers = df.iloc[:, 4:10].values.flatten().tolist() + df.iloc[:, 11:17].values.flatten().tolist()

# Count frequency of each number
number_counts = Counter(all_numbers)

# Identify Hot & Cold numbers
hot_numbers = [num for num, count in number_counts.most_common(12)]  # Top 12 frequent numbers
cold_numbers = [num for num, count in number_counts.most_common()[-12:]]  # Bottom 12 least frequent numbers

# Function to generate a Sportka number set
def generate_lottery_numbers():
    selected_numbers = set()
    
    # Pick 2-3 hot numbers
    selected_numbers.update(random.sample(hot_numbers, k=random.choice([2, 3])))
    
    # Pick 1-2 cold numbers
    selected_numbers.update(random.sample(cold_numbers, k=random.choice([1, 2])))
    
    # Fill remaining numbers while ensuring a balanced mix of even/odd & high/low numbers
    while len(selected_numbers) < 6:
        num = random.randint(1, 49)
        if num not in selected_numbers:
            selected_numbers.add(num)
    
    return sorted(selected_numbers)

# Generate 8 Sportka "sloupečky" (sets)
lottery_tickets = [generate_lottery_numbers() for _ in range(8)]

# Display the generated numbers
df_tickets = pd.DataFrame(lottery_tickets, columns=[f"Number {i+1}" for i in range(6)])
print(df_tickets)
