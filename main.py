"""
Windows System Cleaner Pro v1.0.0
A modern, production-ready disk cleaning application built with
CustomTkinter and native Windows APIs.
Full Arabic / English bilingual support.
"""

# ══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ══════════════════════════════════════════════════════════════════════════════
import sys
import os
import ctypes
import threading
import queue
import time
import shutil
import subprocess
from tkinter import filedialog, messagebox

# ══════════════════════════════════════════════════════════════════════════════
# UAC ELEVATION CHECK
# ══════════════════════════════════════════════════════════════════════════════
def _is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

if not _is_admin():
    try:
        if getattr(sys, "frozen", False):
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, "", None, 1
            )
        else:
            params = " ".join(f'"{a}"' for a in sys.argv)
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, params, None, 1
            )
    except Exception:
        pass
    sys.exit(0)

# ══════════════════════════════════════════════════════════════════════════════
# CUSTOMTKINTER
# ══════════════════════════════════════════════════════════════════════════════
try:
    import customtkinter as ctk
except ImportError:
    from tkinter import messagebox as _mb
    _mb.showerror(
        "Missing Dependency",
        "customtkinter is required.\n\nInstall it:\n  pip install customtkinter",
    )
    sys.exit(1)

# ══════════════════════════════════════════════════════════════════════════════
# LANGUAGE SYSTEM — all UI strings in Arabic & English
# ══════════════════════════════════════════════════════════════════════════════
STRINGS = {
    "app_title":       {"en": "Windows System Cleaner Pro",   "ar": "مُنظّف ويندوز الاحترافي"},
    "scan":            {"en": "🔍  Scan System",              "ar": "🔍  فحص النظام"},
    "scanning":        {"en": "⏳  Scanning…",                "ar": "⏳  جاري الفحص…"},
    "clean":           {"en": "🧹  Start Cleaning",           "ar": "🧹  بدء المسح"},
    "cleaning":        {"en": "⏳  Cleaning…",                "ar": "⏳  جاري المسح…"},
    "ready":           {"en": "Ready",                        "ar": "جاهز"},
    "scan_complete":   {"en": "Scan complete ✓",              "ar": "اكتمل الفحص ✓"},
    "clean_complete":  {"en": "Cleaned ✓",                    "ar": "اكتمل المسح ✓"},
    "recoverable":     {"en": "recoverable",                  "ar": "قابل للاسترجاع"},
    "freed":           {"en": "freed",                        "ar": "تم تحريره"},
    "skipped":         {"en": "skipped",                      "ar": "تم تخطيه"},
    "locked":          {"en": "locked files",                 "ar": "ملفات مقفلة"},
    "select_all":      {"en": "Select All",                   "ar": "تحديد الكل"},
    "confirm_clean":   {"en": "Confirm Cleaning",             "ar": "تأكيد المسح"},
    "confirm_msg":     {"en": "Delete all selected files?",   "ar": "هل أنت متأكد من حذف جميع الملفات المحددة؟"},
    "nothing_selected":{"en": "No categories selected",       "ar": "لم يتم تحديد أي فئة"},
    "nothing_to_clean":{"en": "Nothing to clean",             "ar": "لا شيء لمسحه"},
    "total":           {"en": "Total recoverable",            "ar": "الإجمالي القابل للاسترجاع"},
    "categories":      {"en": "Scan Categories",              "ar": "فئات الفحص"},
    "custom_paths":    {"en": "Custom Paths",                 "ar": "مسارات مخصصة"},
    "add_folder":      {"en": "＋  Add Folder",               "ar": "＋  إضافة مجلد"},
    "age_filter":      {"en": "Delete files older than (days, 0 = all):",
                        "ar":  "حذف الملفات الأقدم من (أيام، 0 = الكل):"},
    "select_folder":   {"en": "Select Folder",                "ar": "اختر مجلداً"},
    "lang_toggle":     {"en": "عربي",                        "ar": "EN"},
    "shortcut_created":{"en": "Desktop shortcut created ✓",  "ar": "تم إنشاء شورتكت سطح المكتب ✓"},
    # Category names
    "user_temp":       {"en": "User Temp Files",              "ar": "ملفات المؤقت للمستخدم"},
    "sys_temp":        {"en": "Windows System Temp",          "ar": "ملفات مؤقت النظام"},
    "prefetch":        {"en": "Windows Prefetch",             "ar": "ملفات التنقل المسبق"},
    "error_dumps":     {"en": "Error Reports & Crash Dumps",  "ar": "تقارير الأخطاء وملفات العطل"},
    "recycle":         {"en": "Recycle Bin",                  "ar": "سلة المهملات"},
    "chrome":          {"en": "Google Chrome Cache",          "ar": "ذاكرة كروم المؤقتة"},
    "edge":            {"en": "Microsoft Edge Cache",         "ar": "ذاكرة إيدج المؤقتة"},
    # Log messages
    "log_scan_start":  {"en": "═══ SCAN STARTED ═══",         "ar": "═══ بدء الفحص ═══"},
    "log_scan_done":   {"en": "═══ SCAN COMPLETE ═══",        "ar": "═══ اكتمل الفحص ═══"},
    "log_clean_start": {"en": "═══ CLEAN STARTED ═══",        "ar": "═══ بدء المسح ═══"},
    "log_clean_done":  {"en": "═══ CLEAN COMPLETE ═══",       "ar": "═══ اكتمل المسح ═══"},
    "log_freed":       {"en": "freed",                        "ar": "تم تحريره"},
    "log_scanning":    {"en": "Scanning…",                    "ar": "جاري الفحص…"},
    "log_cleaning":    {"en": "Cleaning…",                    "ar": "جاري المسح…"},
    "log_no_select":   {"en": "No categories selected.",      "ar": "لم يتم تحديد أي فئة."},
    "log_nothing":     {"en": "Nothing to clean.",            "ar": "لا شيء لمسحه."},
}

