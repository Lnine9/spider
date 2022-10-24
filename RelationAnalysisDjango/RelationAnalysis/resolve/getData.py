
import re

from RelationAnalysis.data_operate.relation_analysis.category_data import CategoryData

CN_NUM = {
    '〇': 0,
    '一': 1,
    '二': 2,
    '三': 3,
    '四': 4,
    '五': 5,
    '六': 6,
    '七': 7,
    '八': 8,
    '九': 9,

    '零': 0,
    '壹': 1,
    '贰': 2,
    '叁': 3,
    '肆': 4,
    '伍': 5,
    '陆': 6,
    '柒': 7,
    '捌': 8,
    '玖': 9,

    '貮': 2,
    '两': 2,
}
CN_UNIT = {
    '十': 10,
    '拾': 10,
    '百': 100,
    '佰': 100,
    '千': 1000,
    '仟': 1000,
    '万': 10000,
    '萬': 10000,
    '亿': 100000000,
    '億': 100000000,
    '兆': 1000000000000,
}


def cn2dig(cn):
    lcn = list(cn)
    unit = 0  # 当前的单位
    ldig = []  # 临时数组

    while lcn:
        cndig = lcn.pop()

        if CN_UNIT.get(cndig):
            unit = CN_UNIT.get(cndig)
            if unit == 10000:
                ldig.append('w')  # 标示万位
                unit = 1
            elif unit == 100000000:
                ldig.append('y')  # 标示亿位
                unit = 1
            elif unit == 1000000000000:  # 标示兆位
                ldig.append('z')
                unit = 1

            continue

        else:
            dig = CN_NUM.get(cndig)

            if unit:
                dig = dig * unit
                unit = 0

            ldig.append(dig)

    if unit == 10:  # 处理10-19的数字
        ldig.append(10)

    ret = 0
    tmp = 0

    while ldig:
        x = ldig.pop()

        if x == 'w':
            tmp *= 10000
            ret += tmp
            tmp = 0

        elif x == 'y':
            tmp *= 100000000
            ret += tmp
            tmp = 0

        elif x == 'z':
            tmp *= 1000000000000
            ret += tmp
            tmp = 0

        else:
            tmp += x

    ret += tmp
    return ret


def all_table(content):
    titleRow = 0
    maxWeight = 0
    weight = 0
    supplierName = []
    totalPrice = []
    for row, item in enumerate(content[0]):
        for col, mes in enumerate(item):
            if '供应商名称' in mes or '金额' in mes and '中标' in mes or '总价' in mes or '合价' in mes or '单价' in mes or '报价' in mes \
                    or '品牌' in mes or '型号' in mes or '数量' in mes or ('品目' in mes and '名称' in mes) or '供应商名称' in mes:
                weight += 1
            if '供应商名称' in mes:
                supplierName = [content[0][row + 1][col]]
            if '金额' in mes and '中标' in mes or '总价' in mes or '合价' in mes or '成交金额' in mes:
                totalPrice = [content[0][row + 1][col]]
        if weight > maxWeight:
            maxWeight = weight
            weight = 0
            titleRow = row
    content[0] = content[0][titleRow:]
    return get_category_entity(content, supplierName, totalPrice)


def p_and_table(text, listOfCategory):
    supplierName = []
    totalPrice = []
    for message in text.xpath('//div[@class="vF_detail_content"]//text()'):
        content = message.replace(' ', '').replace('\n', '').strip("\n\r    \xa0").replace('\t', '')
        if '供应商名称' in content:
            if "：" in content:
                supplierName.append(content.split("：")[1])
        if '金额' in content and '中标' in content or '总价' in content or '合价' in content or '成交金额' in content:
            if "：" in content:
                totalPrice.append(content.split("：")[1])
        if '主要标的信息' in content:
            break
    return get_category_entity(listOfCategory, supplierName, totalPrice)


def table_and_p(content):
    pass


def table_and_table(content):
    title_list = content[0]
    mes = content[1]
    supplierName = []
    totalPrice = []
    for title in title_list:
        for col, text in enumerate(title):
            if '供应商名称' in text:
                supplierName = [title_list[1][col]]
            if '金额' in text and '中标' in text or '总价' in text or '合价' in text or '成交金额' in text:
                totalPrice = [title_list[1][col]]
    listOfCategory = [mes]
    return get_category_entity(listOfCategory, supplierName, totalPrice)


