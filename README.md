网上找的一些免费接口,用unittest搭建自动化接口测试框架

1.环境

1.1 ubuntu18.04LST

1.2 windowns 10

1.3 安装依赖

pip install -r requirements.txt -i https://pypi.douban.com/simple/

2.运行

python runall.py

3.配置

配置文件在config有详细说明

4.添加测试用例

在files文件夹放入以.xls为后缀的接口测试文档,文档架构参考APi.xls,如需更改,请自行修改

在testapi.py添加如下方法

def test_03(self):
    NONE = self.Request()
    self.assertIsNotNone(NONE)

意思是执行文档里第三条测试用例

可以在Request里面填入需要关注的参数例如:

def test_03(self):
    NONE = self.Request({'id':1})
    self.assertIsNotNone(NONE)

5.项目待改进的地方:

5.1项目只是在百度上搜索的免费接口,没找到注册登陆接口(已找到50多的接口)

5.2一次只能运行一张表里的测试用例,待改进

5.3无法在windowns运行,待改进(已解决)

5.4还没把Request改成公共方法,待改进(已修改)

5.5测试用例无法使用@unittest.skip直接跳过,待改进

5.6没有发送邮件功能,待添加

5.7还没写保持会话的公共方法,待添加ls


5.8日志文件重复打印待修改(控制台打印没什么问题)

6.其他说明

6.1关注参数优先级

文档里的响应参数为最高优先级,当此参数有值,其他参数值将无视

self.Request里的参数为第二优先级

config.RESPONSE_MESSAGE里为最次级优先级,当此处有值将会关注所有的用例是否有这参数

此三处都无值将会以响应码200,响应时间是否超过期望值来判断接口是否通过

6.2不定期更新

6.3项目目录

6.3.1

Commom:公共方法

config:配置(里面有详细的说明)

files:存放测试用例.xls后缀

log:生成的日志存放的目录

report:测试报告存放的目录

testcase:测试用例

runall:运行文件
