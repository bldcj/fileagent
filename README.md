# fileagent

基于[Dify](https://github.com/langgenius/dify)构建的文件管理agent

## 目录

- [fileagent](#fileagent)
  - [目录](#目录)
  - [安装](#安装)
    - [文件服务端](#文件服务端)
    - [webUI](#webui)
    - [Dify API](#dify-api)
    - [ollama（非必需）](#ollama非必需)
  - [用法](#用法)
    - [启动Dify](#启动dify)
    - [启动文件服务端](#启动文件服务端)
    - [启动webUI](#启动webui)
    - [使用webUI](#使用webui)
  - [文件和目录结构](#文件和目录结构)
    - [/py](#py)
    - [/js](#js)
      - [/src](#src)
  - [文件服务端API](#文件服务端api)
    - [获取文件列表](#获取文件列表)
      - [请求信息](#请求信息)
      - [请求参数](#请求参数)
      - [请求示例](#请求示例)
      - [响应示例](#响应示例)
    - [获取或切换当前目录](#获取或切换当前目录)
      - [请求信息](#请求信息-1)
      - [请求参数](#请求参数-1)
      - [请求示例](#请求示例-1)
      - [响应示例](#响应示例-1)
    - [新建文件夹](#新建文件夹)
      - [请求信息](#请求信息-2)
      - [请求参数](#请求参数-2)
      - [请求示例](#请求示例-2)
      - [响应示例](#响应示例-2)
    - [删除文件或文件夹](#删除文件或文件夹)
      - [请求信息](#请求信息-3)
      - [请求参数](#请求参数-3)
      - [请求示例](#请求示例-3)
      - [响应示例](#响应示例-3)
    - [重命名](#重命名)
      - [请求信息](#请求信息-4)
      - [请求参数](#请求参数-4)
      - [请求示例](#请求示例-4)
      - [响应示例](#响应示例-4)
    - [复制](#复制)
      - [请求信息](#请求信息-5)
      - [请求参数](#请求参数-5)
      - [请求示例](#请求示例-5)
      - [响应示例](#响应示例-5)
    - [剪切](#剪切)
      - [请求信息](#请求信息-6)
      - [请求参数](#请求参数-6)
      - [请求示例](#请求示例-6)
      - [响应示例](#响应示例-6)
    - [获取文件信息](#获取文件信息)
      - [请求信息](#请求信息-7)
      - [请求参数](#请求参数-7)
      - [请求示例](#请求示例-7)
      - [响应示例](#响应示例-7)
    - [提取文本](#提取文本)
      - [请求信息](#请求信息-8)
      - [请求参数](#请求参数-8)
      - [请求示例](#请求示例-8)
      - [响应示例](#响应示例-8)
    - [存储关键词](#存储关键词)
      - [请求信息](#请求信息-9)
      - [请求参数](#请求参数-9)
      - [请求示例](#请求示例-9)
      - [响应示例](#响应示例-9)
    - [保存设置](#保存设置)
      - [请求信息](#请求信息-10)
      - [请求参数](#请求参数-10)
      - [请求示例](#请求示例-10)
      - [响应示例](#响应示例-10)
    - [读取设置](#读取设置)
      - [请求信息](#请求信息-11)
      - [无请求参数](#无请求参数)
      - [请求示例](#请求示例-11)
      - [响应示例](#响应示例-11)
    - [读取历史目录](#读取历史目录)
      - [请求信息](#请求信息-12)
      - [无请求参数](#无请求参数-1)
      - [请求示例](#请求示例-12)
      - [响应示例](#响应示例-12)
  - [相关项目](#相关项目)

## 安装

请先安装并配置好python、node.js、docker，然后运行
`git clone https://github.com/bldcj/fileagent.git`

### 文件服务端
`cd fileagent/py`
建议创建虚拟环境并激活
```bash
python -m venv .venv
.venv/Scripts/activate
```
安装依赖
`pip install -r requirements.txt`
服务端默认开放5000端口，将`py/preferences.json`中`fileAPI`的值改为`http://你的文件服务器地址:5000`

### webUI
`cd fileagent/js`
安装依赖并初始化环境
`npm install`
运行`vue ui`来启动vue web控制台进行serve或build
或是通过以下命令执行
`npm run serve`（用于开发环境）
`npm run build`（用于生产环境）
项目出现问题时使用`npm run lint`修复项目
Vue项目的具体配置详见`js/README.md`

### Dify API
Dify的安装与部署参见[Dify Docs-使用Docker Compose部署Dify](https://docs.dify.ai/zh/self-host/quick-start/docker-compose)

在dify控制台-工作室中导入`fileagent.yml`,并在控制台-工具中新建自定义工具，将`filetools.json`的内容作为api文档导入。
在模型设置中配置自己的模型api，见[Dify Docs-模型供应商](https://docs.dify.ai/zh/use-dify/workspace/model-providers)
在控制台-访问API处复制API服务器地址及api密钥，将`py/preferences.json`中的`difyAPI`项的值改为API服务器地址，`difyAPIKey`的值改为api密钥。

### ollama（非必需）
如果想要本地部署大模型，可以安装ollama，拉取所需模型，并在设置中勾选`Expose Ollama to the network`

## 用法

### 启动Dify
`docker compose up -d`

### 启动文件服务端
`cd fileagent/py`
若配置了虚拟环境则启动
`.venv/Scripts/activate`
运行服务
`python file_manager.py`

### 启动webUI
开发环境下，运行`npm run serve`即可在8080端口运行服务
生产环境下，运行`npm run build`，将`js/dist`下生成的所有文件托管到web服务器即可
第一次运行需要在webUI的设置面板中更改文件API和Dify API的地址（也可以在发行前手动更改`js/src/App.vue`中`fileAPI`和`difyAPI`的值）

### 使用webUI
在浏览器中访问webUI的链接，进入主界面
主界面分为三部分
-上方为标题栏，点击右侧按钮可以打开设置面板
-左侧为文件管理器，由可下拉选择父目录的地址栏和文件列表组成。文件管理器左侧的按钮为复制、粘贴等功能按钮
-右侧为对话区，可以在文本框内输入指令并发送，与模型对话。对话结果显示在上方的聊天窗口中。模型的部分响应会被包装为标签，点击可以展开并执行对应的文件操作。

## 文件和目录结构
|文件/目录|描述|
|---|---|
|/js|前端项目文件|
|/py|文件服务器|
|fileagent.yml|Dify项目配置文件|
|filetools.json|工具链接口定义|
|README.md|项目说明|
|提示词.txt|用于Dify项目的提示词模板|

### /py
|文件/目录|描述|
|---|---|
|file_manager.py|文件服务主程序|
|file_reader.py|文本提取接口|
|preferences.json|webUI配置文件|
|last_directory|存储目录访问历史记录|
|requirements.txt|项目依赖列表|

### /js
|文件/目录|描述|
|---|---|
|/src|源代码目录|
|/public|Vue项目公共文件（网站图标及index.html模板）
|\*.js,\*.json|node.js,Vue,babel配置文件

#### /src
|文件/目录|描述|
|---|---|
|/assets|资源文件目录|
|/components|自定义组件|
|/plugins|插件配置|
|App.vue|Vue项目主文件|
|main.js|依赖项配置和项目初始化|

## 文件服务端API

### 获取文件列表
获取指定路径的文件树。

#### 请求信息
- 方法：GET
- 路径：`/ls`
- 完整URL：`http://example.com:port/ls`

#### 请求参数
|参数名|类型|必选|说明|
|---|---|---|---|
|p|string|是|要查询的路径|

#### 请求示例
`curl -X GET http://example.com:port/ls?p=/test`

#### 响应示例
```xml
<directory path="/test">
  <folder name="folder1" time="2026-02-20 11:45:14"></folder>
  <file name="file2" time="2026-02-20 11:45:14" size="1919810" keywords="关键词1 关键词2"></file>
</directory>
```

### 获取或切换当前目录
获取当前工作目录或者切换当前工作目录，返回操作后的工作目录。

#### 请求信息
- 方法：GET
- 路径：`/cd`
- 完整URL：`http://example.com:port/cd`

#### 请求参数
|参数名|类型|必选|说明|
|---|---|---|---|
|p|string|否|要切换到的目录，缺省则返回当前工作目录|

#### 请求示例
`curl -X GET http://example.com:port/cd`
`curl -X GET http://example.com:port/cd`

#### 响应示例
`/test/folder1`

### 新建文件夹
新建一个文件夹，返回新建文件夹的文件树。

#### 请求信息
- 方法：GET
- 路径：`/mkdir`
- 完整URL：`http://example.com:port/mkdir`

#### 请求参数
|参数名|类型|必选|说明|
|---|---|---|---|
|p|string|是|新建文件夹的绝对路径|

#### 请求示例
`curl -X GET http://example.com:port/mkdir?p=/test/newfolder`

#### 响应示例
```xml
<directory path="/test/newfolder"/>
```

### 删除文件或文件夹
删除文件或文件夹，返回操作是否成功。

#### 请求信息
- 方法：GET
- 路径：`/rm`
- 完整URL：`http://example.com:port/rm`

#### 请求参数
|参数名|类型|必选|说明|
|---|---|---|---|
|p|string|是|要删除的文件或文件夹路径|

#### 请求示例
`curl -X GET http://example.com:port/rm?p=/test`

#### 响应示例
`Done.`

### 重命名
重命名文件夹或文件，返回操作是否成功。

#### 请求信息
- 方法：GET
- 路径：`/rename`
- 完整URL：`http://example.com:port/rename`

#### 请求参数
|参数名|类型|必选|说明|
|---|---|---|---|
|p|string|是|父文件夹路径|
|s|string|是|原文件名|
|d|string|是|新文件名|

#### 请求示例
`curl -X GET http://example.com:port/rename?p=/test&s=file2&d=newfilename`

#### 响应示例
`Done.`

### 复制
复制文件或文件夹到指定目录，返回操作是否成功。

#### 请求信息
- 方法：GET
- 路径：`/copy`
- 完整URL：`http://example.com:port/copy`

#### 请求参数
|参数名|类型|必选|说明|
|---|---|---|---|
|s|string|是|源文件路径|
|d|string|是|目的文件路径|

#### 请求示例
`curl -X GET http://example.com:port/copy?s=/test/folder1/file.txt&d=/test/folder2/file.txt`

#### 响应示例
`Done.`

### 剪切
剪切文件或文件夹到指定目录，返回操作是否成功。

#### 请求信息
- 方法：GET
- 路径：`/cut`
- 完整URL：`http://example.com:port/cut`

#### 请求参数
|参数名|类型|必选|说明|
|---|---|---|---|
|s|string|是|源文件路径|
|d|string|是|目的文件路径|

#### 请求示例
`curl -X GET http://example.com:port/cut?s=/test/folder1/file.txt&d=/test/folder2/file.txt`

#### 响应示例
`Done.`

### 获取文件信息
获取操作系统提供的文件信息，返回一个数组。

#### 请求信息
- 方法：GET
- 路径：`/stat`
- 完整URL：`http://example.com:port/stat`

#### 请求参数
|参数名|类型|必选|说明|
|---|---|---|---|
|p|string|是|文件或文件夹路径|

#### 请求示例
`curl -X GET http://example.com:port/stat?p=/test/file.txt`

#### 响应示例
`[33206, 1407374883777926, 199129662973451948, 1, 0, 0, 48, 1771338019, 1771061074, 1771061048]`

### 提取文本
提取指定文件的文本信息并返回（支持.txt .docx .pdf三种扩展名）

#### 请求信息
- 方法：GET
- 路径：`get-text`
- 完整URL：`http://example.com:port/get-text`

#### 请求参数
|参数名|类型|必选|说明|
|---|---|---|---|
|p|string|是|文件或文件夹路径|

#### 请求示例
`curl -X GET http://example.com:port/get-text?p=/test/file.txt`

#### 响应示例
`这是一个测试文件`

### 存储关键词
存储文件对应的关键词，返回当前目录的文件关键词表

#### 请求信息
- 方法：POST
- 路径：`store-keywords`
- 完整URL：`http://example.com:port/store-keywords`

#### 请求参数
|参数名|类型|必选|说明|
|---|---|---|---|
|p|string|是|文件路径|
|keywords|string|是|存储了关键词的json字符串|

#### 请求示例
```bash
curl -X POST -H "Content-Type:application/json" \
-d '{"keywords":["keywords1","keywords2"]}' \
http://example.com:port/store-keywords?p=/test/file1.txt
```

#### 响应示例
```json
{
  "file1.txt":{
    "keywords":["keywords1","keywords2"]
  },
  "file2.txt":{
    "keywords":["关键词1","关键词2"]
  }
}
```

### 保存设置
保存webUI配置文件。

#### 请求信息
- 方法：POST
- 路径：`/preferences/set`
- 完整URL：`http://example.com:port/preferences/set`

#### 请求参数
|参数名|类型|必选|说明|
|---|---|---|---|
|preferences|string|是|各项设置的值|

#### 请求示例
```bash
curl -X POST -H "Content-Type:application/json" \
-d '{"fileAPI": "","difyAPI": "","difyAPIKey":"","rememberPath": false,"defaultPath": "D:\\","depth": 0,"keywordsNumber": 3}' \
http://example.com:port/preferences/set
```

#### 响应示例
```json
{
    "fileAPI": "",
    "difyAPI": "",
    "difyAPIKey":"",
    "rememberPath": false,
    "defaultPath": "D:\\",
    "depth": 0,
    "keywordsNumber": 3
}
```

### 读取设置
读取webUI配置文件。

#### 请求信息
- 方法：GET
- 路径：`/preferences/get`
- 完整URL：`http://example.com:port/preferences/get`

#### 无请求参数

#### 请求示例
```bash
curl -X GET http://example.com:port/preferences/get
```

#### 响应示例
```json
{
    "fileAPI": "",
    "difyAPI": "",
    "difyAPIKey":"",
    "rememberPath": false,
    "defaultPath": "D:\\",
    "depth": 0,
    "keywordsNumber": 3
}
```

### 读取历史目录
读取最近一次访问的目录

#### 请求信息
- 方法：GET
- 路径：`/lastdir`
- 完整URL：`http://example.com:port/lastdir`

#### 无请求参数

#### 请求示例
```bash
curl -X GET http://example.com:port/lastdir
```

#### 响应示例
`/test`

## 相关项目
[Dify](https://github.com/langgenius/dify)
[Ollama](https://github.com/ollama/ollama)
[flask](https://github.com/pallets/flask)
[Vue](https://github.com/vuejs/core)
[Vuetify](https://github.com/vuetifyjs/vuetify)
[axios](https://github.com/axios/axios)
[fetch-event-source](https://github.com/Azure/fetch-event-source)