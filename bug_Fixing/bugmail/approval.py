from __future__ import annotations

import os
import tkinter as tk
from pathlib import Path
from tkinter import messagebox


def request_approval(summary: str, cause: str, action: str, confidence: float, report_path: Path) -> str:
    result = {"value": "later"}
    root = tk.Tk()
    root.title("内网报错需要确认")
    width, height = 760, 520
    screen_x = max(0, (root.winfo_screenwidth() - width) // 2)
    screen_y = max(0, (root.winfo_screenheight() - height) // 2)
    root.geometry(f"{width}x{height}+{screen_x}+{screen_y}")
    root.minsize(680, 440)
    root.attributes("-topmost", True)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(2, weight=1)

    tk.Label(root, text="检测到可能需要修改的内网报错", font=("Microsoft YaHei UI", 15, "bold")).grid(
        row=0, column=0, sticky="w", padx=24, pady=(22, 10)
    )
    tk.Label(
        root,
        text=f"类型：{action}    置信度：{confidence:.0%}",
        font=("Microsoft YaHei UI", 10),
    ).grid(row=1, column=0, sticky="w", padx=24)
    text = tk.Text(root, wrap="word", font=("Microsoft YaHei UI", 10), relief="solid", borderwidth=1)
    text.grid(row=2, column=0, sticky="nsew", padx=24, pady=14)
    text.insert("1.0", f"错误摘要\n{summary}\n\n最可能原因\n{cause}")
    text.configure(state="disabled")

    buttons = tk.Frame(root)
    buttons.grid(row=3, column=0, sticky="ew", padx=24, pady=(0, 22))
    buttons.columnconfigure(1, weight=1)

    def choose(value: str) -> None:
        result["value"] = value
        root.destroy()

    def open_report() -> None:
        os.startfile(str(report_path))

    tk.Button(buttons, text="查看完整报告", width=14, height=2, command=open_report).grid(row=0, column=0, sticky="w")
    tk.Button(buttons, text="忽略此错误", width=12, height=2, command=lambda: choose("ignore")).grid(
        row=0, column=2, padx=(8, 0)
    )
    tk.Button(buttons, text="稍后处理", width=12, height=2, command=lambda: choose("later")).grid(
        row=0, column=3, padx=(8, 0)
    )
    approve = tk.Button(
        buttons,
        text="确认并开始修改",
        width=16,
        height=2,
        bg="#176b3a",
        fg="white",
        activebackground="#12572f",
        activeforeground="white",
        font=("Microsoft YaHei UI", 10, "bold"),
        command=lambda: choose("approve"),
    )
    approve.grid(row=0, column=4, padx=(12, 0))
    root.bind("<Control-Return>", lambda _event: choose("approve"))
    root.protocol("WM_DELETE_WINDOW", lambda: choose("later"))
    try:
        root.mainloop()
    except tk.TclError as error:
        messagebox.showerror("内网报错分析", str(error))
        return "later"
    return result["value"]
