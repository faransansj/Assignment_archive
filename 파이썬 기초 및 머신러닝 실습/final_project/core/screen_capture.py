#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
화면 캡처 모듈

이 모듈은 화면 캡처 기능을 제공합니다.
전체 화면, 활성 창, 지정 영역 등 다양한 캡처 모드를 지원합니다.
"""

import cv2
import numpy as np
import platform
import logging

# 운영체제별 화면 캡처 라이브러리 임포트
system = platform.system()

if system == 'Windows':
    import win32gui
    import win32ui
    import win32con
    from PIL import ImageGrab
elif system == 'Darwin':  # macOS
    from PIL import ImageGrab
else:  # Linux
    import pyscreenshot as ImageGrab

class ScreenCapture:
    """
    화면 캡처 클래스
    """
    
    def __init__(self, capture_mode='full_screen'):
        """
        ScreenCapture 초기화
        
        Args:
            capture_mode (str): 캡처 모드 ('full_screen', 'active_window', 'region')
        """
        self.capture_mode = capture_mode
        self.region = None
        self.logger = logging.getLogger('minesweeper_helper')
    
    def set_region(self, region):
        """
        캡처 영역 설정
        
        Args:
            region (tuple): 캡처 영역 (x1, y1, x2, y2)
        """
        self.region = region
    
    def capture(self):
        """
        화면 캡처 실행
        
        Returns:
            numpy.ndarray: 캡처된 이미지 (BGR 형식)
        """
        if self.capture_mode == 'full_screen':
            return self._capture_full_screen()
        elif self.capture_mode == 'active_window':
            return self._capture_active_window()
        elif self.capture_mode == 'region' and self.region:
            return self._capture_region(self.region)
        else:
            self.logger.warning(f"지원되지 않는 캡처 모드: {self.capture_mode}, 전체 화면 캡처로 대체")
            return self._capture_full_screen()
    
    def _capture_full_screen(self):
        """
        전체 화면 캡처
        
        Returns:
            numpy.ndarray: 캡처된 이미지 (BGR 형식)
        """
        self.logger.debug("전체 화면 캡처 시작")
        
        try:
            # PIL ImageGrab으로 화면 캡처
            screenshot = ImageGrab.grab()
            # PIL 이미지를 NumPy 배열로 변환
            image = np.array(screenshot)
            # RGB -> BGR 변환 (OpenCV 형식)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            self.logger.debug(f"전체 화면 캡처 완료: {image.shape[1]}x{image.shape[0]}")
            return image
        except Exception as e:
            self.logger.error(f"전체 화면 캡처 중 오류 발생: {str(e)}")
            # 빈 이미지 반환
            return np.zeros((100, 100, 3), dtype=np.uint8)
    
    def _capture_active_window(self):
        """
        활성 창 캡처
        
        Returns:
            numpy.ndarray: 캡처된 이미지 (BGR 형식)
        """
        self.logger.debug("활성 창 캡처 시작")
        
        try:
            if system == 'Windows':
                # Windows에서는 win32 API 사용
                hwnd = win32gui.GetForegroundWindow()
                left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                width = right - left
                height = bottom - top
                
                # 창 DC 가져오기
                hwndDC = win32gui.GetWindowDC(hwnd)
                mfcDC = win32ui.CreateDCFromHandle(hwndDC)
                saveDC = mfcDC.CreateCompatibleDC()
                
                # 비트맵 생성
                saveBitMap = win32ui.CreateBitmap()
                saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
                saveDC.SelectObject(saveBitMap)
                
                # 창 내용 비트맵에 복사
                saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
                
                # 비트맵을 NumPy 배열로 변환
                bmpinfo = saveBitMap.GetInfo()
                bmpstr = saveBitMap.GetBitmapBits(True)
                img = np.frombuffer(bmpstr, dtype=np.uint8)
                img.shape = (bmpinfo['bmHeight'], bmpinfo['bmWidth'], 4)
                
                # 리소스 해제
                win32gui.DeleteObject(saveBitMap.GetHandle())
                saveDC.DeleteDC()
                mfcDC.DeleteDC()
                win32gui.ReleaseDC(hwnd, hwndDC)
                
                # BGRA -> BGR 변환
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            else:
                # 다른 OS에서는 전체 화면 캡처 후 활성 창 영역 추출 (간단한 구현)
                # 실제로는 OS별 API를 사용하여 정확한 활성 창 캡처 구현 필요
                self.logger.warning("현재 OS에서는 정확한 활성 창 캡처가 지원되지 않습니다. 전체 화면 캡처로 대체합니다.")
                img = self._capture_full_screen()
            
            self.logger.debug(f"활성 창 캡처 완료: {img.shape[1]}x{img.shape[0]}")
            return img
        except Exception as e:
            self.logger.error(f"활성 창 캡처 중 오류 발생: {str(e)}")
            # 오류 발생 시 전체 화면 캡처로 대체
            self.logger.info("전체 화면 캡처로 대체합니다.")
            return self._capture_full_screen()
    
    def _capture_region(self, region):
        """
        지정 영역 캡처
        
        Args:
            region (tuple): 캡처 영역 (x1, y1, x2, y2)
        
        Returns:
            numpy.ndarray: 캡처된 이미지 (BGR 형식)
        """
        self.logger.debug(f"지정 영역 캡처 시작: {region}")
        
        try:
            x1, y1, x2, y2 = region
            
            # PIL ImageGrab으로 지정 영역 캡처
            screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            # PIL 이미지를 NumPy 배열로 변환
            image = np.array(screenshot)
            # RGB -> BGR 변환 (OpenCV 형식)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            self.logger.debug(f"지정 영역 캡처 완료: {image.shape[1]}x{image.shape[0]}")
            return image
        except Exception as e:
            self.logger.error(f"지정 영역 캡처 중 오류 발생: {str(e)}")
            # 오류 발생 시 전체 화면 캡처로 대체
            self.logger.info("전체 화면 캡처로 대체합니다.")
            return self._capture_full_screen()
