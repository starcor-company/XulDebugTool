# xul-debugtool
## 一、连接页面功能
### 1.下拉框可输入ip：port（例如：172.31.11.56:55550）

### 2.展开下拉框，可以选择最近连接的设备

### 3.点击connect按钮，连接设备进入主页面

### 4.点击detail按钮，展示连接日志

![点击连接按钮连接设备](https://github.com/starcor-company/XulDebugTool/blob/logcatapi/resources/readme/connect.png)<br/>

## 二、主页功能
### 1.菜单栏功能
##### （1）file：选中file，单击鼠标右键，选择disconnect，此功能为退出连接，返回到连接页面

##### （2）edit：选中edit，单击鼠标右键，选择find，此功能为查找中部内容区域关键字

##### （3）help：选中help，单击鼠标右键，选择about，此功能为弹出XulDebugTool此款app的简介
![菜单栏展示](https://github.com/starcor-company/XulDebugTool/blob/logcatapi/resources/readme/main_menu.png)<br/>

### 2.左侧列表
##### （1）页面（page）：读取页面以列表形式展示在左侧列表区域

##### （2）用户数据（user-object）：BitmapCache（缓存图片）、DataService（provider）、插件管理器（PluginManager）等用户数据列表

##### （3）插件页面列表（暂未实现）

##### （4）选中左侧列表元素，单击鼠标右键，可以进行选中项名称复制（copy）；还可对provider的数据进行请求（qury-data），查找过的provider会被保存到右侧Faviorities的History中
![provider数据请求](https://github.com/starcor-company/XulDebugTool/blob/logcatapi/resources/readme/main_provider.png)<br/>

### 3.中部内容区域
##### （1）搜索功能：点击菜单栏的edit->find（或者快捷键ctrl + f）,可以呼出搜索框，输入关键字进行搜索

##### （2）筛选功能：搜索框上方是对展示的数据进行筛选（skip-prop：不展示属性、with-children：展示子元素、with-binding-data:展示绑定数据、with-position:展示元素位置信息）

##### （3）元素id可点击，点击后可在右侧进行元素属性和样式设置
![中部内容展示](https://github.com/starcor-company/XulDebugTool/blob/logcatapi/resources/readme/main_search.png)<br/>

### 4.右侧列表
##### （1）右侧的Property展示的是属性和样式，属性和样式修改方式：在中部内容区域点击想要改变属性的元素id，在右侧对其属性和样式进行修改（key和value均可修改）

##### （2）右侧的Favorities展示的是操作过的provider的历史记录和收藏，provider的数据请求方式：选中左侧列表元素，单击鼠标右键，对provider的数据进行请求（qury-data），此时会弹出一个data-qury的对话框，在where列填入请求参数key，在is列填入对应值，点击request金字那个查找，结果显示在中部内容区域，查找过的provider会被保存到右侧Faviorities的History中。

##### （3）provider收藏功能：选中右侧Favorities->History,选中想要收藏的provider，单击鼠标右键，选择收藏，此时，收藏过的provider会出现在History上面的Favorites列表中
![右侧内容展示](https://github.com/starcor-company/XulDebugTool/blob/logcatapi/resources/readme/main_provider.png)<br/>

### 4.底部日志输出
##### （1）日志输出框，输出调试工具运行日志，方便开发人员查看问题

##### （2）点击垃圾桶图标，清空日志
![右侧内容展示](https://github.com/starcor-company/XulDebugTool/blob/logcatapi/resources/readme/logcat.png)<br/>
