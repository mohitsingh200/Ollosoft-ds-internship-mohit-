class Stock:

    def __init__(self, ticker, prices):

        self.ticker = ticker
        self.prices = prices


    def avg_price(self):

        average = sum(self.prices) / len(self.prices)

        return average


    def total_return(self):

        start_price = self.prices[0]

        end_price = self.prices[-1]

        total_return = ((end_price - start_price) / start_price) * 100

        return total_return


    def max_drawdown(self):

        highest_price = max(self.prices)

        lowest_price = min(self.prices)

        drawdown = ((lowest_price - highest_price) / highest_price) * 100

        return drawdown