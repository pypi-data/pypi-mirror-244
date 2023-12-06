import os
import platform
from ctypes import *

OS = platform.system()
if OS == "Windows":
    import win32api

class Recognize:
    def __init__(self):
        dll_name_han = ''

        if OS == "Windows":
            dll_name_han = 'dinkit.dll'
        elif OS == "Linux":
            dll_name_han = 'libdinkit.so'
        else:
            dll_name_han = 'libdinkit.dylib'
        
        self.buf_max_size = 1024
        self.RetBuff =create_string_buffer(''.encode(), self.buf_max_size)

        dll_file_han = os.path.join(os.path.dirname(os.path.abspath(__file__)), dll_name_han)

        self.library_han = cdll.LoadLibrary(dll_file_han)
        self.handle = self.New()
        if OS == "Windows":
            self.dll_close = win32api.FreeLibrary
        elif OS == "Linux":
            try:
                stdlib = CDLL("")
            except OSError:
                stdlib = CDLL("libc.so")
            self.dll_close = stdlib.dlclose
            self.dll_close.argtypes = [c_void_p]
        else:
            self.dll_close = None

    def __del__(self):
        self.Free()
        if self.dll_close is not None:
            self.dll_close(self.library_han._handle)

    def Free(self):
        self.library_han.HRHan_Free.argtypes = [c_void_p]
        self.library_han.HRHan_Free(self.handle)

    def New(self):        
        self.library_han.HRHan_New.restype  = c_void_p
        ret = self.library_han.HRHan_New()
        return ret
    
    def Single(self, strokes, cand_num = 10):
        list_data = []

        for stroke in strokes:
            for point in stroke:
                x, y = point
                list_data.append(x)
                list_data.append(y)
            list_data.append(65535)
            list_data.append(0)
        
        data_len = len(list_data)
        c_data_array = c_uint16 * len(list_data)
        c_data = c_data_array()

        for i in range(len(list_data)):
            c_data[i] = list_data[i]

        self.library_han.HRHan_Recognize.argtypes = [c_void_p, c_void_p, c_int16, c_int16, c_char_p, c_int16]
        self.library_han.HRHan_Recognize.restype  = c_int16
        cand_len = self.library_han.HRHan_Recognize(self.handle, c_data, data_len, cand_num, self.RetBuff, self.buf_max_size)

        cand_str = string_at(self.RetBuff, cand_len)
        cand_str = cand_str.decode()
        items = cand_str.split(' ')

        cands = {}
        for i in range(0, len(items), 2):
            cands[items[i]] = int(items[i+1])

        return cands
