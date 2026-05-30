import csv

try:
    with open("week01/Day06/reliance_prices02.csv", "r") as file:

        reader = csv.DictReader(file)

        closing_prices = []
        dates = []

        for row in reader:

            close_price = float(row["CLOSE"].replace(",", ""))

            closing_prices.append(close_price)
            dates.append(row["DATE"])

        total_days = len(closing_prices)

        average_price = sum(closing_prices) / total_days

        highest_price = max(closing_prices)
        lowest_price = min(closing_prices)

        highest_index = closing_prices.index(highest_price)
        lowest_index = closing_prices.index(lowest_price)

        highest_date = dates[highest_index]
        lowest_date = dates[lowest_index]

        first_price = closing_prices[-1]
        last_price = closing_prices[0]

        total_return = ((last_price - first_price) / first_price) * 100

        print("\n===== RELIANCE STOCK REPORT =====\n")

        print("Total Trading Days :", total_days)

        print("Average Closing Price :", round(average_price, 2))

        print("\nHighest Closing Price :", highest_price)
        print("Highest Price Date :", highest_date)

        print("\nLowest Closing Price :", lowest_price)
        print("Lowest Price Date :", lowest_date)

        print("\nTotal Return (%) :", round(total_return, 2))

except FileNotFoundError:
    print("Error: CSV file not found!")

except Exception as e:
    print("Unexpected Error:", e)
