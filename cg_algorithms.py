#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
import math


def draw_line(p_list, algorithm):
    """绘制线段

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'，此处的'Naive'仅作为示例，测试时不会出现
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
    if algorithm == 'Naive':
        if x0 == x1:
            for y in range(min(y0, y1), max(y0, y1) + 1):
                result.append((x0, y))  
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1 - y0) / (x1 - x0)
            for x in range(x0, x1 + 1):
                result.append((x, int(y0 + k * (x - x0))))

    elif algorithm == 'DDA':
        if x0 == x1:
            for y in range(min(y0, y1), max(y0, y1) + 1):
                result.append((x0, y))
        else:
            m = (y1 - y0) / (x1 - x0)
            result.append((x0, y0))
            if abs(m) <= 1:
                if x0 > x1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                y = y0
                for x in range(x0 + 1, x1 + 1):
                    y = y + m
                    result.append((x, round(y)))
            else:
                if y0 > y1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                x = x0
                for y in range(y0 + 1, y1 + 1):
                    x = x + 1/m
                    result.append((round(x), y))                                 

    elif algorithm == 'Bresenham':
        if x0 == x1:
            for y in range(min(y0, y1), max(y0, y1) + 1):
                result.append((x0, y))
        elif y0 == y1:
            for x in range(min(x0, x1), max(x0, x1) + 1):
                result.append((x, y0))
        elif x1 - x0 == y1 - y0:
            for i in range(x1 + 1 - x0):
                result.append((x0 + i, y0 + i))
        elif x1 - x0 == -(y1 - y0):
            for i in range(x1 + 1 - x0):
                result.append((x0 + i, y0 - i))
        else:
            result.append((x0, y0))
            delta_x = abs(x1 - x0)
            delta_y = abs(y1 - y0)
            m = delta_y / delta_x
            sign = int((y1 - y0) / (x1 - x0) / m)
            if m < 1:
                if x0 > x1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                p = 2 * delta_y - delta_x
                y = y0
                for x in range(x0 + 1, x1 + 1):
                    if(p <= 0):
                        result.append((x, y))
                        p += 2 * delta_y
                    else:
                        y += sign
                        result.append((x, y))
                        p += 2 * delta_y - 2 * delta_x
            else:
                if y0 > y1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                p = 2 * delta_x - delta_y
                x = x0
                for y in range(y0 + 1, y1 + 1):
                    if(p <= 0):
                        result.append((x, y))
                        p += 2 * delta_x
                    else:
                        x += sign
                        result.append((x, y))
                        p += 2 * delta_x - 2 * delta_y                   

    return result


def draw_polygon(p_list, algorithm):
    """绘制多边形

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)
        result += line
    return result


def draw_ellipse(p_list):
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    xc, yc = int((x0 + x1) / 2), int((y0 + y1) / 2)
    rx, ry = int(abs(x1 - x0) / 2), int(abs(y1 - y0) / 2)
    p = ry**2 - rx**2 * ry + rx**2 / 4 
    x, y = 0, ry
    result.append((x + xc, y + yc))
    result.append((x + xc, -y + yc))
    while ry**2 * x < rx**2 * y:
        x += 1
        if p < 0:
            p += 2 * ry**2 * x + ry**2
        else:
            y += -1
            p += 2 * ry**2 * x - 2 * rx**2 * y + ry**2
        result.append((x + xc, y + yc))
        result.append((-x + xc, y + yc))
        result.append((x + xc, -y + yc))
        result.append((-x + xc, -y + yc)) 
    p = ry**2 * (x + 1/2)**2 + rx**2 * (y - 1)**2 - rx**2 * ry**2
    while y >= 0:
        y += -1
        if p > 0:
            p += rx**2 - 2 * rx**2 * y
        else:
            x += 1
            p += 2 * ry**2 * x - 2 * rx**2 * y + rx**2
        result.append((x + xc, y + yc))
        result.append((-x + xc, y + yc))
        result.append((x + xc, -y + yc))
        result.append((-x + xc, -y + yc)) 
    return result


def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result, points = [], []
    x, y = [], []
    n = len(p_list)
    for i in range(n):
        x.append (p_list[i][0])
        y.append (p_list[i][1])
        if i != 0:
            result.extend(draw_line([[x[i],y[i]], [x[i - 1], y[i - 1]]], "DDA"))
    if algorithm == "Bezier":
        for u in range(0, 100):
            u = u / 100
            px, py = x, y
            for i in range(1, n):
                for j in range(n - i):
                    px[j] = (1 - u) * px[j] + u * px[j + 1]
                    py[j] = (1 - u) * py[j] + u * py[j + 1]
            points.append((round(px[0]), round(py[0])))
    elif algorithm == "B-spline":
        pass
    ##points = list(set(points))
    for i in range(len(points) - 1):
        points_list = [points[i], points[i + 1]]
        result.extend(draw_line(points_list, "DDA"))
    return result


def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    pass


def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    pass


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    pass


def clip(p_list, x_min, y_min, x_max, y_max, algorithm):
    """线段裁剪

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param x_min: 裁剪窗口左上角x坐标
    :param y_min: 裁剪窗口左上角y坐标
    :param x_max: 裁剪窗口右下角x坐标
    :param y_max: 裁剪窗口右下角y坐标
    :param algorithm: (string) 使用的裁剪算法，包括'Cohen-Sutherland'和'Liang-Barsky'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1]]) 裁剪后线段的起点和终点坐标
    """
    pass
