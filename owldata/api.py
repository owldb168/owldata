#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# =====================================================================
# Copyright (C) 2018-2019 by Owl Data
# author: Danny, Destiny

# =====================================================================

import requests
import json 
import pandas as pd
import datetime
import os

from ._owlerror import OwlError
from . import _owltime

# --------------------
# BLOCK 起始設置
# --------------------
# setting dir 位置
class _Check_dir():
    def __init__(self):
        '''
        Auto create directory
        '''
        self.directory = ['Data']

    def dir(self):
        for dirs in self.directory:
            if not os.path.exists(dirs):
                os.makedirs(dirs)

# --------------------
# BLOCK 商品資訊
# --------------------
# 取得函數與商品對應表
class _DataID():
    def __init__(self):
        # 商品表
        self._fp = ''
        
        # 商品時間對照表
        self._table = ''
        
    # 取得函數與商品對應表
    def _pdid_map(self):
        '''
        擷取商品函數與商品ID表
        Returns
        ----------
        :DataFrame:
            FuncID          PdID
            ssp 	PYPRI-14776a
            msp 	PYPRI-14777b
            sby		PYBAL-14782a
            sbq		PYBAL-14780a
        
        [Notes]
        ----------
        FuncID: ssp-個股股價, msp-多股股價, sby-年度資產負債表(個股), sbq-季度資產負債表(個股)
        PdID: 商品對應的ID
        '''
        get_data_url = self._token['data_url'] + self._token['ctrlmap']
        
        self._fp = self._data_from_owl(get_data_url).set_index("FuncID")
        return self._fp
    
    # 取得函數對應商品
    def _get_pdid(self, funcname):
        return self._fp.loc[funcname][0]
    
    # 商品時間
    def _date_table(self):
        get_data_url = self._token['data_url'] + 'A2-10628a/' + "TWA00/" + "1000"
        self._table = self._data_from_owl(get_data_url)
        return self._table
    
    def _season_to_day(self, day):
        if day == '01':
            return '0331'
        elif day == '02':
            return '0630'
        elif day == '03':
            return '0930'
        elif day == '04':
            return '1231'
        else:
            return ''
        
    def _day_to_season(self, season):
        if season == 1:
            return '0331'
        elif season == 2:
            return '0630'
        elif season == 3:
            return '0930'
        elif season == 4:
            return '1231'
        else:
            return ''
        
    def _date_freq(self, start, end, freq = 'd'):
        self._date_table()
        
        if freq.lower() == 'd':

            date = pd.date_range(start, end, freq = freq.upper())
            user_time = date & self._table['日期']
            return str(len(user_time))
        
        elif freq.lower() == 'm':
            if len(start) or len(end) == 4:
                start = start + '05'
                end = end + '05'
                date = pd.date_range(start, end, freq = freq.upper()  + 'S').strftime('%Y%m')
                user_time = date & self._table['日期'].apply(lambda x: x[:4] + x[4:6]).unique()
                return str(len(user_time))
            else:
                print('輸入格式錯誤, 請輸入 yyymm')
                return None
        
        elif freq.lower() == 'q':
            if (start[4:6] not in ['01', '02', '03', '04']):
                print('格式輸入錯誤, 請輸入 yyyqq, ex:201903 = 2019Q3')
                return None
            start = start[:4] + self._season_to_day(start[4:6])
            end = end[:4] + self._season_to_day(end[4:6])
            date = pd.date_range(start, end, freq= freq.upper())
            
            usertable = (self._table['日期']).apply(lambda x: x[:4]) + self._day_to_season(pd.to_datetime(self._table['日期']).dt.quarter).astype('str')
            user_time = date & usertable.unique()
            return str(len(user_time))

        elif freq.lower() == 'y':
            date = pd.date_range(start, end, freq = "M").strftime('%Y').unique()
            user_time = date & self._table['日期'].apply(lambda x: x[:4]).unique()
            return str(len(user_time))
            


