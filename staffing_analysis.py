# How many cashiers does the shop actually need?
# Runs the same shop simulation 50 times for 2, 3, 4, 5 and 6 cashiers
# and compares the average waiting time.
#
# Quick check: 60 customers arrive per hour and each cashier serves about 15 per hour,
# so 4 cashiers only just keep up and 5 are needed for short waits.

import random
import matplotlib.pyplot as plt

random.seed(42)            # same results every run

SIM_TIME = 180             # 3-hour day
RUNS = 50                  # number of random days per staffing level
ARRIVAL_RATE = 1           # about 1 customer per minute


def average_wait(num_cashiers):
    """Simulate one random day with this many cashiers and return the average wait."""
    # Invent the customers: random arrival times and random service times (2-6 min)
    time, arrivals, services = 0, [], []
    while True:
        time += random.expovariate(ARRIVAL_RATE)
        if time > SIM_TIME:
            break
        arrivals.append(time)
        services.append(random.uniform(2, 6))

    # Same rules as the main simulation: go to the cashier who is free soonest
    cashiers = [0] * num_cashiers          # time when each cashier is next free
    waits = []
    for arrival, service in zip(arrivals, services):
        i = cashiers.index(min(cashiers))  # cashier who is free soonest
        start = max(arrival, cashiers[i])  # wait if that cashier is still busy
        waits.append(start - arrival)
        cashiers[i] = start + service      # cashier busy until the customer leaves
    return sum(waits) / len(waits)


levels = [2, 3, 4, 5, 6]
results = []
print(f"{'Cashiers':>8} | {'rho':>5} | {'Mean avg wait (min)':>20}")
print("-" * 40)
for c in levels:
    waits = [average_wait(c) for _ in range(RUNS)]   # 50 random days with c cashiers
    mean_wait = sum(waits) / RUNS
    rho = ARRIVAL_RATE / (c * 0.25)       # arrivals / serving capacity (above 1 = line keeps growing)
    results.append(mean_wait)
    print(f"{c:>8} | {rho:>5.2f} | {mean_wait:>20.2f}")

# Bar chart of average wait for each number of cashiers
plt.figure(figsize=(7, 4))
bars = plt.bar([str(c) for c in levels], results, color="lightgreen", edgecolor="white")
for bar, val in zip(bars, results):       # write the value on top of each bar
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
             f"{val:.1f}", ha="center", fontsize=10, fontweight="bold")
plt.title("Average Waiting Time vs Number of Cashiers", fontsize=13, fontweight="bold")
plt.xlabel("Number of cashiers")
plt.ylabel("Mean average wait (minutes)")
plt.tight_layout()
plt.savefig("staffing_chart.png", dpi=150)
plt.show()
print("\n[Figure saved: staffing_chart.png]")
