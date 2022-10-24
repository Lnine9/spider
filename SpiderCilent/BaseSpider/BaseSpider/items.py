# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BasespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class TenderAndPreReviewItem(scrapy.Item):
    # 公告标题
    announcement_title = scrapy.Field()
    # 项目名称
    name_of_procurement_project = scrapy.Field()
    # 项目编号
    item_number = scrapy.Field()
    # 品目
    item = scrapy.Field()
    # 采购单位
    procurement_unit = scrapy.Field()
    # 行政区域
    administrative_division = scrapy.Field()
    # 公告时间
    announcement_time = scrapy.Field()
    # 预算金额
    budget_amount = scrapy.Field()
    # 项目联系人
    project_contact_person = scrapy.Field()
    # 项目联系人联系方式
    project_contact_method = scrapy.Field()
    # 代理机构联系人
    contact_person_of_agency = scrapy.Field()
    # 代理机构联系人联系方式
    contact_method_of_agency = scrapy.Field()
    # 采购方式
    procurement_mode = scrapy.Field()
    # 开标时间
    opening_time = scrapy.Field()
    # 投标地点
    place_of_tender = scrapy.Field()
    # 标书发售方式
    tender_offering_method = scrapy.Field()
    # 标书发售开始时间
    starting_time_of_tender_offer = scrapy.Field()
    # 标书发售结束时间
    ending_time_of_tender_offer = scrapy.Field()
    # 标书售价
    tender_price = scrapy.Field()
    # 标书发售地点
    place_of_tender_offer = scrapy.Field()
    # 投标截止时间
    deadline_for_bid_submission = scrapy.Field()
    # 开标地点
    bid_opening_place = scrapy.Field()
    # 附件
    attachments = scrapy.Field()
    # 其它说明
    other_instructions = scrapy.Field()
    # 源URL地址
    source_URL_address = scrapy.Field()


'''
预审公告
'''


class PreReviewItem(scrapy.Item):
    # 公告标题
    announcement_title = scrapy.Field()
    # 项目名称
    name_of_procurement_project = scrapy.Field()
    # 项目编号
    item_number = scrapy.Field()
    # 品目
    item = scrapy.Field()
    # 采购单位
    procurement_unit = scrapy.Field()
    # 行政区域
    administrative_division = scrapy.Field()
    # 公告时间
    announcement_time = scrapy.Field()
    # 预算金额
    budget_amount = scrapy.Field()
    # 项目联系人
    project_contact_person = scrapy.Field()
    # 项目联系人联系方式
    project_contact_method = scrapy.Field()
    # 代理机构联系人
    contact_person_of_agency = scrapy.Field()
    # 代理机构联系人联系方式
    contact_method_of_agency = scrapy.Field()
    # 采购方式
    procurement_mode = scrapy.Field()
    # 开标时间
    opening_time = scrapy.Field()
    # 投标地点
    place_of_tender = scrapy.Field()
    # 标书发售方式
    tender_offering_method = scrapy.Field()
    # 标书发售开始时间
    starting_time_of_tender_offer = scrapy.Field()
    # 标书发售结束时间
    ending_time_of_tender_offer = scrapy.Field()
    # 标书售价
    tender_price = scrapy.Field()
    # 标书发售地点
    place_of_tender_offer = scrapy.Field()
    # 投标截止时间
    deadline_for_bid_submission = scrapy.Field()
    # 开标地点
    bid_opening_place = scrapy.Field()
    # 附件
    attachments = scrapy.Field()
    # 其它说明
    other_instructions = scrapy.Field()
    # 源URL地址
    source_URL_address = scrapy.Field()


'''
中标公告
'''


class WinBidItem(scrapy.Item):
    # 公告标题
    announcement_title = scrapy.Field()
    # 项目名称
    name_of_procurement_project = scrapy.Field()
    # 项目编号
    item_number = scrapy.Field()
    # 品目
    item = scrapy.Field()
    # 采购单位
    procurement_unit = scrapy.Field()
    # 行政区域
    administrative_division = scrapy.Field()
    # 公告时间
    announcement_time = scrapy.Field()
    # 中标金额
    bid_winning_amount = scrapy.Field()
    # 中标供应商
    bid_winning_supplier = scrapy.Field()
    # 评审时间
    review_time = scrapy.Field()
    # 评审地点
    review_place = scrapy.Field()
    # 评审小组人员
    review_team_personnel = scrapy.Field()
    # 项目联系人
    project_contact_person = scrapy.Field()
    # 项目联系人联系方式
    project_contact_method = scrapy.Field()
    # 代理机构联系人
    contact_person_of_agency = scrapy.Field()
    # 代理机构联系人联系方式
    contact_method_of_agency = scrapy.Field()
    # 代理机构收费标准
    agent_charging_standard = scrapy.Field()
    # 代理机构收费金额
    agent_charging_amount = scrapy.Field()
    # 采购方式
    procurement_mode = scrapy.Field()
    # 其它说明
    other_instructions = scrapy.Field()
    # 附件
    attachments = scrapy.Field()
    # 附件源地址
    source_URL_address = scrapy.Field()


