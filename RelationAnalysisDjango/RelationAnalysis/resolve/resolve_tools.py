import re

from RelationAnalysis.data_operate.relation_analysis.purchase_item import PurchaseItem
from RelationAnalysis.resolve.address_identification import AddressIdentification

item_table = PurchaseItem.query_all()
item_dict = {}
for item in item_table:
    item_dict.update({item.value: item.code})

address_identification = AddressIdentification()


def get_phone(string) -> str:
    """
    拆分电话
    :param string:
    :return: phone
    """

    if string is None:
        return ''
    # 删除含中文字符的括号内容
    phone = re.compile(r'\([\u4E00-\u9FA5].*?\)|（[\u4E00-\u9FA5].*?）', re.S).sub('', string)
    # 删除邮箱
    phone = re.compile(r'[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.(com|cn|net)$').sub('', phone)
    # 找出含数字及指定字符构成的，以数字、中英文前括号开头，长度不低于8个字符的子字符串
    phone = re.findall(r'(?=[0-9(（])([0-9转或、/\-—－，,（）\\(\\)*]{8,})', phone)
    # 对数组中每个不以数字结束的元素删除最后一个字符，并以'/'拼接处理后的元素
    phone = '/'.join((i[:-1] if re.compile(r'(?<![0-9])$').search(i) is not None else i) for i in phone)
    # 删除可能存在的无内容括号
    phone = ''.join(re.split(r'\(\)|（）', phone))
    return phone


