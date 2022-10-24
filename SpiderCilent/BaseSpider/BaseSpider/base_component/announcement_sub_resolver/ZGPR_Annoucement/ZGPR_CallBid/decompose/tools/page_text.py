def get_text(response):
    return ' '.join(response.xpath('//text()'))
