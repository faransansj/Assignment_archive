#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
지뢰 위치 예측 모듈

이 모듈은 셀 분석 결과를 바탕으로 지뢰 위치를 예측합니다.
"""

import logging

class MinePredictor:
    """
    지뢰 위치 예측 클래스
    """
    
    def __init__(self):
        """
        MinePredictor 초기화
        """
        self.logger = logging.getLogger('minesweeper_helper')
    
    def predict_mines(self, cell_contents, grid_info):
        """
        지뢰 위치 예측
        
        Args:
            cell_contents (list): 셀 내용 분석 결과
                [{'position': (x, y, w, h), 'content': 'cell_1', 'confidence': 0.95}, ...]
            grid_info (dict): 격자 정보
                - 'cell_size': 셀 크기
                - 'grid_origin': 격자 원점 (x, y)
                - 'grid_dimensions': 격자 차원 (rows, cols)
        
        Returns:
            dict: 예측 결과
                - 'mines': 지뢰로 예측된 셀 위치 목록 [(x, y, w, h), ...]
                - 'safe_cells': 안전한 셀로 예측된 위치 목록 [(x, y, w, h), ...]
        """
        self.logger.debug("지뢰 위치 예측 시작")
        
        rows, cols = grid_info['grid_dimensions']
        grid_x, grid_y = grid_info['grid_origin']
        cell_size = grid_info['cell_size']
        
        # 2D 그리드로 변환
        grid = [[None for _ in range(cols)] for _ in range(rows)]
        position_map = {}  # (row, col) -> (x, y, w, h) 매핑
        
        # 셀 내용을 그리드에 배치
        for cell in cell_contents:
            x, y, w, h = cell['position']
            row = (y - grid_y) // cell_size
            col = (x - grid_x) // cell_size
            
            if 0 <= row < rows and 0 <= col < cols:
                grid[row][col] = cell['content']
                position_map[(row, col)] = cell['position']
        
        # 지뢰 위치 추론
        mines = []
        safe_cells = []
        
        # 각 숫자 셀 주변 분석
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] and grid[row][col].startswith('cell_') and grid[row][col] != 'cell_empty' and grid[row][col] != 'cell_unopened' and grid[row][col] != 'cell_flag':
                    # 숫자 추출 (예: 'cell_1' -> 1)
                    try:
                        number = int(grid[row][col].split('_')[1])
                    except (ValueError, IndexError):
                        continue
                    
                    # 주변 8개 셀 확인
                    neighbors = self._get_neighbors(grid, row, col, rows, cols)
                    
                    # 미개방 셀 및 깃발 셀 카운트
                    unopened = [n for n in neighbors if n['content'] == 'cell_unopened']
                    flags = [n for n in neighbors if n['content'] == 'cell_flag']
                    
                    # 지뢰 추론 로직
                    if len(flags) == number:
                        # 나머지 미개방 셀은 안전
                        for cell in unopened:
                            pos = position_map.get((cell['row'], cell['col']))
                            if pos and pos not in safe_cells:
                                safe_cells.append(pos)
                    elif len(unopened) + len(flags) == number and len(unopened) > 0:
                        # 모든 미개방 셀이 지뢰
                        for cell in unopened:
                            pos = position_map.get((cell['row'], cell['col']))
                            if pos and pos not in mines:
                                mines.append(pos)
        
        self.logger.debug(f"지뢰 위치 예측 완료: {len(mines)}개 지뢰, {len(safe_cells)}개 안전한 셀")
        
        return {
            'mines': mines,
            'safe_cells': safe_cells
        }
    
    def _get_neighbors(self, grid, row, col, max_rows, max_cols):
        """
        주변 8개 셀 반환
        
        Args:
            grid (list): 2D 그리드
            row (int): 현재 행
            col (int): 현재 열
            max_rows (int): 최대 행 수
            max_cols (int): 최대 열 수
        
        Returns:
            list: 주변 셀 정보 목록
                [{'row': row, 'col': col, 'content': 'cell_1'}, ...]
        """
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                
                r, c = row + dr, col + dc
                if 0 <= r < max_rows and 0 <= c < max_cols:
                    neighbors.append({
                        'row': r,
                        'col': c,
                        'content': grid[r][c]
                    })
        
        return neighbors
