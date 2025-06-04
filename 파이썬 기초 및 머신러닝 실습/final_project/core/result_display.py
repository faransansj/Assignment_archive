#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
결과 표시 모듈

이 모듈은 예측된 지뢰 위치를 화면에 표시합니다.
"""

import cv2
import numpy as np
import logging

class ResultDisplay:
    """
    결과 표시 클래스
    """
    
    def __init__(self, display_mode='overlay', overlay_color=(0, 0, 255), overlay_thickness=2):
        """
        ResultDisplay 초기화
        
        Args:
            display_mode (str): 표시 모드 ('overlay', 'window', 'image')
            overlay_color (tuple): 오버레이 색상 (BGR)
            overlay_thickness (int): 오버레이 선 두께
        """
        self.display_mode = display_mode
        self.overlay_color = overlay_color
        self.overlay_thickness = overlay_thickness
        self.logger = logging.getLogger('minesweeper_helper')
    
    def display_results(self, original_image, prediction_results, cell_size):
        """
        예측 결과 표시
        
        Args:
            original_image (numpy.ndarray): 원본 이미지
            prediction_results (dict): 예측 결과
                - 'mines': 지뢰로 예측된 셀 위치 목록 [(x, y, w, h), ...]
                - 'safe_cells': 안전한 셀로 예측된 위치 목록 [(x, y, w, h), ...]
            cell_size (int): 셀 크기
        
        Returns:
            numpy.ndarray: 결과가 표시된 이미지
        """
        self.logger.debug(f"결과 표시 시작 (모드: {self.display_mode})")
        
        if self.display_mode == 'overlay':
            return self._create_overlay(original_image, prediction_results, cell_size)
        elif self.display_mode == 'image':
            return self._create_result_image(original_image, prediction_results, cell_size)
        else:
            self.logger.warning(f"지원되지 않는 표시 모드: {self.display_mode}, 기본 오버레이 모드로 대체")
            return self._create_overlay(original_image, prediction_results, cell_size)
    
    def _create_overlay(self, image, prediction_results, cell_size):
        """
        원본 이미지 위에 오버레이 생성
        
        Args:
            image (numpy.ndarray): 원본 이미지
            prediction_results (dict): 예측 결과
            cell_size (int): 셀 크기
        
        Returns:
            numpy.ndarray: 오버레이가 적용된 이미지
        """
        self.logger.debug("오버레이 생성 중")
        
        overlay = image.copy()
        
        # 지뢰 위치에 표시
        for x, y, w, h in prediction_results.get('mines', []):
            center_x = x + w // 2
            center_y = y + h // 2
            
            # X 표시
            cv2.line(
                overlay,
                (x + 5, y + 5),
                (x + w - 5, y + h - 5),
                self.overlay_color,
                self.overlay_thickness
            )
            cv2.line(
                overlay,
                (x + w - 5, y + 5),
                (x + 5, y + h - 5),
                self.overlay_color,
                self.overlay_thickness
            )
            
            # 원 표시
            cv2.circle(
                overlay, 
                (center_x, center_y), 
                cell_size // 3, 
                self.overlay_color, 
                self.overlay_thickness
            )
        
        # 안전한 셀 위치에 표시
        for x, y, w, h in prediction_results.get('safe_cells', []):
            center_x = x + w // 2
            center_y = y + h // 2
            
            # 녹색 원 표시
            cv2.circle(
                overlay, 
                (center_x, center_y), 
                cell_size // 3, 
                (0, 255, 0),  # 녹색
                self.overlay_thickness
            )
        
        self.logger.debug(f"오버레이 생성 완료 (지뢰: {len(prediction_results.get('mines', []))}, 안전: {len(prediction_results.get('safe_cells', []))})")
        return overlay
    
    def _create_result_image(self, image, prediction_results, cell_size):
        """
        결과 이미지 생성 (별도 창에 표시용)
        
        Args:
            image (numpy.ndarray): 원본 이미지
            prediction_results (dict): 예측 결과
            cell_size (int): 셀 크기
        
        Returns:
            numpy.ndarray: 결과 이미지
        """
        self.logger.debug("결과 이미지 생성 중")
        
        # 오버레이와 유사하지만 별도 이미지로 생성
        result_image = image.copy()
        
        # 반투명 오버레이 레이어
        overlay = result_image.copy()
        alpha = 0.3  # 투명도
        
        # 지뢰 위치에 표시
        for x, y, w, h in prediction_results.get('mines', []):
            # 빨간색 반투명 사각형
            cv2.rectangle(
                overlay,
                (x, y),
                (x + w, y + h),
                (0, 0, 255),  # 빨간색
                -1  # 채우기
            )
            
            # X 표시
            cv2.line(
                result_image,
                (x + 5, y + 5),
                (x + w - 5, y + h - 5),
                (0, 0, 255),
                2
            )
            cv2.line(
                result_image,
                (x + w - 5, y + 5),
                (x + 5, y + h - 5),
                (0, 0, 255),
                2
            )
        
        # 안전한 셀 위치에 표시
        for x, y, w, h in prediction_results.get('safe_cells', []):
            # 녹색 반투명 사각형
            cv2.rectangle(
                overlay,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),  # 녹색
                -1  # 채우기
            )
            
            # 체크 표시
            center_x = x + w // 2
            center_y = y + h // 2
            cv2.circle(
                result_image, 
                (center_x, center_y), 
                cell_size // 4, 
                (0, 255, 0), 
                2
            )
        
        # 반투명 오버레이 적용
        cv2.addWeighted(overlay, alpha, result_image, 1 - alpha, 0, result_image)
        
        # 결과 정보 텍스트 추가
        mines_count = len(prediction_results.get('mines', []))
        safe_count = len(prediction_results.get('safe_cells', []))
        
        cv2.putText(
            result_image,
            f"Mines: {mines_count}, Safe: {safe_count}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )
        
        self.logger.debug("결과 이미지 생성 완료")
        return result_image
