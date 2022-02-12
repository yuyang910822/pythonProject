import openpyxl
from openpyxl.worksheet.worksheet import Worksheet


class ExcelClass:

    def __init__(self, fileName, sheetName):
        self.workbook = openpyxl.load_workbook(fileName)
        self.sheetName = sheetName

    def close(self):
        """关闭工作薄对象，释放内存"""
        self.workbook.close()

    def readDada(self):
        """
        读取测试用例
        :return:
        """
        worksheet: Worksheet = self.workbook[self.sheetName].values
        data = []
        for i in list(worksheet)[1:]:
            if None not in i[0:1]:
                data.append(dict(zip(worksheet[0], i)))
        return data


if __name__ == '__main__':
    e = ExcelClass('../data/【kk仓现场测试问题】--汇总.xlsx', '现场问题汇总')
    for i in e.readDada():
        print(i)
