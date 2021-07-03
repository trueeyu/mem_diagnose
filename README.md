一个简单的 DorisDB 内存工具，用于获取 DorisDB 的当前内存使用状态，用于分析内存问题

## 使用方法

修改配置文件 config.ini

```
fe_ip: fe 的 ip
fe_port: fe 的查询端口号
user: 用户名
password: 密码
```

执行

```
python3 main.py
```

获取的信息，放在 output 目录下
