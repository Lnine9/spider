import os
import random
import fitz
import numpy as np

from RelationAnalysisDjango import settings
from RelationAnalysisDjango.server.get_table_in_pic import read_img


def get_file():
    files = os.listdir()  # 默认访问的是当前路径
    lis = [file for file in files if os.path.splitext(file)[1] == '.pdf']
    return lis


def conver_img(pdf_address):
    pic_list = []
    doc = fitz.open(pdf_address)
    pdf_name = os.path.splitext(pdf_address)[0].split("/")[-1]  # 取文件名字
    pdflength = doc.pageCount  # pdf 图片数量
    for pg in range(pdflength):
        page = doc[pg]
        rotate = int(0)
        zoom_x, zoom_y = 1, 1  # 提高分辨率
        trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pm = page.getPixmap(matrix=trans, alpha=False)
        pdfitemname = ranstr(16) + str((pg + 1))  # 图片名称
        pm.writePNG(settings.MEDIA_ROOT + '/' + '%s.png' % pdfitemname)  # 生成图片到本地
        pic_list.append(settings.MEDIA_ROOT + '/' + pdfitemname + ".png")
    return pic_list


def delete_img(pic_list):
    for x in pic_list:
        os.remove(x)


def delete_re_and_sim(item):
    return_list = []
    for x in item:
        if len(return_list) == 0:
            return_list.append(x)
        elif x - return_list[len(return_list) - 1] > 2:
            return_list.append(x)
    return return_list


def get_table_mes(text):
    triangle = text[0]
    triangle = np.array(triangle)
    row = triangle[:, 0]
    col = triangle[:, 1]
    col.sort()
    col = delete_re_and_sim(col)
    row = delete_re_and_sim(row)
    if len(col) > 3 and len(row) > 3:
        table = [["" for col in range(len(col) - 1)] for row in range(len(row) - 1)]
        mes_col = 0
        mes_row = 0
        for item in text[1:]:
            left_top = item[0][0]
            right_down = item[0][2]
            mes_index = [(left_top[0] + right_down[0]) / 2, (left_top[1] + right_down[1]) / 2]

            for index, x in enumerate(col):
                if not mes_index[0] + col[0] >= x:
                    mes_col = index - 1
                    break
            for index, y in enumerate(row):
                if not mes_index[1] + row[0] >= y:
                    mes_row = index - 1
                    break

            table[mes_row][mes_col] = table[mes_row][mes_col] + str(item[1][0])
        return table

def remove_table_null(table):
    return_table = []
    for item in table:
        per_table = []
        for row in item:
            is_null = True
            for col in row:
                if col != '':
                    is_null = False
            if not is_null:
                per_table.append(row)
        if per_table:
            return_table.append(per_table)
    return return_table



def table_to_json(text):
    table_list = []
    return_json = []
    for table in text:
        title = table[0:1][0]
        for row_index, row in enumerate(table[1:]):
            table_mes = {}
            mes = str(row)
            if '合计' in mes:
                break
            for col_index, col in enumerate(row):
                if ('名称' in title[col_index] or '产品' in title[col_index]) and '制造商名称' not in title[col_index]:
                    table_mes['采购目录'] = table[row_index + 1][col_index]
                if '品牌' in title[col_index]:
                    table_mes['中标品牌'] = table[row_index + 1][col_index]
                if '数量' in title[col_index]:
                    table_mes['数量'] = table[row_index + 1][col_index]
                if '型号' in title[col_index]:
                    table_mes['型号'] = table[row_index + 1][col_index]
                if '单位' in title[col_index]:
                    table_mes['单位'] = table[row_index + 1][col_index]
                if '单价' in title[col_index]:
                    table_mes['中标单价'] = table[row_index + 1][col_index]
                if '金额' in title[col_index] or '总价' in title[col_index]:
                    table_mes['中标总金额'] = table[row_index + 1][col_index]
                if '备注' in title[col_index]:
                    table_mes['简要信息'] = table[row_index + 1][col_index]
            if '采购目录' in table_mes.keys() and table_mes.get('采购目录') != '' and len(table_mes) > 1:
                return_json.append(table_mes)
    return return_json


def input_pdf(pdf):
    img_list = conver_img(pdf)  # 图片路径
    table_list = []
    text = read_img(img_list)
    for x in text:
        item = get_table_mes(x)
        if item is not None:
            table_list.append(item)

    table_list = remove_table_null(table_list)
    json = table_to_json(table_list)
    delete_img(img_list)
    return json


def ranstr(num):
    H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

    salt = ''
    for i in range(num):
        salt += random.choice(H)

    return salt