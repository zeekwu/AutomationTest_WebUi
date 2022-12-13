#-*- coding:utf8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo
from common.dateTimeTool import DateTimeTool
from common.pytest import deal_pytest_ini_file
from init.api.api_init import api_init
from init.java.java_maven_init import java_maven_init
from init.httpserver.http_server_init import http_server_init
import argparse
import pytest
import sys

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('-k','--keyword',help='只执行匹配关键字的用例，会匹配文件名、类名、方法名',type=str)
    parser.add_argument('-d','--dir',help='指定要测试的目录',type=str)
    parser.add_argument('-m','--markexpr',help='只运行符合给定的mark表达式的测试',type=str)
    parser.add_argument('-s', '--capture', help='是否在标准输出流中输出日志,1:是、0:否,默认为0',type=str)
    parser.add_argument('-r', '--reruns', help='失败重跑次数,默认为0',type=str)
    parser.add_argument('-lf', '--lf', help='是否运行上一次失败的用例,1:是、0:否,默认为0',type=str)
    parser.add_argument('-clr', '--clr', help='是否清空已有测试结果,1:是、0:否,默认为0', type=str)
    args=parser.parse_args()

    # 处理pytest文件
    deal_pytest_ini_file()

    # 初始化java依赖的libs
    java_maven_init()

    # 初始化
    print('%s开始初始化......'%DateTimeTool.getNowTime())
    api_init()
    print('%s初始化完成......'%DateTimeTool.getNowTime())

    # 执行pytest前的参数准备
    pytest_execute_params=['-c', 'config/pytest.ini', '-v', '--alluredir', 'output/api/report_data/']
    # 判断目录参数
    dir = 'cases/api/'
    if args.dir:
        dir=args.dir
    # 判断关键字参数
    if args.keyword:
        pytest_execute_params.append('-k')
        pytest_execute_params.append(args.keyword)
    # 判断markexpr参数
    if args.markexpr:
        pytest_execute_params.append('-m')
        pytest_execute_params.append(args.markexpr)
    # 判断是否输出日志
    if args.capture:
        if int(args.capture):
            pytest_execute_params.append('-s')
    # 判断是否失败重跑
    if args.reruns:
        if int(args.reruns):
            pytest_execute_params.append('--reruns')
            pytest_execute_params.append(args.reruns)
    # 判断是否只运行上一次失败的用例
    if args.lf:
        if int(args.lf):
            pytest_execute_params.append('--lf')
    # 判断是否清空已有测试结果
    if args.clr:
        if int(args.clr):
            pytest_execute_params.append('--clean-alluredir')
    pytest_execute_params.append(dir)

    print('%s开始测试......'%DateTimeTool.getNowTime())
    exit_code=pytest.main(pytest_execute_params)