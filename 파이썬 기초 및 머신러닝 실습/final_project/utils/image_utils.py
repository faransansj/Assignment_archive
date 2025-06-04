#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
이미지 처리 유틸리티 모듈

이 모듈은 이미지 처리 관련 유틸리티 함수를 제공합니다.
"""

import cv2
import numpy as np
import logging

logger = logging.getLogger('minesweeper_helper')

def resize_image(image, scale_percent):
    """
    이미지 크기 조정
    
    Args:
        image (numpy.ndarray): 원본 이미지
        scale_percent (float): 크기 조정 비율 (%)
    
    Returns:
        numpy.ndarray: 크기가 조정된 이미지
    """
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

def show_image(image, window_name='Image', wait=True):
    """
    이미지 표시 (디버깅용)
    
    Args:
        image (numpy.ndarray): 표시할 이미지
        window_name (str): 창 이름
        wait (bool): 키 입력 대기 여부
    """
    cv2.imshow(window_name, image)
    if wait:
        cv2.waitKey(0)
        cv2.destroyWindow(window_name)

def save_image(image, filename):
    """
    이미지 저장
    
    Args:
        image (numpy.ndarray): 저장할 이미지
        filename (str): 파일 경로
    
    Returns:
        bool: 저장 성공 여부
    """
    try:
        cv2.imwrite(filename, image)
        logger.debug(f"이미지 저장됨: {filename}")
        return True
    except Exception as e:
        logger.error(f"이미지 저장 중 오류 발생: {str(e)}")
        return False

def crop_image(image, x, y, width, height):
    """
    이미지 자르기
    
    Args:
        image (numpy.ndarray): 원본 이미지
        x (int): 시작 x 좌표
        y (int): 시작 y 좌표
        width (int): 너비
        height (int): 높이
    
    Returns:
        numpy.ndarray: 잘린 이미지
    """
    return image[y:y+height, x:x+width]

def draw_grid(image, grid_origin, cell_size, rows, cols, color=(0, 255, 0), thickness=1):
    """
    이미지에 격자 그리기
    
    Args:
        image (numpy.ndarray): 원본 이미지
        grid_origin (tuple): 격자 원점 (x, y)
        cell_size (int): 셀 크기
        rows (int): 행 수
        cols (int): 열 수
        color (tuple): 선 색상 (BGR)
        thickness (int): 선 두께
    
    Returns:
        numpy.ndarray: 격자가 그려진 이미지
    """
    result = image.copy()
    x0, y0 = grid_origin
    
    # 수평선
    for i in range(rows + 1):
        y = y0 + i * cell_size
        cv2.line(result, (x0, y), (x0 + cols * cell_size, y), color, thickness)
    
    # 수직선
    for i in range(cols + 1):
        x = x0 + i * cell_size
        cv2.line(result, (x, y0), (x, y0 + rows * cell_size), color, thickness)
    
    return result

def add_text_overlay(image, text, position=(10, 30), font=cv2.FONT_HERSHEY_SIMPLEX, 
                    font_scale=1, color=(255, 255, 255), thickness=2):
    """
    이미지에 텍스트 오버레이 추가
    
    Args:
        image (numpy.ndarray): 원본 이미지
        text (str): 표시할 텍스트
        position (tuple): 텍스트 위치 (x, y)
        font: 폰트
        font_scale (float): 폰트 크기
        color (tuple): 텍스트 색상 (BGR)
        thickness (int): 텍스트 두께
    
    Returns:
        numpy.ndarray: 텍스트가 추가된 이미지
    """
    result = image.copy()
    cv2.putText(result, text, position, font, font_scale, color, thickness)
    return result
