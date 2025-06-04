#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
게임 격자 감지 모듈

이 모듈은 지뢰찾기 게임의 격자 구조를 감지하고 각 셀의 위치를 추출합니다.
"""

import cv2
import numpy as np
import logging

class GridDetector:
    """
    게임 격자 감지 클래스
    """
    
    def __init__(self):
        """
        GridDetector 초기화
        """
        self.cell_size = None  # 감지된 셀 크기
        self.logger = logging.getLogger('minesweeper_helper')
    
    def detect_grid(self, processed_images):
        """
        게임 격자 감지 및 각 셀 위치 반환
        
        Args:
            processed_images (dict): 전처리된 이미지들의 딕셔너리
                - 'original': 원본 이미지
                - 'gray': 그레이스케일 이미지
                - 'blurred': 블러 처리된 이미지
                - 'thresh': 이진화된 이미지
        
        Returns:
            dict: 격자 정보
                - 'cells': 감지된 셀 목록 [(x, y, w, h), ...]
                - 'cell_size': 셀 크기
                - 'grid_origin': 격자 원점 (x, y)
                - 'grid_dimensions': 격자 차원 (rows, cols)
        """
        self.logger.debug("게임 격자 감지 시작")
        
        thresh = processed_images['thresh']
        original = processed_images['original']
        
        # 윤곽선 검출
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        self.logger.debug(f"윤곽선 {len(contours)}개 검출됨")
        
        # 셀 후보 필터링 (크기, 비율 등)
        cells = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            # 셀 크기 및 비율 조건 확인
            if w > 10 and h > 10 and 0.8 < w/h < 1.2:
                cells.append((x, y, w, h))
        
        self.logger.debug(f"셀 후보 {len(cells)}개 필터링됨")
        
        if not cells:
            self.logger.warning("셀이 감지되지 않았습니다.")
            return {
                'cells': [],
                'cell_size': None,
                'grid_origin': None,
                'grid_dimensions': None
            }
        
        # 셀 크기 추정 (최빈값 사용)
        widths = [w for _, _, w, _ in cells]
        heights = [h for _, _, _, h in cells]
        
        # 최빈값 계산 함수
        def get_mode(values):
            counts = {}
            for value in values:
                if value in counts:
                    counts[value] += 1
                else:
                    counts[value] = 1
            return max(counts.items(), key=lambda x: x[1])[0]
        
        # 셀 크기 추정
        cell_width = get_mode(widths)
        cell_height = get_mode(heights)
        self.cell_size = (cell_width + cell_height) // 2
        
        # 격자 원점 및 차원 추정
        min_x = min(x for x, _, _, _ in cells)
        min_y = min(y for _, y, _, _ in cells)
        max_x = max(x + w for x, _, w, _ in cells)
        max_y = max(y + h for _, y, _, h in cells)
        
        grid_x = min_x
        grid_y = min_y
        
        # 격자 차원 (행, 열) 추정
        cols = (max_x - min_x) // self.cell_size + 1
        rows = (max_y - min_y) // self.cell_size + 1
        
        self.logger.debug(f"격자 감지 완료: {rows}x{cols} 격자, 셀 크기 {self.cell_size}px")
        
        # 셀 위치 정규화 (격자에 맞추기)
        normalized_cells = []
        for row in range(rows):
            for col in range(cols):
                x = grid_x + col * self.cell_size
                y = grid_y + row * self.cell_size
                normalized_cells.append((x, y, self.cell_size, self.cell_size))
        
        return {
            'cells': normalized_cells,
            'cell_size': self.cell_size,
            'grid_origin': (grid_x, grid_y),
            'grid_dimensions': (rows, cols)
        }
