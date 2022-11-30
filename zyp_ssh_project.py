#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2022/11/27 16:48 
# @Author : zhangyp
# @File : cy_ssh_project.py
import subprocess

import paramiko
import datetime


# ssh连接
def ssh_transport(host, username, password, port=22):
	"""
	:param host: 主机名
	:param username: 用户名
	:param password: 密码
	:param port: 端口默认22
	:return:
	"""
	transport = paramiko.Transport((host, port))
	start_time = datetime.datetime.now()
	transport.connect(username=username, password=password)

	# 声明一个sshclient实例
	ssh = paramiko.SSHClient()
	ssh._transport = transport

	conn_time = datetime.datetime.now()
	print(f"链接成功，耗时{conn_time - start_time}")
	return ssh


# =============这一段是交互命令行的，你看着用============================#
# 命令执行函数
def execute_cmd(ssh_object):
	flag = True
	while flag:
		cmd = input("请输入执行指令（若要退出远程终端请输入exit)：")
		if cmd == 'exit':
			flag = False
		conn_time = datetime.datetime.now()
		stdin, stdout, stderr = ssh_object.exec_command(cmd)
		execute_time = datetime.datetime.now()
		print(f"执行命令，耗时{execute_time - conn_time}")
		print(stdout.read().decode('utf-8'))


# windows的cmd执行函数
def run_shell(cli_str):
	"""
	:param cli_str: 命令行
	:return:
	"""
	try:
		msg = subprocess.Popen(cli_str, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
		stdout, stderr = msg.communicate()
		return stdout
	except subprocess.SubprocessError as e:
		raise str(e)


def validate_host():
	host = input("请输入远程主机名:")
	# 判断远程主机是否能连通，通过ping 3个数据据包判断
	if host:
		if run_shell(f'ping {host} -n 3').count("无法访问目标主机") == 0:
			return host
		else:
			print("输入的主机无法访问，请确认后重试")
	else:
		print("主机地址不能为空，请重新输入")


def validate_account():
	# 判断用户密码是否正确
	username = input("请输入用户名:")
	password = input("请输入密码:")
	if username == 'root' and password == 'mmc':
		print('账号正确，登录中...')
		return username, password
	elif username + password == 'root':
		print('密码不能为空！！！请重新输入')
		return False
	else:
		print("用户名或密码错误！！！请重新输入")
		return False


# main函数
def main():
	host = validate_host()
	while not host:
		host = validate_host()
	account = validate_account()
	while not account:
		account = validate_account()
	execute_cmd(ssh_transport(host, account[0], account[1]))


# =============以上是交互式命令行的，你看着用============================#

# 检查函数，你这里跟你主管确认下怎么来做断言

# 校验函数1
def check_one(ssh_conn):
	res = ssh_conn.exec_command("cat/etc/passwd")  # 这里写执行命令
	# 检查点1，根据情况编写校验规则
	if res.count('PASS_MAX_DAYS=90') == 1:
		print("生命期最大为90天")  # 直接打印出来
	else:
		print("校验失败")


# 校验函数2

def check_two(ssh_conn):
	pass


# 这里可以继续判断


# 这里开始是写死的
def check_linux_stand():
	# 连接服务器
	# ssh_conn = ssh_transport(host='192.168.96.63', username='root', password='qtec@123')
	ssh_conn = ssh_transport(host='192.168.1.241', username='root', password='mmc')
	# 执行指令
	check_one(ssh_conn)
	check_two(ssh_conn)
	# 关闭服务器连接
	ssh_conn.close()


if __name__ == '__main__':
	# main()
	check_linux_stand()
