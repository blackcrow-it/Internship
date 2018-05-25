import httpagentparser
filepath = 'access.log'
common = ''
with open(filepath) as fp:
	lines = fp.readlines()
	for i in lines:
		i = i.split('"')
		host = i[0].split(' ')[0]
		time = i[0].split(' ')[3] + " " + i[0].split(' ')[4]
		get = i[1]
		status = i[2].split(' ')[1]
		size = i[2].split(' ')[2]
		user_agent = i[5]
		frank = i[3]
		common = host + ' ' + '"' +user_agent+ '"' + ' ' + '"' +frank+ '"' + ' ' + time + ' ' + '"' +get+ '"' + ' ' + status + ' ' + size +'\n'
		print common
		
