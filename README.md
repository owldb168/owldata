# Python 串接 數據貓頭鷹 API 說明文件

---

## 引用方式

## (1) 於程式開頭引用owl_api

``` python
import owl_api
```

## 2. 函數說明

## (1) ssp(sid, bpd, epd, col) -- 股價資訊 (個股)

## 3. 程式碼範例

``` python
import owldata

#輸入數據貓頭鷹會員ID & Secret
appid = '請輸入 ID'
appsecret = '請輸入金鑰 Secret'

#引用函數取得資料
owl = owldata.OwlData(appid, appsecret)
col = []
owl_data = owl.ssp("2330","20190301","20190531",col)

```
