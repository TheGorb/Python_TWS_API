
from time import sleep
from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import *
from ibapi.contract import *
from ibapi.ticktype import TickTypeEnum
 
import threading
from time import sleep
from contractSamples import *
from excelManagers import *
import datetime

port = 7497

global globalInformation;
globalInformation = []

for i in range(200):
    globalInformation.append(contractInformations());

global currentReqId;
currentReqId = 1;

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
 
    def nextValidId(self, orderId: int):
        self.nextOrderId = orderId
        #self.reqMktData(orderId, contractSamples.AAPL(), "", 0, 0, []);
        self.reqMarketDataType(4);
        queryTime = (datetime.datetime.today() - datetime.timedelta(days=180)).strftime("%Y%m%d-%H:%M:%S")
        self.reqHistoricalData(orderId, contractSamples.Amazon(), queryTime, "1 D", "4 hours", "TRADES", 1, 1,  False, []);
 
    def tickPrice(self, reqId, tickType, price, attrib):
        global globalInformation
        print(f"tickPrice. reqId: {reqId}, tickType: {TickTypeEnum.to_str(tickType)}, price: {price}, attribs: {attrib}")
        self.classesArray[reqId].price = price;
        globalInformation[reqId] = price;
 
    def tickSize(self, reqId, tickType, size):
        global globalInformation
        print(f"tickSize. reqId: {reqId}, tickType: {TickTypeEnum.to_str(tickType)}, size: {size}")
 
    def historicalData(self, reqId, bar):
        print(f"Historical Data: {bar}")
 
    def historicalDataEnd(self, reqId, start, end):
        print(f"End of HistoricalData")
        print(f"Start: {start}, End: {end}")

    def stop(self):
        self.done = True
        self.disconnect()

def run_loop(app_obj: TestApp):
    print("Run_Loop")
    app_obj.run()  

class twsApiInitiator():
    def newContractRequest(app, currentContract):
        global currentReqId
        queryTime = (datetime.datetime.today() - datetime.timedelta(days=180)).strftime("%Y%m%d-%H:%M:%S")
        app.reqMarketDataType(4);
        #app.reqContractDetails(currentReqId, currentContract);
        #app.reqMktDepth(currentReqId, currentContract, 1, False, []);
        ##app.reqMktData(currentReqId, currentContract, "", 0, 0, []);
        app.reqHistoricalData(currentReqId, currentContract, queryTime, "1 D", "4 hours", "TRADES", 1, 1,  False, []);
        
        app.cancelMktData(currentReqId);
        return;

    def buildApp():
        app = TestApp()
        app.connect("127.0.0.1", 7497, 1000)
        app.run()

        queryTime = (datetime.datetime.today() - datetime.timedelta(days=180)).strftime("%Y%m%d-%H:%M:%S")
        #app.reqMarketDataType(4);
        #app.reqHistoricalData(currentReqId, contractSamples.AAPL(), queryTime, "1 D", "4 hours", "TRADES", 1, 1,  False, []);

        #twsApiInitiator.newContractRequest(app, contractSamples.EurGbpFx());
        #sleep(1)
        #twsApiInitiator.newContractRequest(app, contractSamples.Amazon());
        #sleep(1)
        #twsApiInitiator.newContractRequest(app, contractSamples.GBPEUR());
        #sleep(1)
        #twsApiInitiator.newContractRequest(app, contractSamples.GBPUSD());
        #sleep(1)
        #twsApiInitiator.newContractRequest(app, contractSamples.EuropeanStock());
        #sleep(1)
        #twsApiInitiator.newContractRequest(app, contractSamples.AAPL());
        #sleep(1)
        #twsApiInitiator.newContractRequest(app, contractSamples.GOOGL());
        #sleep(1)
        #twsApiInitiator.newContractRequest(app, contractSamples.SwissBonds());
        #sleep(1)
        #twsApiInitiator.newContractRequest(app, contractSamples.Euthereum());
        #sleep(1)
        #twsApiInitiator.newContractRequest(app, contractSamples.Bitcoin());
        return;
        

    def printResult():
        global globalInformation

        print (globalInformation[0].price);

def main():
    twsApiInitiator.buildApp()
    twsApiInitiator.printResult()

if __name__ == "__main__":
    main()