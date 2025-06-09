#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
로깅 유틸리티 모듈

이 모듈은 로깅 관련 유틸리티 함수를 제공합니다.
"""

import logging
import os
from datetime import datetime

def setup_logger(log_dir='logs', log_level=logging.INFO):
    """
    로거 설정
    
    Args:
        log_dir (str): 로그 파일 저장 디렉토리
        log_level: 로깅 레벨
    
    Returns:
        logging.Logger: 설정된 로거 객체
    """
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(log_dir, f'minesweeper_helper_{timestamp}.log')
    
    # 로거 설정
    logger = logging.getLogger('minesweeper_helper')
    logger.setLevel(log_level)
    
    # 기존 핸들러 제거
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # 파일 핸들러
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(log_level)
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # 포맷 설정
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 핸들러 추가
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info(f"로거 설정 완료 (로그 파일: {log_file})")
    return logger

def get_logger():
    """
    설정된 로거 반환
    
    Returns:
        logging.Logger: 설정된 로거 객체
    """
    return logging.getLogger('minesweeper_helper')
