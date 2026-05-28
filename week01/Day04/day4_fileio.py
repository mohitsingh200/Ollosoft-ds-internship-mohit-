try:

    with open("week01/Day04/reliance_prices.csv", "r") as file:

        lines = file.readlines()

        closing_prices = []

        for line in lines[1:]:

            parts = line.strip().split(",")

            close_price = float(parts[7].replace('"', ''))

            closing_prices.append(close_price)

        average_price = sum(closing_prices) / len(closing_prices)

        print("Average Closing Price:")
        print(round(average_price, 2))

        print("\nDaily Percentage Changes:")

        for i in range(1, len(closing_prices)):

            old = closing_prices[i - 1]
            new = closing_prices[i]

            change = ((new - old) / old) * 100

            print(round(change, 2), "%")

except FileNotFoundError:

    print("Error: CSV file not found")

except Exception as e:

    print("Unexpected Error:", e)