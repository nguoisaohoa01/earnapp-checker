import tkinter as tk
from tkinter import ttk, filedialog
import requests
import threading
import queue
import time

CHECK_IP_API = "https://api.ipify.org"
EARNAPP_API = "https://earnapp.com/dashboard/api/check_ip/{}"

class VIPTool:
    def __init__(self, root):
        self.root = root
        self.root.title("EarnApp IP Checker (VIP)")
        self.root.geometry("1100x650")
        self.root.configure(bg="#0b1220")

        self.q = queue.Queue()

        self.ok = 0
        self.blocked = 0
        self.error = 0

        self.setup_ui()
        self.root.after(100, self.update_gui)

    # ================= UI =================
    def setup_ui(self):
        # TITLE
        tk.Label(self.root, text="🔍 EarnApp IP Checker (Simple API)",
                 bg="#0b1220", fg="white", font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=10, pady=5)

        # INPUT
        tk.Label(self.root, text="Nhập IP hoặc Proxy (mỗi dòng):",
                 bg="#0b1220", fg="#9ca3af").pack(anchor="w", padx=10)

        self.input_box = tk.Text(self.root, height=6, bg="#111827", fg="white",
                                 insertbackground="white", relief="flat")
        self.input_box.pack(fill="x", padx=10, pady=5)

        # BUTTONS
        btn_frame = tk.Frame(self.root, bg="#0b1220")
        btn_frame.pack(fill="x")

        self.btn_start = tk.Button(btn_frame, text="▶ Start Check", bg="#22c55e", fg="black",
                                   command=self.start)
        self.btn_start.pack(side="left", padx=5)

        tk.Button(btn_frame, text="📋 Paste", command=self.paste).pack(side="left", padx=5)
        tk.Button(btn_frame, text="🧹 Clear", command=self.clear).pack(side="left", padx=5)
        tk.Button(btn_frame, text="💾 Export", command=self.export).pack(side="left", padx=5)

        # TABLE
        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview",
                        background="#111827",
                        foreground="white",
                        rowheight=26,
                        fieldbackground="#111827")

        style.map("Treeview", background=[("selected", "#2563eb")])

        columns = ("proxy", "ip", "status", "reason", "time")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col.upper())

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # COLOR TAGS
        self.tree.tag_configure("ok", foreground="#22c55e")
        self.tree.tag_configure("blocked", foreground="#ef4444")
        self.tree.tag_configure("error", foreground="#facc15")

        # STATUS BAR
        self.status = tk.Label(self.root,
                               text="OK: 0 | Blocked: 0 | Error: 0 | Total: 0",
                               bg="#0b1220", fg="white")
        self.status.pack(anchor="w", padx=10)

    # ================= ACTION =================
    def paste(self):
        try:
            self.input_box.insert("end", self.root.clipboard_get() + "\n")
        except:
            pass

    def clear(self):
        self.tree.delete(*self.tree.get_children())
        self.ok = self.blocked = self.error = 0
        self.update_status()

    def export(self):
        file = filedialog.asksaveasfilename(defaultextension=".txt")
        if not file:
            return

        with open(file, "w") as f:
            for row in self.tree.get_children():
                f.write(str(self.tree.item(row)["values"]) + "\n")

    def update_status(self):
        total = self.ok + self.blocked + self.error
        self.status.config(text=f"OK: {self.ok} | Blocked: {self.blocked} | Error: {self.error} | Total: {total}")

    # ================= CORE =================
    def parse_proxy(self, line):
        parts = line.split(":")
        if len(parts) == 4:
            ip, port, user, pwd = parts
            return {
                "http": f"http://{user}:{pwd}@{ip}:{port}",
                "https": f"http://{user}:{pwd}@{ip}:{port}"
            }
        return None

    def worker(self, line):
        start = time.time()
        proxy = self.parse_proxy(line)

        try:
            # Lấy outbound IP qua proxy
            r_ip = requests.get(CHECK_IP_API, proxies=proxy, timeout=8)
            outbound_ip = r_ip.text.strip()

            # Check EarnApp
            r = requests.get(EARNAPP_API.format(outbound_ip), timeout=8)

            if r.status_code == 200:
                status = "OK"
                tag = "ok"
                self.ok += 1
                reason = "-"
            else:
                status = "BLOCKED"
                tag = "blocked"
                self.blocked += 1
                reason = "EarnApp Reject"

        except:
            outbound_ip = "-"
            status = "ERROR"
            tag = "error"
            self.error += 1
            reason = "CONN_FAIL"

        t = int((time.time() - start) * 1000)

        self.q.put((line, outbound_ip, status, reason, f"{t} ms", tag))

    def start(self):
        lines = self.input_box.get("1.0", "end").strip().splitlines()

        for line in lines:
            threading.Thread(target=self.worker, args=(line.strip(),)).start()

    def update_gui(self):
        while not self.q.empty():
            data = self.q.get()
            self.tree.insert("", "end",
                             values=data[:5],
                             tags=(data[5],))
            self.update_status()

        self.root.after(100, self.update_gui)


root = tk.Tk()
VIPTool(root)
root.mainloop()