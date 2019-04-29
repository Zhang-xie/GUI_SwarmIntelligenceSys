## 通信模块

### server.py

  1. 服务器对小车终端一对多多播通信的发送模块
  2. 小车对服务器多对一TCP多线程通信的接受模块
  3. 通信模块与数据库进行数据交换
  
  4. 新增小车历史轨迹上传

接口如下：
```
server.runSendService()
server.runReceiveService()
```

### client.py

  1. 服务器对小车终端一对多多播通信的接收模块
  2. 小车对服务器多对一TCP多线程通信的发送模块
  3. 通信模块与小车进行数据交换的模块

  4. 新增小车历史轨迹上传（使用相同接口）

接口如下：
```
Car_socket_client()
Car_socket_client().send(dict data)
Car_socket_client().send(list<dict> data)
```

### 迭代方向
  1. 考虑将文件传输格式从json转变为bytes，手动完成编码解码，以加快传输速率
  2. 目前通过轮询获取数据库内命令变更以进行发送，或需优化为监听
