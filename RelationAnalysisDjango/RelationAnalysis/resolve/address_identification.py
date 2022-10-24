import re
import jieba
import cpca

from RelationAnalysis.data_operate.relation_analysis.zone_id import ZoneId

zone_id_table = ZoneId.query_all()
zone_dict = {}
for item in zone_id_table:
    zone_dict.update({item.value: item.code})


class AddressIdentification:
    """
    地址编号解析
    """
    zone = ZoneId()
    province = ''
    city = ''
    district = ''
    detail = ''
    province_id = []
    city_id = []
    district_id = []

    def address_identification(self, *args) -> dict:
        """
        被调用函数
        """
        # 初始化
        self.province = ''
        self.province_id = None
        self.city = ''
        self.city_id = None
        self.district = ''
        self.district_id = None
        self.detail = ''
        # 地址拆分
        self.address_split('cpca', *args)
        # 省、市、区拼接
        self.address_splice()
        # 严格匹配（初步匹配）
        self.strict_match()
        # 对初步匹配后的结果进一步处理
        self.situation_judgment(*args)

        return {"province": self.province,
                "province_id": self.province_id,
                "city": self.city.split()[-1] if self.city else self.city,
                "city_id": self.city_id,
                "district": self.district.split()[-1] if self.district else self.district,
                "district_id": self.district_id,
                "detail": self.detail}

    def address_split(self, split_style, *args):
        """
        地址拆分

        参数说明：
        一至多个地址字符串
        :param split_style:
        :param args:
        :return:
        """
        # 通过cpca拆分
        if split_style == 'cpca':
            for item in args:
                if (self.province == '' or self.city == '' or self.district == '') and item and item != '市辖区':
                    # cpca分词
                    address = cpca.transform([item])  # 地址

                    # 截取省、市、区、详细地址
                    if address.省.values:
                        self.province = ''.join(address.省.values) if self.province == '' else self.province
                    if address.市.values:
                        self.city = ''.join(address.市.values) if self.city == '' else self.city
                    if address.区.values:
                        self.district = ''.join(address.区.values) if self.district == '' else self.district
                    if address.地址.values:
                        self.detail = ''.join(address.地址.values) if self.detail == '' else self.detail
                    # cpca的bug，对于**县改为**区后，cpca会分析错误，错误特征为city='县'
                    if self.city == '县' and self.province == '北京市':
                        self.province = self.city = self.district = ''

        # 通过jieba拆分
        elif split_style == 'jieba':

            self.province = self.city = self.district = ''

            for item in args:
                if (self.province == '' or self.city == '' or self.district == '') and item and item is not None:
                    jieba_list = list(jieba.cut(item, cut_all=False))
                    province = city = district = ''
                    for little in jieba_list:
                        if little[-1] == '省' and len(little) > 1 and province == '':
                            self.province = little
                        if little[-1] == '市' and len(little) > 1 and city == '':
                            self.city = little
                        if (little[-1] == '区' or little[-1] == '县') and len(little) > 1 and district == '':
                            self.district = little
                # cpca的bug，对于**县改为**区后，cpca会分析错误，错误特征为city='县'
                if self.city == '县' and self.province == '北京市':
                    self.province = self.city = self.district = ''

        # 最后统一排除仅有'市辖区'的情况
        if (self.district == '市辖区' or self.district == '新区' or self.district == '自治县') \
                and not self.province and not self.city:
            self.district = ''

    def address_splice(self):
        """
        省、市、区拼接

        参数说明：
        尚未拼接的省、市、区（县），例：
        province: 山东省
        city: 泰安市
        district: 泰山区
        :return:
        """
        # 常规地址
        if self.province != self.city \
                and self.province != '北京市' \
                and self.province != '天津市' \
                and self.province != '上海市' \
                and self.province != '重庆市':  # cpca解析直辖市时province == city
            if self.province and self.city:
                self.city = self.province + ' ' + self.city

            if self.province and self.city and self.district:
                self.district = self.city + ' ' + self.district

        # 直辖市：北京、天津、上海、重庆
        elif self.province == '北京市' and self.district:
            rex = re.compile(r'^((密云|延庆).)*$')
            if rex.search(self.district) is None:
                self.city = self.province + ' 市辖区'
            else:
                self.city = self.province + ' 县'
            self.district = self.city + ' ' + self.district
        elif self.province == '天津市' and self.district:
            rex = re.compile(r'^((宁河|静海|蓟).)*$')
            if rex.search(self.district) is None:
                self.city = self.province + ' 市辖区'
            else:
                self.city = self.province + ' 县'
            self.district = self.province + ' ' + self.district
        elif self.province == '上海市' and self.district:
            if '崇明' not in self.district:
                self.city = self.province + ' 市辖区'
            else:
                self.city = self.province + ' 县'
            self.district = self.province + ' ' + self.district
        elif self.province == '重庆市' and self.district:
            rex = re.compile(r'^((潼南|铜梁|荣昌|璧山|梁平|城口|丰都|垫江|武隆|忠|开|云阳|奉节|巫山|巫溪|石柱|秀山|酉阳|彭水).)*$')
            if rex.search(self.district) is None:
                self.city = self.province + ' 市辖区'
            else:
                self.city = self.province + ' 县'
            self.district = self.province + ' ' + self.district

    def strict_match(self):
        """
        严格匹配

        参数格式（如下）：
        province：山东省
        city: 山东省 青岛市
        district: 山东省 青岛市 即墨区
        :return:
        """
        if self.province:
            self.province_id = zone_dict.get(self.province)

        if self.city:
            self.city_id = zone_dict.get(self.city)

        if self.district:
            self.district_id = zone_dict.get(self.district)

    def fuzzy_match(self):
        """
        模糊匹配

        参数格式（如下）：
        province：山东省
        city: 山东省 青岛市
        district: 山东省 青岛市 即墨区
        :return:
        """
        if self.district:
            # 先查询3级地址
            district_split = [i[:-1] for i in self.district.split()]
            district_and_id = self.zone_dict_query(district_split)

            # 仅用3级地址查询，会有3级重复，默认选中第一个的问题，所以尽量带上1,2级地址一起去模糊查询
            if not district_and_id.get('key'):
                if len(district_split) >= 2:
                    # 1,3级地址模糊查询
                    district_and_id = self.zone_dict_query(district_split[0], district_split[-1])
                    if not district_and_id.get('key'):
                        # 1,2级地址模糊查询
                        district_and_id = self.zone_dict_query(district_split[0], district_split[1])
            # 1,3级、1,2级地址模糊查询均失败，最后才用单独的3级地址模糊查询
            if not district_and_id.get('key'):
                district_and_id = self.zone_dict_query(district_split[-1])
            if district_and_id.get('key'):
                self.district = district_and_id.get('key')
            if district_and_id.get('value'):
                self.district_id = district_and_id.get('value')

                # 如果3级地址获取成功
                if self.district_id:
                    # 通过3及地址获取2级地址
                    district_split = self.district.split()
                    if not re.search(r'北京|天津|上海|重庆', district_split[0]):
                        self.city = ' '.join(self.district.split()[:2])
                        self.city_id = zone_dict.get(self.city)
                    else:
                        self.city = district_split[0] + ' 县'
                        self.city_id = zone_dict.get(self.city)
                    # 通过3及地址获取1级地址
                    self.province = ' '.join(self.district.split()[:1])
                    self.province_id = zone_dict.get(self.province)

        elif self.city:
            # 先查询2级地址
            city_split = [i[:-1] for i in self.city.split()]
            city_and_id = self.zone_dict_query(city_split)
            if not city_and_id.get('key'):
                city_and_id = self.zone_dict_query(city_split[-1])
            if city_and_id.get('key'):
                self.city = city_and_id.get('key')
            if city_and_id.get('value'):
                self.city_id = city_and_id.get('value')

                # 如果2级地址获取成功
                if self.city_id:
                    # 通过2及地址获取1级地址
                    self.province = ' '.join(self.city.split()[:1])
                    self.province_id = zone_dict.get(self.province)

    def province_direct_units(self):
        """
        省直辖行政单位处理
        :return:
        """
        code_value = self.zone_dict_query(self.district[:-1])

        if code_value.get('key') and ('省直辖行政单位' in code_value.get('key') or '省直辖县级行政单位' in code_value.get('key')):
            split_value = code_value.get('key').split()
            if len(split_value) > 0:
                self.province = split_value[0]
                self.province_id = zone_dict.get(self.province)
                self.city = split_value[0] + " 省直辖县级行政区划"
                self.city_id = zone_dict.get(self.city)
                self.district = code_value.get('key')
                self.district_id = code_value.get('value')

    def infer_upper_by_lower(self):
        """
        处理错误解析1
        通过下级地址推断上级地址
        :return:
        """
        # 如果3级地址存在，通过3级地址拆分
        if self.district:
            # 拆分出正确的2,3级地址
            split_address = self.district.split()
            if len(split_address) > 2:
                right_address = split_address[1] + ' ' + split_address[2]

                # 通过正确的部分地址模糊匹配出3级地址的值和编号
                district_code_value = self.zone_dict_query(right_address[:-1])
                if district_code_value.get('key'):
                    self.district = district_code_value.get('key')
                    self.district_id = district_code_value.get('value')

                # 通过3级地址的值，拆分出1,2级地址
                split_address = self.district.split()
                if len(split_address) >= 2:
                    self.province = split_address[0]
                    self.city = self.province + ' ' + split_address[1]

                # 最后查询1,2级地址编号，3级地址是查询出来的，拆分开后1,2级地址一定存在，故直接精确查询
                self.province_id = zone_dict.get(self.province)
                self.city_id = zone_dict.get(self.city)

        # 如果3级地址不存在，则通过2级地址拆分
        else:
            # 拆分出正确的2级地址
            split_address = self.city.split()
            if len(split_address) >= 2:
                right_address = split_address[1]
                city_code_value = self.zone_dict_query(right_address[:-1])

                if city_code_value.get('key'):
                    self.city = city_code_value.get('key')
                    self.city_id = city_code_value.get('value')

                # 通过2级地址的值，拆分出1级地址
                self.province = split_address[0]

                # 最后查询1级地址编号
                self.province_id = zone_dict.get(self.province)

    def upper_right(self):
        """
        上级地址正确，下级地址cpca推荐错误
        :return:
        """
        if self.province and not self.province_id:
            self.province = ''
        if self.city and not self.city_id:
            self.city = ''
        if self.district and not self.district_id:
            self.district = ''

    def address_identification_by_jieba(self):
        """
        处理错误解析2
        jieba分词匹配
        :param args:
        :return:
        """
        # 通过jieba分词拆分
        code_value = self.zone_dict_query(self.province[:-1], self.city[:-1], self.district[:-1])
        print(code_value)
        print()
        # 通过查询出地址值的长度存入对应情况的对应值
        if code_value.get('key'):
            address_value_list = code_value.get('key').split()
            if len(address_value_list) == 1:
                self.province = address_value_list[0]
                self.province_id = code_value.get('value')
            if len(address_value_list) == 2:
                self.province = address_value_list[0]
                self.province_id = zone_dict.get(self.province)
                self.city = self.province + ' ' + address_value_list[1]
                self.city_id = code_value.get('value')
            if len(address_value_list) == 3:
                self.province = address_value_list[0]
                self.province_id = zone_dict.get(self.province)
                self.city = self.province + ' ' + address_value_list[1]
                self.city_id = zone_dict.get(self.city)
                self.district = self.city + ' ' + address_value_list[2]
                self.district_id = code_value.get('value')

    def situation_judgment(self, *args):
        """
        情况判断
        :param args:
        :return:
        """
        # 去除查询不到编号的部分
        self.upper_right()

        # 尚未解析完整
        if not self.province_id or not self.city_id or not self.district_id:
            # 进行模糊匹配
            self.fuzzy_match()

        # 可能为省直辖县级行政单位(方法内会二次判断)
        if self.province == '' and self.city == '' and self.district:
            self.province_direct_units()

        # 区县混乱
        if self.province_id and self.city_id and not self.district_id and self.district:
            self.district_id = self.zone_dict_query(self.district[:-1]).get('value')

        # 省直辖行政单位处理
        if not self.city_id and self.district:
            self.province_direct_units()

        # cpca智能推荐错误（推荐错1级地址，即当1,2级地址皆存在，但查询2级地址编号失败的情况）
        if not self.city_id and self.province and self.city:
            # 通过下级地址推断上级地址
            self.infer_upper_by_lower()
            # 仍然未解决错误，采用jieba分词匹配
            if not self.city_id and self.province and self.city:
                self.address_split('jieba', *args)
                self.address_identification_by_jieba()

        # 全为空时，用结巴分词
        if not self.province_id and not self.city_id and not self.district_id:
            self.address_split('jieba', *args)
            self.address_identification_by_jieba()

        # 3级地址解析被干扰，
        # 例：海南省海口市名门广场北区B座1-5号605室 --> 海南省 海口市 北区
        if self.district and not self.district_id:
            self.district = ''

        # 直辖市仅能解析出一级地址时
        if self.province == self.city:
            self.city = ''
            self.city_id = None

    @staticmethod
    def zone_dict_query(*args):
        """
        zone_dict字典中模糊查询地址编号
        :param args:
        :return:
        """
        # 如果传入的是个数组
        if isinstance(args[0], list):
            args = args[0]

        # 排除所有参数全为空的情况
        not_all_args_none = False
        for i in args:
            if i:
                not_all_args_none = True
                break

        for key, value in zone_dict.items():
            # 所有参数均在key中的标志
            all_args_in_key = True
            # 循环判断所有参数
            for arg in args:
                if arg not in key:
                    all_args_in_key = False
                    break
            # 如果所有参数均在key中，则模糊查找成功
            if all_args_in_key and not_all_args_none:
                return {'key': key, 'value': value}
        return {'key': None, 'value': None}