def get_name(string) -> str:
    """
    拆分姓名（拆分出了有符号隔开的或中文数字相连的2-3个字的姓名）
    :param string:
    :return: name
    """
    if string is None:
        return ''
    # 去除指定字符串（存在姓名与指定字符串未用任何符号分开的情况）
    name = ''.join(re.compile(r'联系(人|代表)?|电话|方[法式]|地址|传真|项目', re.S).sub('', string))
    # 留下中文字符和指定字符
    name = '/'.join(re.findall(r'[\u4E00-\u9FA5、,，；;。：: /]{2,}', name))
    # 按指定字符分割开
    name_list = re.split(r'[、,，；;。：: /]', name)
    bai_jia_xin_pattern = r'[赵|钱|孙|李|周|吴|郑|王|冯|陈|褚|卫|蒋|沈|韩|杨|朱|秦|尤|许|何|吕|施|张|孔|曹|严|华|金|魏|陶|姜|戚|谢|邹|喻|柏|水|窦|章|云|付|苏|潘|葛|奚|范|彭|郎|鲁|韦|昌|马|苗|凤|花|方|俞|任|袁|柳|酆|鲍|史|唐|费|廉|岑|薛|雷|贺|倪|汤|滕|殷|罗|毕|郝|邬|安|常|乐|于|时|傅|皮|卞|齐|康|伍|余|元|卜|顾|孟|平|黄|和|穆|萧|尹|姚|邵|湛|汪|祁|毛|禹|狄|米|贝|明|臧|计|伏|成|戴|谈|宋|茅|庞|熊|纪|舒|屈|项|祝|董|梁|杜|阮|蓝|闵|席|季|麻|强|贾|路|娄|危|江|童|颜|郭|梅|盛|林|刁|锺|徐|邱|骆|高|夏|蔡|田|樊|胡|凌|霍|虞|万|支|柯|昝|管|卢|莫|经|房|裘|缪|干|解|应|宗|丁|宣|贲|邓|郁|单|杭|洪|包|诸|左|石|崔|吉|钮|龚|程|嵇|邢|滑|裴|陆|荣|翁|荀|羊|於|惠|甄|麴|家|封|芮|羿|储|靳|汲|邴|糜|松|井|段|富|巫|乌|焦|巴|弓|牧|隗|山|谷|车|侯|宓|蓬|全|郗|班|仰|秋|仲|伊|宫|宁|仇|栾|暴|甘|钭|历|戎|祖|武|符|刘|景|詹|束|龙|叶|幸|司|韶|郜|黎|溥|印|宿|白|怀|蒲|邰|从|鄂|索|咸|籍|卓|蔺|屠|蒙|池|乔|阳|郁|胥|能|苍|双|闻|莘|党|翟|谭|贡|劳|逄|姬|申|扶|堵|冉|宰|郦|雍|却|桑|桂|濮|牛|寿|通|边|扈|燕|冀|浦|尚|农|温|别|庄|晏|柴|瞿|充|慕|连|茹|习|宦|艾|鱼|容|向|古|易|慎|戈|廖|庾|终|暨|居|衡|步|都|耿|满|弘|匡|国|文|寇|广|禄|阙|东|欧|沃|利|蔚|越|夔|隆|师|巩|厍|聂|晁|勾|敖|融|冷|訾|辛|阚|那|简|饶|空|曾|毋|沙|乜|养|鞠|须|丰|巢|关|蒯|相|荆|红|游|竺|权|司马|上官|欧阳|夏侯|诸葛|闻人|东方|赫连|皇甫|尉迟|公羊|澹台|公冶宗政|濮阳|淳于|单于|太叔|申屠|公孙|仲孙|轩辕|令狐|钟离|宇文|长孙|慕容|司徒|司空|召|有|舜|岳|黄辰|寸|贰|皇|侨|彤|竭|端|赫|实|甫|集|象|翠|狂|辟|典|良|函|芒|苦|其|京|中|夕|乌孙|完颜|富察|费莫|蹇|称|诺|来|多|繁|戊|朴|回|毓|鉏|税|荤|靖|绪|愈|硕|牢|买|但|巧|枚|撒|泰|秘|亥|绍|以|壬|森|斋|释|奕|姒|朋|求|羽|用|占|真|穰|翦|闾|漆|贵|代|贯|旁|崇|栋|告|休|褒|谏|锐|皋|闳|在|歧|禾|示|是|委|钊|频|嬴|呼|大|威|昂|律|冒|保|系|抄|定|化|莱|校|么|抗|祢|綦|悟|宏|功|庚|务|敏|捷|拱|兆|丑|丙|畅|苟|随|类|卯|俟|友|答|乙|允|甲|留|尾|佼|玄|乘|裔|延|植|环|矫|赛|昔|侍|度|旷|遇|偶|前|由|咎|塞|敛|受|泷|袭|衅|叔|圣|御|夫|仆|镇|藩|邸|府|掌|首|员|焉|戏|可|智|尔|凭|悉|进|笃|厚|仁|业|肇|资|合|仍|九|衷|哀|刑|俎|仵|圭|夷|徭|蛮|汗|孛|乾|帖|罕|洛|淦|洋|邶|郸|郯|邗|邛|剑|虢|隋|蒿|茆|菅|苌|树|桐|锁|钟|机|盘|铎|斛|玉|线|针|箕|庹|绳|磨|蒉|瓮|弭|刀|疏|牵|浑|恽|势|世|仝|同|蚁|止|戢|睢|冼|种|涂|肖|己|泣|潜|卷|脱|谬|蹉|赧|浮|顿|说|次|错|念|夙|斯|完|丹|表|聊|源|姓|吾|寻|展|出|不|户|闭|才|无|书|学|愚|本|性|雪|霜|烟|寒|少|字|桥|板|斐|独|千|诗|嘉|扬|善|揭|祈|析|赤|紫|青|柔|刚|奇|拜|佛|陀|弥|阿|素|长|僧|隐|仙|隽|宇|祭|酒|淡|塔|琦|闪|始|星|南|天|接|波|碧|速|禚|腾|潮|镜|似|澄|潭|謇|纵|渠|奈|风|春|濯|沐|茂|英|兰|檀|藤|枝|检|生|折|登|驹|骑|貊|虎|肥|鹿|雀|野|禽|飞|节|宜|鲜|粟|栗|豆|帛|官|布|衣|藏|宝|钞|银|门|盈|庆|喜|及|普|建|营|巨|望|希|道|载|声|漫|犁|力|贸|勤|革|改|兴|亓|睦|修|信|闽|北|守|坚|勇|汉|练|尉|士|旅|五|令|将|旗|军|行|奉|敬|恭|仪|母|堂|丘|义|礼|慈|孝|理|伦|卿|问|永|辉|位|让|尧|依|犹|介|承|市|所|苑|杞|剧|第|零|谌|招|续|达|忻|六|鄞|战|迟|候|宛|励|粘|萨|邝|覃|辜|初|楼|城|区|局|台|原|考|妫|纳|泉|老|清|德|卑|过|麦|曲|竹|百|福|言|第五|佟|爱|年|笪|谯|哈|墨|连|南宫|赏|伯|佴|佘|牟|商|西门|东门|左丘|梁丘|琴|后|况|亢|缑|帅|微生|羊舌|海|归|呼延|南门|东郭|百里|钦|鄢|汝|法|闫|楚|晋|谷梁|宰父|夹谷|拓跋|壤驷|乐正|漆雕|公西|巫马|端木|颛孙|子车|督|仉|司寇|亓官|三小|鲜于|锺离|盖|逯|库|郏|逢|阴|薄|厉|稽|闾丘|公良|段干|开|光|操|瑞|眭|泥|运|摩|伟|铁|迮][\u4e00-\u9fa5]{1,3}$'
    # 一边循环一边删除内容，其中name_list[:]是对name_list的复制，是不同的内存地址
    for item in name_list[:]:
        search_result = re.compile(r'[\u4E00-\u9FA5]{4,}').search(item)
        if search_result is not None or len(item) < 2 or re.match(bai_jia_xin_pattern, item) is None:
            name_list.remove(item)
    name = '、'.join(name_list)
    return name


