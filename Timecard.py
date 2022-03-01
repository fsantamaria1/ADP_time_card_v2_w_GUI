from decimal import Decimal

class TimeEntry:

    def __init__(self, payPeriodStart, payPeriodEnd, date, department: str,
                paycode: str, hours: Decimal, exceptions: str,
                clockIns: [], clockOuts: []):
        self.PayPeriodStart = payPeriodStart
        self.PayPeriodEnd = payPeriodEnd
        self.Date = date
        self.Department = department
        self.PayCode = paycode
        self.Hours = hours
        self.Exceptions = exceptions
        self.ClockIns = clockIns
        self.ClockOuts = clockOuts

    def RegularHours(self):
        if self.PayCode == "REGULAR":
            return self.Hours
        else:
            return 0

    def OverTimeHours(self):
        if self.PayCode == "OT":
            return self.Hours
        else:
            return 0

    def SalaryHours(self):
        if self.PayCode == "REGSAL":
            return self.Hours
        else:
            return 0

    def CsvStr(self):
        output = ""

        # Department, Salary, Regular, Overtime, Other
        if(self.PayCode == "REGULAR"):
            output = '"' + self.PayPeriodStart + '","' + \
                     self.PayPeriodEnd + '","' + \
                     self.Date + '","' + \
                     self.Department + '","' + \
                     '","' + self.Hours.__str__() + '","","","' + \
                     self.PayCode + '","' + \
                     self.Exceptions
        elif(self.PayCode == "REGSAL"):
            output = '"' + self.PayPeriodStart + '","' + \
                     self.PayPeriodEnd + '","' + \
                     self.Date + '","' + \
                     self.Department + '","' + \
                     self.Hours.__str__() + '","","","","' + \
                     self.PayCode + '","' + \
                     self.Exceptions
        elif(self.PayCode == "OVERTIME"):
            output = '"' + self.PayPeriodStart + '","' + \
                     self.PayPeriodEnd + '","' + \
                     self.Date + '","' + \
                     self.Department + '","' + \
                     '","","' + self.Hours.__str__() + '","","' + \
                     self.PayCode + '","' + \
                     self.Exceptions
        else:
            output = '"' + self.PayPeriodStart + '","' + \
                     self.PayPeriodEnd + '","' + \
                     self.Date + '","' + \
                     self.Department + '","' + \
                     '","","","' + self.Hours.__str__() + '","' + \
                     self.PayCode + '","' + \
                     self.Exceptions

        if len(self.ClockIns) == 0:
            self.ClockIns.append('')
        if len(self.ClockOuts) == 0:
            self.ClockOuts.append('')

        for t in range(len(self.ClockIns)):
            output = output + '","' + \
                    self.ClockIns[t] + '","' + self.ClockOuts[t]

        output = output + '"\n'
        return output

    def PayType(self):
        switcher = {
            "REGSAL": "SALARY",
            "REGULAR": "REGULAR",
            "UPT": "UNPAID TIME OFF",
            "PTO": "PAID TIME OFF",
            "SAL VACATION": "SALARY VACATION",
            "VACATION": "VACATION",
            "OVERTIME": "OVERTIME",
            "HOLIDAY": "HOLIDAY",
            "FF-PSL-EE": "WHO",
            "FF-FMLA": "WHAT",
            "FF-PSL-FAM": "WHERE"
        }
        return switcher[self.PayCode]

class Timecardv2:

    def __init__(self, associateOId: str, workerId: str,
                 firstName: str, lastName: str,
                 timeentries: []):
        self.AssociateOID = associateOId
        self.WorkerID = workerId
        self.FirstName = firstName
        self.LastName = lastName
        self.Entries = timeentries

    def CsvStr(self):
        output = ''
        for TE in self.Entries:
            output = output + self.AssociateOID + '","' + \
                self.WorkerID + '","' + \
                self.FirstName + '","' + \
                self.LastName + '",' + \
                TE.CsvStr()
        return output

class Timecard:

    def __init__(self, associateOId: str, workerId: str,
                 firstName: str, lastName: str,
                 timeentries: []):
        self.AssociateOID = associateOId
        self.WorkerID = workerId
        self.FirstName = firstName
        self.LastName = lastName
        self.Entries = timeentries

    def CsvStr(self):
        output = ''
        for TE in self.Entries:
            output = output + self.AssociateOID + '","' + \
                     self.WorkerID + '","' + \
                     self.FirstName + '","' + \
                     self.LastName + '",' + \
                     TE.CsvStr()
        return output

    @staticmethod
    def csvTitles():
        return '"Associate_ID","Worker_ID","First_Name","Last_Name","Pay_Period_Start","Pay_Period_End","Date","Department","Salary","Regular","Overtime","Other","Pay_Code","Exceptions","Clock-In_Time","Clock-Out_Time"\n'

