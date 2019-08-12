# /usr/bin/env python3
# -*- coding: utf-8 -*-

# =====================================================================
# Copyright (C) 2018-2019 by Owl Dat123a
# author: Danny, Destiny

# =====================================================================

#%%
import pandas as pd

class Acount():
    def __init__(self):
        self._account = input('請輸入帳號: ')
        self._password = input('請輸入密碼: ')
    def showdata(self):
        return {'account':self._account, 'password':self._password}
    
if __name__ == "__main__":
    test = Acount()
    pd.Series(test.showdata())

#%%
