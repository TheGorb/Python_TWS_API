from ibapi.contract import *
from ibapi.client import *
from ibapi.wrapper import *

class contractInformations:
    reqId: 0
    conId: 0
    price: 0.0
    barCount: 0
    volume: 0.0
    highPrice: 0.0
    lowPrice: 0.0
    currentPrice: 0.0
    bid: 0.0
    ask: 0.0
    WAP: 0.0
    VWAP: 0.0

    def __init__(self):
        self.conId = 0
        self.ticker = ""
        self.price = 0.0
        self.barCount = 0
        self.volume = 0.0
        self.highPrice = 0.0
        self.lowPrice = 0.0
        self.currentPrice = 0.0
        self.bid = 0.0
        self.ask = 0.0
        self.WAP = 0.0
        self.VWAP = 0.0
        self.reqId = 0

class indexVerifier:
    closingPrice: 0.0;
    contract: Contract();
    currentPrice: 0.0;
    reqIdAttributed: 10000;

    def __init__(self):
        self.closingPrice = 0.0;
        self.contract = Contract();
        self.currentPrice = 0.0;
        self.reqIdAttributed = 10000;

class contractSamples:

    def EurGbpFx(self):
        contract = Contract();
        contract.symbol = "EUR";
        contract.secType = "CASH";
        contract.currency = "GBP";
        contract.exchange = "IDEALPRO";
        return contract;

    def Euthereum(self):
        contract = Contract();
        contract.symbol = "ETH";
        contract.exchange = "PAXOS";
        contract.conId = 495759171;
        return contract;

    def Bitcoin(self):
        contract = Contract();
        contract.symbol = "BTC";
        contract.exchange = "PAXOS";
        contract.conId = 479624278;
        return contract;

    def Amazon(self):
        contract = Contract();
        contract.symbol = "AMZ";
        contract.secType = "STK";
        contract.currency = "EUR";
        contract.exchange = "SMART";
        return contract;
    
    def USDCHEF(self):
        contract = Contract();
        contract.symbol = "USD";
        contract.secType = "CASH";
        contract.currency = "CHF";
        contract.exchange = "IDEALPRO";
        return contract;

    def GBPUSD(self):
        contract = Contract();
        contract.symbol = "GBP";
        contract.secType = "CASH";
        contract.currency = "USD";
        contract.exchange = "IDEALPRO";
        return contract;

    def Tesla(self):
        contract = Contract();
        contract.symbol = "TSLA";
        contract.secType = "STK";
        contract.currency = "USD";
        contract.exchange = "SMART";
        return contract;

    def EuropeanStock(self):
        contract = Contract();
        contract.symbol = "BMW";
        contract.secType = "STK";
        contract.currency = "EUR";
        contract.exchange = "SMART";
        contract.PrimaryExch = "IBIS";
        return contract;

    def AAPL(self):
        contract = Contract();
        contract.symbol = "AAPL";
        contract.currency = "USD";
        contract.exchange = "SMART";
        contract.secType = "STK";
        return contract;

    def GOOGL(self):
        contract = Contract();
        contract.symbol = "GOOGL";
        contract.currency = "USD";
        contract.exchange = "SMART";
        contract.secType = "STK";
        return contract;

class indexContract:
    def DOW():
        contract = Contract();
        contract.symbol = "DJ600";
        contract.secType = "IND";
        contract.currency = "EUR";
        contract.exchange = "EUREX";
        return contract;

    def SPX():
        contract = Contract();
        contract.symbol = "SPX";
        contract.secType = "IND";
        contract.currency = "USD";
        contract.exchange = "CBOE";
        return contract;

class spxContract:

    def AMZ(self):
        contract = Contract();
        contract.symbol = "AMZ";
        contract.secType = "STK";
        contract.currency = "EUR";
        contract.exchange = "SMART";
        contract.primaryExch = "IBIS";
        return contract;

    def IBM(self):
        contract = Contract();
        contract.symbol = "IBM";
        contract.secType = "STK";
        contract.currency = "USD";
        contract.exchange = "SMART";
        contract.primaryExch = "NYSE";
        return contract;

    def GOOG(self):
        contract = Contract();
        contract.symbol = "GOOG";
        contract.secType = "STK";
        contract.currency = "USD";
        contract.exchange = "SMART";
        contract.primaryExch = "NASDAQ";
        return contract;

    def LTC(self):
        contract = Contract();
        contract.symbol = "LTC";
        contract.secType = "STK";
        contract.currency = "USD";
        contract.exchange = "SMART";
        contract.primaryExch = "NYSE";
        return contract;

    def MATIC(self):
        contract = Contract();
        contract.symbol = "MATIC";
        contract.secType = "CRYPTO";
        contract.currency = "USD";
        contract.exchange = "PAXOS";
        return contract;

    def USDCHEF(self):
        contract = Contract();
        contract.symbol = "USD";
        contract.secType = "CASH";
        contract.currency = "CHF";
        contract.exchange = "IDEALPRO";
        return contract;

    def GBPUSD(self):
        contract = Contract();
        contract.symbol = "GBP";
        contract.secType = "CASH";
        contract.currency = "USD";
        contract.exchange = "IDEALPRO";
        return contract;



