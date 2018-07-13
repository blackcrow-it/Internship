filelog = '/home/quanghung/Desktop/Internship/Ex5/var/log/nghttp2/access.log'
list_ssl_protocol = []
list_ssl_cipher = []
with open(filelog) as f:
    lines = f.readlines()
    for i in lines:
        ssl_cipher = i.split(' ')
        list_ssl_protocol.append(ssl_cipher[3])
        list_ssl_cipher.append(ssl_cipher[4].replace('\n',''))
    count_ssl_cipher = len(list(set(list_ssl_cipher)))
    count_ssl_protocol = len(list(set(list_ssl_protocol)))
    ratio = float(count_ssl_protocol) / float(count_ssl_cipher)
    print str(int(ratio*100))+"%"

  