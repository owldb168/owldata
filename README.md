數據貓頭鷹官方網站: https://owl.cmoney.com.tw/Owl/

# owldata 數據貓頭鷹 API

--------

## Dependencies

- pandas
- request

## Install

安裝資源可以詳見 Github at https://github.com/owldb168/owldata

By PyPI

``` python
pip install owldata
```

Install source from GitHub

``` sh
git clone https://github.com/owldb168/owldata.git
cd owldata
python setup.py install
```

## HTTP Authentication

``` python
import owldata

#輸入數據貓頭鷹會員AppID & 應用程式密鑰
appid = '請輸入 AppID'
appsecret = '請輸入 應用程式密鑰'

#引用函數取得資料
owlapi = owldata.OwlData(appid, appsecret)
```

## Data Function

1. 個股日收盤行情 (single stock price)

    **可指定個股，查詢台股個股日收盤行情**
   - ssp(sid, bpd, epd, colist)
       - sid = 股票代號
       - bpd = 查詢起始日期 8碼數字，格式: yyyymmdd
       - epd = 查詢起始日期 8碼數字，格式: yyyymmdd
       - colist = 指定顯示欄位 (若不輸入則顯示所有欄位)
    - 欄位：[日期], [股票名稱], [開盤價], [最高價], [最低價], [收盤價], [漲跌], [漲幅(%)], [成交量], [成交筆數], [成交金額(千)], [均張], [均價], [成交量(股)]
    - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
    - 範例
        ``` python
        # 擷取台積電股價 from 2019/01/01 to 2019/06/30
        owlapp.ssp("2330", "20190101", "20190630")
        ```

2. 多股每日收盤行情 (multi stock price)

    **最新一日，所有上市櫃台股之每日交易數據**
   - msp(dt, colist)
     - dt =  查詢某日代碼8碼，格式: yyyymmdd
     - colist = 指定顯示欄位 (若不輸入則顯示所有欄位)
     - 欄位：[日期], [股票名稱], [開盤價], [最高價], [最低價], [收盤價], [漲跌], [漲幅(%)], [成交量], [成交筆數], [成交金額(千)], [均張], [均價], [成交量(股)]
     - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
     - 範例
        ``` python
        # 擷取台股上市上櫃  2019/06/30 所有盤後資訊
        owlapp.msp("20190630")
        ```

3. fis

    個股財務簡表
   - fis(di, sid, bpd, epd, colist)
       - di = 查詢資料時間頻率，y = 年度, q = 季度, m = 月
       - sid = 股票代號
       - bpd = 查詢起始日期 8碼數字，格式: yyyymmdd
       - epd = 查詢起始日期 8碼數字，格式: yyyymmdd
       - colist = 指定顯示欄位 (若不輸入則顯示所有欄位)
    - 欄位：[日期], [股票名稱], [開盤價], [最高價], [最低價], [收盤價], [漲跌], [漲幅(%)], [成交量], [成交筆數], [成交金額(千)], [均張], [均價], [成交量(股)]
    - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
    - 範例
        ``` python
        # 擷取台積電股價 from 2019/01/01 to 2019/06/30
        owlapp.ssp("2330", "20190101", "20190630")
        ```


## Contribute
