## 通信模块

### server.py

  1. 服务器对小车终端一对多多播通信的发送模块
  2. 小车对服务器多对一TCP多线程通信的接受模块
  3. 通信模块与数据库进行数据交换
  4. 目前通过轮询获取数据库内命令变更以进行发送，或需优化为监听

接口如下：
```
server.runSendService()
server.runReceiveService()
```

### client.py

  1. 服务器对小车终端一对多多播通信的接收模块
  2. 小车对服务器多对一TCP多线程通信的发送模块
  3. 通信模块与小车进行数据交换的模块（待完善）考虑通过文件读写

接口如下：
```
client.run()
client.send(dict data)
```


### 待完善模块
```
#server.py
	#监听数据库变化并读取数据进行发送
    #flag 需要定义
    flag = True
    while flag :
    	data = __fetchDataFromSql()
    	__sendData(s, bytes(data, encoding = 'utf8'))

```
```
#client.py
def __dataProcessing(string data)
```
