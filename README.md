<table>
  <tr>
    <th>日期</th>
    <th>功能点</th>
    <th>版本号</th>
  </tr>
  <tr>
    <th>2017.11.30</th>
    <th>基础功能见下文</th>
    <th>1.0</th>
  </tr>
  <tr>
    <th>2018.02.09</th>
    <th>1.日志路径选择 2.设置焦点元素 3.历史记录的批量删除 4.触发元素事件 5.清缓存--菜单</th>
    <th>1.1</th>
  </tr>
</table>

# xul-debugtool
## 一、项目资料
### 1.[项目整体流程](http://github.com/starcor-company/XulDebugTool/blob/README/doc/design/flow.puml)<br/>

### 2.[项目设计图](https://github.com/starcor-company/XulDebugTool/blob/README/doc/design/%E8%AE%BE%E8%AE%A1%E5%9B%BE.png)<br/>

### 3.[项目使用指令说明](https://github.com/starcor-company/XulDebugTool/blob/README/doc/debug%20instruction.txt)<br/>

### 4.[项目预期功能列表](https://github.com/starcor-company/XulDebugTool/blob/README/doc/%E5%8A%9F%E8%83%BD%E5%88%97%E8%A1%A8.txt)<br/>

## 二、使用方法
### 1、连接页面功能
#### （1）下拉框可输入ip：adbport:xulport（例如：172.31.11.56:55550:55550）,如示例，ip为所连接设备的ip地址，adbport为adb的端口号，xulport为所调试的apk的xul调试端口，两种端口号都可省略，省略adb端口号格式（ip：:xulport）

#### （2）展开下拉框，可以选择最近连接的设备

#### （3）点击connect按钮，连接设备进入主页面

#### （4）点击detail按钮，展示连接日志

![点击连接按钮连接设备](https://github.com/starcor-company/XulDebugTool/blob/master/resources/readme/connect.png)<br/>

### 2、主页功能
#### （1）菜单栏功能
* file：选中file，单击鼠标右键：（1）Disconnect（退出连接）；（2）ClearCache（清除缓存）；（3）LogPath（设置日志输出路径）

* edit：选中edit，单击鼠标右键：（1）find（查找中部内容区域关键字）；（2）Focus Item（设置焦点元素）

* help：选中help，单击鼠标右键，选择about，此功能为弹出XulDebugTool此款app的简介
![ClearCache And LogPath](https://github.com/starcor-company/XulDebugTool/blob/master/resources/readme/log_path.png)<br/>
![Focus Item](https://github.com/starcor-company/XulDebugTool/blob/master/resources/readme/get_focus.png)<br/>

#### （2）左侧列表
* 页面（page）：读取页面以列表形式展示在左侧列表区域

* 用户数据（user-object）：BitmapCache（缓存图片）、DataService（provider）、插件管理器（PluginManager）等用户数据列表

* 插件页面列表（暂未实现）

* 选中左侧列表元素，单击鼠标右键，可以进行选中项名称复制（copy）；还可对provider的数据进行请求（qury-data），查找过的provider会被保存到右侧Faviorities的History中
![provider数据请求](https://github.com/starcor-company/XulDebugTool/blob/master/resources/readme/querydata.png)<br/>

#### （3）中部内容区域
* 搜索功能：点击菜单栏的edit->find（或者快捷键ctrl + f）,可以呼出搜索框，输入关键字进行搜索

* 筛选功能：搜索框上方是对展示的数据进行筛选（skip-prop：不展示属性、with-children：展示子元素、with-binding-data:展示绑定数据、with-position:展示元素位置信息）

* 元素id可点击，点击后可在右侧进行元素属性和样式设置

* 触发元素事件（列表列出事件为布局文件已有的事件）
![触发元素事件](https://github.com/starcor-company/XulDebugTool/blob/master/resources/readme/action_excute.png)<br/>

#### （4）右侧列表
* 右侧的Property展示的是属性和样式，属性和样式修改方式：在中部内容区域点击想要改变属性的元素id，在右侧对其属性和样式进行修改（key和value均可修改）

* 右侧的Favorities展示的是操作过的provider的历史记录和收藏，provider的数据请求方式：选中左侧列表元素，单击鼠标右键，对provider的数据进行请求（qury-data），此时会弹出一个data-qury的对话框，在where列填入请求参数key，在is列填入对应值，点击request金字那个查找，结果显示在中部内容区域，查找过的provider会被保存到右侧Faviorities的History中。

* provider收藏功能：选中右侧Favorities->History,选中想要收藏的provider，单击鼠标右键，选择收藏，此时，收藏过的provider会出现在History上面的Favorites列表中

* 批量删除记录
![批量删除](https://github.com/starcor-company/XulDebugTool/blob/master/resources/readme/multiple_del.png)<br/>

#### （5）底部日志输出
* 日志输出框，输出调试工具运行日志，方便开发人员查看问题

* 点击垃圾桶图标，清空日志

## 三、注意事项
### 1.使用之前请检查检查设备是否支持adb

### 2.使用之前请检查所调试apk是否支持XUL调试

## 四、TODO
### 1.完善日志窗口搜索关键字功能

### 2.实现新增元素属性和样式的功能