def update_resolve(new, old):
    """
    更新解析内容
    用旧解析对象去完善新解析对象，仅替换新解析对象中为空而旧解析对象不为空的属性
    :param new:
    :param old:
    :return: new
    """

    # 参数类型不同，不做修改
    if not isinstance(new, type(old)):
        return new

    for attr in old.__dict__:

        # 不以_开头的属性（剔除无关属性）
        if re.match(r'^_', attr) is None:
            new_attr = getattr(new, attr)
            old_attr = getattr(old, attr)

            # 旧解析对象有值而新解析对象无值的属性，将旧解析对象该属性值赋给新解析对象
            if (not new_attr or new_attr == '无' or new_attr == '/' or '详见' in str(new_attr)) \
                    and (old_attr or old_attr == 0):
                setattr(new, attr, old_attr)

    return new


def get_purchase_method(purchase_m, sourse_url):
    """
    采购方式编号
    :param purchase_m:
    :param sourse_url:
    :return:
    """
    switch_purchase_method = {
        '公开招标': 100,
        '邀请招标': 200,
        '竞争性谈判': 300,
        '询价': 400,
        '单一来源': 500,
        '协议供货': 600,
        '电子竞价': 6001,
        '电子反拍': 6002,
        '定点采购': 700,
        '竞争性磋商': 800,
    }

    url_keys = {
        '/gkzb/': '公开招标',
        '/yqzbgg/': '邀请招标',
        '/jzxtpgg/': '竞争性谈判',
        '/xjgg/': '询价',
        '/dylygg/': '单一来源',
        '/jzxcs/': '竞争性磋商',
    }

    # 如果采购方式在字典中
    if purchase_m in switch_purchase_method.keys():
        return {"purchase_method": purchase_m, "purchase_code": switch_purchase_method[purchase_m]}
    else:

        # 通过url获取采购方式
        for key in url_keys.keys():
            if re.compile(key).search(sourse_url) is not None:
                purchase_m = url_keys.get(key)
                return {"purchase_method": purchase_m, "purchase_code": switch_purchase_method[purchase_m]}

    return {"purchase_method": None, "purchase_code": None}


