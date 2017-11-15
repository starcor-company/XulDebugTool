# coding: utf-8
from XulDebugTool.logcatapi.Logcat import STCLogger
# 以下是日志模块基本类型调用接口
# 如果后期有跟多类型日志类型，将考虑更加具有扩展性的接口

STCLogger("TAG").i("这是一个info信息","你可以在后面加任意类型，任意数量的信息",{"1":"mke"},(1,2,3,4))

STCLogger("TAG").w("这是一个warning信息","你可以在后面加任意类型，任意数量的信息",{"1":"mke","rytu":"chaili"},(1,2,3,4))

STCLogger("TAG").e("这是一个error信息","你可以在后面加任意类型，任意数量的信息")

STCLogger("TAG").c("这是一个critical信息","你可以在后面加任意类型，任意数量的信息")

STCLogger("TAG").d("这是一个debug信息","你可以在后面加任意类型，任意数量的信息")

