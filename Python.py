# coding=gbk
from sys import * 
from ctypes import * 
import json
#这里加载的是64位的DLL   加载32的也一样可以用    
Dll = WinDLL("t_json")#载入DLL

#定义交易接口函数参数类型——————————————————————————————————————————————————————————————————————————————————
    #不定义也不报错所以懒得写了！
#定义函数返回类型——————————————————————————————————————————————————————————
Dll.Logon.restype =  POINTER(c_void_p)
#Dll.Logoff.restype =  c_void
Dll.QueryData.restype = c_int 
Dll.SendOrder.restype = c_int 
Dll.QueryHQ.restype = c_int 
Dll.CancelOrder.restype = c_int 
Dll.CancelOrder.CancelOrder = c_int 
Dll.QueryHistoryData.restype = c_int 




print("交易接口测试—————————————————————————")
qsid = 0
host = c_buffer(b"trade.10jqka.com.cn")#实盘需联系授权 panghu1103@gmail.com
post  = 8002
version = c_buffer(b"E065.18.81.002")
yybid = c_buffer(b"")#营业部ID  多数券商不需要这个参数 如需要选择营业部情况下 需要这个参数
accounttype = 0x30
account = c_buffer(b"xxx")#自己的资金账号
password = c_buffer(b"xxxx")#写自己要密码
comm_password = c_buffer(b"")#通讯密码没有就留空
#——————————————————————————————————————————————重要——————————————————————————————————————
Out = c_buffer(1024*1024)#多线程中要写成局部变量避免内存冲突造成崩溃

print("登录交易接口=====================================================")
ClientID = Dll.Logon(qsid, host, post, version, yybid, accounttype,account,password,comm_password,False,Out)

if ClientID:
    print("登录成功，客户端ID",ClientID)
else:
    print(Out.value.decode('gb2312'))
    exit()
print("查询资产=====================================================")
Category = 0 #查询信息的种类 0资金 1股份 2当日委托 3当日成交 4当日委托可撤单 5股东账户 12=可申购新股 13=申购额度 14=配号查询 15=中签查询
b = Dll.QueryData(ClientID,Category,Out)
if b > 0 :
    _json = json.loads(Out.value.decode('gb2312'))
    print(_json)
else:
    print(Out.value.decode('gb2312'))

print("五档行情=====================================================")

Zqdm = c_buffer(b"000001")
b = Dll.QueryHQ(ClientID,Zqdm,Out)

if b > 0 :
    _json = json.loads(Out.value.decode('gb2312'))

    print(_json)
else:
    print(Out.value.decode('gb2312'))

print("持仓股票=====================================================")
Category = 1
b = Dll.QueryData(ClientID,Category,Out)

if b > 0 :
    _json = json.loads(Out.value.decode('gb2312'))

    print(_json)
else:
    print(Out.value.decode('gb2312'))
print("下单=====================================================")

Category = 0    #0买 1卖
Gddm = c_buffer(b"")    #股东代码 可空 指针多股东账户的情况可以指定股东
Zqdm = c_buffer(b"000001")
Price = c_float(8.99)
Quantity = 100

b = Dll.SendOrder(ClientID, Category, Gddm, Zqdm, Price, Quantity, Out)
if b > 0 :
    OrderID = Out.value.decode('gb2312')

    print("下单成功，合同编号：",OrderID)

    print("撤单=====================================================")

    OrderID = OrderID.encode('utf-8')

    b = Dll.CancelOrder(ClientID, OrderID, Out)

    if b > 0 :

        OrderID = Out.value.decode('gb2312')

        print("撤单成功,合同编号：",OrderID)
    else:
        print(Out.value.decode('gb2312'))

else:
    print(Out.value.decode('gb2312'))


#交易接口其他功能使用跟上面差不多，就不一一演示了————————————————————————————————————————————————————————


#下面看行情接口演示——————————————————————————————————————————————————————————————————————————————————
#定义行情接口函数参数类型——————————————————————————————————————————————————————————————————————————————————
Dll.HQ_Logon.restype =  POINTER(c_void_p)
#Dll.HQ_Logoff.restype =  c_void
Dll.HQ_QueryData.restype =  c_int
Dll.HQ_PushData.restype =  c_int