def get_item_and_code(item_value):
    """
    查询品目名称及编号
    :param item_value:
    :return:
    """
    if item_value is None or item_value == '':
        return [{'code': None, 'name': None}]

    # 拆分出的列表
    item_list = list(set(re.split(r'[/]', item_value)))
    # 已查询的列表，用于去重
    queried_list = []
    # 结果列表
    result = []

    for item in item_list:
        query_result = []
        # 去重
        if item not in queried_list and '，' not in item:
            query_result = item_dict.get(item)

        # 品目表中有9条品目带中文都好，为了后面去重时好用中文逗号拆分，表中这9条数据的中文逗号已经改问英文逗号
        elif item not in queried_list and '，' in item:
            item = item.replace('，', ',')
            query_result = item_dict.get(item)

        # 未找到时可能存在不规范写法，继续拆分
        if not query_result:
            item_split = re.split(r'[,，。；;、]', item)
            for split in item_split:
                # 去重
                if split not in queried_list:
                    # 查询
                    query_result = item_dict.get(split)
                    if query_result:
                        queried_list.append(query_result)
                        result.append({'code': query_result, 'name': split})
        # 找到了直接加入list中
        else:
            queried_list.append(query_result)
            result.append({'code': query_result, 'name': item})

    return result


def merge_item(old_code, old_value, new_code, new_value, split_char='，'):
    """
    1、用于合并品目及品目编号，并去重
    2、用于合并行业划分，并去重
    :param old_code:str
    :param old_value:str
    :param new_code:str
    :param new_value:str
    :param split_char:str用于拆分的字符，默认为中文逗号
    :return:返回结果，例：[('A', '货物'), ('A99', '其他货物'), ('A9999', '其他不另分类的物品'), ('C', '服务'), ('C99', '其他服务')]
    """
    # 旧数据字典
    old_set = {}
    # 新数据字典
    new_set = {}

    # 处理参数
    old_code = old_code if old_code else ''
    old_value = old_value if old_value else ''
    new_code = new_code if new_code else ''
    new_value = new_value if new_value else ''

    # 拆分参数
    old_code_list = [i for i in old_code.split(split_char) if i]
    old_value_list = [i for i in old_value.split(split_char) if i]
    new_code_list = [i for i in new_code.split(split_char) if i]
    new_value_list = [i for i in new_value.split(split_char) if i]

    # 填充旧数据字典
    for i in range(min(len(old_code_list), len(old_value_list))):
        # 先判断字典是否为空，空字典不可直接添加内容，会报错
        if old_set:
            old_set.update({old_code_list[i]: old_value_list[i]})
        else:
            old_set = {old_code_list[i]: old_value_list[i]}
    # 填充新数据字典
    for i in range(min(len(new_code_list), len(new_value_list))):
        if new_set:
            new_set.update({new_code_list[i]: new_value_list[i]})
        else:
            new_set = {new_code_list[i]: new_value_list[i]}

    # 新旧数据字典合并（自行去重）、排序
    # 要保持两个字段中各个元素一一对应，不可直接合并字典，
    for new_code in new_code_list:
        if new_code not in old_code_list:
            if old_set:
                old_set.update({new_code: new_set.get(new_code)})
            else:
                old_set = {new_code: new_set.get(new_code)}

    return sorted(old_set.items(), key=lambda x: x[0])


def get_distrcit_name_and_code(call_unit_address, call_unit, region):
    """
    采购项目行政区域及编号
    :param call_unit_address:
    :param call_unit:
    :param region:
    :return:
    """
    region_dic = address_identification.address_identification(call_unit_address, call_unit, region)
    # 取能解析出来的最详细的编码：县->市->省
    DistrcitCode = None
    if region_dic.get("district_id"):
        DistrcitCode = region_dic.get("district_id")
    elif region_dic.get("city_id"):
        DistrcitCode = region_dic.get("city_id")
    elif region_dic.get("province_id"):
        DistrcitCode = region_dic.get("province_id")

    # 拼接所有级别地址
    DistrictName = ''
    if region_dic.get("province"):
        DistrictName = region_dic.get("province")
    if region_dic.get("city"):
        DistrictName += ' ' + region_dic.get("city")
    if region_dic.get("district"):
        DistrictName += ' ' + region_dic.get("district")
    # 一些特别的行政区，没有编号（如：经济开发区、新区、试验区等）
    if not DistrictName \
            and (region[-1] == '区' or '洋浦' in region) \
            and '市辖区' not in region:
        DistrictName = region
    if not DistrictName:
        DistrictName = None

    return {'DistrcitCode': DistrcitCode, 'DistrictName': DistrictName}







