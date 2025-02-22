# 夸克自动签到

## 配置

抓包流程：
【手机端】

1. 打开抓包，手机端访问签到页
2. 找到域名 https://drive-m.quark.cn 的请求信息
3. 复制url后面的参数: kps sign vcode并设置到config.json内部的对应字段中

## 参考开源项目

[Auto_Check_In](https://github.com/BNDou/Auto_Check_In/blob/main/checkIn_Quark.py)