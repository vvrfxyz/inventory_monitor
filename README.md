## 库存监控框架
主要用于一些羊毛抢购，监控库存使用。

## 目前实现得功能
- [x] 通知（Bark）
- [x] 简易配置
- [x] 限定时间运行
- [x] 自定义任务监控

## 配置说明
```yaml
time_settings:
  start: "09:00" #起始启动时间
  end: "21:00" #结束启动时间 
sleep_interval: 10 #查询间隔

websites:
    #任务名字
  - name: "建行1元购" 
    #是否监控 true：开启
    active: true 
    # 模拟请求url
    url: "https://vtravel.link2shops.com/vfuliApi/api/client/ypJyActivity/goodsDetail" 
    # 请求方法
    method: "POST"
    # 自定义头
    headers: 
      Content-Type: "application/json;charset=UTF-8"
    # 自定义post数据
    data: 
      goodsId: "b2e55c4df58245d2a133929198b19f09"
      activityId: "c34758ef34bd4970bfbf7fcb9159f420"
      channelId: "5d85806e97454f78a0ea81c370a105e6"
    # 如果是json 则是jsonpath-ng 解析的json库存路径
    # 如果是html 则是BeautifulSoup 进行解析
    stock_expression: "$.goodsMap.stock" 
    # bark通知标题
    title: "建行1元购"
    # bark通知内容
    message: "京东E卡已上架"
  - name: "广发里程"
    active: true
    url: "https://mall.cgbchina.com.cn/api/item/all/sku/inventory/query/113000700557181"
    method: "GET"
    headers:
      device-type: "APP"
    # get请求参数
    # params: {}
    stock_expression: "$.data.cgbSingleSkuInventoryInfoList[0].inventory"
    title: "广发里程"
    message: "东航里程已上架"