# Category icon mapping
CAT_ICONS = {
    "user_temp":  "📁",
    "sys_temp":   "⚙️",
    "prefetch":   "⚡",
    "error_dumps":"⚠️",
    "recycle":    "🗑️",
    "chrome":     "🌐",
    "edge":       "🔷",
}

# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════
APP_VER = "1.0.0"
LOCAL = os.environ.get("LOCALAPPDATA", "")
TEMP = os.environ.get("TEMP", "")

CATEGORIES = [
    {
        "id": "user_temp",
        "paths": [TEMP] if TEMP else [],
    },
    {
        "id": "sys_temp",
        "paths": [r"C:\Windows\Temp"],
    },
    {
        "id": "prefetch",
        "paths": [r"C:\Windows\Prefetch"],
    },
    {
        "id": "error_dumps",
        "paths": [
            r"C:\Windows\LiveKernelReports",
            r"C:\Windows\Minidump",
            os.path.join(LOCAL, "CrashDumps") if LOCAL else "",
            r"C:\ProgramData\Microsoft\Windows\WER",
        ],
    },
    {
        "id": "recycle",
        "paths": [],
    },
    {
        "id": "chrome",
        "paths": [
            os.path.join(LOCAL, p) for p in (
                r"Google\Chrome\User Data\Default\Cache",
                r"Google\Chrome\User Data\Default\Code Cache",
                r"Google\Chrome\User Data\Default\Service Worker\CacheStorage",
            )
        ] if LOCAL else [],
    },
    {
        "id": "edge",
        "paths": [
            os.path.join(LOCAL, p) for p in (
                r"Microsoft\Edge\User Data\Default\Cache",
                r"Microsoft\Edge\User Data\Default\Code Cache",
                r"Microsoft\Edge\User Data\Default\Service Worker\CacheStorage",
            )
        ] if LOCAL else [],
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════
def fmt(n):
    for u in ("B", "KB", "MB", "GB", "TB"):
        if abs(n) < 1024:
            return f"{n:.1f} {u}"
        n /= 1024
    return f"{n:.1f} PB"


def dir_size(path):
    total = 0
    try:
        for dp, _, fns in os.walk(path):
            for f in fns:
                try:
                    total += os.path.getsize(os.path.join(dp, f))
                except Exception:
                    pass
    except Exception:
        pass
    return total


def dir_size_aged(path, days):
    if not days:
        return dir_size(path)
    total = 0
    cutoff = time.time() - days * 86400
    try:
        for dp, _, fns in os.walk(path):
            for f in fns:
                fp = os.path.join(dp, f)
                try:
                    if os.path.getmtime(fp) < cutoff:
                        total += os.path.getsize(fp)
                except Exception:
                    pass
    except Exception:
        pass
    return total


def wipe_dir(path, days=0):
    freed = skipped = 0
    cutoff = time.time() - days * 86400 if days else 0
    try:
        for dp, dns, fns in os.walk(path, topdown=False):
            for fn in fns:
                fp = os.path.join(dp, fn)
                try:
                    if cutoff and os.path.getmtime(fp) >= cutoff:
                        continue
                    freed += os.path.getsize(fp)
                    os.remove(fp)
                except (PermissionError, OSError):
                    skipped += 1
                except Exception:
                    skipped += 1
            for d in dns:
                try:
                    os.rmdir(os.path.join(dp, d))
                except Exception:
                    pass
    except Exception:
        pass
    return freed, skipped


def scan_recycle_bin():
    try:
        import winshell
        return sum(item.original_size() for item in winshell.recycle_bin())
    except Exception:
        return dir_size(r"C:\$Recycle.Bin")


def empty_recycle_bin():
    try:
        import winshell
        winshell.empty()
        return 0, 0
    except Exception:
        return wipe_dir(r"C:\$Recycle.Bin")


def create_desktop_shortcut():
    """Create a desktop shortcut using PowerShell IShellLink COM."""
    desktop = os.path.join(os.environ.get("USERPROFILE", ""), "Desktop")
    shortcut_path = os.path.join(desktop, "SystemCleanerPro.lnk")

    if os.path.exists(shortcut_path):
        return True

    # Determine the target path
    if getattr(sys, "frozen", False):
        target = sys.executable
    else:
        target = sys.executable
        script = os.path.abspath(sys.argv[0])
    powershell_script = f'''
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
'''
    if getattr(sys, "frozen", False):
        powershell_script += f'$Shortcut.TargetPath = "{sys.executable}"\n'
    else:
        powershell_script += f'$Shortcut.TargetPath = "{sys.executable}"\n'
        powershell_script += f'$Shortcut.Arguments = "{os.path.abspath(sys.argv[0])}"\n'

    powershell_script += f'''$Shortcut.WorkingDirectory = "{os.path.dirname(os.path.abspath(sys.argv[0]))}"
$Shortcut.Description = "Windows System Cleaner Pro"
$Shortcut.Save()
'''
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", powershell_script],
            capture_output=True, text=True, timeout=10,
        )
        return os.path.exists(shortcut_path)
    except Exception:
        return False


# ══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ══════════════════════════════════════════════════════════════════════════════
class CleanerApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self._lang = "en"
        self.title(f"{STRINGS['app_title'][self._lang]}  v{APP_VER}")
        self.geometry("960x760")
        self.minsize(860, 660)

        self._busy = False
        self._cat_vars = {}
        self._cat_labels = {}
        self._cat_checkboxes = {}
        self._custom_rows = []
        self._q = queue.Queue()

        self._build_ui()
        self._refresh_text()
        self._pump_queue()

        self.after(500, self._try_create_shortcut)

    # ── LANGUAGE TOGGLE ─────────────────────────────────────────────────────
    def _toggle_lang(self):
        self._lang = "ar" if self._lang == "en" else "en"
        self._refresh_text()

    def _t(self, key):
        return STRINGS.get(key, {}).get(self._lang, key)

    # ── REFRESH ALL TEXT ────────────────────────────────────────────────────
    def _refresh_text(self):
        lang = self._lang

        self.title(f"{self._t('app_title')}  v{APP_VER}")

        self._lang_btn.configure(text=self._t("lang_toggle"))

        self._scan_btn.configure(text=self._t("scan"))

        self._status_lbl.configure(text=f"{self._t('ready')}  •")

        self._badge_lbl.configure(
            text=f"💾  0 MB  {self._t('recoverable')}"
        )

        self._scroll.configure(label_text=f"{self._t('categories')}  •  فئات الفحص" if lang == "en"
                               else f"{self._t('categories')}  •  Scan Categories")

        for cat in CATEGORIES:
            cid = cat["id"]
            if cid in self._cat_checkboxes:
                icon = CAT_ICONS.get(cid, "")
                name = self._t(cid)
                self._cat_checkboxes[cid].configure(
                    text=f"{icon}  {name}"
                )

        self._custom_label.configure(
            text=f"─── {self._t('custom_paths')}  ───"
        )

        self._age_lbl.configure(text=self._t("age_filter"))
        self._add_btn.configure(text=self._t("add_folder"))

        self._all_cb.configure(text=self._t("select_all"))

        if not self._busy:
            self._clean_btn.configure(text=self._t("clean"))

    # ── UI BUILD ────────────────────────────────────────────────────────────
    def _build_ui(self):
        root = ctk.CTkFrame(self, fg_color="transparent")
        root.pack(fill="both", expand=True, padx=14, pady=14)
        self._build_top_bar(root)
        self._build_scrollable(root)
        self._build_bottom(root)

    def _build_top_bar(self, parent):
        bar = ctk.CTkFrame(parent, height=60, corner_radius=10)
        bar.pack(fill="x", pady=(0, 8))
        bar.pack_propagate(False)

        self._scan_btn = ctk.CTkButton(
            bar, text="🔍  Scan System", width=185, height=46,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._on_scan,
        )
        self._scan_btn.pack(side="left", padx=10, pady=7)

        self._status_lbl = ctk.CTkLabel(
            bar, text="Ready  •",
            font=ctk.CTkFont(size=13),
        )
        self._status_lbl.pack(side="left", padx=8, expand=True)

        self._badge_lbl = ctk.CTkLabel(
            bar, text="💾  0 MB  recoverable",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#4CAF50",
        )
        self._badge_lbl.pack(side="right", padx=(0, 10))

        self._lang_btn = ctk.CTkButton(
            bar, text="عربي", width=55, height=34,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#555", hover_color="#777",
            command=self._toggle_lang,
        )
        self._lang_btn.pack(side="right", padx=(0, 6), pady=13)

        self._shortcut_btn = ctk.CTkButton(
            bar, text="🔗", width=34, height=34,
            font=ctk.CTkFont(size=14),
            fg_color="#555", hover_color="#777",
            command=self._manual_shortcut,
        )
        self._shortcut_btn.pack(side="right", padx=(0, 6), pady=13)

    def _build_scrollable(self, parent):
        self._scroll = ctk.CTkScrollableFrame(
            parent,
            label_text="Scan Categories",
            label_font=ctk.CTkFont(size=13, weight="bold"),
        )
        self._scroll.pack(fill="both", expand=True, pady=(0, 8))

        for cat in CATEGORIES:
            self._add_category_row(cat)

        self._custom_label = ctk.CTkLabel(
            self._scroll, text="─── Custom Paths  ───",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#888",
        )
        self._custom_label.pack(pady=(14, 4))

        age_frame = ctk.CTkFrame(self._scroll, fg_color="transparent")
        age_frame.pack(fill="x", padx=4, pady=(0, 4))
        self._age_lbl = ctk.CTkLabel(
            age_frame, text="Delete files older than (days, 0 = all):",
            font=ctk.CTkFont(size=11),
        )
        self._age_lbl.pack(side="left", padx=4)
        self._age_entry = ctk.CTkEntry(age_frame, width=60, placeholder_text="0")
        self._age_entry.pack(side="left", padx=4)
        self._age_entry.insert(0, "0")

        self._custom_frame = ctk.CTkFrame(self._scroll, fg_color="transparent")
        self._custom_frame.pack(fill="x", padx=4)

        self._add_btn = ctk.CTkButton(
            self._custom_frame, text="＋  Add Folder",
            width=300, height=32,
            font=ctk.CTkFont(size=12),
            command=self._add_custom_path,
        )
        self._add_btn.pack(pady=6)

    def _add_category_row(self, cat):
        cid = cat["id"]
        icon = CAT_ICONS.get(cid, "")
        name = self._t(cid)

        row = ctk.CTkFrame(self._scroll, height=44, corner_radius=8)
        row.pack(fill="x", pady=2, padx=4)
        row.pack_propagate(False)

        var = ctk.BooleanVar(value=True)
        cb = ctk.CTkCheckBox(
            row, text=f"{icon}  {name}",
            variable=var, font=ctk.CTkFont(size=12),
        )
        cb.pack(side="left", padx=10, pady=6)

        lbl = ctk.CTkLabel(
            row, text="—", width=110,
            font=ctk.CTkFont(size=11), text_color="#777",
        )
        lbl.pack(side="right", padx=10)

        self._cat_vars[cid] = var
        self._cat_labels[cid] = lbl
        self._cat_checkboxes[cid] = cb

    def _build_bottom(self, parent):
        box = ctk.CTkFrame(parent, corner_radius=10)
        box.pack(fill="x")

        ctrl = ctk.CTkFrame(box, fg_color="transparent")
        ctrl.pack(fill="x", padx=10, pady=(8, 4))

        self._all_var = ctk.BooleanVar(value=True)
        self._all_cb = ctk.CTkCheckBox(
            ctrl, text="Select All",
            variable=self._all_var, command=self._toggle_all,
            font=ctk.CTkFont(size=12),
        )
        self._all_cb.pack(side="left")

        self._clean_btn = ctk.CTkButton(
            ctrl, text="🧹  Start Cleaning",
            width=190, height=46,
            font=ctk.CTkFont(size=13, weight="bold"),
            state="disabled",
            fg_color="#c62828", hover_color="#b71c1c",
            command=self._on_clean,
        )
        self._clean_btn.pack(side="right")

        self._progress = ctk.CTkProgressBar(box, height=18, corner_radius=6)
        self._progress.pack(fill="x", padx=10, pady=(4, 4))
        self._progress.set(0)

        self._log = ctk.CTkTextbox(
            box, height=88,
            font=ctk.CTkFont(family="Consolas", size=10),
            state="disabled",
        )
        self._log.pack(fill="both", expand=True, padx=10, pady=(0, 8))

    # ── QUEUE PUMP ──────────────────────────────────────────────────────────
    def _pump_queue(self):
        try:
            while True:
                msg = self._q.get_nowait()
                cmd = msg[0]

                if cmd == "log":
                    self._log.configure(state="normal")
                    self._log.insert("end", msg[1] + "\n")
                    self._log.see("end")
                    self._log.configure(state="disabled")
                elif cmd == "progress":
                    self._progress.set(msg[1])
                elif cmd == "status":
                    self._status_lbl.configure(text=msg[1])
                elif cmd == "badge":
                    self._badge_lbl.configure(
                        text=f"💾  {fmt(msg[1])}  {self._t('recoverable')}"
                    )
                elif cmd == "cat_size":
                    cid, text = msg[1], msg[2]
                    if cid in self._cat_labels:
                        self._cat_labels[cid].configure(text=text)
                elif cmd == "custom_size":
                    row, text = msg[1], msg[2]
                    if row in self._custom_rows:
                        row["lbl"].configure(text=text)
                elif cmd == "done":
                    mode = msg[1]
                    self._busy = False
                    self._scan_btn.configure(state="normal", text=self._t("scan"))
                    if mode == "scan":
                        self._clean_btn.configure(state="normal", text=self._t("clean"))
                    else:
                        self._clean_btn.configure(state="disabled", text=self._t("clean"))
        except queue.Empty:
            pass
        self.after(80, self._pump_queue)

    # ── HELPERS ─────────────────────────────────────────────────────────────
    def _emit(self, *args):
        self._q.put(args)

    def _toggle_all(self):
        v = self._all_var.get()
        for var in self._cat_vars.values():
            var.set(v)
        for row in self._custom_rows:
            row["var"].set(v)

    def _get_age_days(self):
        try:
            return max(0, int(self._age_entry.get()))
        except (ValueError, AttributeError):
            return 0

    def _add_custom_path(self):
        path = filedialog.askdirectory(title=self._t("select_folder"))
        if not path:
            return
        row_frame = ctk.CTkFrame(self._custom_frame, height=38, corner_radius=8)
        row_frame.pack(fill="x", pady=2)
        row_frame.pack_propagate(False)

        var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            row_frame, text=f"📁  {path}",
            variable=var, font=ctk.CTkFont(size=11),
        ).pack(side="left", padx=8, fill="x", expand=True)

        size_lbl = ctk.CTkLabel(
            row_frame, text="—", width=100,
            font=ctk.CTkFont(size=10), text_color="#777",
        )
        size_lbl.pack(side="right", padx=4)

        rec = {"path": path, "var": var, "lbl": size_lbl, "frame": row_frame}

        ctk.CTkButton(
            row_frame, text="✕", width=28, height=24,
            fg_color="transparent", hover_color="#c62828",
            command=lambda r=rec: self._remove_custom(r),
        ).pack(side="right", padx=2)
        self._custom_rows.append(rec)

    def _remove_custom(self, rec):
        rec["frame"].destroy()
        if rec in self._custom_rows:
            self._custom_rows.remove(rec)

    def _try_create_shortcut(self):
        try:
            created = create_desktop_shortcut()
            if created:
                self._emit("log", f"✅  {self._t('shortcut_created')}")
        except Exception:
            pass

    def _manual_shortcut(self):
        try:
            created = create_desktop_shortcut()
            if created:
                messagebox.showinfo(
                    self._t("shortcut_created"),
                    self._t("shortcut_created"),
                )
            else:
                messagebox.showerror("Error", "Failed to create shortcut")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ════════════════════════════════════════════════════════════════════════
    # SCAN
    # ════════════════════════════════════════════════════════════════════════
    def _on_scan(self):
        if self._busy:
            return
        self._busy = True
        self._scan_btn.configure(state="disabled", text=self._t("scanning"))
        self._clean_btn.configure(state="disabled")
        self._log.configure(state="normal")
        self._log.delete("1.0", "end")
        self._log.configure(state="disabled")
        self._progress.set(0)
        self._emit("status", f"{self._t('log_scanning')}  •")
        threading.Thread(target=self._scan_worker, daemon=True).start()

    def _scan_worker(self):
        self._emit("log", self._t("log_scan_start"))
        total = 0
        items = []

        for cat in CATEGORIES:
            if self._cat_vars[cat["id"]].get():
                items.append(("cat", cat))
        for row in self._custom_rows:
            if row["var"].get():
                items.append(("custom", row))

        n = len(items)
        if n == 0:
            self._emit("log", self._t("log_no_select"))
            self._emit("status", f"{self._t('nothing_selected')}  •")
            self._emit("done", "scan")
            return

        age = self._get_age_days()
        for i, (kind, obj) in enumerate(items):
            if kind == "cat":
                sz = self._scan_cat(obj)
            else:
                sz = self._scan_custom(obj, age)
            total += sz
            self._emit("progress", (i + 1) / n)

        self._emit("log", "")
        self._emit("log", f"══  {self._t('total')}: {fmt(total)}  ══")
        self._emit("badge", total)
        self._emit("status", f"{self._t('scan_complete')}  •  {fmt(total)} {self._t('recoverable')}")
        self._emit("done", "scan")

    def _scan_cat(self, cat):
        cid = cat["id"]
        icon = CAT_ICONS.get(cid, "")
        name = self._t(cid)
        self._emit("log", f"▸  {icon}  {name}...")
        if cid == "recycle":
            sz = scan_recycle_bin()
        else:
            sz = sum(dir_size(p) for p in cat["paths"] if p and os.path.exists(p))
        self._emit("cat_size", cid, fmt(sz))
        self._emit("log", f"   →  {fmt(sz)}")
        return sz

    def _scan_custom(self, row, age):
        p = row["path"]
        self._emit("log", f"▸  📁  {p}...")
        sz = dir_size_aged(p, age) if os.path.exists(p) else 0
        self._emit("custom_size", row, fmt(sz))
        self._emit("log", f"   →  {fmt(sz)}")
        return sz

    # ════════════════════════════════════════════════════════════════════════
    # CLEAN
    # ════════════════════════════════════════════════════════════════════════
    def _on_clean(self):
        if self._busy:
            return
        if not messagebox.askyesno(self._t("confirm_clean"), self._t("confirm_msg")):
            return
        self._busy = True
        self._clean_btn.configure(state="disabled", text=self._t("cleaning"))
        self._scan_btn.configure(state="disabled")
        self._progress.set(0)
        self._emit("status", f"{self._t('log_cleaning')}  •")
        threading.Thread(target=self._clean_worker, daemon=True).start()

    def _clean_worker(self):
        self._emit("log", "")
        self._emit("log", self._t("log_clean_start"))
        total_freed = total_skipped = 0
        items = []

        for cat in CATEGORIES:
            if self._cat_vars[cat["id"]].get():
                items.append(("cat", cat))
        for row in self._custom_rows:
            if row["var"].get():
                items.append(("custom", row))

        n = len(items)
        if n == 0:
            self._emit("log", self._t("log_nothing"))
            self._emit("done", "clean")
            return

        age = self._get_age_days()
        for i, (kind, obj) in enumerate(items):
            if kind == "cat":
                f, s = self._clean_cat(obj, age)
            else:
                f, s = self._clean_custom(obj, age)
            total_freed += f
            total_skipped += s
            self._emit("progress", (i + 1) / n)

        self._emit("log", "")
        self._emit("log",
            f"══  {self._t('clean_complete')} — "
            f"{self._t('freed')}: {fmt(total_freed)}, "
            f"{self._t('skipped')}: {total_skipped} {self._t('locked')}  ══"
        )
        self._emit("badge", total_freed)
        self._emit("status",
            f"{self._t('clean_complete')}  •  "
            f"{self._t('freed')}: {fmt(total_freed)}"
        )
        self._emit("done", "clean")

    def _clean_cat(self, cat, age):
        cid = cat["id"]
        icon = CAT_ICONS.get(cid, "")
        name = self._t(cid)
        self._emit("log", f"▸  {icon}  {name}...")
        if cid == "recycle":
            f, s = empty_recycle_bin()
        else:
            f = s = 0
            for p in cat["paths"]:
                if p and os.path.exists(p):
                    ff, ss = wipe_dir(p, age)
                    f += ff; s += ss
        self._emit("log", f"   →  {self._t('freed')}: {fmt(f)}, {self._t('skipped')}: {s}")
        return f, s

    def _clean_custom(self, row, age):
        p = row["path"]
        self._emit("log", f"▸  📁  {p}...")
        f, s = wipe_dir(p, age) if os.path.exists(p) else (0, 0)
        self._emit("log", f"   →  {self._t('freed')}: {fmt(f)}, {self._t('skipped')}: {s}")
        return f, s


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = CleanerApp()
    app.mainloop()
