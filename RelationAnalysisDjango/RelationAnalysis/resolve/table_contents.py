import numpy


def obtain_td_matrix(response):
    """
    获得td、th规则矩阵
    对colspan、rowspan自动扩充
    :param response:
    :return:
    """
    table = response
    rows = 0
    first_line = table.xpath('./th')
    if first_line:
        return obtain_td_matrix_direct_th(response, first_line)
    else:
        return obtain_td_matrix_direct_tr(response)


def obtain_td_matrix_direct_th(table, first_line):
    rows = 1
    trs = table.xpath('.//tr')

    li = []
    for one in first_line:
        line_str = remove_empty_space(''.join(one.xpath('.//text()')))
        count_list = one.xpath('./@colspan')
        if count_list:
            try:
                count = int(count_list[0])
            except Exception:
                count = 1
        else:
            count = 1
        for times in range(count):
            li.append(line_str)

    cols = len(li)
    rows += len(trs)
    matrix = numpy.empty((rows, cols), dtype=object)
    matrix[0] = li
    for row_start in range(len(trs)):
        tr = trs[row_start]
        tds = tr.xpath('./td|./th')
        for col_start in range(len(tds)):
            td = tds[col_start]
            line_str = remove_empty_space(''.join(td.xpath('.//text()')))
            colspan = td.xpath('./@colspan')
            rowspan = td.xpath('./@rowspan')
            if colspan:
                try:
                    colspan = int(colspan[0])
                except Exception:
                    colspan = 1
            else:
                colspan = 1

            if rowspan:
                try:
                    rowspan = int(rowspan[0])
                except Exception:
                    rowspan = 1
            else:
                rowspan = 1

            if colspan == cols:
                for i in range(col_start, cols):
                    if matrix[row_start][i] is None:
                        for index in range(rowspan):
                            matrix[row_start + index][i] = ''
                        colspan -= 1
                        if colspan == 0:
                            break
            for i in range(col_start, cols):
                if matrix[row_start + 1][i] is None:
                    for index in range(rowspan):
                        matrix[row_start + 1 + index][i] = line_str
                    colspan -= 1
                    if colspan == 0:
                        break

    return matrix.tolist()


def obtain_td_matrix_direct_tr(table):
    trs = table.xpath('.//tr')
    if not trs:
        return

    first_line = trs[0].xpath('./td|./th')
    if not first_line:
        return

    rows = 0
    li = []
    for one in first_line:
        line_str = remove_empty_space(''.join(one.xpath('.//text()')))
        count_list = one.xpath('./@colspan')
        if count_list:
            try:
                count = int(count_list[0])
            except Exception:
                count = 1
        else:
            count = 1
        for times in range(count):
            li.append(line_str)

    cols = len(li)
    rows += len(trs)
    matrix = numpy.empty((rows, cols), dtype=object)
    matrix[0] = li
    for row_start in range(len(trs)):
        tr = trs[row_start]
        tds = tr.xpath('./td|./th')
        for col_start in range(len(tds)):
            td = tds[col_start]
            line_str = remove_empty_space(''.join(td.xpath('.//text()')))
            colspan = td.xpath('./@colspan')
            rowspan = td.xpath('./@rowspan')
            if colspan:
                try:
                    colspan = int(colspan[0])
                except Exception:
                    colspan = 1
            else:
                colspan = 1
            if rowspan:
                try:
                    rowspan = int(rowspan[0])
                except Exception:
                    rowspan = 1
            else:
                rowspan = 1
            if colspan == cols:
                for i in range(col_start, cols):
                    if matrix[row_start][i] is None:
                        for index in range(rowspan):
                            matrix[row_start + index][i] = ''
                        colspan -= 1
                        if colspan == 0:
                            break
            for i in range(col_start, cols):
                if matrix[row_start][i] is None:
                    for index in range(rowspan):
                        matrix[row_start + index][i] = line_str
                    colspan -= 1
                    if colspan == 0:
                        break

    return matrix.tolist()


def remove_empty_space(s):
    return s.replace(' ', '').replace('\t', '').replace('\r', '').replace('\n', '').replace('\u3000', '') \
        .replace('\xa0', '').replace('/', '')