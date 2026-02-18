# Import libraries
import pandas as pd
import matplotlib.pyplot as plt

from ai_helper import ask_llama

# Read CSV file
df = pd.read_csv("data/amplitude_funnel.csv")

# Clean column names
df.columns = df.columns.str.replace("\t", "").str.strip()

# Clean all text cells
df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

# Remove Total rows
df = df[df["Date"] != "Total"]

# Convert numbers from text to numbers
df["Search"] = pd.to_numeric(df["Search"], errors="coerce")
df["Add"] = pd.to_numeric(df["Add"], errors="coerce")
df["Export"] = pd.to_numeric(df["Export"], errors="coerce")

print("\n=== Clean Data ===")
print(df.head())

# Sum users in each step
total_search = df["Search"].sum()
total_add = df["Add"].sum()
total_export = df["Export"].sum()

print("\n=== Funnel Totals ===")
print("Search:", total_search)
print("Add:", total_add)
print("Export:", total_export)

conv_search_add = total_add / total_search
conv_add_export = total_export / total_add

print("\n=== Conversion ===")
print("Search → Add:", round(conv_search_add, 3))
print("Add → Export:", round(conv_add_export, 3))

if conv_search_add < conv_add_export:
    weakest = "Search → Add"
else:
    weakest = "Add → Export"

print("\n=== Weakest Step ===")
print(weakest)

country_stats = df.groupby("Country")[["Search", "Add", "Export"]].sum()

country_stats["Search→Add"] = country_stats["Add"] / country_stats["Search"]
country_stats["Add→Export"] = country_stats["Export"] / country_stats["Add"]
country_stats = country_stats.fillna(0)

big_countries = country_stats[country_stats["Search"] > 50]
big_countries = big_countries.sort_values("Add→Export")

worst_country_name = big_countries.index[0]   # string
worst_country_data = big_countries.iloc[0]   # row


print("\n=== Country Funnel ===")
big_countries = big_countries.sort_values("Add→Export")
print(big_countries)

# Only countries with enough users

if len(big_countries) == 0:
    print("No countries with enough data")
else:
    big_countries = big_countries.sort_values("Add→Export")

    worst_country = big_countries.index[0]
    worst_data = big_countries.iloc[0]

print("\n=== Worst Country ===")
print("Country:", worst_country_name)
print("Search:", int(worst_country_data["Search"]))
print("Add:", int(worst_country_data["Add"]))
print("Export:", int(worst_country_data["Export"]))
print("Add → Export:", round(worst_country_data["Add→Export"], 3))

steps = ["Search", "Add", "Export"]
users = [total_search, total_add, total_export]

plt.plot(steps, users)
plt.title("Real Funnel From Amplitude")
plt.xlabel("Step")
plt.ylabel("Users")
plt.show()

prompt = f"""
You are a senior Product Manager at a SaaS company.

We have a funnel problem.

Country: {worst_country_name}
Search users: {int(worst_country_data["Search"])}
Add users: {int(worst_country_data["Add"])}
Export users: {int(worst_country_data["Export"])}

Goal: Improve Add → Export conversion.

Return EXACTLY 3 ideas in this format:

1. Hypothesis:
2. Why users drop:
3. A/B test design:
4. Metric to track:
5. Expected impact (%):

Be specific and realistic.
"""

print("\n=== AI Hypotheses ===")
answer = ask_llama(prompt)
print(answer)

with open("ai_hypotheses.txt", "w", encoding="utf-8") as f:
    f.write(answer)