'''
成交公告
'''


class DealItem(scrapy.Item):
    # 公告标题
    announcement_title = scrapy.Field()
    # 项目名称
    name_of_procurement_project = scrapy.Field()
    # 项目编号
    item_number = scrapy.Field()
    # 品目
    item = scrapy.Field()
    # 采购单位
    procurement_unit = scrapy.Field()
    # 行政区域
    administrative_division = scrapy.Field()
    # 公告时间
    announcement_time = scrapy.Field()
    # 中标金额
    bid_winning_amount = scrapy.Field()
    # 中标供应商
    bid_winning_supplier = scrapy.Field()
    # 评审时间
    review_time = scrapy.Field()
    # 评审地点
    review_place = scrapy.Field()
    # 评审小组人员
    review_team_personnel = scrapy.Field()
    # 项目联系人
    project_contact_person = scrapy.Field()
    # 项目联系人联系方式
    project_contact_method = scrapy.Field()
    # 代理机构联系人
    contact_person_of_agency = scrapy.Field()
    # 代理机构联系人联系方式
    contact_method_of_agency = scrapy.Field()
    # 代理机构收费标准
    agent_charging_standard = scrapy.Field()
    # 代理机构收费金额
    agent_charging_amount = scrapy.Field()
    # 采购方式
    procurement_mode = scrapy.Field()
    # 其它说明
    other_instructions = scrapy.Field()
    # 附件
    attachments = scrapy.Field()
    # 源地址
    source_URL_address = scrapy.Field()


'''
更改公告
'''


class ChangeItem(scrapy.Item):
    # 公告标题
    announcement_title = scrapy.Field()
    # 项目名称
    name_of_procurement_project = scrapy.Field()
    # 项目编号
    item_number = scrapy.Field()
    # 行政区域
    administrative_division = scrapy.Field()
    # 公告时间
    announcement_time = scrapy.Field()
    # 项目联系人
    project_contact_person = scrapy.Field()
    # 项目联系人联系方式
    project_contact_method = scrapy.Field()
    # 代理机构联系人
    contact_person_of_agency = scrapy.Field()
    # 代理机构联系人联系方式
    contact_method_of_agency = scrapy.Field()
    # 采购方式
    procurement_mode = scrapy.Field()
    # 原公告时间（首次公告日期）
    original_announcement_time = scrapy.Field()
    # 更正（补遗、澄清）内容及附件
    contents = scrapy.Field()
    # 其它说明
    other_instructions = scrapy.Field()
    # 附件
    attachments = scrapy.Field()
    # 源URL地址
    source_URL_address = scrapy.Field()


'''
（中央）终止公告
'''


class EndItem(scrapy.Item):
    # 公告标题
    announcement_title = scrapy.Field()
    # 项目名称
    name_of_procurement_project = scrapy.Field()
    # 项目编号
    item_number = scrapy.Field()
    # 行政区域
    administrative_division = scrapy.Field()
    # 公告时间
    announcement_time = scrapy.Field()
    # 项目联系人
    project_contact_person = scrapy.Field()
    # 项目联系人联系方式
    project_contact_method = scrapy.Field()
    # 代理机构联系人
    contact_person_of_agency = scrapy.Field()
    # 代理机构联系人联系方式
    contact_method_of_agency = scrapy.Field()
    # 采购方式
    procurement_mode = scrapy.Field()
    # 开标时间
    opening_time = scrapy.Field()
    # 终止（废标、流标）内容及附件
    contents = scrapy.Field()
    # 其它说明
    other_instructions = scrapy.Field()
    # 附件
    attachments = scrapy.Field()
    # 源地址
    source_URL_address = scrapy.Field()
