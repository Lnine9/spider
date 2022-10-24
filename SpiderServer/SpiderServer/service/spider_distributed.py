# coding: utf-8
from django.http import HttpResponse, JsonResponse


# 中国政府爬虫ID
from DataBaseOperate.data_operate.spider_manage.distributed_group import DistributedGroup

ZGZF_ID = [40, 41, 42, 43, 44, 45, 47, 48, 49, 50, 51]

def get(password):
    # 校验口令是否正确
    ZGZFid_list = []
    Otherid_list = []
    group_id = DistributedGroup.queryid(password)
    if group_id != []:
        # 获取口令对应的分组
        one_id = ZGZF_ID.pop(0)
        ZGZF_ID.append(one_id)
        ZGZFid_list.append(one_id)
        # spider_list = GroupSpiderRel.queryspiderid(group_id[0].id)
        # for i in spider_list:
        #     if int(i.spider_id) in ZGZF_ID:
        #         ZGZFid_list.append(int(i.spider_id))
        #     else:
        #         Otherid_list.append(int(i.spider_id))
        # return JsonResponse({"ZGZF": ZGZFid_list, "other": Otherid_list})
        return JsonResponse({"ZGZF": ZGZFid_list})
    return HttpResponse("password is not exist.")