class dowContract:

    def MSFT(self):
        contract = Contract();
        contract.symbol = "MSFT";
        contract.secType = "STK";
        contract.currency = "USD";
        contract.exchange = "SMART";
        contract.primaryExch = "NASDAQ";
        return contract;

    def AAPL(self):
        contract = Contract();
        contract.symbol = "AAPL";
        contract.currency = "USD";
        contract.exchange = "SMART";
        contract.secType = "STK";
        contract.primaryExch = "NASDAQ";
        return contract;

    def Tesla(self):
        contract = Contract();
        contract.symbol = "TSLA";
        contract.secType = "STK";
        contract.currency = "USD";
        contract.exchange = "SMART";
        contract.primaryExch = "NASDAQ";
        return contract;

    def Euthereum(self):
        contract = Contract();
        contract.symbol = "ETH";
        contract.exchange = "PAXOS";
        contract.conId = 495759171;
        return contract;

    def Bitcoin(self):
        contract = Contract();
        contract.symbol = "BTC";
        contract.exchange = "PAXOS";
        contract.conId = 479624278;
        return contract;

    def USDCHEF(self):
        contract = Contract();
        contract.symbol = "USD";
        contract.secType = "CASH";
        contract.currency = "CHF";
        contract.exchange = "IDEALPRO";
        return contract;

    def GBPUSD(self):
        contract = Contract();
        contract.symbol = "GBP";
        contract.secType = "CASH";
        contract.currency = "USD";
        contract.exchange = "IDEALPRO";
        return contract;

class crudeOil:

    def COP(self):
        contract = Contract();
        contract.symbol = "COP";
        contract.secType = "STK";
        contract.currency = "USD";
        contract.exchange = "SMART";
        contract.primaryExch = "NYSE";
        return contract;

    def DVN(self):
        contract = Contract();
        contract.symbol = "DVN";
        contract.secType = "STK";
        contract.currency = "USD";
        contract.exchange = "SMART";
        contract.primaryExch = "NYSE";
        return contract;

    def ENB(self):
        contract = Contract();
        contract.symbol = "ENB";
        contract.secType = "STK";
        contract.currency = "USD";
        contract.exchange = "SMART";
        contract.primaryExch = "NYSE";
        return contract;

    def XOM(self):
        contract = Contract();
        contract.symbol = "XOM";
        contract.secType = "STK";
        contract.currency = "USD";
        contract.exchange = "SMART";
        contract.primaryExch = "NYSE";
        return contract;

    def PSX(self):
        contract = Contract();
        contract.symbol = "PSX";
        contract.secType = "STK";
        contract.currency = "USD";
        contract.exchange = "SMART";
        contract.primaryExch = "NYSE";
        return contract;

class covidComebackBuy:

    def AMD(self):
        contract = Contract();
        contract.symbol = "AMD";
        contract.secType = "STK";
        contract.currency = "USD";
        contract.exchange = "SMART";
        contract.primaryExch = "NASDAQ";
        return contract;

    def GOOGL(self):
        contract = Contract();
        contract.symbol = "GOOGL";
        contract.currency = "USD";
        contract.exchange = "SMART";
        contract.secType = "STK";
        contract.primaryExch = "NASDAQ";
        return contract;

    def Amazon(self):
        contract = Contract();
        contract.symbol = "AMZN";
        contract.secType = "STK";
        contract.currency = "USD";
        contract.exchange = "SMART";
        contract.primaryExch = "NASDAQ";
        return contract;

class covidComebackSell:

    def JBLU(self):
        contract = Contract();
        contract.symbol = "DAL";
        contract.secType = "STK";
        contract.currency = "USD";
        contract.exchange = "SMART";
        contract.primaryExch = "NYSE";
        return contract;

    def UAL(self):
        contract = Contract();
        contract.symbol = "UAL";
        contract.secType = "STK";
        contract.currency = "USD";
        contract.exchange = "SMART";
        contract.primaryExch = "NASDAQ";
        return contract;


class financials:
    '''
    def FVX(self):
        contract = Contract();
        contract.symbol = "FVX";
        contract.secType = "IND";
        contract.currency = "USD";
        contract.exchange = "CBOE";
        return contract;

    def TNX(self):
        contract = Contract();
        contract.symbol = "TNX";
        contract.secType = "IND";
        contract.currency = "USD";
        contract.exchange = "CBOE";
        return contract;

    def C(self):
        contract = Contract();
        contract.symbol = "C";
        contract.secType = "STK";
        contract.currency = "USD";
        contract.exchange = "SMART";
        contract.primaryExch = "NYSE";
        contract.conId = 87335484;
        return contract;

    def GS(self):
        contract = Contract();
        contract.symbol = "GS";
        contract.secType = "STK";
        contract.currency = "USD";
        contract.exchange = "SMART";
        contract.primaryExch = "NYSE";
        contract.conId = 4627828;
        return contract;

    def MS(self):
        contract = Contract();
        contract.symbol = "MS";
        contract.secType = "STK";
        contract.currency = "USD";
        contract.exchange = "SMART";
        contract.primaryExch = "NYSE";
        contract.conId = 2841574;
        return contract;

    def JPM(self):
        contract = Contract();
        contract.symbol = "JPM";
        contract.secType = "STK";
        contract.currency = "USD";
        contract.exchange = "SMART";
        contract.primaryExch = "NYSE";
        contract.conId = 1520593;
        return contract;

    def AXP(self):
        contract = Contract();
        contract.symbol = "AXP";
        contract.secType = "STK";
        contract.currency = "USD";
        contract.exchange = "SMART";
        contract.primaryExch = "NYSE";
        contract.conId = 4721;
        return contract;
 
    def DB(self):
        contract = Contract();
        contract.symbol = "DB";
        contract.secType = "STK";
        contract.currency = "USD";
        contract.exchange = "SMART";
        contract.primaryExch = "NYSE";
        contract.conId = 13435352;
        return contract;'''

    def C_PRJStock(self):
        contract = Contract();
        contract.symbol = "C PRJ";
        contract.secType = "STK";
        contract.exchange = "SMART";
        contract.currency = "USD";
        contract.conId = 135424250;
        return contract;
