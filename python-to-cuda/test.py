#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import ctypes


# Requires full path
SHARED_OBJECT = "cubridge.so"

PATH_TO_SHARED_OBJECT = os.getcwd() + "/" + SHARED_OBJECT

# cubridge_lib = ctypes.cdll.LoadLibrary(PATH_TO_SHARED_OBJECT)




# def load_function(name, lib=cubridge_lib):
#     orig_func = getattr(lib, name)

#     def wrapped_func(*args, **kwargs):
#         print(orig_func, args, kwargs)

#         for item in args:
#             if type(item) == list:
#                 dtype = type(item[0])
#             else:
#                 dtype = type(item)
            



#         # Allocate pointers to values
#         p_a = allocate(args[0])
#         p_b = allocate(args[1])
#         p_result = allocate(len(args[0]))

#         # Call the kernel
#         orig_func(p_a, p_b, p_result, len(args[0]))

#         return list(p_result)
#     setattr(lib, name, wrapped_func)
#     return getattr(lib, name)


class CBridge():
    type_converter = {int: ctypes.c_int,
                      float: ctypes.c_double, }

    function = None
    def __init__(self, path):
        self.path = path
        # super().__init__(self.path)
        self.lib = ctypes.cdll.LoadLibrary(self.path)

    def load(self, name):
        original_function = getattr(self.lib, name)

        def hijacker(*args):
            self.function = getattr(self.lib, name)
            parsed = []
            for item in args:
                if type(item) == list:
                    dtype = type(item[0])
                else:
                    dtype = type(item)
                try:
                    parsed.append(self.allocate(item, dtype=self.type_converter[dtype]))
                except:
                    pass
            
            def f(n_bytes):
                original_function(*parsed, args[-1], n_bytes)
            if type(args[-1]) != int:
                n_bytes = len(list(args[-1]))
                # f(n_bytes)
                original_function(*parsed, args[-1], n_bytes)
                return list(args[-1])
            else:
                # n_bytes = args[-1]
                # f(n_bytes)
                # buffer = (ctypes.c_int*n_bytes)()
                pointer = ctypes.POINTER(ctypes.c_int)


                buffer = pointer(ctypes.c_int(1))
                original_function(ctypes.c_int(8), ctypes.c_int(9), buffer)
                # a = ctypes.cast(buffer, ctypes.c_int_p).value
                # buffer = ctypes.c_void_p.from_buffer(buffer).contents
                return buffer.contents
        setattr(self.lib, name, hijacker)
        self.function = getattr(self.lib, name)
        return self.function

    def allocate(self, data, dtype=ctypes.c_int):
        if type(data) == list:
            return (dtype*len(data))(*data)
        else:
            return (dtype*data)()

    def empty(self, n_bytes: int, dtype=ctypes.c_int):
        return (dtype*n_bytes)()


bridge = CBridge(PATH_TO_SHARED_OBJECT)

function = bridge.load("pythonCudaBridgeWrapper")


a = [1,2,3,4,5,6,7,8,9]
b = [9,8,7,6,5,4,3,2,1]

buffer = bridge.empty(9)

result = function(a, b, buffer)

# f2 = bridge.load("python2")

# a = f2(9, 8)
# print(a)

print(result)
print(f"{a} * {b} = {list(buffer)}")
