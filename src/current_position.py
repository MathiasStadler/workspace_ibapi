# FROM HERE
# https://stackoverflow.com/questions/70869327/how-to-return-positions-from-ibkr-api-interactive-brokers-consistently
import threading
import pandas as pd
from threading import Thread, Event
import time
from typing import Any
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.common import *
from ibapi.account_summary_tags import AccountSummaryTags


class ib_class(EWrapper, EClient): 
    def __init__(self): 
        EClient.__init__(self, self)
        self.all_positions = pd.DataFrame([], columns = ['Account','Symbol', 'Quantity', 'Average Cost'])
        self.execution_event = threading.Event()

    def position(self, account, contract, pos, avgCost):
        index = str(account)+str(contract.symbol)
        self.all_positions.loc[index]=account,contract.symbol,pos,avgCost
        # set the event
        self.positions_event.set()

    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        if reqId > -1:
            print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " , errorString)
        # set the event
        self.positions_event.set()

    def positionEnd(self):
        super().positionEnd()
        self.disconnect()

ib_api = ib_class() 
ib_api.connect("127.0.0.1", 7496, 0) 


# https://qoppac.blogspot.com/2017/03/getting-position-and-accounting-data.html
ib_api.positions_event.clear() # reset positions_event
position_list = ib_api.reqPositions()
ib_api.positions_event.wait()  # Wait for positions data to come in
current_positions = ib_api.all_positions
ib_api.run()

# return(current_positions)