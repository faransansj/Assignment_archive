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
        self.is_closing = False  # 창이 닫히는 중인지 확인하는 플래그

        # 오토플레이 관련 변수
        self.auto_playing = False
        self.auto_after_id = None
        self.robot_position = None  # 로봇의 현재 위치

        # UI 요소 및 변수
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]
        self.mine_count_var = tk.StringVar()
        self.found_mines_var = tk.StringVar()  # 찾은 지뢰 수 표시용
        self.timer_var = tk.StringVar()
        self.seconds_passed = 0
        self.timer_id = None
        
        self.create_widgets()
        self.start_new_game()

    def create_widgets(self):
        """게임의 UI 위젯들을 생성합니다."""
        top_frame = tk.Frame(self.master, pady=10, bg='lightgray')
        top_frame.pack(fill='x', padx=10)

        # 왼쪽: 남은 지뢰 수
        mine_count_label = tk.Label(top_frame, textvariable=self.mine_count_var, 
                                   font=('Helvetica', 12, 'bold'), width=10, anchor='w',
                                   bg='black', fg='red', relief='sunken', bd=2)
        mine_count_label.pack(side=tk.LEFT, padx=2)

        # 찾은 지뢰 수 표시
        found_mines_label = tk.Label(top_frame, textvariable=self.found_mines_var, 
                                    font=('Helvetica', 12, 'bold'), width=10, anchor='w',
                                    bg='black', fg='orange', relief='sunken', bd=2)
        found_mines_label.pack(side=tk.LEFT, padx=2)

        # 중앙: 버튼들
        button_frame = tk.Frame(top_frame, bg='lightgray')
        button_frame.pack(side=tk.LEFT, expand=True)

        restart_button = tk.Button(button_frame, text="🙂 새 게임", command=self.start_new_game, 
                                 font=('Helvetica', 12, 'bold'), bg='lightblue')
        restart_button.pack(side=tk.LEFT, padx=5)

        hint_button = tk.Button(button_frame, text="💡 힌트", command=self.on_hint_click, 
                              font=('Helvetica', 12, 'bold'), bg='lightyellow')
        hint_button.pack(side=tk.LEFT, padx=5)

        # 오토플레이 버튼 추가
        self.auto_button = tk.Button(button_frame, text="🤖 오토", command=self.toggle_auto_play, 
                                   font=('Helvetica', 12, 'bold'), bg='lightgreen')
        self.auto_button.pack(side=tk.LEFT, padx=5)

        # 오른쪽: 타이머
        timer_label = tk.Label(top_frame, textvariable=self.timer_var, 
                              font=('Helvetica', 12, 'bold'), width=10, anchor='e',
                              bg='black', fg='green', relief='sunken', bd=2)
        timer_label.pack(side=tk.RIGHT, padx=2)
        
        self.board_frame = tk.Frame(self.master, padx=10, pady=10)
        self.board_frame.pack()

        for r in range(self.rows):
            for c in range(self.cols):
                button = tk.Button(self.board_frame, width=2, height=1, font=('Helvetica', 14, 'bold'))
                button.grid(row=r, column=c)
                button.bind('<Button-1>', lambda e, r_bind=r, c_bind=c: self.on_left_click(r_bind, c_bind))
                button.bind('<Button-3>', lambda e, r_bind=r, c_bind=c: self.on_right_click(r_bind, c_bind))
                button.bind('<Button-2>', lambda e, r_bind=r, c_bind=c: self.on_right_click(r_bind, c_bind))
                self.buttons[r][c] = button

    def toggle_auto_play(self):
        """오토플레이를 시작하거나 중지합니다."""
        if self.auto_playing:
            self.stop_auto_play()
        else:
            self.start_auto_play()

    def start_auto_play(self):
        """오토플레이를 시작합니다."""
        if self.game_over or self.first_click:
            if not self.is_closing:
                messagebox.showinfo("오토플레이", "게임을 먼저 시작해주세요!")
            return
        
        self.auto_playing = True
        self.auto_button.config(text="⏸️ 중지", bg='lightcoral')
        if not self.is_closing:
            print("\n🤖 오토플레이 시작!")
        self.auto_play_step()

    def stop_auto_play(self):
        """오토플레이를 중지합니다."""
        self.auto_playing = False
        self.auto_button.config(text="🤖 오토", bg='lightgreen')
        if self.auto_after_id:
            self.master.after_cancel(self.auto_after_id)
            self.auto_after_id = None
        self.clear_robot_position()
        if not self.is_closing:
            print("🤖 오토플레이 중지!")

    def auto_play_step(self):
        """오토플레이의 한 단계를 실행합니다."""
        if not self.auto_playing or self.game_over or self.is_closing:
            self.stop_auto_play()
            return

        # 논리적 분석 수행
        guaranteed_safes, guaranteed_mines = self.analyze_board_logic()
        
        if not self.is_closing:
            print(f"\n🤖 로봇 분석 결과:")
            print(f"확실한 안전 위치: {sorted(list(guaranteed_safes))}")
            print(f"확실한 지뢰 위치: {sorted(list(guaranteed_mines))}")

        actions_taken = False

        # 먼저 지뢰가 확실한 칸들에 깃발 설치
        for mine_r, mine_c in guaranteed_mines:
            if (mine_r, mine_c) not in self.flags:
                self.show_robot_at_position(mine_r, mine_c)
                self.flags.add((mine_r, mine_c))
                self.buttons[mine_r][mine_c].config(text='🚩', fg='red')
                self.update_mine_count_label()
                self.update_found_mines_label()
                actions_taken = True
                if not self.is_closing:
                    print(f"🤖 로봇이 지뢰 발견: ({mine_r}, {mine_c})")
                break  # 한 번에 하나씩 처리

        # 지뢰 처리가 없었다면 안전한 칸 클릭
        if not actions_taken and guaranteed_safes:
            safe_r, safe_c = list(guaranteed_safes)[0]
            self.show_robot_at_position(safe_r, safe_c)
            self.reveal_cell(safe_r, safe_c)
            actions_taken = True
            if not self.is_closing:
                print(f"🤖 로봇이 안전한 칸 클릭: ({safe_r}, {safe_c})")

        if actions_taken:
            self.check_win_condition()
            # 다음 단계를 위해 일정 시간 후 재귀 호출
            self.auto_after_id = self.master.after(800, self.auto_play_step)
        else:
            # 더 이상 확실한 수가 없으면 오토플레이 중지
            if not self.is_closing:
                print("🤖 더 이상 확실한 수를 찾을 수 없습니다. 오토플레이를 중지합니다.")
                messagebox.showinfo("오토플레이", "더 이상 논리적으로 확실한 수를 찾을 수 없습니다.")
            self.stop_auto_play()

    def show_robot_at_position(self, r, c):
        """로봇의 현재 위치를 시각화합니다."""
        if self.is_closing:
            return
            
        # 이전 로봇 위치 제거
        self.clear_robot_position()
        
        # 새로운 로봇 위치 표시
        self.robot_position = (r, c)
        button = self.buttons[r][c]
        
        try:
            # 현재 버튼이 열리지 않은 상태라면 로봇 표시
            if (r, c) not in self.revealed:
                current_text = button.cget('text')
                if current_text != '🚩':  # 깃발이 아닌 경우만
                    button.config(bg='gold', text='🤖')
        except tk.TclError:
            pass

    def clear_robot_position(self):
        """로봇 위치 표시를 제거합니다."""
        if self.robot_position and not self.is_closing:
            r, c = self.robot_position
            try:
                button = self.buttons[r][c]
                if button.winfo_exists() and (r, c) not in self.revealed:
                    # 원래 상태로 복원
                    if (r, c) in self.flags:
                        button.config(bg='SystemButtonFace', text='🚩', fg='red')
                    else:
                        button.config(bg='SystemButtonFace', text='')
            except tk.TclError:
                pass
        self.robot_position = None

    def analyze_board_logic(self):
        """현재 보드 상태를 분석하여 확실한 안전/지뢰 위치를 찾습니다."""
        guaranteed_safes = set()
        guaranteed_mines = set()

        for r_rev, c_rev in self.revealed:
            if not self.solution_board[r_rev][c_rev].strip().isdigit():
                continue
            
            value = int(self.solution_board[r_rev][c_rev])
            adj_flags = []
            adj_hidden = []
            
            for i in range(max(0, r_rev - 1), min(self.rows, r_rev + 2)):
                for j in range(max(0, c_rev - 1), min(self.cols, c_rev + 2)):
                    if (i, j) == (r_rev, c_rev): 
                        continue
                    if (i, j) in self.flags:
                        adj_flags.append((i, j))
                    elif (i, j) not in self.revealed:
                        adj_hidden.append((i, j))

            # 인접한 깃발의 수가 숫자와 같으면, 나머지 숨겨진 칸들은 안전함
            if len(adj_hidden) > 0 and value == len(adj_flags):
                for cell in adj_hidden: 
                    guaranteed_safes.add(cell)

            # 남은 숨겨진 칸의 수가 (숫자 - 깃발 수)와 같으면, 모든 숨겨진 칸이 지뢰임
            if len(adj_hidden) > 0 and value - len(adj_flags) == len(adj_hidden):
                for cell in adj_hidden:
                    if cell not in self.flags: 
                        guaranteed_mines.add(cell)

        return guaranteed_safes, guaranteed_mines

    def start_new_game(self):
        """게임을 초기 상태로 리셋합니다."""
        print("\n=== 새 게임 시작 ===")
        
        # 오토플레이 중지
        if self.auto_playing:
            self.stop_auto_play()
        
        self.game_over = False
        self.first_click = True
        self.flags.clear()
        self.revealed.clear()
        self.solution_board = []
        self.mine_positions.clear()
        
        # 타이머 정리
        self.stop_timer()
        self.seconds_passed = 0
        
        # GUI 초기값 설정
        self.update_mine_count_label()
        self.update_found_mines_label()  # 찾은 지뢰 수 초기화
        self.timer_var.set("⏰ 000")

        for r in range(self.rows):
            for c in range(self.cols):
                self.buttons[r][c].config(text='', state='normal', relief='raised', bg='SystemButtonFace')

    def stop_timer(self):
        """타이머를 완전히 정지합니다."""
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
            self.timer_id = None

    def create_board_and_mines(self, safe_row, safe_col):
        """첫 클릭이 항상 안전하도록 보장하며 게임판과 지뢰를 생성합니다."""
        self.solution_board = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]
        
        possible_mine_locations = []
        for r in range(self.rows):
            for c in range(self.cols):
                if abs(r - safe_row) > 1 or abs(c - safe_col) > 1:
                    possible_mine_locations.append((r, c))

        self.mine_positions = set(random.sample(possible_mine_locations, self.mines))

        # 지뢰 위치 로그 출력 (창이 닫히는 중이 아닐 때만)
        if not self.is_closing:
            print(f"지뢰 위치: {sorted(list(self.mine_positions))}")

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
        if self.is_closing or self.game_over or (r, c) in self.revealed or (r, c) in self.flags:
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
        if self.is_closing or self.game_over or (r, c) in self.revealed:
            return

        if (r, c) in self.flags:
            self.flags.remove((r, c))
            self.buttons[r][c].config(text='')
            if not self.is_closing:
                print(f"깃발 제거: ({r}, {c})")
        else:
            if len(self.flags) < self.mines:
                self.flags.add((r, c))
                self.buttons[r][c].config(text='🚩', fg='red')
                if not self.is_closing:
                    print(f"깃발 설치: ({r}, {c})")
        
        self.update_mine_count_label()
        self.update_found_mines_label()  # 찾은 지뢰 수 업데이트

    def on_hint_click(self):
        """논리적으로 확실한 안전한 칸 또는 지뢰 칸을 찾아 힌트를 제공합니다."""
        if self.is_closing or self.game_over or self.first_click:
            return

        guaranteed_safes, guaranteed_mines = self.analyze_board_logic()

        if not self.is_closing:
            print(f"\n힌트 분석 결과:")
            print(f"확실한 안전 위치: {sorted(list(guaranteed_safes))}")
            print(f"확실한 지뢰 위치: {sorted(list(guaranteed_mines))}")

        # 지뢰가 확실한 칸들을 모두 처리
        if guaranteed_mines:
            mines_flagged = 0
            for mine_r, mine_c in guaranteed_mines:
                if (mine_r, mine_c) not in self.flags:
                    self.flags.add((mine_r, mine_c))
                    self.buttons[mine_r][mine_c].config(text='🚩', fg='red')
                    self.highlight_cell(mine_r, mine_c, 'yellow')
                    mines_flagged += 1
                    if not self.is_closing:
                        print(f"자동 깃발 설치: ({mine_r}, {mine_c})")
            
            if mines_flagged > 0:
                self.update_mine_count_label()
                self.update_found_mines_label()  # 찾은 지뢰 수 업데이트
                if not self.is_closing:
                    messagebox.showinfo("힌트", f"{mines_flagged}개의 지뢰 위치에 깃발을 표시했습니다!")
                self.check_win_condition()
                return
        
        # 안전한 칸이 있으면 녹색으로 강조 (하나만)
        if guaranteed_safes:
            hint_r, hint_c = list(guaranteed_safes)[0]
            self.highlight_cell(hint_r, hint_c, 'lightgreen')
            if not self.is_closing:
                messagebox.showinfo("힌트", f"({hint_r+1}, {hint_c+1}) 위치는 안전합니다!")
            return

        if not self.is_closing:
            messagebox.showinfo("힌트", "현재 상태에서 확실한 힌트를 찾을 수 없습니다.")

    def highlight_cell(self, r, c, color):
        """지정한 칸을 특정 색상으로 잠시 강조합니다."""
        if self.is_closing:
            return
            
        button = self.buttons[r][c]
        try:
            original_color = button.cget('bg')
            button.config(bg=color)
            # GUI가 즉시 변경사항을 그리도록 강제합니다.
            if not self.is_closing:
                self.master.update()
                self.master.after(1500, lambda: self.reset_cell_color(button, original_color))
        except tk.TclError:
            pass
            
    def reset_cell_color(self, button, color):
        """강조된 칸의 색상을 원래대로 복원합니다."""
        if self.is_closing:
            return
            
        try:
            if button.winfo_exists():
                button.config(bg=color)
        except tk.TclError:
            pass

    def update_mine_count_label(self):
        """남은 지뢰 수 표시"""
        remaining_mines = self.mines - len(self.flags)
        mine_text = f"💣 {remaining_mines:03d}"
        self.mine_count_var.set(mine_text)

    def update_found_mines_label(self):
        """찾은 지뢰 수 표시"""
        found_mines = len([pos for pos in self.flags if pos in self.mine_positions])
        found_text = f"🎯 {found_mines:03d}"
        self.found_mines_var.set(found_text)
        if not self.is_closing:
            print(f"찾은 지뢰: {found_mines}/{self.mines}개")

    def start_timer(self):
        self.update_timer()

    def update_timer(self):
        """타이머를 초 단위로 업데이트"""
        if self.is_closing or self.game_over: 
            # 게임이 끝났거나 창이 닫히는 중이면 타이머 정리
            self.stop_timer()
            return
        
        timer_text = f"⏰ {self.seconds_passed:03d}"
        self.timer_var.set(timer_text)
        self.seconds_passed += 1
        self.timer_id = self.master.after(1000, self.update_timer)

    def reveal_cell(self, r, c):
        """칸을 열고, 상태를 비활성화하여 시각적 구분을 명확히 합니다."""
        if self.is_closing or (r, c) in self.revealed or not (0 <= r < self.rows and 0 <= c < self.cols):
            return

        if (r, c) in self.flags:
            self.flags.remove((r, c))
            self.update_mine_count_label()
            self.update_found_mines_label()

        # 로봇 위치 제거
        if self.robot_position == (r, c):
            self.robot_position = None

        self.revealed.add((r, c))
        button = self.buttons[r][c]
        value = self.solution_board[r][c]
        
        button.config(text=value, state='disabled', relief='sunken', disabledforeground=self.get_color(value))
        
        if value == ' ':
            for i in range(max(0, r - 1), min(self.rows, r + 2)):
                for j in range(max(0, c - 1), min(self.cols, c + 2)):
                    if (i, j) != (r, c): 
                        self.reveal_cell(i, j)

    def game_over_lose(self, clicked_r, clicked_c):
        """게임 오버 (패배) 처리"""
        self.game_over = True
        
        # 오토플레이 중지
        if self.auto_playing:
            self.stop_auto_play()
        
        # 타이머 완전히 정리
        self.stop_timer()
            
        if not self.is_closing:
            print(f"\n게임 오버! 지뢰 클릭: ({clicked_r}, {clicked_c})")
            print(f"게임 시간: {self.seconds_passed}초")
            found_mines = len([pos for pos in self.flags if pos in self.mine_positions])
            print(f"찾은 지뢰: {found_mines}/{self.mines}개")
        
        for r_flag, c_flag in self.flags:
            if (r_flag, c_flag) not in self.mine_positions:
                self.buttons[r_flag][c_flag].config(text='❌')
                if not self.is_closing:
                    print(f"잘못된 깃발: ({r_flag}, {c_flag})")
                
        for r_mine, c_mine in self.mine_positions:
            if (r_mine, c_mine) not in self.flags:
                self.buttons[r_mine][c_mine].config(text='💣', bg='lightgray', state='disabled')
        
        self.buttons[clicked_r][clicked_c].config(text='💥', bg='red', state='disabled')
        if not self.is_closing:
            found_mines = len([pos for pos in self.flags if pos in self.mine_positions])
            messagebox.showinfo("게임 오버", 
                               f"지뢰를 밟았습니다!\n\n시간: {self.seconds_passed}초\n찾은 지뢰: {found_mines}/{self.mines}개")

    def check_win_condition(self):
        """승리 조건을 확인합니다."""
        if len(self.revealed) == self.rows * self.cols - self.mines:
            self.game_over = True
            
            # 오토플레이 중지
            if self.auto_playing:
                self.stop_auto_play()
            
            # 타이머 완전히 정리
            self.stop_timer()
                
            if not self.is_closing:
                print(f"\n게임 승리! 시간: {self.seconds_passed}초")
            
            # 남은 지뢰들에 자동으로 깃발 표시
            for r in range(self.rows):
                for c in range(self.cols):
                    if (r, c) not in self.revealed and (r, c) not in self.flags:
                        self.flags.add((r, c))
                        self.buttons[r][c].config(text='🚩', fg='red', state='disabled')
            
            self.update_mine_count_label()
            self.update_found_mines_label()
            if not self.is_closing:
                messagebox.showinfo("승리!", 
                                   f"축하합니다!\n\n시간: {self.seconds_passed-1}초\n모든 지뢰를 찾았습니다! ({self.mines}/{self.mines}개)")
            
    def get_color(self, value):
        """숫자에 따라 다른 색상을 반환합니다."""
        colors = { '1': 'blue', '2': 'green', '3': 'red', '4': 'purple', '5': 'maroon', '6': 'turquoise', '7': 'black', '8': 'gray' }
        return colors.get(value, 'black')

    def cleanup(self):
        """게임 종료 시 정리 작업"""
        self.is_closing = True
        if self.auto_playing:
            self.stop_auto_play()
        self.stop_timer()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("지뢰찾기 - 오토플레이 버전")
    root.resizable(False, False)
    
    game = MinesweeperGUI(root, 9, 9, 10)
    
    # 창 닫을 때 정리 작업
    def on_closing():
        game.cleanup()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()