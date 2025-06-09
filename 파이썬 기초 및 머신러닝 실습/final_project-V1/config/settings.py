#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
설정 모듈

이 모듈은 애플리케이션의 설정을 관리합니다.
기본 설정 정의, 사용자 설정 저장 및 로드 기능을 제공합니다.
"""

import json
import os
from pathlib import Path

# 기본 설정
DEFAULT_SETTINGS = {
    'capture_mode': 'active_window',  # 'full_screen', 'active_window', 'region'
    'display_mode': 'overlay',        # 'overlay', 'window', 'image'
    'overlay_color': (255, 0, 0),     # 빨간색 (BGR)
    'overlay_thickness': 2,
    'debug_mode': False,
    'capture_region': None,           # 캡처 영역 (x1, y1, x2, y2)
}

def get_settings_path():
    """
    설정 파일 경로 반환
    
    Returns:
        str: 설정 파일의 절대 경로
    """
    config_dir = Path(__file__).parent.absolute()
    return os.path.join(config_dir, 'user_settings.json')

def load_settings():
    """
    사용자 설정 파일 로드, 없으면 기본 설정 반환
    
    Returns:
        dict: 로드된 설정 (기본 설정 + 사용자 설정)
    """
    settings_path = get_settings_path()
    
    if os.path.exists(settings_path):
        try:
            with open(settings_path, 'r', encoding='utf-8') as f:
                user_settings = json.load(f)
                # 기본 설정에 사용자 설정 덮어쓰기
                settings = DEFAULT_SETTINGS.copy()
                settings.update(user_settings)
                return settings
        except (json.JSONDecodeError, IOError) as e:
            print(f"설정 파일 로드 중 오류 발생: {str(e)}")
            return DEFAULT_SETTINGS
    
    return DEFAULT_SETTINGS

def save_settings(settings):
    """
    사용자 설정 저장
    
    Args:
        settings (dict): 저장할 설정
    
    Returns:
        bool: 저장 성공 여부
    """
    settings_path = get_settings_path()
    
    try:
        # 기본 설정과 다른 값만 저장
        user_settings = {}
        for key, value in settings.items():
            if key in DEFAULT_SETTINGS and value != DEFAULT_SETTINGS[key]:
                user_settings[key] = value
        
        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(user_settings, f, indent=4, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"설정 파일 저장 중 오류 발생: {str(e)}")
        return False

def reset_settings():
    """
    설정을 기본값으로 초기화
    
    Returns:
        bool: 초기화 성공 여부
    """
    return save_settings(DEFAULT_SETTINGS)
