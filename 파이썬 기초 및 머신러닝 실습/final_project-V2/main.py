import tkinter as tk
from tkinter import messagebox
import random

class MinesweeperGUI:
    def __init__(self, master, rows, cols, mines):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines

        # 게임 로직에 필요한 변수들
        self.solution_board = []
        self.mine_positions = set()
        self.flags = set()
        self.revealed = set()
        self.game_over = False
        self.first_click = True

        # UI 요소 및 변수
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]
        self.mine_count_var = tk.StringVar()
        self.timer_var = tk.StringVar()
        self.seconds_passed = 0
        self.timer_id = None
        
        self.create_widgets()
        self.start_new_game()

    def create_widgets(self):
        """게임의 UI 위젯들을 생성합니다."""
        # 상단 정보 프레임 (깃발 카운터, 버튼, 타이머)
        top_frame = tk.Frame(self.master, pady=5)
        top_frame.pack(fill='x', padx=10)

        # 깃발 카운터 라벨
        mine_count_label = tk.Label(top_frame, textvariable=self.mine_count_var, font=('Helvetica', 12, 'bold'), width=10, anchor='w')
        mine_count_label.pack(side=tk.LEFT)

        # 중앙 버튼 프레임
        button_frame = tk.Frame(top_frame)
        button_frame.pack(side=tk.LEFT, expand=True)

        # 새 게임 버튼
        restart_button = tk.Button(button_frame, text="새 게임", command=self.start_new_game, font=('Helvetica', 10, 'bold'))
        restart_button.pack(side=tk.LEFT, padx=5)

        # 힌트 버튼
        hint_button = tk.Button(button_frame, text="힌트", command=self.on_hint_click, font=('Helvetica', 10, 'bold'))
        hint_button.pack(side=tk.LEFT, padx=5)

        # 타이머 라벨
        timer_label = tk.Label(top_frame, textvariable=self.timer_var, font=('Helvetica', 12, 'bold'), width=10, anchor='e')
        timer_label.pack(side=tk.RIGHT)
        
        # 게임판 프레임
        self.board_frame = tk.Frame(self.master, padx=10, pady=10)
        self.board_frame.pack()

        for r in range(self.rows):
            for c in range(self.cols):
                button = tk.Button(self.board_frame, width=2, height=1, font=('Helvetica', 14, 'bold'))
                button.grid(row=r, column=c)
                button.bind('<Button-1>', lambda e, r=r, c=c: self.on_left_click(r, c))
                button.bind('<Button-3>', lambda e, r=r, c=c: self.on_right_click(r, c))
                button.bind('<Button-2>', lambda e, r=r, c=c: self.on_right_click(r, c))
                self.buttons[r][c] = button

    def start_new_game(self):
        """게임을 초기 상태로 리셋합니다."""
        self.game_over = False
        self.first_click = True
        self.flags.clear()
        self.revealed.clear()
        self.solution_board = []
        self.mine_positions.clear()
        
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
            self.timer_id = None
        self.seconds_passed = 0
        
        self.update_mine_count_label()
        self.timer_var.set(f"⏰ {self.seconds_passed}")

        for r in range(self.rows):
            for c in range(self.cols):
                self.buttons[r][c].config(text='', state='normal', relief='raised', bg='SystemButtonFace')

    def create_board_and_mines(self, safe_row, safe_col):
        """첫 클릭이 항상 안전하도록 보장하며 게임판과 지뢰를 생성합니다."""
        self.solution_board = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]
        
        possible_mine_locations = []
        for r in range(self.rows):
            for c in range(self.cols):
                if abs(r - safe_row) > 1 or abs(c - safe_col) > 1:
                    possible_mine_locations.append((r, c))

        self.mine_positions = set(random.sample(possible_mine_locations, self.mines))

        for r, c in self.mine_positions:
            self.solution_board[r][c] = '*'
        
        for r in range(self.rows):
            for c in range(self.cols):
                if self.solution_board[r][c] == '*':
                    continue
                mine_count = 0
                for i in range(max(0, r - 1), min(self.rows, r + 2)):
                    for j in range(max(0, c - 1), min(self.cols, c + 2)):
                        if (i, j) in self.mine_positions:
                            mine_count += 1
                if mine_count > 0:
                    self.solution_board[r][c] = str(mine_count)

    def on_left_click(self, r, c):
        """왼쪽 마우스 클릭 처리"""
        if self.game_over or (r, c) in self.revealed or (r, c) in self.flags:
            return

        if self.first_click:
            self.first_click = False
            self.create_board_and_mines(r, c)
            self.start_timer()

        if (r, c) in self.mine_positions:
            self.game_over_lose(r, c)
            return
        
        self.reveal_cell(r, c)
        self.check_win_condition()

    def on_right_click(self, r, c):
        """오른쪽 마우스 클릭 처리 (깃발)"""
        if self.game_over or (r, c) in self.revealed:
            return

        if (r, c) in self.flags:
            self.flags.remove((r, c))
            self.buttons[r][c].config(text='')
        else:
            if len(self.flags) < self.mines:
                self.flags.add((r, c))
                self.buttons[r][c].config(text='🚩', fg='red')
        
        self.update_mine_count_label()

    def on_hint_click(self):
        """논리적으로 확실한 안전한 칸 또는 지뢰 칸을 찾아 강조 표시하고, 과정을 터미널에 출력합니다."""
        print("\n=====================================")
        print(" [INFO] 힌트 버튼 클릭: 검색 시작")
        print("=====================================")

        if self.game_over or self.first_click:
            print(" [DEBUG] 게임이 시작되지 않았거나 종료되어 힌트 검색을 중단합니다.")
            return

        guaranteed_safes = set()
        guaranteed_mines = set()

        # 모든 열린 숫자 칸을 순회하며 가능한 모든 힌트를 수집합니다.
        for r_rev, c_rev in self.revealed:
            # 숫자 타일이 아니면 건너뜁니다.
            if not self.solution_board[r_rev][c_rev].strip().isdigit():
                continue
            
            value = int(self.solution_board[r_rev][c_rev])
            adj_flags = []
            adj_hidden = []
            
            print(f"\n [DEBUG] 검사 중인 칸: ({r_rev}, {c_rev}), 숫자: {value}")
            
            # 주변 8칸을 탐색하여 깃발과 숨겨진 칸의 정보를 수집합니다.
            for i in range(max(0, r_rev - 1), min(self.rows, r_rev + 2)):
                for j in range(max(0, c_rev - 1), min(self.cols, c_rev + 2)):
                    if (i, j) == (r_rev, c_rev):
                        continue
                    if (i, j) in self.flags:
                        adj_flags.append((i, j))
                    elif (i, j) not in self.revealed:
                        adj_hidden.append((i, j))

            print(f"   - 주변 깃발 수: {len(adj_flags)}")
            print(f"   - 주변 숨겨진 칸 수: {len(adj_hidden)}")

            # 로직 1: (칸의 숫자) == (주변 깃발 수) 이면, 나머지 숨겨진 칸은 모두 안전합니다.
            print(f"   - 안전 로직 검사: {value} == {len(adj_flags)} ?  결과: {value == len(adj_flags)}")
            if len(adj_hidden) > 0 and value == len(adj_flags):
                for cell in adj_hidden:
                    guaranteed_safes.add(cell)
                print(f"   >>> [발견!] 안전한 칸 추가: {adj_hidden}")

            # 로직 2: (칸의 숫자) - (주변 깃발 수) == (숨겨진 칸 수) 이면, 나머지 숨겨진 칸은 모두 지뢰입니다.
            print(f"   - 지뢰 로직 검사: {value} - {len(adj_flags)} == {len(adj_hidden)} ?  결과: {value - len(adj_flags) == len(adj_hidden)}")
            if len(adj_hidden) > 0 and value - len(adj_flags) == len(adj_hidden):
                for cell in adj_hidden:
                    if cell not in self.flags: # 이미 깃발이 꽂힌 곳은 제외
                        guaranteed_mines.add(cell)
                print(f"   >>> [발견!] 지뢰 확실 칸 추가: {[c for c in adj_hidden if c not in self.flags]}")
        
        print("\n-------------------------------------")
        print(f" [INFO] 최종 검색 결과:")
        print(f"   - 찾은 안전한 칸: {guaranteed_safes if guaranteed_safes else '없음'}")
        print(f"   - 찾은 지뢰 확실 칸: {guaranteed_mines if guaranteed_mines else '없음'}")
        print("-------------------------------------")

        # 힌트 표시: 안전한 칸을 우선으로 보여줍니다.
        if guaranteed_safes:
            hint_r, hint_c = list(guaranteed_safes)[0]
            print(f" [ACTION] 안전한 칸 ({hint_r}, {hint_c})을(를) 연두색으로 강조합니다.")
            self.highlight_cell(hint_r, hint_c, 'lightgreen')
            return

        if guaranteed_mines:
            hint_r, hint_c = list(guaranteed_mines)[0]
            print(f" [ACTION] 지뢰 확실 칸 ({hint_r}, {hint_c})을(를) 노란색으로 강조합니다.")
            self.highlight_cell(hint_r, hint_c, 'yellow')
            return

        print(" [RESULT] 표시할 힌트를 찾지 못했습니다.")
        messagebox.showinfo("힌트", "현재 상태에서 확실한 힌트를 찾을 수 없습니다.")

    # --- 수정된 함수 ---
    def highlight_cell(self, r, c, color):
        """지정한 칸을 특정 색상으로 잠시 강조합니다."""
        button = self.buttons[r][c]
        try:
            original_color = button.cget('bg')
            button.config(bg=color)
            # GUI가 즉시 변경사항을 그리도록 강제합니다.
            self.master.update_idletasks() 
            self.master.after(1500, lambda: self.reset_cell_color(button, original_color))
        except tk.TclError:
            pass # 위젯이 파괴된 후 실행되는 경우를 대비한 예외 처리
            
    def reset_cell_color(self, button, color):
        """강조된 칸의 색상을 원래대로 복원합니다."""
        try:
            button.config(bg=color)
        except tk.TclError:
            pass
    # ----------------------------------------

    def update_mine_count_label(self):
        """깃발 수와 전체 지뢰 수를 표시하는 라벨을 업데이트합니다."""
        self.mine_count_var.set(f"🚩 {len(self.flags)} / {self.mines}")

    def start_timer(self):
        """타이머를 시작합니다."""
        self.update_timer()

    def update_timer(self):
        """1초마다 타이머를 업데이트합니다."""
        if self.game_over:
            return
        self.timer_var.set(f"⏰ {self.seconds_passed}")
        self.seconds_passed += 1
        self.timer_id = self.master.after(1000, self.update_timer)

    def reveal_cell(self, r, c):
        """칸을 열고, 빈 칸일 경우 주변 칸을 재귀적으로 엽니다."""
        if (r, c) in self.revealed or not (0 <= r < self.rows and 0 <= c < self.cols):
            return

        if (r, c) in self.flags:
            self.flags.remove((r, c))
            self.update_mine_count_label()

        self.revealed.add((r, c))
        button = self.buttons[r][c]
        value = self.solution_board[r][c]

        button.config(text=value, state='disabled', relief='sunken', disabledforeground=self.get_color(value), bg='#d9d9d9')
        
        if value == ' ':
            for i in range(max(0, r - 1), min(self.rows, r + 2)):
                for j in range(max(0, c - 1), min(self.cols, c + 2)):
                    if (i, j) != (r, c):
                        self.reveal_cell(i, j)

    def game_over_lose(self, clicked_r, clicked_c):
        """게임 오버 (패배) 처리"""
        self.game_over = True
        for r_flag, c_flag in self.flags:
            if (r_flag, c_flag) not in self.mine_positions:
                self.buttons[r_flag][c_flag].config(text='❌')
        for r_mine, c_mine in self.mine_positions:
            if (r_mine, c_mine) not in self.flags:
                self.buttons[r_mine][c_mine].config(text='💣', bg='lightgray')
        
        self.buttons[clicked_r][clicked_c].config(bg='red')
        messagebox.showinfo("게임 오버", "지뢰를 밟았습니다!")

    def check_win_condition(self):
        """승리 조건을 확인합니다."""
        if len(self.revealed) == self.rows * self.cols - self.mines:
            self.game_over = True
            self.update_mine_count_label()
            messagebox.showinfo("승리!", "축하합니다! 모든 지뢰를 찾았습니다!")
            
            for r in range(self.rows):
                for c in range(self.cols):
                    if (r, c) not in self.revealed and (r, c) not in self.flags:
                        self.buttons[r][c].config(state='disabled')
            
    def get_color(self, value):
        """숫자에 따라 다른 색상을 반환합니다."""
        colors = {
            '1': 'blue', '2': 'green', '3': 'red', '4': 'purple', 
            '5': 'maroon', '6': 'turquoise', '7': 'black', '8': 'gray'
        }
        return colors.get(value, 'black')


if __name__ == "__main__":
    root = tk.Tk()
    root.title("지뢰찾기")
    root.resizable(False, False)

    # 9x9 크기, 10개 지뢰
    game = MinesweeperGUI(root, 9, 9, 10)

    root.mainloop()
