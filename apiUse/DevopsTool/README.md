# DevopsTool

## 概览

Anker Devops 建设需要的一系列自动化工具合集

## 使用说明

### 依赖安装
> 请先安装 python3.6 及以上版本 

```
pip3 install jinja2
```

### 应用说明

#### 检查代码仓库配置
* 应用概述：以邮件方式发送当前用户可以看到的coding代码仓不符合配置规范的列表
* 调用方式：
```
    cd apps/checkDepotSetting
    python3 main.py --token <Coding Token> --emails <Email Address1>,<Email Address2>
```
* 参数说明：
```
Coding Token: Coding API调用令牌，获取方式 Coding头像-个人账户设置-访问令牌
Email Address：邮件发送地址，多个地址用英文逗号分隔
```

## 其他
* 邮件发送的公共邮箱 ap-devops@anker-in.com