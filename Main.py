from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

"""
Website: https://imc-prosperity.notion.site/Writing-an-Algorithm-in-Python-19ee8453a0938114a15eca1124bf28a1

Description: This is a sample algorithm for the IMC Trading competition.
Classes implemented:
    Trader
    TradingState
    Trade
    OrderDepth
    ConversionObservation
    Order
    Listing
    Observation
    ProsperityEncoder

"""

'''
This is the class that handles the trader logic
We need to implement our investment approach here

Notes:
    When placing an order, if there is bid qt 2, and 3, must check its price to place an order
'''

class Trader:
    def run(self, state: TradingState):
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        result = {}
        
        # Iterate over every product that has an order depth in the current state
        for product, order_depth in state.order_depths.items():
            orders: List[Order] = []
            
            # Check that we have level 1 data on both sides before calculating current mid price.
            # We assume the best bid is the highest available bid and the best ask is the lowest available ask.
            if order_depth.buy_orders and order_depth.sell_orders:
                best_bid = max(order_depth.buy_orders.keys())
                best_ask = min(order_depth.sell_orders.keys())
                current_mid_price = (best_bid + best_ask) / 2
            else:
                # If one side is missing, we cannot compute a reliable mid price, so skip.
                continue
            
            # Retrieve the average values (paste in from your calculation)
            if product in AVERAGES:
                avg_info = AVERAGES[product]
                avg_price = avg_info["avg_mid_price"]
                spread = avg_info["spread"]
            else:
                # If you don't have historical averages for a product, you might skip it.
                continue
            
            # Determine if the current price is undervalued or overvalued.
            # Here, the definition is:
            # - Undervalued: current price < (avg_price - spread)
            # - Overvalued: current price > (avg_price + spread)
            if current_mid_price < (avg_price - spread):
                # Under-valuation: we want to buy.
                # For this example, we look at the sell side. We assume we can take the entire quantity
                # available at the best ask price.
                best_ask = min(order_depth.sell_orders.keys())
                quantity_to_buy = -order_depth.sell_orders[best_ask]  # sell orders come in negative volumes
                # Create buy order (positive quantity indicates a buy)
                orders.append(Order(product, best_ask, quantity_to_buy))
                
            elif current_mid_price > (avg_price + spread):
                # Over-valuation: we want to sell.
                # Here, we look at the buy side and assume selling the available volume.
                best_bid = max(order_depth.buy_orders.keys())
                quantity_to_sell = order_depth.buy_orders[best_bid]
                # Create sell order (negative quantity indicates a sell)
                orders.append(Order(product, best_bid, -quantity_to_sell))
            
            # Add the orders for the product to the result dictionary
            result[product] = orders
        
        # traderData can be used to serialize any state for the next call.
        traderData = ""
        # Conversions is set to 0 if there is no conversion request.
        conversions = 0
        
        return result, conversions, traderData
    
    
    def run(self, state: TradingState):
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))

		# Orders to be placed on exchange matching engine
        result = {}
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            acceptable_price = 10  # Participant should calculate this value
            print("Acceptable price : " + str(acceptable_price))
            print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))
    
            if len(order_depth.sell_orders) != 0:
                best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                if int(best_ask) < acceptable_price:
                    print("BUY", str(-best_ask_amount) + "x", best_ask)
                    orders.append(Order(product, best_ask, -best_ask_amount))
    
            if len(order_depth.buy_orders) != 0:
                best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                if int(best_bid) > acceptable_price:
                    print("SELL", str(best_bid_amount) + "x", best_bid)
                    orders.append(Order(product, best_bid, -best_bid_amount))
            
            result[product] = orders
    
        # String value holding Trader state data required. 
        # It will be delivered as TradingState.traderData on next execution.
        traderData = "SAMPLE" 
        
        # Sample conversion request. Check more details below. 
        conversions = 1
        return result, conversions, traderData


'''
Tradingstate class holds all the important market information that an algorithm needs to make decisions about which orders to send. 
'''
Time = int
Symbol = str
Product = str
Position = int