print("行情接口测试————————————————————————")

Host = c_buffer(b"112.17.10.222")#行情服务器IP
Port = 9601#端口
account = c_buffer(b"xxx")#自己的LS手机号 普通账号无法查询到L2数据
password = c_buffer(b"xxx")#写自己要密码
print("行情登录——————————————————————————")
ClientID = Dll.HQ_Logon (Host, Port, account, password, Out)
if ClientID:
    print("行情登录成功，客户端ID",ClientID)
else:
    print(Out.value.decode('gb2312'))
    exit()

print("十档行情测试————————————————————————")
#自定义要查询的字段 相当于查询数据库字段的意思
#股票代码 可以一次查询多只股票的行情   但是必须是同一个板块的  比如 第一只股票是深圳板块股 那么第二只也要是深圳板块股才能一次达到批量查询
#custom_data是要查询的字段  可以自定义增加或减少来满足自己需要查询的数据
custom_data = c_buffer(b"id=200&market=USZA&codelist=000001&datatype=5,6,7,10,13,24,25,26,27,28,29,30,31,32,33,34,35,69,70,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,150,151,152,153,154,155,156,157,1968584,201,202,203,204,205,206,207,208,209,210,211,212,213,214,3541450,3475914")#代码
b = Dll.HQ_QueryData(ClientID,custom_data,Out)
if b > 0 :
    _json = json.loads(Out.value.decode('gb2312'))

    print(_json)
else:
    print(Out.value.decode('gb2312'))
print("成交明细测试————————————————————————")

custom_data = c_buffer(b"id=220&market=USZA&code=000001&start=-32&end=0&datatype=10,12,13")

b = Dll.HQ_QueryData(ClientID,custom_data,Out)
if b > 0 :
    _json = json.loads(Out.value.decode('gb2312'))

    print(_json)
else:
    print(Out.value.decode('gb2312'))

print("买卖列队测试————————————————————————")

custom_data = c_buffer(b"id=223&market=USZA&code=000001&codelist=000001&datatype=10")

b = Dll.HQ_QueryData(ClientID,custom_data,Out)
if b > 0 :
    _json = json.loads(Out.value.decode('gb2312'))

    print(_json)
else:
    print(Out.value.decode('gb2312'))

print("快速涨幅排名————————————————————————")
#&sortcount=7（取7只）’&sortid=527527（1分钟排序ID）527526（3分钟）3934664（5分钟）461438（10分钟）461439（15分钟）
custom_data = c_buffer(b"id=7&blockid=E&reqflag=blockserver&sortbegin=0&sortcount=7&sortid=527527&sortorder=D")

b = Dll.HQ_QueryData(ClientID,custom_data,Out)
if b > 0 :
    _json = json.loads(Out.value.decode('gb2312'))

    print(_json)
else:
    print(Out.value.decode('gb2312'))



#只在开盘期间才会有数据推送过来
#以下回调函数  每个功能都可以定义不同的回调
#-------------------------------------------------------------------一下功能只在开盘期间有效  本人没有测试 不知道有没有写错

print('数据推送测试=====================================================')
推送回调类型 = CFUNCTYPE(c_int, POINTER(c_char_p))
def 推送回调函数(type, Result):
    if type == 10001:#普通十档行情 3秒
        _json = json.loads(Out.value.decode('gb2312'))

        print(_json)
    elif type == 10206:# 逐笔委托
        _json = json.loads(Out.value.decode('gb2312'))

        print(_json)
    elif type == 10207:#全速500档转10档
        _json = json.loads(Out.value.decode('gb2312'))

        print(_json)
推送回调函数指针 = 推送回调类型(推送回调函数)
Zqdm = c_buffer(b"000001")
b = Dll.HQ_PushData(ID, 0, Zqdm, 推送回调函数指针, True);#参数2 0为十档行情推送间隔3秒 1为逐笔委托毫秒级全速 2为全速10档 参数6 真为开启这只股票推送  假为关闭这只股推送
if b > 0 :
    print('开启成功无提示')
else:
    print(Out.value.decode('gb2312'))