def div_table(content):
    title = str(content[0]).replace('[', '').replace(']', '').replace('\'', '')
    titleRow = 0
    maxWeight = 0
    weight = 0
    supplierName = []
    totalPrice = []
    for row, item in enumerate(content[1]):
        for col, mes in enumerate(item):
            if '供应商名称' in mes or '金额' in mes and '中标' in mes or '总价' in mes or '合价' in mes or '单价' in mes or '报价' in mes \
                    or '品牌' in mes or '型号' in mes or '数量' in mes or ('品目' in mes and '名称' in mes) or '供应商名称' in mes:
                weight += 1
            if '供应商名称' in mes:
                supplierName = [content[0][row + 1][col]]
            if '金额' in mes and '中标' in mes or '总价' in mes or '合价' in mes or '成交金额' in mes:
                totalPrice = [content[0][row + 1][col]]
        if weight > maxWeight:
            maxWeight = weight
            weight = 0
            titleRow = row

    pre_text = str(content[1][0:titleRow]).replace('[', '').replace(']', '').replace('\'', '')
    mes = (pre_text + title).split(" ")
    for col, text in enumerate(mes):
        if '供应商名称' in text:
            supplierName = mes[col + 1]
        if '金额' in text and '中标' in text or '总价' in text or '合价' in text or '成交金额' in text:
            totalPrice = mes[col + 1]
    listOfCategory = [content[1][titleRow:]]
    return get_category_entity(listOfCategory, supplierName, totalPrice)


def get_category_entity(listOfCategory, supplierName, totalPrice):
    categoryDataList = []
    for order in listOfCategory:

        for row, item in enumerate(order):
            categoryData = CategoryData()
            deleteData = False
            isNone = True

            for index, mes in enumerate(item):

                title = order[0][index]
                fakeTitle = order[row - 1][index]
                if title == mes:
                    deleteData = True
                    break

                if mes != '':
                    isNone = False

                if '单价' in title or '报价' in title or '单价' in fakeTitle or '报价' in fakeTitle:
                    categoryData.unit_price = solve_price(mes)
                if '品牌' in title or '品牌' in fakeTitle:
                    categoryData.brand = mes
                if '型号' in title or '型号' in fakeTitle:
                    categoryData.type = mes
                if '数量' in title or '数量' in fakeTitle:
                    categoryData.number = mes
                if '品目' in title or '品目' in fakeTitle:
                    categoryData.item = mes
                if '名称' in title or '名称' in fakeTitle:
                    categoryData.category_name = mes
                if '供应商名称' in title or '供应商名称' in fakeTitle:
                    categoryData.supplier_name = mes
            if not deleteData and not isNone:
                if len(supplierName) == 1:
                    categoryData.supplier_name = supplierName[0]
                else:
                    categoryData.supplier_name = supplierName[len(categoryDataList)]
                if len(totalPrice) == 1:
                    categoryData.total_price = solve_price(totalPrice[0])
                else:
                    categoryData.total_price = solve_price(totalPrice[len(categoryDataList)])

                categoryDataList.append(categoryData)
    return categoryDataList


def judge_is_need(listOfCategory):
    real_table = []
    for table in listOfCategory:
        weight = 0
        for th in table[0]:
            if "货物名称" in th or "产品名称" in th or "品名" in th or "成交标的名称" in th or "名称" in th or "标的名称" in th or "采购标的" in th \
                    or "数量" in th or "型号" in th or "品目" in th or "品牌" in "th" or "单价" in th:
                weight += 1
        if weight > 3:
            real_table.append(table)
    return real_table


def solve_price(price):
    price = price.replace(",", '').replace('￥', '')
    has_chinese_char = False
    price_str = ''
    not_only_wan = False

    for item in price:
        if CN_NUM.get(item) or CN_UNIT.get(item):
            has_chinese_char = True
            price_str += item
        if CN_NUM.get(item):
            not_only_wan = True
    if has_chinese_char and not_only_wan:
        price_str = cn2dig(price_str)
        return price_str
    else:
        if '万' in price:
            return float(re.findall('[\d+\.\d]*', price)[0]) * 10000
        else:
            return re.findall('[\d+\.\d]*', price)[0]