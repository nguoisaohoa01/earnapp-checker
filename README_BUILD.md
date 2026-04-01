# 🚀 EarnApp Checker - Build Instructions

## ✨ Có 2 cách để build .EXE:

### Cách 1️⃣: Tự động với GitHub Actions (Khuyến nghị)
- ✅ Dễ nhất, không cần cài đặt gì trên máy
- ✅ Tự động build khi push code
- **Cách làm:**
  1. Push code lên GitHub
  2. Vào tab **Actions** → tìm workflow **Build EXE**
  3. Download file .exe từ **Artifacts**

### Cách 2️⃣: Build trên máy Windows cá nhân
**Yêu cầu:**
- ✅ Python 3.8+ (từ https://www.python.org/)
- ✅ Thêm Python vào PATH

**Các bước:**
```bash
# 1. Mở Command Prompt (cmd) hoặc PowerShell
# 2. Điều hướng đến thư mục project
cd C:\path\to\earnapp-checker

# 3. Cài đặt dependencies
pip install -r requirements.txt

# 4. Build EXE
python build_exe.py
```

**Result:**
- File .exe sẽ nằm trong: `dist/EarnApp-Checker.exe`
- Có thể chia sẻ file này cho bất kỳ ai mà không cần Python

---

## 📋 File Structure

```
earnapp-checker/
├── tool_vip.py              # Mã nguồn chính
├── requirements.txt         # Thư viện cần thiết
├── build_exe.py            # Script build tự động
├── .github/
│   └── workflows/
│       └── build.yml       # GitHub Actions workflow
└── README.md
```

---

## 🔍 Troubleshooting

### ❌ "Python not found"
- Cài lại Python từ https://www.python.org/
- Chọn ✅ "Add Python to PATH"

### ❌ "ModuleNotFoundError: No module named 'tkinter'"
- Windows: Cài lại Python, chọn ✅ "tcl/tk and IDLE"
- Ubuntu/Debian: `sudo apt install python3-tk`

### ❌ "pyinstaller: command not found"
```bash
pip install --upgrade pyinstaller
```

---

## 📝 Notes
- File .exe là single-file executable (không cần thư viện phụ)
- Kích thước: ~50-100MB (tùy Python version)
- Chạy được trên bất kỳ Windows nào (không cần Python)