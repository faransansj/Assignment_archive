#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
템플릿 생성 스크립트

이 스크립트는 지뢰찾기 게임의 셀 템플릿 이미지를 생성합니다.
"""

import cv2
import numpy as np
import os

def create_templates(output_dir):
    """
    기본 템플릿 이미지 생성
    
    Args:
        output_dir (str): 템플릿 이미지를 저장할 디렉토리 경로
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 기본 템플릿 크기
    size = 30
    
    # 빈 셀 템플릿
    empty = np.ones((size, size), dtype=np.uint8) * 255
    cv2.imwrite(os.path.join(output_dir, 'cell_empty.png'), empty)
    
    # 미개방 셀 템플릿
    unopened = np.ones((size, size), dtype=np.uint8) * 200
    cv2.rectangle(unopened, (0, 0), (size-1, size-1), 150, 2)
    cv2.imwrite(os.path.join(output_dir, 'cell_unopened.png'), unopened)
    
    # 깃발 템플릿
    flag = np.ones((size, size), dtype=np.uint8) * 200
    cv2.rectangle(flag, (0, 0), (size-1, size-1), 150, 2)
    cv2.line(flag, (size//2, 5), (size//2, size-5), 0, 2)
    cv2.fillConvexPoly(flag, np.array([[size//2, 5], [size//2+10, 10], [size//2, 15]]), 0)
    cv2.imwrite(os.path.join(output_dir, 'cell_flag.png'), flag)
    
    # 숫자 템플릿 (1-8)
    for i in range(1, 9):
        number = np.ones((size, size), dtype=np.uint8) * 255
        cv2.putText(number, str(i), (size//3, size*2//3), cv2.FONT_HERSHEY_SIMPLEX, 0.8, 0, 2)
        cv2.imwrite(os.path.join(output_dir, f'cell_{i}.png'), number)
    
    print(f"템플릿 이미지가 {output_dir}에 생성되었습니다.")

if __name__ == "__main__":
    # 현재 디렉토리에 템플릿 생성
    create_templates(os.path.dirname(os.path.abspath(__file__)))
