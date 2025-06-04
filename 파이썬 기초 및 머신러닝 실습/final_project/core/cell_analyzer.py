#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
셀 내용 분석 모듈

이 모듈은 각 셀의 내용(숫자, 빈칸, 깃발 등)을 분석합니다.
"""

import cv2
import numpy as np
import os
import logging

class CellAnalyzer:
    """
    셀 내용 분석 클래스
    """
    
    def __init__(self, templates_dir):
        """
        CellAnalyzer 초기화
        
        Args:
            templates_dir (str): 템플릿 이미지가 저장된 디렉토리 경로
        """
        # 로거 초기화를 먼저 수행
        self.logger = logging.getLogger('minesweeper_helper')
        self.templates = self._load_templates(templates_dir)
    
    def _load_templates(self, templates_dir):
        """
        템플릿 이미지 로드
        
        Args:
            templates_dir (str): 템플릿 이미지가 저장된 디렉토리 경로
        
        Returns:
            dict: 템플릿 이름과 이미지의 딕셔너리
        """
        templates = {}
        
        # 템플릿 디렉토리가 없으면 기본 템플릿 사용
        if not os.path.exists(templates_dir):
            self.logger.warning(f"템플릿 디렉토리가 존재하지 않습니다: {templates_dir}")
            self.logger.info("기본 템플릿을 생성합니다.")
            os.makedirs(templates_dir, exist_ok=True)
            self._create_default_templates(templates_dir)
        
        # 템플릿 이미지 로드
        for filename in os.listdir(templates_dir):
            if filename.endswith('.png'):
                name = os.path.splitext(filename)[0]
                path = os.path.join(templates_dir, filename)
                try:
                    template = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                    if template is not None:
                        templates[name] = template
                        self.logger.debug(f"템플릿 로드됨: {name}")
                    else:
                        self.logger.warning(f"템플릿 로드 실패: {path}")
                except Exception as e:
                    self.logger.error(f"템플릿 로드 중 오류 발생: {str(e)}")
        
        self.logger.info(f"총 {len(templates)}개의 템플릿이 로드되었습니다.")
        return templates
    
    def _create_default_templates(self, templates_dir):
        """
        기본 템플릿 이미지 생성
        
        Args:
            templates_dir (str): 템플릿 이미지를 저장할 디렉토리 경로
        """
        # 기본 템플릿 크기
        size = 30
        
        # 빈 셀 템플릿
        empty = np.ones((size, size), dtype=np.uint8) * 255
        cv2.imwrite(os.path.join(templates_dir, 'cell_empty.png'), empty)
        
        # 미개방 셀 템플릿
        unopened = np.ones((size, size), dtype=np.uint8) * 200
        cv2.rectangle(unopened, (0, 0), (size-1, size-1), 150, 2)
        cv2.imwrite(os.path.join(templates_dir, 'cell_unopened.png'), unopened)
        
        # 깃발 템플릿
        flag = np.ones((size, size), dtype=np.uint8) * 200
        cv2.rectangle(flag, (0, 0), (size-1, size-1), 150, 2)
        cv2.line(flag, (size//2, 5), (size//2, size-5), 0, 2)
        cv2.fillConvexPoly(flag, np.array([[size//2, 5], [size//2+10, 10], [size//2, 15]]), 0)
        cv2.imwrite(os.path.join(templates_dir, 'cell_flag.png'), flag)
        
        # 숫자 템플릿 (1-8)
        for i in range(1, 9):
            number = np.ones((size, size), dtype=np.uint8) * 255
            cv2.putText(number, str(i), (size//3, size*2//3), cv2.FONT_HERSHEY_SIMPLEX, 0.8, 0, 2)
            cv2.imwrite(os.path.join(templates_dir, f'cell_{i}.png'), number)
        
        self.logger.info("기본 템플릿 생성 완료")
    
    def analyze_cells(self, image, cells):
        """
        각 셀 내용 분석
        
        Args:
            image (numpy.ndarray): 원본 이미지
            cells (list): 셀 위치 목록 [(x, y, w, h), ...]
        
        Returns:
            list: 각 셀의 내용 분석 결과
                [{'position': (x, y, w, h), 'content': 'cell_1', 'confidence': 0.95}, ...]
        """
        self.logger.debug(f"셀 내용 분석 시작 (총 {len(cells)}개 셀)")
        
        if not self.templates:
            self.logger.error("템플릿이 로드되지 않았습니다.")
            return []
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cell_contents = []
        
        for i, (x, y, w, h) in enumerate(cells):
            # 셀 영역 추출
            cell_img = gray[y:y+h, x:x+w]
            
            # 템플릿 매칭으로 셀 내용 식별
            best_match = None
            best_score = 0
            
            for name, template in self.templates.items():
                # 템플릿 크기 조정
                resized_template = cv2.resize(template, (w, h))
                
                # 템플릿 매칭
                result = cv2.matchTemplate(
                    cell_img, resized_template, cv2.TM_CCOEFF_NORMED
                )
                _, score, _, _ = cv2.minMaxLoc(result)
                
                if score > best_score:
                    best_score = score
                    best_match = name
            
            # 신뢰도가 낮으면 미개방 셀로 간주
            if best_score < 0.6:
                best_match = 'cell_unopened'
                best_score = 0.6
            
            cell_contents.append({
                'position': (x, y, w, h),
                'content': best_match,
                'confidence': best_score
            })
            
            if i % 50 == 0 and i > 0:
                self.logger.debug(f"{i}개 셀 분석 완료")
        
        self.logger.debug(f"셀 내용 분석 완료 (총 {len(cell_contents)}개 셀)")
        return cell_contents