# --------------------
# BLOCK API擷取資料
# --------------------
# 核心程式
class OwlData(_DataID):  
    def __init__(self, auid, ausrt):
        '''
        Please insert your personal information
        Parameters
        ----------
        :param auid: str 
            - Owl account's appId
        :param ausrt: str
            - Owl application's secret key
        
        Returns
        ----------
        str - '歡迎使用貓頭鷹數據庫'
        
        [Notes]
        ----------
        
        '''
        self._token = {
            'token_url':"https://owl.cmoney.com.tw/OwlApi/auth",
            'token_params':"appId=" + auid + "&appSecret=" + ausrt,
            'token_headers':{'content-type': "application/x-www-form-urlencoded"},  #POST表單，預設的編碼方式 (enctype)
            'data_url':"https://owl.cmoney.com.tw/OwlApi/api/v2/json/",
            'ctrlmap':"PYCtrl-14778b"
        }
        
        # 取得 TOKEN 結果
        self._token_result = ''
        
        # data token
        self._data_headers = {}
        
        # 連線進入並輸出連線狀態
        self.status_code = self._request_token_authorization()
        
        # 建立時間表
        
        
    def __repr__(self):
        return '歡迎使用數據貓頭鷹資料庫'
    
    # FIXME #TODO 建立 HTTP error 表
    def _request_token_authorization(self):
        self._token_result = requests.request("POST",self._token['token_url'],
                                        data = self._token['token_params'],
                                        headers = self._token['token_headers'])

        if (self._token_result.status_code == 200):    
            token = json.loads(self._token_result.text).get("token")
            self._data_headers = {'authorization':'Bearer ' + token}
            self._pdid_map()
            return self._token_result.status_code

        elif(self._token_result.status_code == 401):
            print("appid 或 appsecret 輸入錯誤，請重新確認。")

        else:
            print("連線錯誤，請洽業務人員")

    # 呼叫OWL取回資料
    def _data_from_owl(self, url:str) -> "dataframe":
        '''
        輸入API網址，獲取對應的數據資料
        
        Parameters
        ------------
        :param url: str

            - 在url的地方輸入API網址，回傳數據資料 - 個股/多股
        
        Returns
        --------
        :DataFrame: 輸出分別為個股與多股

        Examples
        ---------
        個股/多股: 輸出帶有DataFrame的資料格式
        
            個股: 
                日期     股票名稱   開盤價   最高價  最低價  ...
            0  20171229     台泥     36.20   36.80   36.10  ...
            1  20171228     台泥     36.10   36.25   36.00  ...
            2  20171227     台泥     36.10   36.45   36.00  ...
            3  20171226     台泥     36.10   36.50   35.95  ...
            4  20171225     台泥     35.30   36.25   35.10  ...
            
            多股: 
                股票代號    股票名稱     日期     開盤價  ...
            0    1101        台泥    20171229   36.20  ...
            1    1102        亞泥    20171229   27.80  ...
            2    1103        嘉泥    20171229   12.85  ...
            3    1104        環泥    20171229   22.85  ...
        
           
        [Notes]
        -------
        先請求網址回覆200後，才會抓取資料(網址輸入錯誤，才會撈不到資料)
        個股: 假設基準日: 20190701、股票代號: 1101、期數: 20，則會撈取自20190701往前20筆 1101的資料
        多股: 取指定日期當天，各檔的數據資料
        '''
        
        
        data_result = requests.request('GET', url, headers = self._data_headers)
        if (data_result.status_code == 200):
            data=json.loads(data_result.text)
            return pd.DataFrame(data.get('Data'), columns = data.get('Title'))
        else:
            #print(OwlError._http_error[data_result.status_code])
            return 'err'

    # 個股日收盤行情 (single stock price)
    def ssp(self, sid, bpd, epd, colist = ""):
        '''
        Parameters
        ----------
        :param sid: str
            - 台股股票代號
            
        :param bpd: str
            - 起始日，格式:yyyymmdd 8碼
            
        :param epd: str
            - 結束日，格式:yyyymmdd 8碼
            
        :param colist: list
            - 填入欲查看的欄位名稱，未寫colist參數或list為空時，則取全部的欄位
            
        Returns
        ----------
        DataFrame: 
        
            日期       開盤價    收盤價     ....
            20190807   43.40     43.35
            20190806   43.00     43.30
            20190805   43.50     43.55
            20190802   43.85     43.55
        
        [Notes]
        ----------
        '''
        if self.status_code == 200:
            try:
                if len(bpd) == 8 and len(epd) == 8:
                    PdID = self._get_pdid("ssp")
                    dt = self._date_freq(bpd, epd, 'd')
                    if (dt != "err"):
                        # 獲取資料
                        get_data_url = self._token['data_url']+"date/" + epd + "/" + PdID + "/" + sid + "/" + dt
                        result = self._data_from_owl(get_data_url)
                        
                        if result.empty:
                            print(OwlError._dicts["SidError"])
                        else:
                            # 利用欄位擷取資料
                            if (len(colist)>0):
                                result = result[colist]
                                result.iloc[2:] = result.iloc[2:].apply(pd.to_numeric)
                                
                            return result
                else:
                    print(OwlError._dicts["DayError"])
            except KeyError:
                print(OwlError._dicts["ColumnsError"])
            except Exception:
                print(OwlError._dicts["PdError"]+"("+PdID+")/"+OwlError._dicts["ValueError"])

    # 多股每日收盤行情 (multi stock price)
    def msp(self, dt, colist = ""):
        '''
        
        Parameters
        ----------
        :param dt: str
            - 輸入某一天日期代碼，格式:yyyymmdd 8碼
            
        :param colist: list
            - 填入欲查看的欄位名稱，未寫colist參數或list為空時，取全部的欄位
        
        Returns
        ----------
        DataFrame: 
        
        
        [Notes]
        ----------
        
        '''
        if self.status_code==200:
            try:
                if len(dt)==8:
                    PdID = self._get_pdid("msp")
                    get_data_url = self._token['data_url']+'date/'+dt+'/'+PdID
                    result = self._data_from_owl(get_data_url)
                    
                    if result != "err":
                        if(len(colist) > 0):  #只撈取指定欄位，未指定則全取
                            result = result[colist]
                        return result
                    
                    else:
                        print(OwlError._dicts["PdError"]+"("+PdID+")/"+OwlError._dicts["ValueError"])
                        return ''
                    
                else: #有日期但不是8碼，則顯示錯誤訊息
                    print(OwlError._dicts["DayError"])
                    
            except ValueError:
                try:
                    if(len(colist)>0):  #只撈取指定欄位，未指定則全取
                        result=result[colist]
                    return result
                
                except:
                    print(OwlError._dicts["ColumnsError"])

    # TODO #FIXME 不知道這英文是什麼!
    # 個股財務簡表 (Single Financial Statements)
    def fis(self, di, sid, bpd, epd, colist = ""):
        '''
        
        Parameters
        ----------
        :param di: str
            - 查詢資料時間頻率，y = 年度, q = 季度, m = 月
            
        :param sid: str
            - 台股股票代號
            
        :param bpd: str
            - 起始日，格式:yyyymmdd 8碼
            
        :param epd: str
            - 結束日，格式:yyyymmdd 8碼
            
        :param colist: list
            - 填入欲查看的欄位名稱，未寫colist參數或list為空時，則取全部的欄位
            - ['年度', '流動資產', '非流動資產', '資產總計', '流動負債', '非流動負債', '負債總計', '權益總計', '公告每股淨值', '營業收入(千)', '營業成本(千)', '營業毛利(千)', '營業費用(千)', '營業利益(千)', '營業外收入及支出(千)', '稅前純益(千)', '所得稅(千)', '稅後純益歸屬(千)', '每股盈餘(元)', '營業活動現金流量(千)', '投資活動現金流量(千)', '籌資活動現金流量(千)', '本期現金及約當現金增減數(千)', '期末現金及約當現金餘額(千)', '自由現金流量(千)']
        
        Returns
        ----------
        
        [Notes]
        ----------
        
        '''
        if self.status_code==200:
            try:
                if (di == "Y" or di == "y"):  #判斷要查詢的資料是年度或季度
                    if len(bpd)==4 and len(epd)==4:
                        PdID=self._get_pdid("sby")
                        dt=self._date_freq(bpd,epd)
                        if(dt!="err"):
                            get_data_url=self._token['data_url']+"date/"+epd+"0101/"+PdID+"/"+sid+"/"+dt
                            result=self._data_from_owl(get_data_url)
                            if result.empty:
                                print(OwlError._dicts["SidError"])
                            else:
                                if(len(colist)>0):
                                    result=result[colist]
                                return result
                    else:
                        print(OwlError._dicts["YearError"])
                elif (di == "Q" or di ==  "q"):
                    if len(bpd)==6 and len(epd)==6:
                        if (int(bpd[4:6])>=1 and int(bpd[4:6])<=4) and int(epd[4:6])>=1 and int(epd[4:6])<=4:
                            PdID=self._get_pdid("sbq")
                            dt=self._date_freq(bpd, epd, trans = 's')
                            if(dt!="err"):
                                get_data_url=self._token['data_url']+"date/"+epd+"01/"+PdID+"/"+sid+"/"+dt
                                result=self._data_from_owl(get_data_url)
                                if result.empty:
                                    print(OwlError._dicts["SidError"])
                                else:
                                    if(len(colist)>0):
                                        result=result[colist]
                                    return result
                        else:
                            print(OwlError._dicts["ValueError"])                            
                    else:
                        print(OwlError._dicts["SeasonError"])
                elif (di == "M" or di == "m"):
                    if len(bpd)==6 and len(epd)==6:
                        if (int(bpd[4:6])>=1 and int(bpd[4:6])<=12) and (int(epd[4:6])>=1 and int(epd[4:6])<=12):
                            PdID=self._get_pdid("sbm")
                            dt=self._date_freq(bpd, epd, trans = 'm')
                            if(dt!="err"):
                                get_data_url=self._token['data_url']+"date/"+epd+"01/"+PdID+"/"+sid+"/"+dt
                                result=self._data_from_owl(get_data_url)
                                if result.empty:
                                    print(OwlError._dicts["SidError"])
                                else:
                                    if(len(colist)>0):
                                        result=result[colist]
                                    return result
                        else:
                            print(OwlError._dicts["ValueError"])
                    else:
                        print(OwlError._dicts["MonthError"])                        
                else:
                    print(OwlError._dicts["YQMError"])
            except KeyError:
                print(OwlError._dicts["ColumnsError"])
            except Exception:
                print(OwlError._dicts["PdError"]+"("+PdID+")")
    # 多股資產負債表歷史資料 (Balance sheet multi)
    def fim(self, di, dt, colist = ""):
        '''
        
        Parameters
        ----------
        :param di:
            -
        :param dt:
            -
        :param colist:
            -
        
        Returns
        ----------
        
        [Notes]
        ----------
        
        '''
        if self.status_code==200:
            try:
                if (di == "Y" or di == "y"):
                    if len(dt) == 4:
                        PdID=self._get_pdid("mby")
                        get_data_url=self._token['data_url']+"date/"+dt+"0101/"+PdID
                        result=self._data_from_owl(get_data_url)
                        if result !="err":
                            if(len(colist)>0):
                                result=result[colist]
                            return result
                        else:
                            print(OwlError._dicts["PdError"]+"("+PdID+")")
                    else:
                        print(OwlError._dicts["YearError"])
                elif (di == "Q" or di == "q"):
                    if len(dt) == 6:
                        if int(dt[4:6])>=1 and int(dt[4:6])<=4:
                            PdID=self._get_pdid("mbq")
                            if int(dt[4:6])==1:
                                get_data_url=self._token['data_url']+"date/"+dt+"01/"+PdID
                            elif int(dt[4:6])==2:
                                dt=str(int(dt)+2)
                                get_data_url=self._token['data_url']+"date/"+dt+"01/"+PdID
                            elif int(dt[4:6])==3:
                                dt=str(int(dt)+4)
                                get_data_url=self._token['data_url']+"date/"+dt+"01/"+PdID
                            else:
                                dt=str(int(dt)+6)
                                get_data_url=self._token['data_url']+"date/"+dt+"01/"+PdID
                            result=self._data_from_owl(get_data_url)
                            if result !="err":
                                if(len(colist)>0):
                                    result=result[colist]
                                return result
                            else:
                                print(OwlError._dicts["PdError"]+"("+PdID+")")
                        else:
                            print(OwlError._dicts["ValueError"])
                    else:
                        print(OwlError._dicts["SeasonError"])
                elif (di == "M" or di == "m"):
                    if len(dt) == 6:
                        if (int(dt[4:6])<=12):
                            PdID=self._get_pdid("mbm")
                            get_data_url=self._token['data_url']+"date/"+dt+"01/"+PdID
                            result=self._data_from_owl(get_data_url)
                            if result !="err":
                                if(len(colist)>0):
                                    result=result[colist]
                                return result
                            else:
                                print(OwlError._dicts["PdError"]+"("+PdID+")")
                        else:
                            print(OwlError._dicts["ValueError"])
                    else:
                        print(OwlError._dicts["MonthError"])
                else:
                    print(OwlError._dicts["YQMError"])
            except ValueError:
                try:
                    if(len(colist)>0):  #只撈取指定欄位，未指定則全取
                        result=result[colist]
                    return result
                except:
                    print(OwlError._dicts["ColumnsError"])
                    
    # 法人籌碼個股歷史資料 (Corporate Chip single)
    def chs(self, sid, bpd, epd, colist = ""):
        '''
        
        Parameters
        ----------
        :param sid:
            -
        :param bpd:
            -
        :param epd:
            -
        :param colist:
            -
        Returns
        ----------
        
        [Notes]
        ----------
        
        '''
        if self.status_code==200:
            try:
                if len(bpd)==8 and len(epd)==8:
                    PdID=self._get_pdid("sch")
                    dt=self._date_freq(bpd,epd)
                    if (dt!="err"):
                        get_data_url=self._token['data_url']+"date/"+epd+"/"+PdID+"/"+sid+"/"+dt
                        result=self._data_from_owl(get_data_url)
                        if result.empty:
                            print(OwlError._dicts["SidError"])
                        else:
                            if (len(colist)>0):
                                result=result[colist]
                            return result
                else:
                    print(OwlError._dicts["YearError"])
            except KeyError:
                print(OwlError._dicts["ColumnsError"])
            except Exception:
                    print(OwlError._dicts["PdError"]+"("+PdID+")/"+OwlError._dicts["ValueError"])
    # 法人籌碼多股歷史資料 (Corporate Chip multi)
    def chm(self, dt, colist = ""):
        '''
        
        Parameters
        ----------
        :param dt:
            -
        :param colist:
            -
        :param 
            -
        
        Returns
        ----------
        
        [Notes]
        ----------
        
        '''
        if self.status_code==200:
            try:
                if len(dt)==8:
                    PdID=self._get_pdid("mch")
                    get_data_url=self._token['data_url']+'date/'+dt+'/'+PdID
                    result=self._data_from_owl(get_data_url)
                    if result !="err":
                        if(len(colist)>0):  #只撈取指定欄位，未指定則全取
                            result=result[colist]
                        return result
                    else:
                        print(OwlError._dicts["PdError"]+"("+PdID+")/"+OwlError._dicts["ValueError"])
                else: #有日期但不是8碼，則顯示錯誤訊息
                    print(OwlError._dicts["DayError"])
            except ValueError:
                try:
                    if(len(colist)>0):  #只撈取指定欄位，未指定則全取
                        result=result[colist]
                    return result
                except:
                    print(OwlError._dicts["ColumnsError"])                
    # 技術指標 個股 (Technical indicators single)
    def tis(self, sid, bpd, epd, colist = ""):
        '''
        
        Parameters
        ----------
        :param 
            -
        :param 
            -
        :param 
            -
        
        Returns
        ----------
        
        [Notes]
        ----------
        
        '''
        if self.status_code==200:
            try:
                if len(bpd)==8 and len(epd)==8:
                    PdID=self._get_pdid("sth")
                    dt=self._date_freq(bpd,epd)
                    if (dt!="err"):
                        get_data_url=self._token['data_url']+"date/"+epd+"/"+PdID+"/"+sid+"/"+dt
                        result=self._data_from_owl(get_data_url)
                        if result.empty:
                            print(OwlError._dicts["SidError"])
                        else:
                            if (len(colist)>0):
                                result=result[colist]
                            return result
                else:
                    print(OwlError._dicts["YearError"])
            except KeyError:
                print(OwlError._dicts["ColumnsError"])
            except Exception:
                    print(OwlError._dicts["PdError"]+"("+PdID+")/"+OwlError._dicts["ValueError"])
   
    # 技術指標 多股 (Technical indicators multi) 
    def tim(self, dt, colist = ""):
        '''
        
        Parameters
        ----------
        :param 
            -
        :param 
            -
        :param 
            -
        
        Returns
        ----------
        
        [Notes]
        ----------
        
        '''
        if self.status_code==200:
            try:
                if len(dt)==8:
                    PdID=self._get_pdid("mth")
                    get_data_url=self._token['data_url']+'date/'+dt+'/'+PdID
                    result=self._data_from_owl(get_data_url)
                    if result !="err":
                        if(len(colist)>0):  #只撈取指定欄位，未指定則全取
                            result=result[colist]
                        return result
                    else:
                       print(OwlError._dicts["PdError"]+"("+PdID+")/"+OwlError._dicts["ValueError"])
                else: #有日期但不是8碼，則顯示錯誤訊息
                    print(OwlError._dicts["DayError"])
            except ValueError:
                try:
                    if(len(colist)>0):  #只撈取指定欄位，未指定則全取
                        result=result[colist]
                    return result
                except:
                    print(OwlError._dicts["ColumnsError"])
    
    # 公司基本資料 多股 (Company information multi)
    def cim(self, colist = ""):
        '''
        
        Parameters
        ----------
        :param 
            -
        :param 
            -
        :param 
            -
        
        Returns
        ----------
        
        [Notes]
        ----------
        
        '''
        if self.status_code==200:
            try:
                PdID=self._get_pdid("mcm")
                get_date_url=self._token['data_url']+PdID
                result=self._data_from_owl(get_date_url)
                if result !="err":
                    if(len(colist)>0):
                        result=result[colist]
                    return result
                else:
                    print(OwlError._dicts["PdError"]+"("+PdID+")")
            except ValueError:
                try:
                    if(len(colist)>0):  #只撈取指定欄位，未指定則全取
                        result=result[colist]
                    return result
                except:
                    print(OwlError._dicts["ColumnsError"])
    
    # 股利政策 個股 (Dividend policy single)
    def dps(self, sid, bpd, epd, colist = ""):
        '''
        
        Parameters
        ----------
        :param 
            -
        :param 
            -
        :param 
            -
        
        Returns
        ----------
        
        [Notes]
        ----------
        
        '''
        if self.status_code==200:
            try:
                if len(bpd)==4 and len(epd)==4:
                    PdID=self._get_pdid("scm1")
                    dt=self._date_freq(bpd,epd)
                    if (dt!="err"):
                        get_data_url=self._token['data_url']+"date/"+epd+"0101/"+PdID+"/"+sid+"/"+dt
                        result=self._data_from_owl(get_data_url)
                        if result.empty:
                            print(OwlError._dicts["SidError"])
                        else:
                            if (len(colist)>0):
                                result=result[colist]
                            return result
                else:
                    print(OwlError._dicts["YearError"])
            except KeyError:
                print(OwlError._dicts["ColumnsError"])
            except Exception:
                print(OwlError._dicts["PdError"]+"("+PdID+")")
    
    # 股利政策 多股 (Dividend policy multi)    
    def dpm(self, dt, colist = ""):
        '''
        
        Parameters
        ----------
        :param 
            -
        :param 
            -
        :param 
            -
        
        Returns
        ----------
        
        [Notes]
        ----------
        
        '''
        if self.status_code==200:
            try:
                if len(dt)==4:
                    PdID=self._get_pdid("mcm1")
                    get_data_url=self._token['data_url']+'date/'+dt+'0101/'+PdID
                    result=self._data_from_owl(get_data_url)
                    if result!="err":
                        if(len(colist)>0):  #只撈取指定欄位，未指定則全取
                            result=result[colist]
                        return result
                    else:
                        print(OwlError._dicts["PdError"]+"("+PdID+")")
                else: #有日期但不是8碼，則顯示錯誤訊息
                    print(OwlError._dicts["YearError"])
            except:
                try:
                    if(len(colist)>0):  #只撈取指定欄位，未指定則全取
                        result=result[colist]
                    return result
                except:
                    print(OwlError._dicts["ColumnsError"])
    
    # 除權除息 個股 (Exemption Dividend policy single)
    def edps(self, sid, bpd, epd, colist = ""):
        '''
        
        Parameters
        ----------
        :param 
            -
        :param 
            -
        :param 
            -
        
        Returns
        ----------
        
        [Notes]
        ----------
        
        '''
        if self.status_code==200:
            try:
                if len(bpd)==4 and len(epd)==4:
                    PdID=self._get_pdid("scm2")
                    dt=self._date_freq(bpd,epd)
                    if (dt!="err"):
                        get_data_url=self._token['data_url']+"date/"+epd+"0101/"+PdID+"/"+sid+"/"+dt
                        result=self._data_from_owl(get_data_url)
                        if result.empty:
                            print(OwlError._dicts["SidError"])
                        else:
                            if (len(colist)>0):
                                result=result[colist]
                            return result
                else:
                    print(OwlError._dicts["YearError"])
            except KeyError:
                print(OwlError._dicts["ColumnsError"])
            except Exception:
                print(OwlError._dicts["PdError"]+"("+PdID+")")
    
    # 除權除息 多股 (Exemption Dividend policy multi)    
    def edpm(self, dt, colist = ""):
        '''
        
        Parameters
        ----------
        :param 
            -
        :param 
            -
        :param 
            -
        
        Returns
        ----------
        
        [Notes]
        ----------
        
        '''
        if self.status_code==200:
            try:
                if len(dt)==4:
                    PdID=self._get_pdid("mcm2")
                    get_data_url=self._token['data_url']+'date/'+dt+'0101/'+PdID
                    result=self._data_from_owl(get_data_url)
                    if result!="err":
                        if(len(colist)>0):  #只撈取指定欄位，未指定則全取
                            result=result[colist]
                        return result
                    else:
                        print(OwlError._dicts["PdError"]+"("+PdID+")")
                else: #有日期但不是8碼，則顯示錯誤訊息
                    print(OwlError._dicts["YearError"])
            except:
                try:
                    if(len(colist)>0):  #只撈取指定欄位，未指定則全取
                        result=result[colist]
                    return result
                except:
                    print(OwlError._dicts["ColumnsError"])
    
    # 即時報價 (Timely stock price)
    def tsp(self, sid, colist = ""):
        '''
        
        Parameters
        ----------
        :param 
            -
        :param 
            -
        :param 
            -
        
        Returns
        ----------
        
        [Notes]
        ----------
        
        '''
        if self.status_code==200:
            try:
                PdID=self._get_pdid("mnp")
                get_data_url=self._token['data_url']+PdID+"/"+sid
                result=self._data_from_owl(get_data_url)
                if result.empty:
                    print(OwlError._dicts["SidError"])
                else:
                    if len(colist)>0:
                        result=result[colist]
                    return result
            except KeyError:
                print(OwlError._dicts["ColumnsError"])
            except Exception:
                print(OwlError._dicts["PdError"]+"("+PdID+")")


