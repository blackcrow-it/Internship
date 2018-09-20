import dns.resolver
check = 0
try:
    a = dns.resolver.query("cdn.spro.vn", "CNAME")
    for i in a:
        print i
    check = 1
except:
    a = dns.resolver.query("cdn.spro.vn", "A")
    for i in a:
        print i
    check = 0
print check
# domain = "https://google.com"
# dns = domain[domain.find('//')+2:]
# print dns