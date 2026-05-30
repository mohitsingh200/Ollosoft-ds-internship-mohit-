try:

    with open("reliance_prices.csv", "r") as file:

        lines = file.readlines()


    total_days = 0

    closing_prices = []

    highest_price = 0

    lowest_price = float('inf')

    highest_date = ""

    lowest_date = ""


    for line in lines[1:]:

        parts = line.strip().split(",")

        date = parts[0]

        close_price = float(parts[4])


        closing_prices.append(close_price)

        total_days += 1


        if close_price > highest_price:

            highest_price = close_price

            highest_date = date


        if close_price < lowest_price:

            lowest_price = close_price

            lowest_date = date


    average_price = sum(closing_prices) / len(closing_prices)


    first_price = closing_prices[-1]

    last_price = closing_prices[0]


    total_return = ((last_price - first_price) / first_price) * 100


    print("========== STOCK ANALYSIS ==========")

    print()

    print("Total Trading Days:", total_days)

    print("Average Closing Price:", round(average_price, 2))

    print()

    print("Highest Closing Price:", highest_price)

    print("Highest Price Date:", highest_date)

    print()

    print("Lowest Closing Price:", lowest_price)

    print("Lowest Price Date:", lowest_date)

    print()

    print("Total Return (%):", round(total_return, 2))


except FileNotFoundError:

    print("Error: CSV file not found.")


except Exception as e:

    print("Unexpected Error:", e)