import win32com.client as wx


class Xp:
    def __init__(self, filepath):
        self.ea = wx.dynamic.Dispatch('Excel.Application')
        self.ea.Visible = True
        self.workbook = self.ea.Workbooks.Open(filepath)
        self.worksheet = self.workbook.ActiveSheet

    def sheet_names(self, sheet_name=None):
        sheet_name_list = [sheet.Name for sheet in self.workbook.Sheets]
        if sheet_name:
            if sheet_name in sheet_name_list:
                return True
            else:
                return False
        return sheet_name_list

    def activity_sheet(self, sheet_name, activation=False):
        self.worksheet = self.workbook.Sheets(sheet_name)
        if activation:
            self.worksheet.Activate()
        return self.worksheet

    def max_row_column(self, index=None, row=True):
        if index:
            if row:
                return self.worksheet.Cells(self.worksheet.Rows.Count, index).End(wx.constants.xlUp).Row
            else:
                return self.worksheet.Cells(index, self.worksheet.Columns.Count).End(wx.constants.xlToLeft).Column
        else:
            return self.worksheet.UsedRange.Rows.Count, self.worksheet.UsedRange.Columns.Count

    def read_sheet_data(self, *args):
        return self.worksheet.Range(self.worksheet.Cells(args[0], args[1]), self.worksheet.Cells(args[2], args[3]))

    def write_sheet_data(self, *args):
        self.worksheet.Range(self.worksheet.Cells(args[1], args[2]),
                             self.worksheet.Cells(len(args[0]) + args[1] - 1,
                                                  len(args[0][0]) + args[2] - 1)).Value = args[0]
