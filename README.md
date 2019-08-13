數據貓頭鷹官方網站: https://owl.cmoney.com.tw/Owl/

# owldata 數據貓頭鷹 API

--------

## Outline

- [owldata 數據貓頭鷹 API](#owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api)
  - [Outline](#outline)
  - [Dependencies](#dependencies)
  - [Install](#install)
  - [HTTP Authentication](#http-authentication)
  - [Data Function](#data-function)
  - [Contribute](#contribute)
  
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

[top](#owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api)

## HTTP Authentication

``` python
import owldata

#輸入數據貓頭鷹會員AppID & 應用程式密鑰
appid = '請輸入 AppID'
appsecret = '請輸入 應用程式密鑰'

#引用函數取得資料
owlapp = owldata.OwlData(appid, appsecret)
```

[top](#owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api)

## Data Function

1. 個股日收盤行情 (Single Stock Price)

   ``` python
   OwlData.ssp(sid:str, bpd:str, epd:str, colist:list) -> DataFrame
   ```

    <table>
    <tr>
        <td rowspan="4"><b>Parameters<b></td>
        <td> - <b> sid </b> : <i> string </i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;股票代號
        </td>
    </tr>
    <tr>
        <td> - <b>  bpd </b> : <i> string </i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;查詢起始日期 8 碼數字，格式: yyyymmdd
        </td>
    </tr>
    <tr>
        <td> - <b> epd</b> : <i> string</i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;查詢結束日期 8 碼數字，格式: yyyymmdd
        </td>
    </tr>
    <tr>
        <td> - <b> colist</b> : <i> list, default None</i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
        </td>
    </tr>
    <tr>
        <td><b> Returns</b></td><td>DataFrame or Series</td>
    </tr>
    <tr>
        <td colspan="2">
        <b> Note</b>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
        </td>
    </tr>
    </table>

   - 欄位：

    <table>
        <tr>
            <td>日期</td>
            <td>股票名稱</td>
            <td>開盤價</td>
            <td>最高價</td>
            <td>最低價</td>
            <td>收盤價</td>
            <td>漲跌</td>
        </tr>
        <tr>
            <td>漲幅(%)</td>
            <td>成交量</td>
            <td>成交筆數</td>
            <td>成交金額(千)</td>
            <td>均張</td>
            <td>均價</td>
            <td>成交量(股)</td>
        </tr>
    </table>

   - 範例

    ``` python
    # 擷取台積電股價 from 2019/01/01 to 2019/06/30
    >>> owlapp.ssp("2330", "20190101", "20190630")
    [out]

           日期   股票名稱	開盤價	最高價	最低價	收盤價	 漲跌	漲幅(%)	 成交量	
    0    20190813  台積電	249.00	249.50	246.50	246.50	-4.50	-1.79	23121.00
    1    20190812  台積電	254.50	254.50	251.00	251.00	-2.50	-0.99	24732.00
    ```



2. 多股每日收盤行情 (Multi-Stock Price)
    **msp(dt, colist)**
    <table>
    <tr>
        <td rowspan="2"><b>Parameters<b></td>
        <td> - <b> dt </b> : <i> string </i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;查詢某一日期
        </td>
    </tr>
    
    <tr>
        <td> - <b> colist </b>: 
        <i> list, default None</i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
        </td>
    </tr>
    <tr>
        <td><b> Returns</b></td><td>DataFrame or Series</td>
    </tr>
    <tr>
        <td colspan="2">
        <b> Note</b>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
        </td>
    </tr>
    </table>

     - 欄位：
     [日期], [股票名稱], [開盤價], [最高價], [最低價], [收盤價], [漲跌], [漲幅(%)], [成交量], [成交筆數], [成交金額(千)], [均張], [均價], [成交量(股)]
     - 例外:發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
     - 範例
        ``` python
        # 擷取台股上市上櫃  2019/06/30 所有盤後資訊
        owlapp.msp("20190630")
        ```

3. 個股財務簡表
    **OwlData.fis(di, sid, bpd, epd, colist)**
    <table>
    <tr>
        <td rowspan="5"><b>Parameters<b></td>
        <td> - <b> di </b> : <i> string </i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;設定資料時間頻率
            <ul style="list-style-type:disc;">
                <li>Y : 年度, 格式 : yyyy</li>
                <li>Q : 季度, 格式 : yyyyqq</li>
                <li>M : 月, 格式 : yyyymm</li>
            </ul>
        </td>
    </tr>
    <tr>
        <td> - <b>  sid </b> : <i> string </i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;股票代號
        </td>
    </tr>
    <tr>
        <td> - <b>  bpd </b> : <i> string </i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;查詢起始日期
        </td>
    </tr>
    <tr>
        <td> - <b> epd</b> : <i> string</i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;查詢結束日期
        </td>
    </tr>
    <tr>
        <td> - <b> colist </b>: 
        <i> list, default None</i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
        </td>
    </tr>
    <tr>
        <td><b> Returns</b></td><td>DataFrame or Series</td>
    </tr>
    <tr>
        <td colspan="2">
        <b> Note</b>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp; - 季度日期格式 yyyqq, 其中 qq 請輸入 01 - 04, 分別表示為第一季至第四季
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
        </td>
    </tr>
    </table>
   
   - 欄位：
   - 範例
        ``` python
        # 擷取台積電股價 from 2019/01/01 to 2019/06/30
        owlapp.fis("2330", "20190101", "20190630")
        ```
4. 多股財務簡表
   **fim(di, dt, colist)**
    <table>
        <tr>
            <td rowspan="3"><b>Parameters<b></td>
            <td> - <b> di </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;設定資料時間頻率
                <ul style="list-style-type:disc;">
                    <li>Y : 年度, 格式 : yyyy</li>
                    <li>Q : 季度, 格式 : yyyyqq</li>
                    <li>M : 月, 格式 : yyyymm</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td> - <b>  dt </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢某一日期
            </td>
        </tr>
        <tr>
            <td> - <b> colist </b>: 
            <i> list, default None</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
            </td>
        </tr>
        <tr>
            <td><b> Returns</b></td><td>DataFrame or Series</td>
        </tr>
        <tr>
            <td colspan="2">
            <b> Note</b>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 季度日期格式 yyyqq, 其中 qq 請輸入 01 - 04, 分別表示為第一季至第四季
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
            </td>
        </tr>
    </table>

   - 欄位：
   - 例外:發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
   - 範例
        ``` python
        # 擷取台積電股價 from 2019/01/01 to 2019/06/30
        owlapp.fim("2330", "20190101", "20190630")
        ```

5. 法人籌碼個股歷史資料 (Corporate Chip Single)
   **chs(sid, bpd, epd, colist)**
    <table>
        <tr>
            <td rowspan="4"><b>Parameters<b></td>
            <td> - <b> sid </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;股票代號
            </td>
        </tr>
        <tr>
            <td> - <b>  bpd </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢起始日期 8 碼數字，格式: yyyymmdd
            </td>
        </tr>
        <tr>
            <td> - <b> epd</b> : <i> string</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢結束日期 8 碼數字，格式: yyyymmdd
            </td>
        </tr>
        <tr>
            <td> - <b> colist </b>: 
            <i> list, default None</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
            </td>
        </tr>
        <tr>
            <td><b> Returns</b></td><td>DataFrame or Series</td>
        </tr>
        <tr>
            <td colspan="2">
            <b> Note</b>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
            </td>
        </tr>
    </table>

   - 欄位：
   - 例外:發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
   - 範例
        ``` python
        # 擷取台積電股價 from 2019/01/01 to 2019/06/30
        owlapp.chs("2330", "20190101", "20190630")
        ```


6. 法人籌碼多股歷史資料 (Corporate Chip Multi)
   **chm(dt,colist)**
    <table>
    <tr>
        <td rowspan="2"><b>Parameters<b></td>
        <td> - <b> dt </b> : <i> string </i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;查詢某一日期
        </td>
    </tr>
    
    <tr>
        <td> - <b> colist </b>: 
        <i> list, default None</i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
        </td>
    </tr>
    <tr>
        <td><b> Returns</b></td><td>DataFrame or Series</td>
    </tr>
    <tr>
        <td colspan="2">
        <b> Note</b>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
        </td>
    </tr>
    </table>

   - 欄位：
   - 例外:發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
   - 範例
      ``` python
      # 擷取台股上市上櫃  2019/06/30 所有盤後資訊
      owlapp.chm("20190630")
      ```

7. 技術指標 個股 (Technical Indicators Single)
    **tis(sid,bpd,epd,colist)**
    <table>
        <tr>
            <td rowspan="4"><b>Parameters<b></td>
            <td> - <b> sid </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;股票代號
            </td>
        </tr>
        <tr>
            <td> - <b>  bpd </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢起始日期 8 碼數字，格式: yyyymmdd
            </td>
        </tr>
        <tr>
            <td> - <b> epd</b> : <i> string</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢結束日期 8 碼數字，格式: yyyymmdd
            </td>
        </tr>
        <tr>
            <td> - <b> colist </b>: 
            <i> list, default None</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
            </td>
        </tr>
        <tr>
            <td><b> Returns</b></td><td>DataFrame or Series</td>
        </tr>
        <tr>
            <td colspan="2">
            <b> Note</b>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
            </td>
        </tr>
    </table>

    - 欄位：
    - 例外:發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
    - 範例
        ``` python
        # 擷取台積電股價 from 2019/01/01 to 2019/06/30
        owlapp.tis("2330", "20190101", "20190630")
        ```

8. 技術指標 多股 (Technical Indicators Multi)
   **tim(dt,colist)**
    <table>
    <tr>
        <td rowspan="2"><b>Parameters<b></td>
        <td> - <b> dt </b> : <i> string </i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;查詢某一日期
        </td>
    </tr>
    
    <tr>
        <td> - <b> colist </b>: 
        <i> list, default None</i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
        </td>
    </tr>
    <tr>
        <td><b> Returns</b></td><td>DataFrame or Series</td>
    </tr>
    <tr>
        <td colspan="2">
        <b> Note</b>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
        </td>
    </tr>
    </table>

     - 欄位：
     - 例外:發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
     - 範例
        ``` python
        # 擷取台股上市上櫃  2019/06/30 所有盤後資訊
        owlapp.tim("20190630")
        ```

9. 公司基本資料 多股 (Company Information Multi)
   **cim(colist)**
     - colist = 指定顯示欄位 (若不輸入則顯示所有欄位)

    <table>
    <tr>
        <td rowspan="1"><b>Parameters<b></td>
        <td> - <b> colist </b> : <i> list, default None </i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
        </td>
    </tr>
    <tr>
        <td><b> Returns</b></td><td>DataFrame or Series</td>
    </tr>
    <tr>
        <td colspan="2">
        <b> Note</b>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
        </td>
    </tr>
    </table>

   - 欄位：
   - 例外:發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
   - 範例
        ``` python
        # 擷取台股上市上櫃  2019/06/30 所有盤後資訊
        owlapp.cim()
        ```

10. 股利政策 個股 (Dividend Policy Single)
    **dps(sid, bpd, epd, colist)**
    <table>
        <tr>
            <td rowspan="4"><b>Parameters<b></td>
            <td> - <b> sid </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;股票代號
            </td>
        </tr>
        <tr>
            <td> - <b>  bpd </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢起始日期 8 碼數字，格式: yyyymmdd
            </td>
        </tr>
        <tr>
            <td> - <b> epd</b> : <i> string</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢結束日期 8 碼數字，格式: yyyymmdd
            </td>
        </tr>
        <tr>
            <td> - <b> colist </b>: 
            <i> list, default None</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
            </td>
        </tr>
        <tr>
            <td><b> Returns</b></td><td>DataFrame or Series</td>
        </tr>
        <tr>
            <td colspan="2">
            <b> Note</b>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
            </td>
        </tr>
    </table>

    - 欄位：
    - 例外:發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
    - 範例
        ``` python
        # 擷取台積電股價 from 2019/01/01 to 2019/06/30
        owlapp.dps("2330", "20190101", "20190630")
        ```

11. 股利政策 多股 (Dividend Policy Multi) 
    **dpm(dt, colist)**
    <table>
    <tr>
        <td rowspan="2"><b>Parameters<b></td>
        <td> - <b> dt </b> : <i> string </i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;查詢某一日期
        </td>
    </tr>
    
    <tr>
        <td> - <b> colist </b>: 
        <i> list, default None</i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
        </td>
    </tr>
    <tr>
        <td><b> Returns</b></td><td>DataFrame or Series</td>
    </tr>
    <tr>
        <td colspan="2">
        <b> Note</b>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
        </td>
    </tr>
    </table>

    - 欄位：
    - 例外:發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
    - 範例
      ``` python
        # 擷取台股上市上櫃  2019/06/30 所有盤後資訊
        owlapp.dpm("20190630")
        ```

12. 除權除息 個股 (Exemption Dividend Policy Single)
    **edps(sid, bpd, epd, colist)**
    <table>
        <tr>
            <td rowspan="4"><b>Parameters<b></td>
            <td> - <b> sid </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;股票代號
            </td>
        </tr>
        <tr>
            <td> - <b>  bpd </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢起始日期 8 碼數字，格式: yyyymmdd
            </td>
        </tr>
        <tr>
            <td> - <b> epd</b> : <i> string</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢結束日期 8 碼數字，格式: yyyymmdd
            </td>
        </tr>
        <tr>
            <td> - <b> colist </b>: 
            <i> list, default None</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
            </td>
        </tr>
        <tr>
            <td><b> Returns</b></td><td>DataFrame or Series</td>
        </tr>
        <tr>
            <td colspan="2">
            <b> Note</b>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
            </td>
        </tr>
    </table>

    - 欄位：
    - 例外:發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
    - 範例
        ``` python
        # 擷取台積電股價 from 2019/01/01 to 2019/06/30
        owlapp.edps("2330", "20190101", "20190630")
        ```

13. 除權除息 多股 (Exemption Dividend Policy Multi)
    **edpm(dt, colist)**
    <table>
    <tr>
        <td rowspan="2"><b>Parameters<b></td>
        <td> - <b> dt </b> : <i> string </i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;查詢某一日期
        </td>
    </tr>
    
    <tr>
        <td> - <b> colist </b>: 
        <i> list, default None</i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
        </td>
    </tr>
    <tr>
        <td><b> Returns</b></td><td>DataFrame or Series</td>
    </tr>
    <tr>
        <td colspan="2">
        <b> Note</b>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
        </td>
    </tr>
    </table>

    - 欄位：
    - 例外:發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
    - 範例
      ``` python
      # 擷取台股上市上櫃  2019/06/30 所有盤後資訊
      owlapp.edpm("20190630")
      ```

14. 即時報價 (Timely Stock Price)
    **tsp(sid, colist)**
    <table>
    <tr>
        <td rowspan="2"><b>Parameters<b></td>
        <td> - <b> sid </b> : <i> string </i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;股票代號
        </td>
    </tr>
    
    <tr>
        <td> - <b> colist </b>: 
        <i> list, default None</i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
        </td>
    </tr>
    <tr>
        <td><b> Returns</b></td><td>DataFrame or Series</td>
    </tr>
    <tr>
        <td colspan="2">
        <b> Note</b>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
        </td>
    </tr>
    </table>

    - 欄位：
    - 例外:發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
    - 範例
        ``` python
        # 擷取台積電股價 from 2019/01/01 to 2019/06/30
        owlapp.tsp("2330")
        ```

[top](#owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api)

## Contribute
