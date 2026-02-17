import pandas as pd

# читаємо список подій користувачів
events = pd.read_csv("data/events.csv")

print("\n=== Events ===")
print(events)

# список кроків funnel
steps = ["visit", "signup", "paid"]

funnel = []

for step in steps:
    # рахуємо унікальних користувачів на кожному кроці
    users = events[events["event"] == step]["user_id"].nunique()
    funnel.append((step, users))

df = pd.DataFrame(funnel, columns=["step", "users"])

print("\n=== Funnel from real data ===")
print(df)

