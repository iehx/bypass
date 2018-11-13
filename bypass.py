# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division

import requests, urllib, urlparse, re ,sys

url = 'https://doub.io/sszhfx/'
url1 = 'https://www.microsofttranslator.com/bv.aspx'
url2 = ''
url3 = ''
dict_head = {
			'Connection': 'keep-alive',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',
			'Accept': 'application/x-ms-application, image/jpeg, application/xaml+xml, image/gif, image/pjpeg, application/x-ms-xbap, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'en-us',
			}

def main():
    # url_quote=urllib.quote(url,safe='')
    # print(url_quote)
    dict_request1 = {}
    dict_request2 = {}
    dict_request3 = {}
    dict_request1['a'] = url
    dict_request1['from'] = "zh-CHS"
    dict_request1['to'] = "zh-CHT"
    s1 = requests.Session()
    # url1_result = http.request('GET',url1,headers = dict_head)
    url1_result = s1.get(url1,params = dict_request1,headers = dict_head, verify=False)
    print(url1_result.url)
    str_re1 = str(url1_result.text).replace("\r",'').replace("\n",'').replace("\t",'')
    with open(r"D:\temp1.txt",'w') as fp:
        fp.write(str_re1)
    p = re.search(r"BV.InitRoot\(\s*'(.*?)',\s*'(.*?)',\s*'(.*?)',\s*'(.*?)',\s*'(.*?)',\s*'(.*?)',\s*'(.*?)',\s*'(.*?)',\s*'(.*?)',\s*'(.*?)',\s*(.*?),\s*(.*?),\s*'(.*?)',\s*'(.*?)'",str_re1)
    if p is not None:
        url2 = eval("'{}'".format(p.group(2)))
        url3 = urlparse.urljoin(url2,"proxy.ashx")
        dict_request3["from"] = p.group(4)
        dict_request3["to"] = p.group(5)
        dict_request3["csId"] = p.group(6)
        dict_request3["usId"] = p.group(7)
        dict_request3["ac"] = 'true'
        dict_request3["bvrpx"] = 'true'
        dict_request3["bvrpp"] = ''
        dict_request3["dt"] = eval("'{}'".format(p.group(13)))
        dict_request3["h"] = p.group(14)
        dict_request3["a"] = url

    else:
        print("Error!The url1 parameter can not be found!")
        return None
    print(url3)
    print(dict_request3)
    
    # s2 = requests.Session()
    #第二步
    # dict_head['Referer'] = url1_result.url
    # url2_result = s2.get(url2,params = dict_request2,headers = dict_head, verify=False)
    # with open(r"D:\temp2.txt",'w') as fp:
        # fp.write(str(url2_result.text))
    # p = re.search(r"BV.Init\(*.'(.*)',*.'(.*)',*.'(.*)'\)",str(url2_result.text))
    # dict_request3 = {}
    # if p is not None:
        # url3 = urlparse.urljoin(url2,"proxy.ashx")
        # dict_request3["h"] = p.group(3)
        # dict_request3["a"] = dict_request2["a"]
    # else:
        # print("Error!The url2 parameter can not be found!")
        # return None
    # print(url3)
    # print(dict_request3)
    
        
    #第三步
    dict_head['Referer'] = url1_result.url.encode('ASCII')
    print(dict_head)
    url3_result = s1.get(url3,params = dict_request3,headers = dict_head, verify=False)
    print(url3_result.encoding)
    print(url3_result.url)
    url3_result.encoding = 'utf8'
    str_re3 =str(url3_result.text)
    with open(r"D:\temp3.txt",'w') as fp:
        fp.write(str_re3)
    p = re.findall(r'ssr://([a-zA-Z\d_]{8,})',str_re3)
    if p is not None:
        ssr = set(p)
        with open(r"D:\ssr.txt",'w') as fp:
            for line in ssr:
                fp.write("ssr://"+line+"\r\n")
    dict_head['Referer'] = url3_result.url.encode('ASCII')
    p = re.findall(r'<td><a\x20class="dl1"\x20href="([\w:/.?&-_+%]+)"',str_re3)
    if p is not None:
        with open(r"D:\ssr.txt",'a+') as fp:
            fp.write('\r\n')
            for url_ssr in p:
                print(url_ssr)
                ssr_result = s1.get(url_ssr,headers = dict_head, verify=False)
                str_ssr =str(ssr_result.text)
                with open(r"D:\dbssr.txt","a+") as fpssr:
                    fpssr.write('\r\n')
                    fpssr.write(str_ssr)
                p = re.findall(r'ssr://([a-zA-Z\d_]{8,})</a>',str_ssr)
                if p is not None:
                    print(' ssr-'+str(p))
                    fp.write("ssr://"+p[0]+"\r\n")
    else:
        print("Error!The url3 parameter can not be found!")
        return None
	
if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()