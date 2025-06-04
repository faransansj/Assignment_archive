#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
지뢰찾기 헬퍼 GUI 애플리케이션

이 모듈은 지뢰찾기 헬퍼의 GUI 인터페이스를 제공합니다.
버튼 클릭으로 화면 캡처 및 분석을 시작하고, 원본 이미지와 결과 이미지를 나란히 표시합니다.
"""

import os
import sys
import time
import logging
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import cv2
import numpy as np
from pathlib import Path

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

# 내부 모듈 임포트
from config.settings import load_settings, save_settings
from core.screen_capture import ScreenCapture
from core.image_processor import ImageProcessor
from core.grid_detector import GridDetector
from core.cell_analyzer import CellAnalyzer
from core.mine_predictor import MinePredictor
from core.result_display import ResultDisplay
from utils.logging_utils import setup_logger
from utils.image_utils import save_image

class MinesweeperHelperGUI:
    """
    지뢰찾기 헬퍼 GUI 클래스
    """
    
    def __init__(self, root):
        """
        GUI 초기화
        
        Args:
            root (tk.Tk): Tkinter 루트 객체
        """
        self.root = root
        self.root.title("지뢰찾기 헬퍼 GUI")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # 설정 로드
        self.settings = load_settings()
        
        # 로거 설정
        log_dir = os.path.join(project_root, 'logs')
        self.logger = setup_logger(log_dir)
        self.logger.info("지뢰찾기 헬퍼 GUI 시작")
        
        # 이미지 저장 변수
        self.original_image = None
        self.result_image = None
        
        # 분석 스레드
        self.analysis_thread = None
        self.is_analyzing = False
        
        # GUI 구성
        self.setup_ui()
        
        # 종료 시 정리
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        """
        UI 구성
        """
        # 메인 프레임
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 상단 프레임 (버튼 및 상태)
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=5)
        
        # 캡처 버튼
        self.capture_btn = ttk.Button(
            top_frame, 
            text="화면 캡처 및 분석", 
            command=self.start_analysis,
            width=20
        )
        self.capture_btn.pack(side=tk.LEFT, padx=5)
        
        # 이미지 저장 버튼
        self.save_btn = ttk.Button(
            top_frame, 
            text="결과 이미지 저장", 
            command=self.save_result_image,
            width=15
        )
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        # 상태 레이블
        self.status_var = tk.StringVar(value="준비 완료. '화면 캡처 및 분석' 버튼을 클릭하세요.")
        status_label = ttk.Label(top_frame, textvariable=self.status_var)
        status_label.pack(side=tk.LEFT, padx=20)
        
        # 중앙 프레임 (이미지 표시)
        center_frame = ttk.Frame(main_frame)
        center_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 좌측 이미지 프레임 (원본)
        left_frame = ttk.LabelFrame(center_frame, text="원본 이미지")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.original_canvas = tk.Canvas(left_frame, bg="lightgray")
        self.original_canvas.pack(fill=tk.BOTH, expand=True)
        
        # 우측 이미지 프레임 (결과)
        right_frame = ttk.LabelFrame(center_frame, text="분석 결과")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        self.result_canvas = tk.Canvas(right_frame, bg="lightgray")
        self.result_canvas.pack(fill=tk.BOTH, expand=True)
        
        # 하단 프레임 (로그)
        bottom_frame = ttk.LabelFrame(main_frame, text="로그")
        bottom_frame.pack(fill=tk.X, pady=5)
        
        # 로그 텍스트 영역
        self.log_text = scrolledtext.ScrolledText(
            bottom_frame, 
            height=10, 
            wrap=tk.WORD,
            font=("Consolas", 9)
        )
        self.log_text.pack(fill=tk.X, expand=True, padx=5, pady=5)
        
        # 로그 리디렉션
        self.redirect_log()
        
        # 메뉴바
        self.create_menu()
    
    def create_menu(self):
        """
        메뉴바 생성
        """
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 파일 메뉴
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="파일", menu=file_menu)
        file_menu.add_command(label="설정", command=self.open_settings)
        file_menu.add_separator()
        file_menu.add_command(label="종료", command=self.root.quit)
        
        # 도움말 메뉴
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="도움말", menu=help_menu)
        help_menu.add_command(label="사용 방법", command=self.show_help)
        help_menu.add_command(label="정보", command=self.show_about)
    
    def redirect_log(self):
        """
        로그 출력을 GUI로 리디렉션
        """
        class TextHandler(logging.Handler):
            def __init__(self, text_widget):
                logging.Handler.__init__(self)
                self.text_widget = text_widget
            
            def emit(self, record):
                msg = self.format(record)
                def append():
                    self.text_widget.configure(state='normal')
                    self.text_widget.insert(tk.END, msg + '\n')
                    self.text_widget.configure(state='disabled')
                    self.text_widget.see(tk.END)
                self.text_widget.after(0, append)
        
        text_handler = TextHandler(self.log_text)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
        text_handler.setFormatter(formatter)
        text_handler.setLevel(logging.INFO)
        
        logger = logging.getLogger('minesweeper_helper')
        logger.addHandler(text_handler)
    
    def start_analysis(self):
        """
        화면 캡처 및 분석 시작
        """
        if self.is_analyzing:
            messagebox.showinfo("진행 중", "이미 분석이 진행 중입니다. 완료될 때까지 기다려주세요.")
            return
        
        self.is_analyzing = True
        self.capture_btn.config(state=tk.DISABLED)
        self.status_var.set("화면 캡처 및 분석 중...")
        
        # 별도 스레드에서 분석 실행
        self.analysis_thread = threading.Thread(target=self.run_analysis)
        self.analysis_thread.daemon = True
        self.analysis_thread.start()
    
    def run_analysis(self):
        """
        화면 캡처 및 분석 실행 (스레드에서 실행)
        """
        try:
            # 1. 화면 캡처
            self.logger.info("화면 캡처 중...")
            screen_capture = ScreenCapture(self.settings['capture_mode'])
            if self.settings['capture_mode'] == 'region' and self.settings.get('capture_region'):
                screen_capture.set_region(self.settings['capture_region'])
            
            self.original_image = screen_capture.capture()
            
            # 원본 이미지 표시
            self.display_image(self.original_image, self.original_canvas)
            
            # 디버그 모드에서 캡처된 이미지 저장
            if self.settings.get('debug_mode', False):
                debug_dir = os.path.join(project_root, 'debug')
                os.makedirs(debug_dir, exist_ok=True)
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                save_image(self.original_image, os.path.join(debug_dir, f"capture_{timestamp}.png"))
                self.logger.debug(f"캡처 이미지 저장됨: capture_{timestamp}.png")
            
            # 2. 이미지 전처리
            self.logger.info("이미지 전처리 중...")
            image_processor = ImageProcessor()
            processed_images = image_processor.preprocess(self.original_image)
            
            # 3. 게임 격자 감지
            self.logger.info("게임 격자 감지 중...")
            grid_detector = GridDetector()
            grid_info = grid_detector.detect_grid(processed_images)
            
            if not grid_info['cells']:
                self.logger.warning("게임 격자를 감지할 수 없습니다.")
                messagebox.showwarning("감지 실패", "게임 격자를 감지할 수 없습니다. 지뢰찾기 게임 화면이 보이는지 확인하세요.")
                self.status_var.set("게임 격자 감지 실패. 다시 시도하세요.")
                self.capture_btn.config(state=tk.NORMAL)
                self.is_analyzing = False
                return
            
            # 4. 셀 내용 분석
            self.logger.info("셀 내용 분석 중...")
            templates_dir = os.path.join(project_root, 'resources', 'templates')
            cell_analyzer = CellAnalyzer(templates_dir)
            cell_contents = cell_analyzer.analyze_cells(self.original_image, grid_info['cells'])
            
            # 5. 지뢰 위치 예측
            self.logger.info("지뢰 위치 예측 중...")
            mine_predictor = MinePredictor()
            prediction_results = mine_predictor.predict_mines(cell_contents, grid_info)
            
            # 6. 결과 표시
            self.logger.info("결과 표시 중...")
            result_display = ResultDisplay(
                display_mode='image',
                overlay_color=self.settings.get('overlay_color', (0, 0, 255)),
                overlay_thickness=self.settings.get('overlay_thickness', 2)
            )
            self.result_image = result_display.display_results(
                self.original_image, prediction_results, grid_info['cell_size']
            )
            
            # 결과 이미지 표시
            self.display_image(self.result_image, self.result_canvas)
            
            # 분석 결과 요약
            mines_count = len(prediction_results.get('mines', []))
            safe_count = len(prediction_results.get('safe_cells', []))
            self.logger.info(f"분석 완료: {mines_count}개의 지뢰, {safe_count}개의 안전한 셀 감지됨")
            
            # 디버그 모드에서 결과 이미지 저장
            if self.settings.get('debug_mode', False):
                save_image(self.result_image, os.path.join(debug_dir, f"result_{timestamp}.png"))
                self.logger.debug(f"결과 이미지 저장됨: result_{timestamp}.png")
            
            self.status_var.set(f"분석 완료: {mines_count}개의 지뢰, {safe_count}개의 안전한 셀 감지됨")
            
        except Exception as e:
            self.logger.error(f"오류 발생: {str(e)}", exc_info=True)
            messagebox.showerror("오류", f"분석 중 오류가 발생했습니다: {str(e)}")
            self.status_var.set("오류 발생. 로그를 확인하세요.")
        
        finally:
            self.capture_btn.config(state=tk.NORMAL)
            self.is_analyzing = False
    
    def display_image(self, cv_image, canvas):
        """
        OpenCV 이미지를 캔버스에 표시
        
        Args:
            cv_image (numpy.ndarray): OpenCV 이미지
            canvas (tk.Canvas): 표시할 캔버스
        """
        if cv_image is None:
            return
        
        # 캔버스 크기
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        
        # 캔버스 크기가 아직 계산되지 않은 경우
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 500
            canvas_height = 400
        
        # 이미지 크기
        img_height, img_width = cv_image.shape[:2]
        
        # 비율 계산
        width_ratio = canvas_width / img_width
        height_ratio = canvas_height / img_height
        ratio = min(width_ratio, height_ratio)
        
        # 새 크기 계산
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)
        
        # 이미지 크기 조정
        resized = cv2.resize(cv_image, (new_width, new_height))
        
        # OpenCV 이미지를 Tkinter에서 표시 가능한 형식으로 변환
        image = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        photo = ImageTk.PhotoImage(image=image)
        
        # 캔버스 내용 지우기
        canvas.delete("all")
        
        # 이미지 중앙에 표시
        x_offset = (canvas_width - new_width) // 2
        y_offset = (canvas_height - new_height) // 2
        
        # 이미지 표시
        canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=photo)
        canvas.image = photo  # 참조 유지
    
    def save_result_image(self):
        """
        결과 이미지 저장
        """
        if self.result_image is None:
            messagebox.showwarning("저장 실패", "저장할 결과 이미지가 없습니다. 먼저 분석을 실행하세요.")
            return
        
        # 저장 경로 선택
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG 파일", "*.png"), ("JPEG 파일", "*.jpg"), ("모든 파일", "*.*")],
            title="결과 이미지 저장"
        )
        
        if not file_path:
            return
        
        try:
            # 이미지 저장
            cv2.imwrite(file_path, self.result_image)
            self.logger.info(f"결과 이미지 저장됨: {file_path}")
            messagebox.showinfo("저장 완료", f"결과 이미지가 저장되었습니다:\n{file_path}")
        except Exception as e:
            self.logger.error(f"이미지 저장 중 오류 발생: {str(e)}")
            messagebox.showerror("저장 실패", f"이미지 저장 중 오류가 발생했습니다: {str(e)}")
    
    def open_settings(self):
        """
        설정 다이얼로그 열기
        """
        # 설정 다이얼로그 구현 (간단한 버전)
        settings_window = tk.Toplevel(self.root)
        settings_window.title("설정")
        settings_window.geometry("400x300")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # 설정 프레임
        settings_frame = ttk.Frame(settings_window, padding="10")
        settings_frame.pack(fill=tk.BOTH, expand=True)
        
        # 캡처 모드 설정
        ttk.Label(settings_frame, text="캡처 모드:").grid(row=0, column=0, sticky=tk.W, pady=5)
        capture_mode_var = tk.StringVar(value=self.settings['capture_mode'])
        capture_mode_combo = ttk.Combobox(
            settings_frame, 
            textvariable=capture_mode_var,
            values=["full_screen", "active_window", "region"]
        )
        capture_mode_combo.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # 디버그 모드 설정
        ttk.Label(settings_frame, text="디버그 모드:").grid(row=1, column=0, sticky=tk.W, pady=5)
        debug_mode_var = tk.BooleanVar(value=self.settings.get('debug_mode', False))
        debug_mode_check = ttk.Checkbutton(settings_frame, variable=debug_mode_var)
        debug_mode_check.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # 버튼 프레임
        button_frame = ttk.Frame(settings_window)
        button_frame.pack(fill=tk.X, pady=10)
        
        # 저장 버튼
        def save_settings():
            self.settings['capture_mode'] = capture_mode_var.get()
            self.settings['debug_mode'] = debug_mode_var.get()
            save_settings(self.settings)
            self.logger.info("설정이 저장되었습니다.")
            settings_window.destroy()
        
        save_btn = ttk.Button(button_frame, text="저장", command=save_settings)
        save_btn.pack(side=tk.RIGHT, padx=5)
        
        # 취소 버튼
        cancel_btn = ttk.Button(button_frame, text="취소", command=settings_window.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=5)
    
    def show_help(self):
        """
        도움말 표시
        """
        help_text = """
        지뢰찾기 헬퍼 GUI 사용 방법:
        
        1. 지뢰찾기 게임을 실행합니다.
        2. 게임 화면이 보이는 상태에서 '화면 캡처 및 분석' 버튼을 클릭합니다.
        3. 지뢰찾기 헬퍼가 게임 화면을 분석하여 지뢰 위치를 예측합니다.
        4. 예측된 지뢰 위치가 오른쪽 화면에 표시됩니다.
        5. '결과 이미지 저장' 버튼을 클릭하여 분석 결과를 저장할 수 있습니다.
        
        설정 메뉴에서 캡처 모드, 디버그 모드 등을 변경할 수 있습니다.
        """
        messagebox.showinfo("사용 방법", help_text)
    
    def show_about(self):
        """
        정보 표시
        """
        about_text = """
        지뢰찾기 헬퍼 GUI v1.0
        
        이 프로그램은 지뢰찾기 게임 플레이를 보조하는 도구입니다.
        이미지 처리 및 분석 기술을 활용하여 게임 화면에서 지뢰의 위치를 예측합니다.
        
        개발자: 지뢰찾기 헬퍼 개발팀
        """
        messagebox.showinfo("정보", about_text)
    
    def on_closing(self):
        """
        창 닫기 이벤트 처리
        """
        if self.is_analyzing:
            if messagebox.askokcancel("종료", "분석이 진행 중입니다. 정말 종료하시겠습니까?"):
                self.root.destroy()
        else:
            self.root.destroy()

def main():
    """
    메인 함수
    """
    root = tk.Tk()
    app = MinesweeperHelperGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