class TradingState(object):
    # Constructor for the TradingState class
    def __init__(self,
                 traderData: str,
                 timestamp: Time,
                 listings: Dict[Symbol, Listing],
                 order_depths: Dict[Symbol, OrderDepth],
                 # own_trades: the trades the algorithm itself has done since the last TradingState came in
                 own_trades: Dict[Symbol, List[Trade]],
                 # market_trades: the trades that other market participants have done since the last TradingState came in
                 market_trades: Dict[Symbol, List[Trade]],
                 # the long or short position that the player holds in every tradable product, in dictionary
                 position: Dict[Product, Position],
                 observations: Observation):
        self.traderData = traderData
        self.timestamp = timestamp
        self.listings = listings
        # order_depths: all the buy and sell orders per product that other market participants have sent and that the algorithm is able to trade with.
        self.order_depths = order_depths
        self.own_trades = own_trades
        self.market_trades = market_trades
        self.position = position
        self.observations = observations
    
    # toJSON method to convert the TradingState object to a JSON string
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)
    
'''
Trade class holds the information about a trade that has been executed.

Both the own_trades property and the market_trades property provide the traders with a list of trades per products. Every individual trade in each of these lists is an instance of the Trade class.
'''
Symbol = str
UserId = str

class Trade:
    # Constructor for the Trade class
    def __init__(self, 
                 symbol: Symbol, 
                 price: int, 
                 quantity: int, 
                 buyer: UserId = None, 
                 seller: UserId = None, 
                 timestamp: int = 0) -> None:
        self.symbol = symbol
        self.price: int = price
        self.quantity: int = quantity
        self.buyer = buyer
        self.seller = seller
        self.timestamp = timestamp

    # toString method to convert the Trade object to a string
    def __str__(self) -> str:
        return "(" + self.symbol + ", " + self.buyer + " << " + self.seller + ", " + str(self.price) + ", " + str(self.quantity) + ", " + str(self.timestamp) + ")"

    # an another toString method 
    def __repr__(self) -> str:
        return "(" + self.symbol + ", " + self.buyer + " << " + self.seller + ", " + str(self.price) + ", " + str(self.quantity) + ", " + str(self.timestamp) + ")" + self.symbol + ", " + self.buyer + " << " + self.seller + ", " + str(self.price) + ", " + str(self.quantity) + ")"
    
'''
This object contains the collection of all outstanding buy and sell orders, or “quotes” that were sent by the trading bots, for a certain symbol. 
'''
class OrderDepth:
    def __init__(self):
        self.buy_orders: Dict[int, int] = {}
        self.sell_orders: Dict[int, int] = {}

'''
Observation details help to decide on eventual orders or conversion requests
'''
class ConversionObservation:

    def __init__(self, bidPrice: float, askPrice: float, transportFees: float, exportTariff: float, importTariff: float, sugarPrice: float, sunlightIndex: float):
        self.bidPrice = bidPrice
        self.askPrice = askPrice
        self.transportFees = transportFees
        self.exportTariff = exportTariff
        self.importTariff = importTariff
        self.sugarPrice = sugarPrice
        self.sunlightIndex = sunlightIndex

'''
This is a very important class that actually places an order

'''
Symbol = str

class Order:
    def __init__(self, symbol: Symbol, price: int, quantity: int) -> None:
        self.symbol = symbol
        self.price = price
        self.quantity = quantity

    def __str__(self) -> str:
        return "(" + self.symbol + ", " + str(self.price) + ", " + str(self.quantity) + ")"

    def __repr__(self) -> str:
        return "(" + self.symbol + ", " + str(self.price) + ", " + str(self.quantity) + ")"
    

class Listing:

    def __init__(self, symbol: Symbol, product: Product, denomination: Product):
        self.symbol = symbol
        self.product = product
        self.denomination = denomination


class Observation:

    def __init__(self, plainValueObservations: Dict[Product, ObservationValue], conversionObservations: Dict[Product, ConversionObservation]) -> None:
        self.plainValueObservations = plainValueObservations
        self.conversionObservations = conversionObservations
        
    def __str__(self) -> str:
        return "(plainValueObservations: " + jsonpickle.encode(self.plainValueObservations) + ", conversionObservations: " + jsonpickle.encode(self.conversionObservations) + ")"
    

class ProsperityEncoder(JSONEncoder):

        def default(self, o):
            return o.__dict__