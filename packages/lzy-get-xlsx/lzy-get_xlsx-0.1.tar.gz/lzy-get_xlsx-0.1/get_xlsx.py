import win32com.client


def get_xlsx():
    return win32com.client.dynamic.Dispatch('Excel.Application').Selection
