
# Assignment No: 3(a)
# Name: Shreeya Tapaswi
# Roll No: 31474
# Batch: N4
# Subject: AIL Mock-2
# Problem Statement
# Intelligent Traffic Control System
# Using Mamdani Fuzzy Logic

import numpy as np

# 1. Membership Function
def triangular(x, a, b, c):
    if x <= a or x >= c:
        return 0.0
    elif x == b:
        return 1.0
    elif x < b:
        return (x - a) / (b - a)
    else:
        return (c - x) / (c - b)


# 2. Fuzzification
def fuzzify(vehicles):

    low = triangular(vehicles, 0, 0, 25)
    medium = triangular(vehicles, 10, 30, 50)
    high = triangular(vehicles, 35, 60, 80)

    return {
        "Low": low,
        "Medium": medium,
        "High": high
    }


# 3. Fuzzy Rules and Defuzzification
def calculate_green_time(vehicles):

    traffic = fuzzify(vehicles)

    # Output signal time range
    signal_times = np.arange(10, 61, 1)

    # Output membership functions
    short = np.array([
        triangular(t, 0, 10, 30)
        for t in signal_times
    ])

    moderate = np.array([
        triangular(t, 15, 35, 55)
        for t in signal_times
    ])

    long = np.array([
        triangular(t, 40, 60, 80)
        for t in signal_times
    ])

    # 4. Apply Mamdani Fuzzy Rules
    rule_short = np.minimum(traffic["Low"], short)
    rule_moderate = np.minimum(traffic["Medium"], moderate)
    rule_long = np.minimum(traffic["High"], long)

    # 5. Aggregation
    aggregated = np.maximum.reduce([
        rule_short,
        rule_moderate,
        rule_long
    ])

    # 6. Centroid Defuzzification
    if np.sum(aggregated) == 0:
        return 10, traffic

    green_time = np.sum(
        signal_times * aggregated
    ) / np.sum(aggregated)

    return green_time, traffic


# 7. Main Program
print("=" * 55)
print("       INTELLIGENT TRAFFIC CONTROL SYSTEM")
print("              USING FUZZY LOGIC")
print("=" * 55)

directions = ["North", "South", "East", "West"]
cycle = 1

while True:

    print("\n========== TRAFFIC CYCLE", cycle, "==========")

    results = {}
    vehicle_counts = {}

    # Accept traffic input
    for direction in directions:

        while True:
            try:
                vehicles = int(
                    input("Enter vehicles in " + direction + ": ")
                )

                if vehicles < 0 or vehicles > 80:
                    print("Enter a value between 0 and 80.")
                else:
                    break

            except ValueError:
                print("Please enter a valid number.")

        vehicle_counts[direction] = vehicles

        # Calculate fuzzy signal time
        green_time, membership = calculate_green_time(vehicles)

        results[direction] = green_time

        print("\n---", direction, "Direction ---")
        print("Vehicles:", vehicles)

        print("Traffic Membership:")
        for level, value in membership.items():
            print(level, ":", round(value, 2))

        print("Recommended Green Signal Time:",
              round(green_time, 2), "seconds")

    # 8. Final Traffic Report
    print("\n========== FINAL TRAFFIC REPORT ==========")

    print("{:<15} {:<15} {:<15}".format(
        "Direction", "Vehicles", "Green Time"
    ))

    for direction in directions:

        print("{:<15} {:<15} {:<15}".format(
            direction,
            vehicle_counts[direction],
            str(round(results[direction], 2)) + " sec"
        ))

    # Identify highest traffic direction
    priority = max(vehicle_counts, key=vehicle_counts.get)

    print("\nHighest Traffic Direction:", priority)

    print("Recommended Green Time:",
          round(results[priority], 2), "seconds")

    print("\nTraffic analysis completed!")

    choice = input(
        "\nDo you want to analyze another cycle? (yes/no): "
    ).strip().lower()

    if choice not in ["yes", "y"]:
        print("\nTraffic Control System Stopped.")
        break

    cycle += 1
