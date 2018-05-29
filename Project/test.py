import os
import re
import time
from time import gmtime, strftime

def split_file_log(keyword, access_file, temp_file):
	command = 'grep -e "' + keyword + '" ' + access_file + " > " + temp_file
	# print command
	os.system(command)

def get_time(access_file):
	file = open(access_file, 'r')
	lines = file.readlines()
	list_time = []
	for i in lines:
		i = i.split('"')
		time = i[0].split(' ')[3] + " " + i[0].split(' ')[4]
		list_time.append(time[1:-9])
	file.close()
	return list(sorted(set(list_time)))

def get_list_ip(content):
    regex_ip = "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    ips = re.findall(regex_ip, content)
    return ips

def check_ip(list_ips, per_second):
	list_ip_block = []
	for i in list(set(list_ips)):
		# list_ips.count(i)
		if list_ips.count(i) > per_second:
			# print i
			# print "="
			# print list_ips.count(i)
			list_ip_block.append(i)
	return list_ip_block

def get_list_bot_ip():
	split_file_log(BOT_STRING, TEMP_FILE, BOT_FILE)
	file = open(BOT_FILE, 'r')
	content = file.read()
	list_bot_ip = get_list_ip(content)
	file.close()
	return list(set(list_bot_ip))

def check_bot(ip):
    command = 'host ' + ip + ' | grep "' + BOT_DOMAIN + '"'
    code = os.system(command)
    return code

def get_time_now():
	return strftime("%Y-%m-%d %H:%M:%S", gmtime())
	
def import_to_iptables(ip):
	command = 'iptables -A INPUT -s ' + ip + \
		' -j DROP -m comment --comment "blocked from: '\
		+ get_time_now() + '"'
	# os.system(command)
	print command

def main():
	list_ips_block = []
	list_ips_bot = []
	list_ips_bot_real = []
	list_ips_bot_fake = []
	list_ips_blocked = []
	for i in get_time(LOG_FILE):
		split_file_log(i, LOG_FILE, TEMP_FILE)
		file = open(TEMP_FILE, 'r')
		content = file.read()
		list_ip = get_list_ip(content)
		# if len(check_ip(list_ip, MAX_REQUEST_PER_SECOND)):
		list_ips_block += check_ip(list_ip, MAX_REQUEST_PER_SECOND)
		list_ips_bot += get_list_bot_ip()
		for j in list_ips_bot:
			if check_bot(j) == 0:
				list_ips_bot_real.append(j)
			else:
				list_ips_bot_fake.append(j)
	list_ips_blocked = list_ips_blocked + list_ips_block
	list_ips_blocked = list_ips_blocked + list_ips_bot_fake
	print "----------------------------------------------------------"
	print "IP BLOCK:"
	print list(set(list_ips_block))
	print "----------------------------------------------------------"
	print "IP BOT REAL:"
	print list(set(list_ips_bot_real))
	print "----------------------------------------------------------"
	print "IP BOT FAKE:"
	print list(set(list_ips_bot_fake))
	print "----------------------------------------------------------"
	print "IP BLOCKED:"
	for ip in list(set(list_ips_blocked)):
		import_to_iptables(ip)

if __name__ == '__main__':
    LOG_FILE = '/mnt/d/Project/var/log/nginx/access.log'
    TEMP_FILE = '/mnt/d/Project/var/log/nginx/temp.log'
    BOT_FILE = '/mnt/d/Project/var/log/nginx/bot.log'
    BOT_STRING = 'GoogleBot\|bingbot\|Facebot'
    BOT_DOMAIN = 'google.com\|googlebot.com\|msn.net\|tfbnw.net'
    MAX_REQUEST_PER_SECOND = 120
    main()