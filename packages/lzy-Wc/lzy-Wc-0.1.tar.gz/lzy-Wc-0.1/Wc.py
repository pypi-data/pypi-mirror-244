import win32com.client as wc


class Wc:
    def __init__(self, filepath):
        self.wc = wc.dynamic.Dispatch('Excel.Application')
        self.wc.Visible = True
        self.workbook = self.wc.Workbooks.Open(filepath)

    def sheet_names(self):
        return [sheet.Name for sheet in self.workbook.Sheets]

    def active_sheet(self):
        return self.workbook.ActiveSheet

    def sheet_activate(self, sheet_name):
        return self.workbook.Sheets(sheet_name)

    @staticmethod
    def max_row_column(sheet, index=None, row=True):
        if index:
            if row:
                return sheet.Cells(sheet.Rows.Count, index).End(wc.constants.xlUp).Row
            else:
                return sheet.Cells(index, sheet.Columns.Count).End(wc.constants.xlToLeft).Column
        else:
            return sheet.UsedRange.Rows.Count, sheet.UsedRange.Columns.Count

    @staticmethod
    def read_sheet_data(sheet, *args):
        return sheet.Range(sheet.Cells(args[0], args[1]), sheet.Cells(args[2], args[3]))

    @staticmethod
    def write_sheet_data(sheet, *args):
        sheet.Range(sheet.Cells(args[1], args[2]),
                    sheet.Cells(len(args[0]) + args[1] - 1,
                                len(args[0][0]) + args[2] - 1)).Value = args[0]
