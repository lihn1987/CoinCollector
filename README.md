# 新版本升级！！！！！！！
## 部署方式
懒得写，晚点在写
## 目标
1、能够提供ok，火币，币安的深度信息

2、能够提供ok，火币，币安的交易信息

3、ok，火币，币安的延时信息

4、能够记录所有的交易，并配合当时的深度信息

5、量化~~~~哈哈哈哈

## 当前进度
### 信息抓取部分
- ok的深度信息
- 火币的深度信息
- ok的实时交易信息(下一步)
- 火币的实时交易信息（下一步）
### web服务端部分
- 完成了所有币种深度信息的简单整合接口
### web前端部分
- 能够简单展示所有币种的基本信息
- 能够对是否有差价进行颜色显示(下一步)
- 能够对各个交易所最大买入利差进行摘要显示(下一步)
- 能够对延时信息进行显示(下一步)
### 部署部分
- docker虚拟机的部署
- 本地免翻墙方位api

## 数据库格式
### redis
**配置要抓取的币种**
- key:<市场名称>-CONFIG
- value:[[<交易币种>-<计价币种>], [<交易币种>-<计价币种>]...]

**币种交易规则**
- key <交易币种>_<基础币种>-<市场名称>-SYMBOL
- SYMBOL:
"base-coin"基础币种<br/>
"order-coin": 交易币种<br/>
"price-precision": 价格精度<br/>
"amount-precision": 数量精度<br/>
"symbol-partition": 交易区 1 主区  2 其他区域<br/>
"symbol": item["symbol"] 交易名称<br/>
"state": True能够交易 False不能欧交易<br/>
"value-precision": 交易金额进度<br/>
"limit-order-min-order-amt" 交易对限价单最小下单量 ，以基础币种为单位（NEW）<br/>
"limit-order-max-order-amt" 交易对限价单最大下单量 ，以基础币种为单位（NEW）<br/>
"sell-market-min-order-amt" 交易对市价卖单最小下单量，以基础币种为单位（NEW）<br/>
"sell-market-max-order-amt": 交易对市价卖单最大下单量，以基础币种为单位（NEW）<br/>
"buy-market-max-order-value": i交易对市价买单最大下单金额，以计价币种为单位（NEW）<br/>
"min-order-value": 交易对限价单和市价买单最小下单金额 ，以计价币种为单位<br/>
"max-order-value": 交易对限价单和市价买单最大下单金额 ，以折算后的USDT为单位（NEW）<br/>
}

**当前海龟交易法的最优参数**
- key HAIGUI-<交易币种>-<基础币种>-<市场名称>-<k线类型>SYMBOL
- SYMBOL:
"max_profit"预计最大收益<br/>
"best_buy_width_range": 交易窗口大小<br/>
"best_buy_point"最佳买点<br/>
"best_sell_point_low"最佳止损点<br/>
"best_sell_point_hight"最佳止赢点<br/>

**深度行情信息**
- key:<交易币种>-<计价币种>-<市场名称>-DEPTH
- value:{<br>
"up_time" 更新时间</br>
"forbuy" 买盘数据[[<价格>,<数量>],...]</br>
"forsell" 卖盘数据[[<价格>,<数量>],...]</br>
}




