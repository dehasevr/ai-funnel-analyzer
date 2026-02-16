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

weakest = df.loc[df["conversion"].idxmin()]

print("\n=== Weakest Step ===")
print(weakest["step"], weakest["conversion"])

hypotheses = [
    "Improve onboarding UX",
    "Add tooltip explaining value",
    "Send reminder email",
    "Reduce required fields in signup",
    "Add demo video"
]

print("\n=== Hypotheses to Test ===")
for h in hypotheses:
    print("-", h)

