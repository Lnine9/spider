import math
import cv2 as cv
from math import *
import numpy as np
from paddleocr import PaddleOCR



def rotate(pic,degree):
    """
    :param pic:
    :param degree:旋转角度
    :return: 矫正后的图片
    """
    img = pic
    img = np.array(img)
    height, width = img.shape[:2]

    # 旋转后的尺寸
    heightNew = int(width * fabs(sin(radians(degree))) + height * fabs(cos(radians(degree))))
    widthNew = int(height * fabs(sin(radians(degree))) + width * fabs(cos(radians(degree))))

    matRotation = cv.getRotationMatrix2D((width / 2, height / 2), degree, 1)
    matRotation[0, 2] += (widthNew - width) / 2
    matRotation[1, 2] += (heightNew - height) / 2

    imgRotation = cv.warpAffine(img, matRotation, (widthNew, heightNew),borderValue=(255,255,255))
    # cv.imshow("img", img)
    # cv.imshow("imgRotation", imgRotation)
    # cv.waitKey(0)

    return imgRotation


def getBinary(img):
    '''
    :param img:
    :return: 二值化图片b
    '''
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    binary = cv.adaptiveThreshold(~gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 15, -2)
    # cv.imshow("binary", gray)
    # cv.waitKey(0)
    return binary


def getRowsAndCols(rows, cols, binary):
    '''
    :param binary:
    :return:横线图和竖线图
    '''
    horizontal = binary.copy()
    vertical = binary.copy()

    # cols/scale获取横线
    horizontalSize = int(horizontal.shape[1] / 40)
    horizontalStructure = cv.getStructuringElement(cv.MORPH_RECT, (horizontalSize, 1))
    horizontal = cv.erode(horizontal, horizontalStructure)
    dilated_row = cv.dilate(horizontal, horizontalStructure)

    # rows/scale获取竖线
    verticalsize = int(vertical.shape[1] / 20)
    verticalStructure = cv.getStructuringElement(cv.MORPH_RECT, (1, verticalsize))
    vertical = cv.erode(vertical, verticalStructure, (-1, -1))
    dilated_col = cv.dilate(vertical, verticalStructure, (-1, -1))

    return dilated_row, dilated_col


def cutOutTable(img, frame):
    '''
    :param img:原图
    :param frame:表格轮廓
    :return:
    '''
    # 获取交点
    all_cut = []
    contours, hierarchy = cv.findContours(frame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv.contourArea, reverse=True)
    for i in range(len(contours)):
        area0 = cv.contourArea(contours[i])
        if area0 < 20: continue
        epsilon = 0.1 * cv.arcLength(contours[i], True)
        approx = cv.approxPolyDP(contours[i], epsilon, True)  # 获取近似轮廓
        x1, y1, w1, h1 = cv.boundingRect(approx)
        roi = frame[int(y1):int(y1 + h1), int(x1):int(x1 + w1)]
        roi_contours, hierarchy = cv.findContours(roi, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
        if len(roi_contours) < 4: continue
        # 将原图上的表格切割出来
        cut_img = img[y1:y1 + h1, x1:x1 + w1]
        # cv.imshow("cut_img",cut_img)
        # cv.waitKey(0)
        all_cut.append(cut_img)
    return all_cut


def getFrame(dilated_row, dilated_col):
    '''
    :param dilated_row:
    :param dilated_col:
    :return: 表格框架,交点
    '''
    frame = cv.add(dilated_row, dilated_col)
    frame=dilated_col+dilated_row
    # cv.imshow("frame",frame)

    bitwise_and = cv.bitwise_and(dilated_row, dilated_col)
    # cv.imshow("points",bitwise_and)
    # cv.waitKey(0)
    return frame, bitwise_and


def splitTable(img, points):
    """
    将表格进行分块切割
    :param img:
    :param points:
    :return:
    """

    ys, xs = np.where(points > 10)

    mylisty = []  # 纵坐标集合
    mylistx = []  # 横坐标集合

    ocr = PaddleOCR(use_angle_cls=True, lang="ch")

    i = 0
    myxs = np.sort(xs)

    for i in range(len(myxs) - 1):
        if myxs[i + 1] - myxs[i] > 10:
            mylistx.append(myxs[i])
        i = i + 1
    mylistx.append(myxs[i])

    i = 0
    myys = np.sort(ys)

    for i in range(len(myys) - 1):
        if myys[i + 1] - myys[i] > 10:
            mylisty.append(myys[i])
        i = i + 1
    mylisty.append(myys[i])

    k = 0
    text_list = []
    for i in range(len(mylisty) - 1):
        for j in range(len(mylistx) - 1):
            ROI = img[mylisty[i]+3:mylisty[i + 1]-3, mylistx[j]+3:mylistx[j + 1]-3]
            k = k + 1

            # cv.imshow('xx', ROI)
            # cv.waitKey(0)
            result = ocr.ocr(ROI, cls=True)
            textstr = ""

            for line in result:
                textstr += line[1][0]
            text_list.append(textstr)
    return text_list


def read_img(img_list):
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")
    text = []
    for img_src in img_list:
        img = cv.imread(img_src)
        img_cropped = img[10:750, 10:660]
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        edges = cv.Canny(gray,50,150,apertureSize = 3)

        #霍夫变换获取旋转角度
        lines = cv.HoughLines(edges,1,np.pi/180,0)
        rotate_angle=0
        for rho,theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            if x1 == x2 or y1 == y2:
                continue
            t = float(y2-y1)/(x2-x1)
            rotate_angle = math.degrees(math.atan(t))
            if rotate_angle > 45:
                rotate_angle = -90 + rotate_angle
            elif rotate_angle < -45:
                rotate_angle = 90 + rotate_angle

        ro_img=rotate(img_cropped,rotate_angle)

        binary_img = getBinary(ro_img)
        # 获取图片长和宽
        rows, cols = binary_img.shape
        # 获取横线竖线图
        img_row, img_col = getRowsAndCols(rows, cols, binary_img)
        # 获取表格轮廓和交点
        frame_img, points = getFrame(img_row, img_col)
        point_list = []
        for x, item in enumerate(points):
            for y, item1 in enumerate(item):
                if item1 == 255:
                    point_list.append([x, y])
        table_list = cutOutTable(ro_img, frame_img)
        # text.append(splitTable(ro_img, points)
        pic_msg = []
        pic_msg.append(point_list)
        for table in table_list:
            result = ocr.ocr(table, cls=True)
            for line in result:
                pic_msg.append(line)
        if len(table_list) != 0 and str(pic_msg).replace('[', '').replace(']', '') != '':
            text.append(pic_msg)
    return text



