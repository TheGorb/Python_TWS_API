worksheetDictKey = "worksheet";
currentIndexDictKey = "currentIndex"; 
priorDayDictKey = "PriorDay";
isFinished = "IsFinished";
priorDateDict = "priorDateDict";
dateRange = "dateRange";
currentDateNumber = "currentDateNumber";
buyIndex = "buyIndex";
sellIndex = "sellIndex";

import xlwings
import xlsxwriter

class excelClass():
    worksheetSymbole = 0;
    tenDaysWorksheet = 0;
    thirtyDaysWorksheet = 0;
    ninetyDaysWorksheet = 0;
    worksheetDictionary = {};
    workbook = 0;
    filePath = 0;

    def __init__(self, tenDaysWorksheet, thirtyDaysWorksheet, ninetyDaysWorksheet, workbook, worksheetSymbole, filePath):
        self.tenDaysWorksheet = tenDaysWorksheet;
        self.thirtyDaysWorksheet = thirtyDaysWorksheet;
        self.ninetyDaysWorksheet = ninetyDaysWorksheet;
        self.workbook = workbook;
        self.worksheetDictionary = {};
        self.worksheetSymbole = worksheetSymbole;
        self.filePath = filePath;

    def close(self):
        self.workbook.close();

    def reopenWorkbook(self):
        self.workbook = xlsxwriter.Workbook(self.filePath)

    def setTenDaysReqID(self, tenDaysReqId):
        self.worksheetDictionary[tenDaysReqId] = { worksheetDictKey: self.tenDaysWorksheet, currentIndexDictKey: 1, priorDayDictKey: False, isFinished: False, priorDateDict: "00:00:00", dateRange: 0, currentDateNumber: 0 };

    def setThirtyDaysReqID(self, thirtyDaysReqId):
        self.worksheetDictionary[thirtyDaysReqId] = { worksheetDictKey: self.thirtyDaysWorksheet, currentIndexDictKey: 1, priorDayDictKey: False, isFinished: False, priorDateDict: "00:00:00", dateRange: 0, currentDateNumber: 0};

    def setNinetyReqID(self, ninetyDaysReqId):
        self.worksheetDictionary[ninetyDaysReqId] = { worksheetDictKey: self.ninetyDaysWorksheet, currentIndexDictKey: 1, priorDayDictKey: False, isFinished: False, priorDateDict: "00:00:00", dateRange: 0, currentDateNumber: 0};

    def setPriorTenDay(self, priorDayId):
        self.worksheetDictionary[priorDayId] = { worksheetDictKey: self.tenDaysWorksheet, currentIndexDictKey: 1, priorDayDictKey: True, isFinished: False, priorDateDict: "00:00:00", dateRange: 0, currentDateNumber: 0};

    def setPriorThirtyDay(self, priorDayId):
        self.worksheetDictionary[priorDayId] = { worksheetDictKey: self.thirtyDaysWorksheet, currentIndexDictKey: 1, priorDayDictKey: True, isFinished: False, priorDateDict: "00:00:00", dateRange: 0, currentDateNumber: 0};

    def setPriorNinetyDay(self, priorDayId):
        self.worksheetDictionary[priorDayId] = { worksheetDictKey: self.ninetyDaysWorksheet, currentIndexDictKey: 1, priorDayDictKey: True, isFinished: False, priorDateDict: "00:00:00", dateRange: 0, currentDateNumber: 0};

class LiveData():
    liveWorkbook = 0;
    workbook = 0;
    excelApp = 0;
    worksheetSymbole = 0;
    tenDaysWorksheet = 0;
    reqId = 0;

    def __init__(self, workbook, sheet, worksheetSymbole):
        self.excel_app = xlwings.App(visible=False);
        self.workbook = self.excel_app.books.open(workbook);
        self.tenDaysWorksheet = self.workbook.sheets[sheet];
        self.worksheetSymbole = worksheetSymbole;

    def setWorksheetSymbole(self, worksheetSymbole):
        self.worksheetSymbole = worksheetSymbole;

    def printEntireRow(self, row):
        print (self.tenDaysWorksheet['A1'].value)
        print (self.tenDaysWorksheet['A2'].value)
        print (self.tenDaysWorksheet['A3'].value)
        print (self.tenDaysWorksheet['A4'].value)
        print (self.tenDaysWorksheet['A5'].value)


    def saveWorkbook(self):
        self.workbook.save();

    def setReqId(self, reqId):
        self.reqId = reqId;

class pandasDataClass():
    priorVol = 0;
    currentVol = 0;
    yestAvgVol = 0;
    yestGlobalVol = [];
    contractSym = 0;
    reqId = 0;
    currentTime = 0;
    oldTime = 0;
    triggerVolume = 0;
    contract = 0;

    def __init__(self):
        self.priorVol = 0;
        self.currentVol = 0;
        self.yestAvgVol = 0;
        self.contractSym = 0;
        self.oldTime = 0;
        self.reqId = 0;
        self.triggerVolume = 0;

    def setReqId(self, reqId):
        self.reqId = reqId;

    def setyestAvgVol(self, yestAvgVol):
        self.yestAvgVol = yestAvgVol;