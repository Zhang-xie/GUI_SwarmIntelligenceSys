## 通信模块

### server.py

整合了
  1. 服务器对小车终端一对多多播通信的发送模块
  2. 小车对服务器多对一TCP多线程通信的接受模块
  3. 通信模块与数据库进行数据交换的模块（待完善）

接口如下：
```
server.runSendService()
server.runReceiveService()
```

### client.py

整合了
  1. 服务器对小车终端一对多多播通信的接收模块
  2. 小车对服务器多对一TCP多线程通信的发送模块
  3. 通信模块与小车进行数据交换的模块（待完善）

接口如下：
```
client.run()
client.send(dict data)
```
### testClient.py

测试用客户端main文件（待完善）

### 待完善模块
```
#server.py
# 从数据库获取最新数据
def __acquireDataFromSql() :
    return data
# 监听数据库变化并读取数据进行发送
def __listenDatabase() :
    """
    监听数据库变化
    """
    return __acquireDataFromSql
```
```
#client.py
def __dataProcessing(string data) :
```
