#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
이미지 처리 모듈

이 모듈은 캡처된 이미지를 전처리하는 기능을 제공합니다.
그레이스케일 변환, 노이즈 제거, 이진화 등의 작업을 수행합니다.
"""

import cv2
import numpy as np
import logging

class ImageProcessor:
    """
    이미지 처리 클래스
    """
    
    def __init__(self):
        """
        ImageProcessor 초기화
        """
        self.logger = logging.getLogger('minesweeper_helper')
    
    def preprocess(self, image):
        """
        이미지 전처리 (그레이스케일 변환, 노이즈 제거 등)
        
        Args:
            image (numpy.ndarray): 원본 이미지 (BGR 형식)
        
        Returns:
            dict: 전처리된 이미지들의 딕셔너리
                - 'original': 원본 이미지
                - 'gray': 그레이스케일 이미지
                - 'blurred': 블러 처리된 이미지
                - 'thresh': 이진화된 이미지
        """
        self.logger.debug("이미지 전처리 시작")
        
        # 그레이스케일 변환
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.logger.debug("그레이스케일 변환 완료")
        
        # 노이즈 제거 (가우시안 블러)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        self.logger.debug("노이즈 제거 완료")
        
        # 이진화 (Adaptive Thresholding)
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, 11, 2
        )
        self.logger.debug("이진화 완료")
        
        return {
            'original': image,
            'gray': gray,
            'blurred': blurred,
            'thresh': thresh
        }
