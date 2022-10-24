import requests
from lxml import etree
import util


resp = requests.get('http://www.ggzy.gov.cn/information/html/b/130000/0101/202204/26/0013a102c005aaec4c88a90284e00e58c4d6.shtml')

html = etree.HTML(resp.text)

lis = util.parseHtml_list(resp.text)

after1 = util.parse2dict_title_gcjs(lis)

after2 = util.process_callbid_contact_gcjs(after1)

print(after2)
