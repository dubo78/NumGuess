import tkinter as tk
from tkinter import ttk
import random
import os
import ctypes
import platform

class NumGuessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("숫자 맞추기")
        self.root.geometry("460x650") 
        self.root.resizable(False, False)
        
        # 1. 커스텀 폰트 로드 (Paperlogy-5Medium.ttf 사용)
        self.font_family = "Paperlogy-5Medium" # 폰트 내부 패밀리 네임 (윈도우/맥 공용)
        self.load_custom_font("Paperlogy-5Medium.ttf")

        self.colors = {
            "bg": "#F5F5F7",
            "card": "#FFFFFF",
            "primary": "#007AFF",
            "primary_active": "#005BB8",
            "secondary": "#86868B",
            "accent": "#5856D6",
            "success": "#34C759",
            "warning": "#FF9500",
            "error": "#FF3B30",
            "border": "#E5E5E7",
            "text": "#1D1D1F",
            "input_bg": "#F2F2F7"
        }

        self.root.configure(bg=self.colors["bg"])

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
        """윈도우에서 폰트 파일을 런타임에 등록. macOS는 설치된 폰트 사용 권장."""
        font_path = os.path.join(os.path.dirname(__file__), font_filename)
        
        if not os.path.exists(font_path):
            self.font_family = "Helvetica"
            return

        sys_platform = platform.system()
        
        if sys_platform == "Windows":
            try:
                import ctypes
                gdi32 = ctypes.WinDLL('gdi32')
                FR_PRIVATE = 0x10
                gdi32.AddFontResourceExW(font_path, FR_PRIVATE, 0)
            except Exception:
                pass # 윈도우 로딩 실패 시 무시
        
        # macOS/Linux는 폰트가 시스템에 설치되어 있어야 Tkinter가 인식함
        # 설치되어 있지 않으면 Tkinter가 알아서 기본 폰트로 대체하므로 앱은 죽지 않음
        pass

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_modern_button(self, parent, text, command, is_primary=True):
        bg_color = self.colors["primary"] if is_primary else self.colors["input_bg"]
        fg_color = "white" if is_primary else self.colors["text"]
        
        btn_frame = tk.Frame(parent, bg=bg_color, padx=20, pady=15)
        btn_label = tk.Label(btn_frame, text=text, font=(self.font_family, 18, "bold"), 
                             bg=bg_color, fg=fg_color, cursor="hand2")
        btn_label.pack()
        
        def on_click(event):
            if str(btn_label.cget("state")) != "disabled":
                command()
        
        def on_enter(event):
            if str(btn_label.cget("state")) != "disabled":
                new_bg = self.colors["primary_active"] if is_primary else "#E5E5E7"
                btn_frame.config(bg=new_bg)
                btn_label.config(bg=new_bg)

        def on_leave(event):
            if str(btn_label.cget("state")) != "disabled":
                btn_frame.config(bg=bg_color)
                btn_label.config(bg=bg_color)

        btn_label.bind("<Button-1>", on_click)
        btn_label.bind("<Enter>", on_enter)
        btn_label.bind("<Leave>", on_leave)
        
        return btn_frame, btn_label

    def create_modern_entry(self, parent, textvariable, width=7, font_size=32):
        entry_frame = tk.Frame(parent, bg=self.colors["input_bg"], padx=10, pady=8)
        entry = tk.Entry(entry_frame, textvariable=textvariable, font=(self.font_family, font_size, "bold"), 
                         width=width, justify="center", bd=0, bg=self.colors["input_bg"], 
                         fg=self.colors["text"], insertbackground=self.colors["primary"])
        entry.pack(padx=5)
        return entry_frame, entry

    def show_range_input_view(self):
        self.clear_screen()
        container = tk.Frame(self.root, bg=self.colors["bg"], padx=40, pady=50)
        container.pack(expand=True, fill="both")

        tk.Label(container, text="🎯", font=(self.font_family, 80), bg=self.colors["bg"]).pack(pady=(0, 10))
        tk.Label(container, text="숫자 맞추기", font=(self.font_family, 36, "bold"), 
                 bg=self.colors["bg"], fg=self.colors["text"]).pack()
        
        tk.Label(container, text="1부터 정해진 숫자 사이의\n정답을 맞춰보세요!", 
                 font=(self.font_family, 14), fg=self.colors["secondary"], bg=self.colors["bg"], 
                 justify="center").pack(pady=20)

        tk.Label(container, text="어디까지 섞을까요?", font=(self.font_family, 12, "bold"), 
                 fg=self.colors["secondary"], bg=self.colors["bg"]).pack(pady=(20, 5))
        
        input_container = tk.Frame(container, bg=self.colors["bg"])
        input_container.pack(pady=10)

        tk.Label(input_container, text="1  ~", font=(self.font_family, 24, "bold"), 
                 fg=self.colors["secondary"], bg=self.colors["bg"]).pack(side="left", padx=15)
        
        self.max_entry_var = tk.StringVar(value="10")
        entry_frame, self.max_entry = self.create_modern_entry(input_container, self.max_entry_var)
        entry_frame.pack(side="left")
        self.max_entry.focus_set()
        
        self.error_label = tk.Label(container, text="", font=(self.font_family, 10, "bold"), 
                                   fg=self.colors["error"], bg=self.colors["bg"])
        self.error_label.pack(pady=5)

        self.start_btn_frame, self.start_btn_label = self.create_modern_button(
            container, "시작하기", self.validate_and_start
        )
        self.start_btn_frame.pack(pady=40, fill="x")

        self.max_entry_var.trace_add("write", self.update_start_button)
        self.update_start_button()
        self.max_entry.bind("<Return>", lambda e: self.validate_and_start() if self.is_valid_max_input() else None)

    def is_valid_max_input(self):
        val = self.max_entry_var.get()
        return val.isdigit() and 10 <= int(val) <= 99999

    def update_start_button(self, *args):
        if self.is_valid_max_input():
            self.start_btn_frame.config(bg=self.colors["primary"])
            self.start_btn_label.config(bg=self.colors["primary"], state="normal")
            self.error_label.config(text="")
        else:
            self.start_btn_frame.config(bg=self.colors["border"])
            self.start_btn_label.config(bg=self.colors["border"], state="disabled")
            if self.max_entry_var.get():
                self.error_label.config(text="10 ~ 99,999 사이의 숫자를 입력하세요.")

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
        container = tk.Frame(self.root, bg=self.colors["bg"])
        container.pack(expand=True, fill="both")
        tk.Label(container, text="숫자를 섞는 중…", font=(self.font_family, 20, "bold"), 
                 fg=self.colors["secondary"], bg=self.colors["bg"]).pack(pady=(120, 20))
        self.shuffle_canvas = tk.Canvas(container, width=200, height=200, bg=self.colors["bg"], highlightthickness=0)
        self.shuffle_canvas.pack(pady=20)
        self.shuffle_canvas.create_oval(10, 10, 190, 190, outline=self.colors["accent"], width=8)
        self.shuffle_text = self.shuffle_canvas.create_text(100, 100, text="0", 
                                                          font=(self.font_family, 64, "bold"), fill=self.colors["accent"])
        self.progress = ttk.Progressbar(container, mode='indeterminate', length=250)
        self.progress.pack(pady=50)
        self.progress.start(15)
        self.shuffle_count = 0
        self.animate_shuffle()

    def animate_shuffle(self):
        if self.shuffle_count < 25:
            num = random.randint(1, self.max_number)
            self.shuffle_canvas.itemconfig(self.shuffle_text, text=str(num))
            self.shuffle_count += 1
            self.root.after(80, self.animate_shuffle)
        else:
            self.target_number = random.randint(1, self.max_number)
            self.show_guessing_view()

    def show_guessing_view(self):
        self.clear_screen()
        container = tk.Frame(self.root, bg=self.colors["bg"], padx=20, pady=30)
        container.pack(expand=True, fill="both")

        tk.Label(container, text="✨", font=(self.font_family, 54), bg=self.colors["bg"]).pack()
        tk.Label(container, text="어떤 숫자일까요?", font=(self.font_family, 24, "bold"), 
                 bg=self.colors["bg"], fg=self.colors["text"]).pack()
        
        msg_container = tk.Frame(container, bg=self.colors["bg"], height=80)
        msg_container.pack_propagate(False)
        msg_container.pack(fill="x", pady=10)

        self.msg_label = tk.Label(msg_container, text=random.choice(self.fun_messages), 
                                 font=(self.font_family, 15), fg=self.colors["primary"], 
                                 bg=self.colors["bg"], wraplength=400)
        self.msg_label.pack(expand=True)

        board_frame = tk.Frame(container, bg=self.colors["bg"])
        board_frame.pack(pady=20, fill="x")
        board_frame.columnconfigure(0, weight=1, uniform="half")
        board_frame.columnconfigure(1, weight=0)
        board_frame.columnconfigure(2, weight=1, uniform="half")

        left_side = tk.Frame(board_frame, bg=self.colors["bg"])
        left_side.grid(row=0, column=0, sticky="e")
        self.low_label = tk.Label(left_side, text="1", font=(self.font_family, 28, "bold"), 
                                 fg=self.colors["primary"], bg=self.colors["bg"])
        self.low_label.pack(side="left")
        self.low_op_label = tk.Label(left_side, text="≤", font=(self.font_family, 24, "bold"), 
                                    fg=self.colors["secondary"], bg=self.colors["bg"], padx=5)
        self.low_op_label.pack(side="left")

        self.guess_var = tk.StringVar()
        entry_frame, self.guess_entry = self.create_modern_entry(board_frame, self.guess_var, width=5, font_size=28)
        entry_frame.grid(row=0, column=1, padx=10)
        self.guess_entry.focus_set()

        right_side = tk.Frame(board_frame, bg=self.colors["bg"])
        right_side.grid(row=0, column=2, sticky="w")
        self.high_op_label = tk.Label(right_side, text="≤", font=(self.font_family, 24, "bold"), 
                                     fg=self.colors["secondary"], bg=self.colors["bg"], padx=5)
        self.high_op_label.pack(side="left")
        self.high_label = tk.Label(right_side, text="100", font=(self.font_family, 28, "bold"), 
                                  fg=self.colors["warning"], bg=self.colors["bg"])
        self.high_label.pack(side="left")

        self.update_bounds_display()

        self.feedback_container = tk.Frame(container, bg=self.colors["bg"], height=80)
        self.feedback_container.pack_propagate(False)
        self.feedback_container.pack(fill="x", pady=5)
        self.feedback_label = tk.Label(self.feedback_container, text="", font=(self.font_family, 14, "bold"), 
                                      bg=self.colors["bg"], wraplength=400)
        self.feedback_label.pack(expand=True)

        actions_frame = tk.Frame(container, bg=self.colors["bg"])
        actions_frame.pack(side="bottom", fill="x", pady=(0, 20))

        self.confirm_btn_frame, self.confirm_btn_label = self.create_modern_button(
            actions_frame, "확인하기", self.submit_guess
        )
        self.confirm_btn_frame.pack(fill="x", pady=(0, 20))

        footer = tk.Frame(actions_frame, bg=self.colors["bg"])
        footer.pack(fill="x")
        
        reset_btn = tk.Label(footer, text="↺ 처음으로", font=(self.font_family, 12, "bold"), 
                             fg=self.colors["secondary"], bg=self.colors["bg"], cursor="hand2")
        reset_btn.pack(side="left")
        reset_btn.bind("<Button-1>", lambda e: self.reset_game())
        
        self.attempts_label = tk.Label(footer, text=f"시도: {self.attempts}회", 
                                      font=(self.font_family, 12, "bold"), fg=self.colors["secondary"], bg=self.colors["bg"])
        self.attempts_label.pack(side="right")

        self.guess_var.trace_add("write", self.update_confirm_button)
        self.update_confirm_button()
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
            self.confirm_btn_frame.config(bg=self.colors["primary"])
            self.confirm_btn_label.config(bg=self.colors["primary"], state="normal")
        else:
            self.confirm_btn_frame.config(bg=self.colors["border"])
            self.confirm_btn_label.config(bg=self.colors["border"], state="disabled")

    def update_bounds_display(self):
        low_text = str(self.low_bound)
        high_text = str(self.high_bound)
        low_size = 28 if len(low_text) <= 3 else (22 if len(low_text) == 4 else 18)
        high_size = 28 if len(high_text) <= 3 else (22 if len(high_text) == 4 else 18)
        self.low_label.config(text=low_text, font=(self.font_family, low_size, "bold"))
        self.high_label.config(text=high_text, font=(self.font_family, high_size, "bold"))
        self.low_op_label.config(text="≤" if self.is_low_inclusive else "<")
        self.high_op_label.config(text="≤" if self.is_high_inclusive else "<")

    def submit_guess(self):
        if not self.is_valid_guess_input(): return
        
        guess = int(self.guess_var.get())
        self.attempts += 1
        self.attempts_label.config(text=f"시도: {self.attempts}회")
        self.msg_label.config(text=random.choice(self.fun_messages))
        self.guess_var.set("")

        if guess == self.target_number:
            self.feedback_label.config(text="정답입니다! 🎉", fg=self.colors["success"])
            self.show_congrats_view()
        elif guess > self.target_number:
            self.feedback_label.config(text="높아요! 더 낮게 시도해 보세요.", fg=self.colors["warning"])
            self.high_bound = min(self.high_bound, guess)
            self.is_high_inclusive = False
        else:
            self.feedback_label.config(text="낮아요! 더 높게 시도해 보세요.", fg=self.colors["primary"])
            self.low_bound = max(self.low_bound, guess)
            self.is_low_inclusive = False
            
        self.update_bounds_display()
        self.update_confirm_button()

    def show_congrats_view(self):
        congrats_win = tk.Toplevel(self.root)
        congrats_win.title("축하합니다!")
        congrats_win.geometry("380x540")
        congrats_win.transient(self.root)
        congrats_win.grab_set()
        congrats_win.configure(bg=self.colors["card"])
        congrats_win.resizable(False, False)

        tk.Label(congrats_win, text="👑", font=(self.font_family, 80), bg=self.colors["card"]).pack(pady=(60, 10))
        tk.Label(congrats_win, text="축하합니다!", font=(self.font_family, 36, "bold"), bg=self.colors["card"]).pack()
        tk.Label(congrats_win, text=f"정답은 {self.target_number}였습니다!", 
                 font=(self.font_family, 20, "bold"), fg=self.colors["primary"], bg=self.colors["card"]).pack(pady=20)
        tk.Label(congrats_win, text=f"{self.attempts}번 만에 맞추셨네요!", 
                 font=(self.font_family, 15), fg=self.colors["secondary"], bg=self.colors["card"]).pack()

        def restart():
            congrats_win.destroy()
            self.reset_game()

        btn_frame, _ = self.create_modern_button(congrats_win, "새 게임 시작하기", restart)
        btn_frame.pack(pady=60, padx=40, fill="x")
        congrats_win.bind("<Return>", lambda e: restart())

    def reset_game(self):
        self.show_range_input_view()

if __name__ == "__main__":
    root = tk.Tk()
    app = NumGuessApp(root)
    root.mainloop()
