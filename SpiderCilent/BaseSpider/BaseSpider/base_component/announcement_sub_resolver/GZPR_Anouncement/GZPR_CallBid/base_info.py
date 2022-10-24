from BaseSpider.tool.DealDate import get_one_time_from_str


def getCodeHtml(response):
    code_dict = {}

    code_dict['url'] = response.url
    code_dict['file_type'] = 'html'
    code_dict['file_size'] = '-1'
    code_dict['local_path'] = '暂无'
    code_dict['code'] = ''.join(response.xpath('//*[@class="con_box"]').extract())

    return code_dict


def getAttachment(response):
    at_dict = []
    fileName = response.xpath('//*[@class="file"]/a/text()').extract()
    fileUrl = response.xpath('//*[@class="file"]/a/@href').extract()
    for i in range(0, len(fileName)):
        item = {}
        if fileUrl[i] is not None:
            fileName[i] = fileName[i]
            fileName[i] = fileName[i].replace(' ', '%20')  # 防止url出现空字符
            item['file_name'] = fileName[i]
            item['file_type'] = fileName[i][fileName[i].rfind('.') + 1:]
            item['url'] = fileUrl[i]
        item['file_size'] = -1
        item['local_path'] = '暂无'
        at_dict.append(item)
    return at_dict


def BaseInfo(response, content):
    """
    设置标题、发布时间、url来源网址
    :param response:
    :param content:
    :return:
    """
    content['title'] = response.xpath('normalize-space(//div[@class="title"]/h3//text())').get()
    content['ancm_time'] = get_one_time_from_str(response.xpath("//*[@class='fbrq']").get())
    content['sourse_url'] = response.url
    content['web_site'] = 'http://ggzy.guizhou.gov.cn/'
    content['source_web_name'] = '贵州省公共资源交易信息网'
