import xlsxwriter
from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import *
from ibapi.contract import *
from ibapi.ticktype import TickTypeEnum

from LiveCalculation import *
from contractSamples import *
from time import sleep
from ExcelClasses import *

import os
import datetime
import threading
import pandas as pd
import numpy as np

conIdContract = 0;
port = 7497
clientId = 1001
currentReqId = 0;
isLiveData = False;

excelWorkbook = [];
liveDataWorkbook = [];

class wrapperExcelExercise(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
 
    def nextValidId(self, orderId: int):
        self.nextOrderId = orderId

    def historicalData(self, reqId: int, bar: BarData):
        global excelWorkbook;
        global isLiveData;
        global liveDataWorkbook;


        for workbook in excelWorkbook:
            if reqId in workbook.worksheetDictionary:
                if workbook.worksheetDictionary[reqId][priorDayDictKey] == True:
                    workbook.worksheetDictionary[reqId][worksheetDictKey].write_number(workbook.worksheetDictionary[reqId][currentIndexDictKey], 5, bar.close)
                    for row in range(workbook.worksheetDictionary[reqId][currentIndexDictKey], workbook.worksheetDictionary[reqId][currentIndexDictKey] + 50):
                        workbook.worksheetDictionary[reqId][worksheetDictKey].write(row, 4, bar.close);
                        workbook.worksheetDictionary[reqId][worksheetDictKey].write(row, 11, bar.volume);
                else:
                    workbook.worksheetDictionary[reqId][worksheetDictKey].write(workbook.worksheetDictionary[reqId][currentIndexDictKey], 2, str(bar.date).split(" ")[0]);
                    workbook.worksheetDictionary[reqId][worksheetDictKey].write(workbook.worksheetDictionary[reqId][currentIndexDictKey], 1, str(bar.date).split(" ")[1]);
                    workbook.worksheetDictionary[reqId][worksheetDictKey].write_number(workbook.worksheetDictionary[reqId][currentIndexDictKey], 5, bar.close)
                    workbook.worksheetDictionary[reqId][worksheetDictKey].write_number(workbook.worksheetDictionary[reqId][currentIndexDictKey], 12, bar.volume)

                    if datetime.datetime.strptime(workbook.worksheetDictionary[reqId][priorDateDict], "%H:%M:%S") > datetime.datetime.strptime(str(bar.date).split(" ")[1], "%H:%M:%S") and workbook.worksheetDictionary[reqId][currentIndexDictKey] > 2:
                        workbook.worksheetDictionary[reqId][currentDateNumber] += 1;
                        if (workbook.worksheetDictionary[reqId][dateRange] == 0):
                            workbook.worksheetDictionary[reqId][dateRange] = workbook.worksheetDictionary[reqId][currentIndexDictKey] - 1;
                            for row in range(1, workbook.worksheetDictionary[reqId][currentIndexDictKey] + workbook.worksheetDictionary[reqId][dateRange]):
                                if row == 1:
                                    workbook.worksheetDictionary[reqId][worksheetDictKey].write_formula(row, 15, '0');
                                    workbook.worksheetDictionary[reqId][worksheetDictKey].write_formula(row, 17, '0');
                                else:
                                    workbook.worksheetDictionary[reqId][worksheetDictKey].write_formula(row, 15, '=IF(N' + str(row + 1) + '<M' + str(row + 1) + ', IF(P' + str(row) + ' = 10, "0", P' + str(row) + ' + 1), IF(P' + str(row) + ' = -10, "0", P' + str(row) + ' - 1))');
                                    workbook.worksheetDictionary[reqId][worksheetDictKey].write_formula(row, 17, '=IF(P' + str(row + 1) + '>0,IF(P' + str(row + 1) + '>3,IF(P' + str(row + 1) + '=5,"BUY","0"),IF(P' + str(row + 1) + '=3,"BUY","0")),IF(P' + str(row + 1) + '<-3,IF(P' + str(row + 1) + '=-5,"SELL","0"),IF(P' + str(row + 1) + '=-3,"SELL","0")))');
                                workbook.worksheetDictionary[reqId][worksheetDictKey].write_formula(row, 14, '=IF(N' + str(row + 1) + '<M' + str(row + 1) + ', -1, 1)');
                                workbook.worksheetDictionary[reqId][worksheetDictKey].write_formula(row, 16, '=IF(M' + str(row + 1) + '>N' + str(row + 1) + ' * 2, ' + 'IF(M' + str(row + 1) + '>N' + str(row + 1) + ' * 3, "BUY 100", "BUY 50")' + ', "no")');
                                workbook.worksheetDictionary[reqId][worksheetDictKey].write(row, 13, "=L" + str(row + 1) + "/" + str(workbook.worksheetDictionary[reqId][dateRange]));
                        for row in range(workbook.worksheetDictionary[reqId][currentIndexDictKey], workbook.worksheetDictionary[reqId][currentIndexDictKey] + workbook.worksheetDictionary[reqId][dateRange]):
                            workbook.worksheetDictionary[reqId][worksheetDictKey].write(row, 4, "=F" + str(workbook.worksheetDictionary[reqId][currentIndexDictKey]));
                            workbook.worksheetDictionary[reqId][worksheetDictKey].write(row, 11, "=SUM(M" + str(workbook.worksheetDictionary[reqId][currentIndexDictKey] - workbook.worksheetDictionary[reqId][dateRange]) + ":M" + str(workbook.worksheetDictionary[reqId][currentIndexDictKey]) + ")");
                            workbook.worksheetDictionary[reqId][worksheetDictKey].write(row, 13, "=L" + str(row + 1) + "/" + str(workbook.worksheetDictionary[reqId][dateRange]));
                            workbook.worksheetDictionary[reqId][worksheetDictKey].write_formula(row, 14, '=IF(N' + str(row + 1) + '<M' + str(row + 1) + ', -1, 1)');
                            workbook.worksheetDictionary[reqId][worksheetDictKey].write_formula(row, 15, '=IF(N' + str(row + 1) + '<M' + str(row + 1) + ', IF(P' + str(row) + ' = 10, "0", P' + str(row) + ' + 1), IF(P' + str(row) + ' = -10, "0", P' + str(row) + ' - 1))');
                            workbook.worksheetDictionary[reqId][worksheetDictKey].write_formula(row, 16, '=IF(M' + str(row + 1) + '>N' + str(row + 1) + ' * 2, ' + 'IF(M' + str(row + 1) + '>N' + str(row + 1) + ' * 3, "BUY 100", "BUY 50")' + ', "no")');
                            workbook.worksheetDictionary[reqId][worksheetDictKey].write_formula(row, 17, '=IF(P' + str(row + 1) + '>0,IF(P' + str(row + 1) + '>3,IF(P' + str(row + 1) + '=5,"BUY","0"),IF(P' + str(row + 1) + '=3,"BUY","0")),IF(P' + str(row + 1) + '<-3,IF(P' + str(row + 1) + '=-5,"SELL","0"),IF(P' + str(row + 1) + '=-3,"SELL","0")))');

                        workbook.worksheetDictionary[reqId][worksheetDictKey].write(workbook.worksheetDictionary[reqId][currentDateNumber], 21, str(workbook.worksheetDictionary[reqId][currentDateNumber]) + " (" + str(workbook.worksheetDictionary[reqId][currentIndexDictKey] -  workbook.worksheetDictionary[reqId][dateRange] - 1) + "-" + str(workbook.worksheetDictionary[reqId][currentIndexDictKey] - 1) + ")");
                        workbook.worksheetDictionary[reqId][worksheetDictKey].write(workbook.worksheetDictionary[reqId][currentDateNumber], 22, "=MIN(F" + str(workbook.worksheetDictionary[reqId][currentIndexDictKey] - workbook.worksheetDictionary[reqId][dateRange]) + ":F" + str(workbook.worksheetDictionary[reqId][currentIndexDictKey]) + ")");
                        workbook.worksheetDictionary[reqId][worksheetDictKey].write(workbook.worksheetDictionary[reqId][currentDateNumber], 23, "=MAX(F" + str(workbook.worksheetDictionary[reqId][currentIndexDictKey] - workbook.worksheetDictionary[reqId][dateRange]) + ":F" + str(workbook.worksheetDictionary[reqId][currentIndexDictKey]) + ")");
                        workbook.worksheetDictionary[reqId][worksheetDictKey].write(workbook.worksheetDictionary[reqId][currentDateNumber], 24, "=AVERAGE(F" + str(workbook.worksheetDictionary[reqId][currentIndexDictKey] -  workbook.worksheetDictionary[reqId][dateRange]) + ":F" + str(workbook.worksheetDictionary[reqId][currentIndexDictKey]) + ")");
                        workbook.worksheetDictionary[reqId][worksheetDictKey].write(workbook.worksheetDictionary[reqId][currentDateNumber], 25, "=X" + str(workbook.worksheetDictionary[reqId][currentDateNumber] + 1) + "- W" + str(workbook.worksheetDictionary[reqId][currentDateNumber] + 1));
                        workbook.worksheetDictionary[reqId][worksheetDictKey].write(workbook.worksheetDictionary[reqId][currentDateNumber], 26, "=W" + str(workbook.worksheetDictionary[reqId][currentDateNumber] + 1) + "/ X" + str(workbook.worksheetDictionary[reqId][currentDateNumber] + 1));

                    workbook.worksheetDictionary[reqId][priorDateDict] = str(bar.date).split(" ")[1];
                    workbook.worksheetDictionary[reqId][currentIndexDictKey] += 1;
        if isLiveData:
            for workbook in excelWorkbook:
                if reqId in workbook.worksheetDictionary:
                    workbook.worksheetDictionary[reqId][worksheetDictKey].write(0, 0, "TEST");

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        global excelWorkbook;

        print("data End", reqId, start, end);

        for workbook in excelWorkbook:
            if reqId in workbook.worksheetDictionary:
                 workbook.worksheetDictionary[reqId][isFinished] = True;

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        global conIdContract;
        
        conIdContract = contractDetails.contract.conId;
        print(contractDetails.contract.conId);

    def stop(self):
        self.done = True
        self.disconnect()

def run_loop(appObj):
    print("Run excel loop")
    appObj.connect("127.0.0.1", port, clientId)
    appObj.run()

class excelManagers():
    def reqHistoricalDataOfContract(app, currentContract):
        global currentReqId;
        global excelWorkbook;
        
        queryTime = (datetime.datetime.today()).strftime("%Y%m%d-%H:%M:%S")
        app.reqMarketDataType(4);

        for workbook in excelWorkbook:
            if workbook.worksheetSymbole == currentContract.symbol:
                workbook.setPriorTenDay(currentReqId);
                workbook.setPriorThirtyDay(currentReqId + 1);
                workbook.setPriorNinetyDay(currentReqId + 2);
                workbook.setTenDaysReqID(currentReqId + 3);
                workbook.setThirtyDaysReqID(currentReqId + 4);
                workbook.setNinetyReqID(currentReqId + 5);

        dayPrior = (datetime.datetime.today() - datetime.timedelta(days=11)).strftime("%Y%m%d-%H:%M:%S")
        
        app.reqHistoricalData(currentReqId, currentContract, dayPrior, "1 D", "1 day", "TRADES", 1, 1,  False, []);
        currentReqId += 1;

        dayPrior = (datetime.datetime.today() - datetime.timedelta(days=31)).strftime("%Y%m%d-%H:%M:%S")

        app.reqHistoricalData(currentReqId, currentContract, dayPrior, "1 D", "1 day", "TRADES", 1, 1,  False, []);
        currentReqId += 1;

        dayPrior = (datetime.datetime.today() - datetime.timedelta(days=91)).strftime("%Y%m%d-%H:%M:%S")

        app.reqHistoricalData(currentReqId, currentContract, dayPrior, "1 D", "1 day", "TRADES", 1, 1,  False, []);
        currentReqId += 1;

        app.reqHistoricalData(currentReqId, currentContract, queryTime, "10 D", "10 mins", "TRADES", 1, 1,  False, []);
        currentReqId += 1;
        
        app.reqHistoricalData(currentReqId, currentContract, queryTime, "30 D", "10 mins", "TRADES", 1, 1,  False, []);
        currentReqId += 1;

        app.reqHistoricalData(currentReqId, currentContract, queryTime, "90 D", "10 mins", "TRADES", 1, 1,  False, []);
        currentReqId += 1;

    def initWorksheet(worksheet, index, conId):
        worksheet.write('A1', "N-term")
        worksheet.write('B1', "time")
        worksheet.write('C1', "date")
        worksheet.write('D1', "conId")
        worksheet.write('E1', "yestCls")
        worksheet.write('F1', "currentPrice")
        worksheet.write('G1', "$ Δ PX")
        worksheet.write('H1', "% Δ PX (A)")
        worksheet.write('I1', "$ Δ PX (B)")
        worksheet.write('J1', "% Δ PX (B)")
        worksheet.write('K1', "cumulative aggregate avg")
        worksheet.write('L1', "prior volume")
        worksheet.write('M1', "current volume")
        worksheet.write('N1', "yest Avg Volume");
        worksheet.write('P1', "Vol compare");
        worksheet.write('P1', "Trigger curr Vol > Avg yest Vol");
        worksheet.write('Q1', "Trigger curr Vol > Avg yest Vol * 2 or 3");
        worksheet.write('R1', "Trigger vol compare");
        worksheet.write('V1', "Day Of Calculation")
        worksheet.write('W1', "Min of day")
        worksheet.write('X1', "Max of day")
        worksheet.write('Y1', "Avg of day")
        worksheet.write('Z1', "$ Δ PX (C)")
        worksheet.write('AA1', "% Δ PX (C)")
        worksheet.write('AC1', "Buy")
        worksheet.write('AD1', "Sell")
        worksheet.write('AE1', "Total profit")

        for row in range(1, index + 2):
            worksheet.write(row, 0, str(row - 1))
            worksheet.write(row, 3, str(conId))
            worksheet.write(row, 6, "=F" + str(row + 1) + "-" + "F" + str(row))
            worksheet.write(row, 7, "=F" + str(row + 1) + "/" + "E" + str(row))
            worksheet.write(row, 8, "=F" + str(row + 1) + "-" + "F" + str(row))
            worksheet.write(row, 9, "=I" + str(row + 1) + "/" + "F" + str(row))
            worksheet.write(row, 10, "=AVERAGE(J4:J" + str(row + 1) + ")")
            if (row == 1 or row == 2):
                worksheet.write(row, 6, "0")
                worksheet.write(row, 7, "0")
                worksheet.write(row, 8, "0")
                worksheet.write(row, 9, "0")
                worksheet.write(row, 10, "0")

    def createExcel(excelName, folderPath, app):
        global excelWorkbook;
        global currentReqId;
        global conIdContract;

        workbook = xlsxwriter.Workbook(folderPath + "/" + excelName.symbol + '.xlsx')

        if (excelName.conId):
            pass;
        else:
            app.reqContractDetails(currentReqId, excelName);
            currentReqId += 1;
            while conIdContract == 0:
                sleep(0.5);
            excelName.conId = conIdContract;
            conIdContract = 0;

        tenDaysWorksheet = workbook.add_worksheet("10 DAY")
        excelManagers.initWorksheet(tenDaysWorksheet, 400, excelName.conId);

        thirtyDaysWorksheet = workbook.add_worksheet("30 DAY")
        excelManagers.initWorksheet(thirtyDaysWorksheet, 1200, excelName.conId);

        ninetyDaysWorksheet = workbook.add_worksheet("90 DAY")
        excelManagers.initWorksheet(ninetyDaysWorksheet, 3600, excelName.conId);

        excelWorkbook.append(excelClass(tenDaysWorksheet, thirtyDaysWorksheet, ninetyDaysWorksheet, workbook, excelName.symbol, folderPath + "/" + excelName.symbol + '.xlsx'));

    def stillWaitingForData():
        global excelWorkbook;
        currentState = True;

        for workbook in excelWorkbook:
            for dictionary in workbook.worksheetDictionary:
                if workbook.worksheetDictionary[dictionary][isFinished] == False:
                    print("Waiting For Data From ReqId: ", dictionary);
                    currentState = False;
        print("\n");
        return currentState;

    def excelMain():
        global excelWorkbook;
        app = wrapperExcelExercise();
        
        app_thread = threading.Thread(target=run_loop, args=(app,));

        contract = financials()
        currentTime = (datetime.datetime.today()).strftime("%Y%m%d-%H%M%S")
        os.mkdir("excelResult/" + currentTime);

        app_thread.start()
        sleep(1);
        publicMethodNames = [method for method in dir(contract) if callable(getattr(contract, method)) if not method.startswith('_')]
        for method in publicMethodNames:
            excelManagers.createExcel(getattr(contract, method)(), "excelResult/" + currentTime, app);

        for method in publicMethodNames:
            excelManagers.reqHistoricalDataOfContract(app, getattr(contract, method)());

        waitingForRestult = excelManagers.stillWaitingForData();
        while (waitingForRestult == False):
            sleep(1);
            waitingForRestult = excelManagers.stillWaitingForData();


        for workbook in excelWorkbook:
            workbook.close();

        app.stop();
        live_manager.live_main(currentTime);
        print("End");
        exit();
