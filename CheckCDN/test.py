import requests
def get_link(type1 , type2, link_resources, list_link):
    i = 0
    for y in link_resources:
        if (type1 in y or type2 in y):
            bool_http = y.find('http://') >= 0
            bool_https = y.find('https://') >= 0
            bool_htm = y.find('.htm') < 0
            if (bool_https == True or bool_http == True):
                list_link.append(y)
            i += 1
            if i >= 5:
                break
def get_cdn(list_link, list_cdn):
    for z in list_link:
        z_page = requests.get(z)
        z_tree = z_page.headers.get('server') 
        list_cdn.append(z_tree)
def get_result(list_cdn, list_result, list_server):
    for a in list_cdn:
        if a not in list_server:
            list_result.append(a)
def format_cdn(list_cdn):
    dict_format = {'cloudflare': 'Cloud Flare CDN', 'NetDNA-cache/2.2': 'MaxCDN', "yunjiasu": "Yunjiasu", "ECS": "Edgecast", "NetDNA": "NetDNA"}
    for key, value in dict_format.items():
        list_cdn = [x.replace(key, value) for x in list_cdn]
    return list_cdn