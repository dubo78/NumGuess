import customtkinter as ctk
import random
import os
import sys
import ctypes
import platform
from PIL import Image

# 기본 테마 설정
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

def resource_path(relative_path):
    """ 실행 파일 내부에 포함된 리소스의 실제 경로를 찾는 함수 (빌드/개발 겸용) """
    try:
        # PyInstaller 빌드 시 임시 폴더 경로
        base_path = sys._MEIPASS
    except Exception:
        # 개발 중일 때 현재 폴더 경로
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class NumGuessApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("숫자 맞추기")
        self.geometry("500x680")
        self.resizable(False, False)
        
        # 폰트 패밀리 네임 설정 및 런타임 로드
        self.font_family = "Paperlogy-5Medium"
        self.load_custom_font("Paperlogy-5Medium.ttf")
        
        # Game State
        self.max_number = None
        self.target_number = None
        self.attempts = 0
        self.low_bound = 1
        self.high_bound = 100
        self.is_low_inclusive = True
        self.is_high_inclusive = True
        
        self.fun_messages = [
            "행운을 빌어요! 🍀", "어떤 숫자일까요? 🤔", "감을 믿어보세요! ✨",
            "거의 다 왔을지도? 🚀", "천천히 맞춰보세요 🐢", "정답은 이 안에 있습니다! 🎯",
            "두뇌 풀가동! 🧠", "할 수 있어요! 💪", "어디있을까아~? 여기일까아~? 💕",
            "히히, 어떤 숫자인지 궁금하죠? 😉", "두구두구두구... 과연?! 🥁",
            "오늘 운세가 좋은데요? 가보자고! 🔥", "포기하지 마세요! 거의 다 왔어요! 🏆",
            "당신의 직감을 믿으세요. 찍기 신공! ✨", "오! 감이 오나요? 범인은 이 안에 있어! 🕵️",
            "집중! 집중! 숫자가 속삭이고 있어요 🤫", "숫자들의 숨바꼭질! 꼭꼭 숨어라~ 🙈",
            "정답이 부끄러움을 많이 타나 봐요 ☺️", "한 번 더! 이번엔 느낌이 왔어! 🌈",
            "당신의 뇌섹미를 보여주세요! 😎", "정답이 기다리고 있어요! 뀨? 🐾",
            "숫자 신님이 보우하사! ⛩️", "정답과 썸 타는 중인가요? 💘",
            "빨리 맞춰주세요! 현기증 난단 말이에요 😵‍💫", "가장 완벽한 추측은 지금입니다! 💎",
            "정답은 바로 당신의 마음속에... 넝담! 😜", "이 정도면 멘사 가입 권유받겠는데요? 🎓"
        ]

        self.show_range_input_view()

    def load_custom_font(self, font_filename):
        """운영체제별 리소스 경로를 찾아 폰트 등록"""
        font_path = resource_path(font_filename)
        
        if not os.path.exists(font_path):
            self.font_family = "Helvetica"
            return

        if platform.system() == "Windows":
            try:
                import ctypes
                gdi32 = ctypes.WinDLL('gdi32')
                gdi32.AddFontResourceExW(font_path, 0x10, 0)
            except:
                pass
        # macOS는 설치된 폰트를 우선 사용하거나 기본 폰트로 대체 (안정성 우선)

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_range_input_view(self):
        self.clear_screen()
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=40, pady=40)

        icon_label = ctk.CTkLabel(container, text="🎯", font=(self.font_family, 100))
        icon_label.pack(pady=(0, 10))

        ctk.CTkLabel(container, text="숫자 맞추기", font=(self.font_family, 38, "bold"), text_color="#1D1D1F").pack()
        ctk.CTkLabel(container, text="1부터 정해진 숫자 사이의\n정답을 맞춰보세요!", font=(self.font_family, 16), text_color="#86868B").pack(pady=20)

        input_card = ctk.CTkFrame(container, fg_color="#FFFFFF", corner_radius=20, border_width=1, border_color="#E5E5E7")
        input_card.pack(fill="x", pady=20, padx=10)
        
        input_inner = ctk.CTkFrame(input_card, fg_color="transparent")
        input_inner.pack(pady=25, padx=20)

        ctk.CTkLabel(input_inner, text="1  ~", font=(self.font_family, 26, "bold"), text_color="#86868B").pack(side="left", padx=(0, 15))
        
        self.max_entry_var = ctk.StringVar(value="10")
        self.max_entry = ctk.CTkEntry(input_inner, textvariable=self.max_entry_var, width=140, height=55, 
                                     font=(self.font_family, 28, "bold"), justify="center",
                                     fg_color="#F2F2F7", border_width=0, corner_radius=12)
        self.max_entry.pack(side="left")
        self.max_entry.focus_set()
        
        self.error_label = ctk.CTkLabel(container, text="", font=(self.font_family, 13, "bold"), text_color="#FF3B30")
        self.error_label.pack(pady=5)

        self.start_btn = ctk.CTkButton(container, text="시작하기", height=65, font=(self.font_family, 20, "bold"), corner_radius=32, command=self.validate_and_start)
        self.start_btn.pack(pady=30, fill="x")

        self.max_entry_var.trace_add("write", self.update_start_button)
        self.update_start_button()
        self.max_entry.bind("<Return>", lambda e: self.validate_and_start() if self.is_valid_max_input() else None)

    def is_valid_max_input(self):
        val = self.max_entry_var.get()
        return val.isdigit() and 10 <= int(val) <= 99999

    def update_start_button(self, *args):
        if self.is_valid_max_input():
            self.start_btn.configure(state="normal", fg_color="#007AFF")
            self.error_label.configure(text="")
        else:
            self.start_btn.configure(state="disabled", fg_color="#D1D1D6")
            if self.max_entry_var.get():
                self.error_label.configure(text="10 ~ 99,999 사이의 숫자를 입력하세요.")

    def validate_and_start(self):
        if self.is_valid_max_input():
            self.max_number = int(self.max_entry_var.get())
            self.low_bound = 1
            self.high_bound = self.max_number
            self.is_low_inclusive = True
            self.is_high_inclusive = True
            self.attempts = 0
            self.show_shuffle_view()

    def show_shuffle_view(self):
        self.clear_screen()
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(expand=True, fill="both")
        ctk.CTkLabel(container, text="숫자를 섞는 중…", font=(self.font_family, 22, "bold"), text_color="#86868B").pack(pady=(120, 20))
        self.shuffle_frame = ctk.CTkFrame(container, width=220, height=220, corner_radius=110, fg_color="#FFFFFF", border_width=8, border_color="#5856D6")
        self.shuffle_frame.pack_propagate(False)
        self.shuffle_frame.pack(pady=20)
        self.shuffle_label = ctk.CTkLabel(self.shuffle_frame, text="0", font=(self.font_family, 68, "bold"), text_color="#5856D6")
        self.shuffle_label.place(relx=0.5, rely=0.5, anchor="center")
        self.progress = ctk.CTkProgressBar(container, width=280, height=12, indeterminate_speed=1.5)
        self.progress.pack(pady=60)
        self.progress.start()
        self.shuffle_count = 0
        self.animate_shuffle()

    def animate_shuffle(self):
        if self.shuffle_count < 25:
            num = random.randint(1, self.max_number)
            self.shuffle_label.configure(text=str(num))
            self.shuffle_count += 1
            self.after(80, self.animate_shuffle)
        else:
            self.target_number = random.randint(1, self.max_number)
            self.show_guessing_view()

    def show_guessing_view(self):
        self.clear_screen()
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=20, pady=30)

        ctk.CTkLabel(container, text="✨", font=(self.font_family, 64)).pack()
        ctk.CTkLabel(container, text="어떤 숫자일까요?", font=(self.font_family, 26, "bold"), text_color="#1D1D1F").pack()
        
        msg_card = ctk.CTkFrame(container, height=90, fg_color="transparent")
        msg_card.pack_propagate(False)
        msg_card.pack(fill="x", pady=10)
        self.msg_label = ctk.CTkLabel(msg_card, text=random.choice(self.fun_messages), font=(self.font_family, 17, "normal"), text_color="#007AFF", wraplength=450)
        self.msg_label.pack(expand=True)

        board_frame = ctk.CTkFrame(container, fg_color="transparent")
        board_frame.pack(pady=20, fill="x")
        
        board_frame.columnconfigure(0, weight=1)
        board_frame.columnconfigure(1, weight=0)
        board_frame.columnconfigure(2, weight=0)
        board_frame.columnconfigure(3, weight=0)
        board_frame.columnconfigure(4, weight=1)

        self.low_label = ctk.CTkLabel(board_frame, text="1", font=(self.font_family, 32, "bold"), text_color="#007AFF")
        self.low_label.grid(row=0, column=0, sticky="e")
        
        self.low_op_label = ctk.CTkLabel(board_frame, text="≤", font=(self.font_family, 28, "bold"), text_color="#86868B")
        self.low_op_label.grid(row=0, column=1, padx=5)

        self.guess_var = ctk.StringVar()
        self.guess_entry = ctk.CTkEntry(board_frame, textvariable=self.guess_var, width=160, height=65, 
                                       font=(self.font_family, 32, "bold"), justify="center",
                                       fg_color="#FFFFFF", border_width=2, 
                                       border_color="#007AFF", corner_radius=15)
        self.guess_entry.grid(row=0, column=2, padx=10)
        self.guess_entry.focus_set()

        self.high_op_label = ctk.CTkLabel(board_frame, text="≤", font=(self.font_family, 28, "bold"), text_color="#86868B")
        self.high_op_label.grid(row=0, column=3, padx=5)

        self.high_label = ctk.CTkLabel(board_frame, text="100", font=(self.font_family, 32, "bold"), text_color="#FF9500")
        self.high_label.grid(row=0, column=4, sticky="w")

        self.update_bounds_display()

        feedback_card = ctk.CTkFrame(container, height=80, fg_color="transparent")
        feedback_card.pack_propagate(False)
        feedback_card.pack(fill="x", pady=10)
        self.feedback_label = ctk.CTkLabel(feedback_card, text="", font=(self.font_family, 16, "bold"), wraplength=450)
        self.feedback_label.pack(expand=True)

        actions = ctk.CTkFrame(container, fg_color="transparent")
        actions.pack(side="bottom", fill="x", pady=(0, 20))
        self.confirm_btn = ctk.CTkButton(actions, text="확인하기", height=65, font=(self.font_family, 20, "bold"), corner_radius=18, command=self.submit_guess)
        self.confirm_btn.pack(fill="x", pady=(0, 20))

        footer = ctk.CTkFrame(actions, fg_color="transparent")
        footer.pack(fill="x")
        reset_btn = ctk.CTkLabel(footer, text="↺ 처음으로", font=(self.font_family, 14, "bold"), text_color="#86868B", cursor="hand2")
        reset_btn.pack(side="left")
        reset_btn.bind("<Button-1>", lambda e: self.reset_game())
        self.attempts_label = ctk.CTkLabel(footer, text=f"시도: {self.attempts}회", font=(self.font_family, 14, "bold"), text_color="#86868B")
        self.attempts_label.pack(side="right")

        self.guess_var.trace_add("write", self.update_confirm_button)
        self.guess_entry.bind("<Return>", lambda e: self.submit_guess() if self.is_valid_guess_input() else None)

    def is_valid_guess_input(self):
        val_str = self.guess_var.get()
        if not val_str.isdigit(): return False
        val = int(val_str)
        low_check = (val >= self.low_bound) if self.is_low_inclusive else (val > self.low_bound)
        high_check = (val <= self.high_bound) if self.is_high_inclusive else (val < self.high_bound)
        return low_check and high_check

    def update_confirm_button(self, *args):
        if self.is_valid_guess_input():
            self.confirm_btn.configure(state="normal", fg_color="#007AFF")
        else:
            self.confirm_btn.configure(state="disabled", fg_color="#D1D1D6")

    def update_bounds_display(self):
        low_text = str(self.low_bound)
        high_text = str(self.high_bound)
        low_size = 32 if len(low_text) <= 3 else (26 if len(low_text) == 4 else 20)
        high_size = 32 if len(high_text) <= 3 else (26 if len(high_text) == 4 else 20)
        self.low_label.configure(text=low_text, font=(self.font_family, low_size, "bold"))
        self.high_label.configure(text=high_text, font=(self.font_family, high_size, "bold"))
        self.low_op_label.configure(text="≤" if self.is_low_inclusive else "<")
        self.high_op_label.configure(text="≤" if self.is_high_inclusive else "<")

    def submit_guess(self):
        if not self.is_valid_guess_input(): return
        guess = int(self.guess_var.get())
        self.attempts += 1
        self.attempts_label.configure(text=f"시도: {self.attempts}회")
        self.msg_label.configure(text=random.choice(self.fun_messages))
        self.guess_var.set("")
        if guess == self.target_number:
            self.feedback_label.configure(text="정답입니다! 🎉", text_color="#34C759")
            self.show_congrats_view()
        elif guess > self.target_number:
            self.feedback_label.configure(text="높아요! 더 낮게 시도해 보세요.", text_color="#FF9500")
            self.high_bound = min(self.high_bound, guess)
            self.is_high_inclusive = False
        else:
            self.feedback_label.configure(text="낮아요! 더 높게 시도해 보세요.", text_color="#007AFF")
            self.low_bound = max(self.low_bound, guess)
            self.is_low_inclusive = False
        self.update_bounds_display()
        self.update_confirm_button()

    def show_congrats_view(self):
        congrats_win = ctk.CTkToplevel(self)
        congrats_win.title("축하합니다!")
        congrats_win.geometry("400x560")
        congrats_win.attributes("-topmost", True)
        congrats_win.configure(fg_color="#FFFFFF")
        congrats_win.resizable(False, False)
        content = ctk.CTkFrame(congrats_win, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=40, pady=40)
        ctk.CTkLabel(content, text="👑", font=(self.font_family, 100)).pack(pady=(20, 10))
        ctk.CTkLabel(content, text="축하합니다!", font=(self.font_family, 42, "bold"), text_color="#1D1D1F").pack()
        ctk.CTkLabel(content, text=f"정답은 {self.target_number}였습니다!", font=(self.font_family, 22, "bold"), text_color="#007AFF").pack(pady=20)
        ctk.CTkLabel(content, text=f"{self.attempts}번 만에 맞추셨네요!", font=(self.font_family, 17), text_color="#86868B").pack()
        def restart():
            congrats_win.destroy()
            self.reset_game()
        ctk.CTkButton(content, text="새 게임 시작하기", height=65, font=(self.font_family, 20, "bold"), corner_radius=32, command=restart).pack(pady=60, fill="x")
        congrats_win.bind("<Return>", lambda e: restart())

    def reset_game(self):
        self.show_range_input_view()

if __name__ == "__main__":
    app = NumGuessApp()
    app.mainloop()
