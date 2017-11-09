# coding: utf-8
from XulDebugTool.logcatapi.Logcat import STCLogger
# 以下是日志模块基本类型调用接口
# 如果后期有跟多类型日志类型，将考虑更加具有扩展性的接口

STCLogger("TAG").info("一个info信息")

STCLogger("TAG").warning("一个warning信息")

STCLogger("TAG").error("这是一个error信息")

# STCLogger("TAG").request("url地址") 也可这样调用
STCLogger("TAG").request("url地址", "附加信息")

# STCLogger("TAG").response("url地址") 也可这样调用
STCLogger("TAG").response("url地址" "附加信息")

# STCLogger("TAG").adb("adb命令") 也可这样调用
STCLogger("TAG").adb("adb命令", "附加信息")
