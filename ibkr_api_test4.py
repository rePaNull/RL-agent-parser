from ib_async import *
from utility_functions import lagrange1_parser
import random
import yfinance as yf
import asyncio

# --- CONSTANTS --- 
IP_ADDRESS = '127.0.0.1'
PORT_NUMBER = 7496
CLIENT_ID = 2
EXCHANGE = 'SMART/AMEX'
CURRENCY = 'USD'

TICKERS = ['SPY', 'TLT', 'IEF', 'GLD', 'USO']

TAGS_TO_RETRIEVE = [
    'AvailableFunds', 'UnrealizedPnL', 'CashBalance',
    'FullAvailableFunds', 'NetLiquidation', 'RealizedPnL',
    'TotalCashBalance', 'TotalCashValue'
]

R1_L1_action = [0,0,0,0]

R1_L1_action_P = lagrange1_parser(R1_L1_action)

print (R1_L1_action_P)

print (yf.download('SPY', multi_level_index=False)['Close'].values[-1])

print (type(R1_L1_action_P['Stop Loss']))


async def connection_is_fun():
    # --- CONNECTING TO INTERACTIVE BROKERS ---
    print ("\nConnecting to Interactive Brokers...")
    ib = IB()
    await ib.connectAsync(IP_ADDRESS, PORT_NUMBER, clientId=2)
    return ib

async def generate_degen_stats():
    account_values = ib.accountValues()
    account_dict = {av.tag: av.value for av in account_values if av.currency == CURRENCY and av.tag in TAGS_TO_RETRIEVE}
    return account_dict #['AvailableFunds'], account_dict['NetLiquidation']


async def MARKET_FILLS(R1_L1_action_P, account_dict):
    # Try to be a retard
    action = MarketOrder(action=R1_L1_action_P['Position Type'], totalQuantity=R1_L1_action_P['Position Size '] * account_dict['AvailableFunds'], 
                     adjustedStopLimitPrice= yf.download('SPY', multi_level_index=False)['Close'].values * (1+R1_L1_action_P['Stop Loss']))
    

'''  The action is expected to be an iterable of 4 elements:
      [pos_type, direction_idx, loss_idx, size_idx]
      
    Mapping:
      - pos_type: 0 -> Increase (represented as 1), 1 -> Decrease (represented as -1)
      - direction_idx: 0 -> "BUY", 1 -> "SELL"
      - loss_idx: 0 -> 0.5%, 1 -> 1%, 2 -> 1.5%, 3 -> 2% 
                  (as float values: 0.005, 0.01, 0.015, 0.02)
      - size_idx: 0 -> 10%, 1 -> 20%, ..., 9 -> 100%
                  (as float values: 0.1, 0.2, ..., 1.0)
    
    Returns:
        A dictionary with the following keys:
         - "Position Direction": str, either "BUY" or "SELL"
         - "Stop Loss": float
         - "Position Size": float
         - "Position Type": int, either 1 (Increase) or -1 (Decrease)
'''