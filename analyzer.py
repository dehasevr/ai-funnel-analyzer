import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/funnel.csv")

print("\n=== Funnel Data ===")
print(df)

df["conversion"] = df["users"] / df["users"].shift(1)
df.loc[0, "conversion"] = 1

print("\n=== Conversion Rates ===")
print(df)

plt.plot(df["step"], df["users"])
plt.title("Users in Funnel")
plt.xticks(rotation=45)
plt.show()
