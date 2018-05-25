import httpagentparser
filepath = 'gistfile1.txt'
list_browser = []
dict_browser = {}
with open(filepath) as fp:  
	line = fp.readlines()
	for i in line:
		i = i.split('"')
		a = httpagentparser.simple_detect(i[5])
		b = a[1].split(' ')
		list_browser.append(b[0])
	c = list(set(list_browser))
	for j in c:
		count_browser = float(list_browser.count(j))
		sum_browser = len(list_browser)
		scale = (count_browser/sum_browser)*100
		dict_browser[j] = str(round(scale,2)) + " %"
		print j + ':' + ' ' + str(round(scale,2)) + " %"
	# print dict_browser