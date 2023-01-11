from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import *
from ibapi.contract import *
from ibapi.ticktype import TickTypeEnum

import threading
from contractSamples import *
from excelManagers import *
from time import sleep
import datetime

port = 7497

globalArray = [];
globalContractDetails = [];
globalIndexVerifier = [];
globalOilPrice = 0;

for i in range (200):
    globalArray.append(contractInformations());
for i in range (200):
    globalContractDetails.append(ContractDetails);

clientId = 1001
indexArray = 0;
currentReqId = 0;
currentMode = 0;
closingPrice = {};
nextBuyOrderId = 30000;
nextRequestId = 20000;

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
 
    def nextValidId(self, orderId: int):
        self.nextOrderId = orderId

    def tickByTickBidAsk(self, reqId: int, time: int, bidPrice: float, askPrice: float,
                         bidSize: Decimal, askSize: Decimal, tickAttribBidAsk: TickAttribBidAsk):
        print("tick by tick ask: ", reqId, time, bidPrice, "askPrice: ", askPrice, bidSize, askSize);
        globalArray[reqId].currentPrice = bidPrice;
        globalArray[reqId].price = round(askPrice, 5) - round(bidPrice, 5);
        globalArray[reqId].price = round(globalArray[reqId].price, 4);

    def tickByTickAllLast(self, reqId: int, tickType: int, time, price, size, tickAttribLast, exchange, specialConditions):
        print(reqId, tickType, time, price);

    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float, attrib: TickAttrib):
        global globalArray
        print(f"tickPrice. reqId: {reqId}, tickType: {TickTypeEnum.to_str(tickType)}, price: {price}, attribs: {attrib}")

    def tickSnapshotEnd(self, reqId: int):
        if reqId == 49:
            self.disconnect()

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        global globalArray;
        global currentMode;
        print("Contract details : ", reqId, contractDetails);
        if (currentMode == 1):
            globalContractDetails[reqId] = contractDetails;
        else:
            globalArray[reqId].reqId = reqId;
            globalArray[reqId].conId = contractDetails.contract.conId;
            globalArray[reqId].ticker = contractDetails.contract.symbol;

    def tickPrice(self, tickerId: int, field: int, price: float, attribs: TickAttrib):
        print ("tickePrice: ", tickerId, price, attribs, field);
        global currentMode;
        global globalIndexVerifier

        for i in range(len(globalIndexVerifier)):
            if (currentMode == 1 and price != -1 and globalIndexVerifier[i].reqIdAttributed == tickerId):
                globalIndexVerifier[i].currentPrice = price;

    def historicalData(self, reqId: int, bar: BarData):
        global globalArray
        global globalOilPrice;

        print("Historical Data", reqId, bar)
        if (currentMode == 1):
            global globalIndexVerifier;
            for i in range(len(globalIndexVerifier)):
                if globalIndexVerifier[i].closingPrice == 0:
                   globalIndexVerifier[i].closingPrice = bar.close;
            for i in range(len(globalIndexVerifier)):
                if globalIndexVerifier[i].closingPrice != bar.close and globalIndexVerifier[i].reqIdAttributed == reqId:
                    globalIndexVerifier[i].currentPrice = bar.close;
        elif (currentMode == 0):
            globalArray[reqId].reqId = reqId;
            globalArray[reqId].price = bar.close
            globalArray[reqId].WAP = bar.wap
            globalArray[reqId].volume = bar.volume
            globalArray[reqId].highPrice = bar.high
            globalArray[reqId].lowPrice = bar.low
            globalArray[reqId].barCount = bar.barCount
            if (globalArray[reqId].currentPrice == 0.0):
                globalArray[reqId].currentPrice = bar.close
        else:
            globalOilPrice = bar.close;
     
    def historicalDataEnd(self, reqId: int, start: str, end: str):
        print("data End", reqId, start, end);

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"openOrder. orderId: {orderId}, contract: {contract}, order: {order}")
 
    def orderStatus(self, orderId: OrderId, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        print(f"orderId: {orderId}, status: {status}, filled: {filled}, remaining: {remaining}, avgFillPrice: {avgFillPrice}, permId: {permId}, parentId: {parentId}, lastFillPrice: {lastFillPrice}, clientId: {clientId}, whyHeld: {whyHeld}, mktCapPrice: {mktCapPrice}")
 
    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        print(f"reqId: {reqId}, contract: {contract}, execution: {execution}")
 
 
    def nextValidId(self, orderId: int):
        global nextBuyOrderId;

        super().nextValidId(orderId)
        nextBuyOrderId = orderId + 1;

    def stop(self):
        self.done = True
        self.disconnect()
         
def run_loop(app_obj: TestApp):
    print("Run_Loop")
    app_obj.run()
 
class startInvesting():
 
    def newCashContratRequest(app, currentContract):
        global currentReqId
        global indexArray

        app.reqMktDepth(currentReqId, currentContract, 1, False, []);
        queryTime = (datetime.datetime.today() - datetime.timedelta(days=180)).strftime("%Y%m%d-%H:%M:%S")
        app.reqMarketDataType(4);
        app.reqMktData(currentReqId, currentContract, "", 0, 0, []);
        app.reqTickByTickData(currentReqId, currentContract, "BidAsk", 1, True);
        app.reqHistoricalData(currentReqId, currentContract, queryTime, "1 D", "4 hours", "MIDPOINT", 1, 1,  False, []);
        app.reqContractDetails(currentReqId, currentContract);

        app.cancelMktData(currentReqId);
        currentReqId += 1;
        return;

    @staticmethod
    def newContractRequest(app, currentContract):
        global currentReqId
        global indexArray

        app.reqMktDepth(currentReqId, currentContract, 1, False, []);
        queryTime = (datetime.datetime.today() - datetime.timedelta(days=180)).strftime("%Y%m%d-%H:%M:%S")
        app.reqMarketDataType(4);
        app.reqMktData(currentReqId, currentContract, "100", True, 0, []);
        app.reqTickByTickData(currentReqId, currentContract, "AllLast", 1, True);
        app.reqHistoricalData(currentReqId, currentContract, queryTime, "1 D", "4 hours", "TRADES", 1, 1,  False, []);
        app.reqContractDetails(currentReqId, currentContract);

        app.cancelMktData(currentReqId);
        currentReqId += 1;
        return;

    # Create the market scanner
    def requestContractInfo():
        global clientId
        global indexArray
        global currentMode

        currentMode = 0;
        app = TestApp()
        app.connect("127.0.0.1", port, clientId)
 
        contract = contractSamples()
        sleep(1)

        #startInvesting.newContractRequest(app, contract.Tesla())

        publicMethodNames = [method for method in dir(contract) if callable(getattr(contract, method)) if not method.startswith('_')]  # 'private' methods start from _
        for method in publicMethodNames:
            try:
                if (getattr(contract, method)().secType == "CASH"):
                    startInvesting.newCashContratRequest(app, getattr(contract, method)());
                else:
                    startInvesting.newContractRequest(app, getattr(contract, method)());
            except TypeError:
                pass

        threading.Timer(4, app.stop).start()
        app.run();
        return

    # Print Scanner Results
    def printContractInfo():
        global globalArray
        global indexArray
        global currentReqId

        open('result.txt', 'w').close()
        with open('result.txt', 'w') as file:
            file.writelines("#Form: {reqId; ConId; Ticker; Price; Bar Count; Volume; High Price; Low Price; Current Price; WAP}\n\n");
            for i in range(currentReqId):
                file.writelines("{" + str(globalArray[i].reqId) + ";");
                file.writelines(str(globalArray[i].conId) + ";");
                file.writelines(str(globalArray[i].ticker) + ";");
                file.writelines(str(globalArray[i].price) + ";");
                file.writelines(str(globalArray[i].barCount) + ";");
                file.writelines(str(globalArray[i].volume) + ";");
                file.writelines(str(globalArray[i].highPrice) + ";");
                file.writelines(str(globalArray[i].lowPrice) + ";");
                file.writelines(str(globalArray[i].currentPrice) + ";");
                file.writelines(str(globalArray[i].WAP) + "}\n");
                print("____________________________");
                print("reqId:", globalArray[i].reqId);
                print("conId:", globalArray[i].conId);
                print("ticker:", globalArray[i].ticker);
                print("price:", globalArray[i].price);
                print("barCount:", globalArray[i].barCount);
                print("volume:", globalArray[i].volume);
                print("highPrice:", globalArray[i].highPrice);
                print("lowPrice:", globalArray[i].lowPrice);
                print("currentPrice:", globalArray[i].currentPrice);
                print("WAP:", globalArray[i].WAP);
        return

    def sellOrder(app, contract):
        global globalContractDetails;
        global nextBuyOrderId;

        app.reqIds(-1);
        sleep(0.2);
        order = Order();
        order.orderId = nextBuyOrderId;
        order.action = "SELL";
        order.orderType = "MKT";
        order.totalQuantity = 1;
        if contract.secType == "CASH":
            order.totalQuantity = 25000;
        if contract.secType == "CRYPTO":
            order.tif = "IOC";
        else:
            order.tif = "GTC";

        app.placeOrder(nextBuyOrderId, contract, order); 

        nextBuyOrderId += 2;

    def placeOrder(app, contract):
        global globalContractDetails;
        global currentReqId

        order = Order();
        order.orderId = currentReqId;
        order.action = "BUY";
        order.tif = "DAY";
        order.orderType = "LMT";
        order.lmtPrice = 150.0;
        order.totalQuantity = 2;

        app.placeOrder(currentReqId,contract, order); 

    def buyOilContract(app, contract):
        global currentReqId
        global nextBuyOrderId;
        global globalOilPrice;

        print("\n_______________________________\n")
        app.reqMarketDataType(4);
        queryTime = (datetime.datetime.today()).strftime("%Y%m%d-%H:%M:%S");
        app.reqHistoricalData(currentReqId, contract, queryTime, "60 S", "1 min", "TRADES", 1, 1,  False, []);
        currentReqId += 1

        sleep(2);
        app.cancelMktData(currentReqId)
        app.reqIds(-1);
        order = Order();
        order.orderId = nextBuyOrderId;
        order.action = "BUY";
        order.orderType = "LMT";
        order.lmtPrice = globalOilPrice - 0.3;
        order.totalQuantity = 5;

        print("symbol: ", contract.symbol, "price: ", order.lmtPrice);
        app.placeOrder(nextBuyOrderId, contract, order); 

        nextBuyOrderId += 2

    def buyCrudeOil(app):
        global currentMode

        currentMode = 2;
        contract = crudeOil();

        publicMethodNames = [method for method in dir(contract) if callable(getattr(contract, method)) if not method.startswith('_')]  # 'private' methods start from _
        for method in publicMethodNames:
            try:
                startInvesting.buyOilContract(app, getattr(contract, method)());
            except TypeError:
                pass

    def getContractDetails(app, currentContract):
        global currentReqId
        global closePrice;
        global globalIndexVerifier;

        globalIndexVerifier.append(indexVerifier())
        globalIndexVerifier[len(globalIndexVerifier) - 1].contract = currentContract;

        queryTime = (datetime.datetime.today()).strftime("%Y%m%d-%H:%M:%S")

        app.reqMarketDataType(4);
        app.reqHistoricalData(currentReqId, currentContract, queryTime, "1 D", "1 day", "TRADES", 1, 1,  False, []);
        sleep(1);
        currentReqId += 1;

        return;

    def spxSellAssets(app):
        contract = spxContract()
        print ("SELL");

        publicMethodNames = [method for method in dir(contract) if callable(getattr(contract, method)) if not method.startswith('_')]  # 'private' methods start from _
        for method in publicMethodNames:
            try:
                startInvesting.sellOrder(app, getattr(contract, method)());
            except TypeError:
                pass


    def buyOrder(app, contract):
        global globalContractDetails;
        global nextBuyOrderId;

        app.reqIds(-1);
        sleep(0.2);
        order = Order();
        order.orderId = nextBuyOrderId;
        order.action = "BUY";
        order.orderType = "MKT";
        order.totalQuantity = 1;
        if contract.secType == "CASH":
            order.totalQuantity = 25000;
        if contract.secType == "CRYPTO":
            order.tif = "IOC";
        else:
            order.tif = "GTC";

        app.placeOrder(nextBuyOrderId, contract, order); 

        nextBuyOrderId += 2;

    def dowBuyAssets(app):
        contract = dowContract();

        publicMethodNames = [method for method in dir(contract) if callable(getattr(contract, method)) if not method.startswith('_')]  # 'private' methods start from _
        for method in publicMethodNames:
            try:
                startInvesting.buyOrder(app, getattr(contract, method)());
            except TypeError:
                pass

    def checkIndexForBuyOrder(app):
        global globalIndexVerifier;
        global nextRequestId
        index = 0;
        startInvesting.dowBuyAssets(app);
        #startInvesting.spxSellAssets(app);

        for listIterator in globalIndexVerifier:
            app.reqMarketDataType(4);
            app.cancelMktData(globalIndexVerifier[index].reqIdAttributed)
            globalIndexVerifier[index].reqIdAttributed = nextRequestId;
            queryTime = (datetime.datetime.today()).strftime("%Y%m%d-%H:%M:%S");
            #app.reqMktData(globalIndexVerifier[index].reqIdAttributed, globalIndexVerifier[index].contract, "162", False, 0, []);
            #app.reqTickByTickData(globalIndexVerifier[index].reqIdAttributed, globalIndexVerifier[index].contract, "BidAsk", 1, True);
            app.reqHistoricalData(globalIndexVerifier[index].reqIdAttributed, globalIndexVerifier[index].contract, queryTime, "60 S", "1 min", "TRADES", 1, 1,  False, []);
            nextRequestId += 1;

            sleep(0.5);
            if globalIndexVerifier[index].closingPrice > globalIndexVerifier[index].currentPrice + 100 and globalIndexVerifier[index].contract.symbol == "DJ600" and globalIndexVerifier[index].currentPrice != -1:
                globalIndexVerifier[index].closingPrice = round(globalIndexVerifier[index].currentPrice, 4);
                pass
                #startInvesting.dowBuyAssets(app);
            if globalIndexVerifier[index].closingPrice < globalIndexVerifier[index].currentPrice + 5 and globalIndexVerifier[index].contract.symbol == "SPX" and globalIndexVerifier[index].currentPrice != -1:
                globalIndexVerifier[index].closingPrice = round(globalIndexVerifier[index].currentPrice, 4);
                #startInvesting.spxSellAssets(app);
            print("closing: ", globalIndexVerifier[index].closingPrice, " Index: ", index);
            print("current: ", globalIndexVerifier[index].currentPrice, " Index: ", index);
            index += 1;

    def printIndxInfo():
        global globalIndexVerifier;

        sleep(10);

        open('Dow.txt', 'w').close()
        open('SPX.txt', 'w').close()
        queryTime = (datetime.datetime.today()).strftime("[%Y%m%d]");
        with open('SPX.txt', 'a') as file:
            file.writelines(queryTime);
            for listIterator in globalIndexVerifier:
                if listIterator.contract.symbol == "SPX":
                    file.writelines(", ");
                    file.writelines(str(listIterator.closingPrice));

        with open('Dow.txt', 'a') as file:
            file.writelines(queryTime);
            for listIterator in globalIndexVerifier:
                if listIterator.contract.symbol == "DJ600":
                    file.writelines(", ");
                    file.writelines(str(listIterator.closingPrice));

        while (True):
            with open('SPX.txt', 'a') as file:
                for listIterator in globalIndexVerifier:
                    if listIterator.contract.symbol == "SPX":
                        file.writelines(", ");
                        file.writelines(str(listIterator.currentPrice));

            with open('Dow.txt', 'a') as file:
                for listIterator in globalIndexVerifier:
                    if listIterator.contract.symbol == "DJ600":
                        file.writelines(", ");
                        file.writelines(str(listIterator.currentPrice));
            sleep(60);

    def orderManager(app):
        global clientId
        global indexArray
        global currentMode

        currentMode = 1;

        contract = indexContract

        startInvesting.getContractDetails(app, contract.SPX());
        startInvesting.getContractDetails(app, contract.DOW());
        info_thread = threading.Thread(target=startInvesting.printIndxInfo);
        info_thread.start();
        sleep(2);
        while (True):
            startInvesting.checkIndexForBuyOrder(app)
            sleep(59);

    def covidComebackOperation(app, contract, action):
        global currentReqId
        global nextBuyOrderId;
        global globalOilPrice;

        print("\n_______________________________\n")
        app.reqMarketDataType(4);
        queryTime = (datetime.datetime.today()).strftime("%Y%m%d-%H:%M:%S");
        print("REQUEST FOR: ", contract.symbol);
        app.reqHistoricalData(currentReqId, contract, queryTime, "60 S", "1 min", "TRADES", 1, 1,  False, []);
        currentReqId += 1

        sleep(1);
        app.cancelMktData(currentReqId)

        app.reqIds(-1);
        sleep(0.2);
        order = Order();
        order.orderId = nextBuyOrderId;
        order.action = action;
        if (action == "BUY"):
            order.orderType = "LMT";
            order.lmtPrice = globalOilPrice - 0.3;
            order.totalQuantity = 5;
        else:
            order.orderType = "MIT";
            order.totalQuantity = 1;
            order.auxPrice = globalOilPrice;
        app.placeOrder(nextBuyOrderId, contract, order); 

        nextBuyOrderId += 2

    def covidComeback(app):
        global currentMode

        currentMode = 2;
        contract = covidComebackBuy();

        sleep(1);
        queryTime = (datetime.datetime.today()).strftime("%Y%m%d-%H:%M:%S");
        app.reqHistoricalData(currentReqId, contract.AMD(), queryTime, "60 S", "1 min", "TRADES", 1, 1,  False, []);

        publicMethodNames = [method for method in dir(contract) if callable(getattr(contract, method)) if not method.startswith('_')]  # 'private' methods start from _
        for method in publicMethodNames:
            try:
                startInvesting.covidComebackOperation(app, getattr(contract, method)(), "BUY");
            except TypeError:
                pass

        contractSell = covidComebackSell();

        publicMethodNamesSell = [method for method in dir(contractSell) if callable(getattr(contractSell, method)) if not method.startswith('_')]  # 'private' methods start from _
        for method in publicMethodNamesSell:
            try:
                startInvesting.covidComebackOperation(app, getattr(contractSell, method)(), "SELL");
            except TypeError:
                pass

def run_app(app):
    app.connect("127.0.0.1", port, clientId)
    app.run();

def main():
    #app = TestApp();

    #app_thread = threading.Thread(target=run_app, args=(app,));
    #prog_thread = threading.Thread(target=startInvesting.orderManager, args=(app,));

    #startInvesting.requestContractInfo();
 
    #startInvesting.printContractInfo();
    #app_thread.start()
    #prog_thread.start();
    
    #startInvesting.orderManager(app);
    #startInvesting.buyCrudeOil(app);
    #startInvesting.covidComeback(app);

    #t2.join();
    
    #startInvesting.orderManager();
    excelManagers.excelMain();
 
 
if __name__ == "__main__":
    main()