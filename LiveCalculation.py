from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import *
from ibapi.contract import *
from ibapi.ticktype import TickTypeEnum

import xlwings
import openpyxl
import pandas

from ExcelClasses import *
from contractSamples import *
from githubManagement import *
from time import sleep

import os
import datetime
import threading

nextBuyOrderId = 3433;
port = 7497
clientId = 1002
initPhase = True;
pandasData = {};
spxIndex = indexVerifier();
spxIndex.contract = indexContract.SPX();
currentReqId = 1000;
currentTime = (datetime.datetime.today()).strftime("%Y%m%d-%H%M%S")

class wrapperLive(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        global nextBuyOrderId;
        nextBuyOrderId = orderId;

    def historicalData(self, reqId: int, bar: BarData):
        print(bar);
        for data in pandasData:
            if pandasData[data].reqId == reqId:
                if initPhase and pandasData[data].yestAvgVol == 0:
                    pandasData[data].yestAvgVol = bar.volume / 39;
                elif initPhase:
                    pandasData[data].priorVol = bar.volume;
                    pandasData[data].currentVol = bar.volume;
                else:
                    pandasData[data].currentVol = bar.volume;
                if len(str(bar.date).split(" ")) > 1:
                    pandasData[data].currentTime = datetime.datetime.strptime(str(bar.date).split(" ")[1], "%H:%M:%S")

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        print("data End", reqId, start, end);

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        print(contractDetails.contract.conId);

    def stop(self):
        self.done = True
        self.disconnect()

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"openOrder. orderId: {orderId}, contract: {contract}, order: {order}")
        global currentTime;

        timeOfOrder =  (datetime.datetime.today()).strftime("%Y%m%d-%H%M%S")
        fileToAppend = open("output/twsOrderOutput.txt", "a");
        fileToAppend.write("\n");
        fileToAppend.write("[" + timeOfOrder + "] " + order.action + " "  + str(order.totalQuantity) + " " + contract.symbol + " at " + str(order.lmtPrice) + " ");
 
    def orderStatus(self, orderId: OrderId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        print(f"orderId: {orderId}, status: {status}, filled: {filled}, remaining: {remaining}, avgFillPrice: {avgFillPrice}, permId: {permId}, parentId: {parentId}, lastFillPrice: {lastFillPrice}, clientId: {clientId}, whyHeld: {whyHeld}, mktCapPrice: {mktCapPrice}")
 
    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        print(f"reqId: {reqId}, contract: {contract}, execution: {execution}")

class wrapperIndex(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        global nextOrderId
        nextOrderId = orderId;

    def historicalData(self, reqId: int, bar: BarData):
        print(bar);

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        print("data End", reqId, start, end);

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        print(contractDetails.contract.conId);

    def stop(self):
        self.done = True
        self.disconnect()

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"openOrder. orderId: {orderId}, contract: {contract}, order: {order}")

    def orderStatus(self, orderId: OrderId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        print(f"orderId: {orderId}, status: {status}, filled: {filled}, remaining: {remaining}, avgFillPrice: {avgFillPrice}, permId: {permId}, parentId: {parentId}, lastFillPrice: {lastFillPrice}, clientId: {clientId}, whyHeld: {whyHeld}, mktCapPrice: {mktCapPrice}")
 
    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        print(f"reqId: {reqId}, contract: {contract}, execution: {execution}")

def run_wrapper(appObj):
    print("Run Live loop")
    appObj.connect("127.0.0.1", port, clientId)
    appObj.run()


class spxClass():
    def reqSpxHistoricalData(currentContract, app, duration, barSize, historicalType):
        global currentReqId;

        currentDay = (datetime.datetime.today()).strftime("%Y%m%d-%H:%M:%S")

        app.reqMarketDataType(4);
        app.reqHistoricalData(currentReqId, currentContract, currentDay, duration, barSize, historicalType, 1, 1,  False, []);
        currentReqId += 1;

    def SPX_thread(appObj):
        global spxIndex;
        appObj.connect("127.0.0.1", port, clientId + 1)
        appObj.run()

        while(True):
            spxClass.reqSpxHistoricalData(spxIndex.contract, appObj, "60 S", "1 min", "TRADES");
            sleep(10);

class live_manager():
    def reqLiveHistoricalData(currentContract, app):
        global currentReqId;
        currentDay = (datetime.datetime.today()).strftime("%Y%m%d-%H:%M:%S")

        for data in pandasData:
            if (data == currentContract.symbol):
                pandasData[data].setReqId(currentReqId);

        app.reqMarketDataType(4);
        app.reqHistoricalData(currentReqId, currentContract, currentDay, "600 S", "10 mins", "TRADES", 1, 1,  False, []);
        currentReqId += 1;

    def initData(currentContract, app):
        global currentReqId;
        for data in pandasData:
            if (data == currentContract.symbol):
               pandasData[data].setReqId(currentReqId);

        currentDay = (datetime.datetime.today()).strftime("%Y%m%d-%H:%M:%S")

        app.reqMarketDataType(4);
        app.reqHistoricalData(currentReqId, currentContract, currentDay, "1 D", "1 day", "TRADES", 1, 1,  False, []);
        currentReqId += 1;

        sleep(4);
        for data in pandasData:
            if (data == currentContract.symbol):
                pandasData[data].setReqId(currentReqId);
        app.reqMarketDataType(4);
        app.reqHistoricalData(currentReqId, currentContract, currentDay, "1200 S", "10 mins", "TRADES", 1, 1,  False, []);
        currentReqId += 1

    def buyOrder(app, contract, action, quantity):
        global nextBuyOrderId;

        order = Order();
        order.orderId = nextBuyOrderId;
        order.action = action;
        order.orderType = "MKT";
        order.totalQuantity = quantity;
        order.tif = "GTC";

        app.placeOrder(nextBuyOrderId, contract, order); 
        app.reqIds(nextBuyOrderId);

        nextBuyOrderId += 1;

    def readapteData(contract, app):
        app.reqIds(-1);

        for data in pandasData:
            if (pandasData[data].currentVol * 2 > pandasData[data].yestAvgVol):
                live_manager.buyOrder(app, pandasData[contract.symbol].contract, "BUY", 50);
            if (pandasData[data].currentVol * 3 > pandasData[data].yestAvgVol):
                live_manager.buyOrder(app, pandasData[contract.symbol].contract, "BUY", 100);
            if (pandasData[data].currentVol > pandasData[data].yestAvgVol):
                pandasData[data].triggerVolume += 1;
            if (pandasData[data].currentVol < pandasData[data].yestAvgVol):
                pandasData[data].triggerVolume -= 1;
            if (pandasData[data].triggerVolume == 3 or pandasData[data].triggerVolume == 5):
                live_manager.buyOrder(app, pandasData[contract.symbol].contract, "BUY", pandasData[data].triggerVolume * 10);
            if (pandasData[data].triggerVolume == -3 or pandasData[data].triggerVolume == -5):
                live_manager.buyOrder(app, pandasData[contract.symbol].contract, "SELL", pandasData[data].triggerVolume * 10);

            tempVal = pandasData[data].currentVol;
            pandasData[data].priorVol = pandasData[data].currentVol;
            pandasData[data].yestGlobalVol.append(pandasData[data].currentVol);

            pandasData[data].oldTime = pandasData[data].currentTime;
            print("yestavgVol: ", pandasData[data].yestAvgVol);
            print("currentVol: ", pandasData[data].currentVol);
            print("priorVol: ", pandasData[data].priorVol);

    def createPandasData(contract):
        pandasData[contract.symbol] = pandasDataClass();
        pandasData[contract.symbol].contractSym = contract.symbol
        pandasData[contract.symbol].contract = contract;

    def live_main(currentTime):
        app = wrapperLive();
        #indexApp = wrapperIndex();
        app.nextValidId(nextBuyOrderId);
        app_thread = threading.Thread(target=run_wrapper, args=(app,));
        #spx_thread = threading.Thread(target=SPX_thread, args=(indexApp,));
        contract = financials()
        app_thread.start()
        #spx_thread.start()

        githubThread = threading.Thread(target=githubManagementClass.pushTextFile, args=());
        githubThread.start();

        sleep(2);
        publicMethodNames = [method for method in dir(contract) if callable(getattr(contract, method)) if not method.startswith('_')]
        for method in publicMethodNames:
            live_manager.createPandasData(getattr(contract, method)());

        for method in publicMethodNames:
            live_manager.initData(getattr(contract, method)(), app);

        sleep(2);
        initPhase = False;
        while (True):
            for method in publicMethodNames:
                live_manager.reqLiveHistoricalData(getattr(contract, method)(), app);
            sleep(2);
            for method in publicMethodNames:
                live_manager.readapteData(getattr(contract, method)(), app);
            sleep(600);





