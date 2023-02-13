#ci-plugin-demo

## demo 描述
此项目为 CI 自定义插件的一个 demo，希望通过此 demo 可以让开发者更好理解如何开发一个自定义插件。 关于插件开发的详细文档，可参考 [自定义插件开发指引](https://help.coding.net/docs/ci/plugins/customize/develop.html)


### 插件结构
当前插件的核心文件结构如下
```
- /
  - qciplugin.yml    # 插件格式声明文件
  - run.sh           # 插件逻辑实现
```

特别备注
- `qciplugin.yml` 文件名不可变，插件系统会以此名字进行插件解析和执行
- `run.sh` 文件名、存放路径、实现语言不限，用户可以根据插件逻辑复杂度和开发习惯，使用任意实现和逻辑组织方式完成插件逻辑封装。

当前 demo 依赖两个外部输入参数，其中 `name` 必填。在执行时，插件系统会将用户输入的变量，传入到 run.sh 脚本中
```yaml
# 声明插件使用的参数
variables:
  - name: name
    type: text
    label: 姓名
    help: 请输入您想要打招呼的对象
    required: true
  - name: greedings
    type: text
    label: 欢迎语
    help: 请输入您想要打招呼的欢迎语

# 执行入口配置, 声明如何运行插件脚本
entry:
  # 插件启动入口
  start: $QCI_PLUGIN_RUNTIME $QCI_PLUGIN_RUNTIME/run.py $name $greedings
```

`run.sh` 脚本逻辑非常简单，echo 传入的姓名和欢迎语
```bash
#!/bin/sh
# run.sh --name XXXX --greedings XXX

echo $@

name=$2
greedings=$4

[ -z "$greedings" ] && { echo "Hi ${name}"; } || { echo "Hi ${name}, ${greedings}"; }
```


### 插件使用
将此插件在团队插件管理页面注册后，用户就可以在流水线编排页面添加步骤时，在指定的插件分类下看到当前这个插件  
![插件列表](./_static/plugin-list.png)

选择此插件后，在右侧的插件表单里可以看到前端会根据 variables 声明自动生成了表单，表单中有两项参数，其中 `姓名` 参数必填而 `欢迎语` 参数非必填  
![插件表单](./_static/plugin-form.png)

填写表单参数后，保存并执行，可以在流水线执行结果页面看到对应的运行结果  
![插件结果](./_static/plugin-result.png)


## 插件帮助文档
为方便插件的使用者更好的理解此插件的作用和使用方式，我们推荐插件开发者在上传插件后，也能在插件详情页面编辑插件文档，提供更详细的指引信息  
![插件描述](./_static/plugin-description.png)

我们推荐的插件使用文档结构如下：

### 1. 插件介绍
介绍当前插件的主要功能是什么，使用什么场景，可以达到什么效果

### 2. 插件使用依赖
如果使用此插件前需要依赖其他外部资源（例如先注册某个凭据、先创建某个仓库等），可在此特殊声明

### 3. 插件使用方式
介绍当前插件的输入参数，并提供图形化及文本编辑模式下的配置 demo

### 4. 插件返回声明
描述插件在正常执行或异常执行时，会提供什么输出及提示，包括且不限于：`动态环境变量`、`制品`， `报告或链接`

### 5. 插件维护人
如当前插件仅在自己团队用，维护人可以细到具体的人员，方便团队内咨询沟通；如果当前插件计划公开，建议维护人填写为 当前团队 + 人员信息