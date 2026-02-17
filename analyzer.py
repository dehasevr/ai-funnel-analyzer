import pandas as pd
import matplotlib.pyplot as plt
import ollama

from real_funnel import df

df["conversion_rate"] = df["users"] / df["users"].shift(1)
df.loc[0, "conversion_rate"] = 1

print("\n=== Conversion Rates ===")
print(df)

plt.plot(df["step"], df["users"], marker="o")

plt.title("Funnel Conversion Analysis")
plt.xlabel("Funnel Step")
plt.ylabel("Number of Users")

plt.grid(True)  # adds grid lines for better readability

plt.show()


weakest = df.loc[df["conversion_rate"].idxmin()]

print("\n=== Weakest Step ===")
print(weakest["step"], weakest["conversion_rate"])

def ask_llama(prompt):
    response = ollama.chat(
        model="llama3",
        messages=[
            {
            "role":"user",
            "content": prompt
            }
            
        ]
    )
    return response["message"]["content"]

def ice_score(impact, confidence, ease):
    return (impact + confidence + ease) / 3


prompt = f"""
You are a senior Product Manager
Here is the funnel data:
{df.to_string()}

Weakest step: {weakest["step"]}

Suggest 3 realistic hypotheses to improve conversion.
Each hypothesis must be testable with an A/B test. Estimate all of them using ICE score (1-10 each). For each give Impact, Confidence, Ease. Return as a table
"""

response = ask_llama(prompt)
print("\n=== AI Suggestions ===")
print(response)

import re

print("\n=== Parsed ICE Scores ===")

pattern = r"\|\s*(H\d.*?)\|\s*(.*?)\|\s*(\d+)/10\s*\|"

matches = re.findall(pattern, response)

hypotheses = []

for h in matches:
    name = h[0].strip()
    description = h[1].strip()
    ice = int(h[2])

    hypotheses.append((name, description, ice))

hypotheses.sort(key=lambda x: x[2], reverse=True)

for h in hypotheses:
    print(f"{h[0]} | ICE={h[2]} | {h[1]}")



