# Windows System Cleaner Pro

<div dir="rtl">

## مُنظّف ويندوز الاحترافي

تطبيق مكتبي حديث لتنظيف ملفات النظام غير المرغوبة على ويندوز، مبني بـ Python و CustomTkinter.

</div>

<p align="center">
  <img src="screenshot.png" alt="System Cleaner Pro Screenshot" width="700"/>
</p>

---

## Features / الميزات

| Feature | English | العربية |
|---|---|---|
| UAC Auto-Elevation | Automatically requests admin rights | طلب صلاحيات المدير تلقائياً |
| Dark Modern UI | CustomTkinter dark theme | واجهة داكنة عصرية |
| Bilingual | Full Arabic & English with toggle | عربي وإنجليزي مع زر تبديل |
| 7 Scan Categories | Temp, Prefetch, Errors, Recycle Bin, Chrome, Edge | 7 فئات فحص |
| Custom Paths | Add any folder with age filter | مسارات مخصصة مع فلتر عمر |
| Threaded Operations | Non-blocking scan & clean | عمليات في الخلفية |
| Safe Deletion | Skips locked/in-use files gracefully | تخطي الملفات المقفلة |

---

## Requirements / المتطلبات

- **Windows 10/11** (64-bit)
- **Python 3.10+**
- **Administrator privileges** (for system folder access)

---

## Installation / التثبيت

### Step 1: Install Python

Download and install Python 3.10 or newer from:

**https://www.python.org/downloads/**

> **Important:** During installation, check the box that says
> **"Add Python to PATH"** before clicking Install.

Alternatively, install via winget (Windows Package Manager):

```powershell
winget install Python.Python.3.12
```

### Step 2: Clone the Repository

Open **PowerShell** or **Command Prompt** and run:

```powershell
git clone https://github.com/ahmed4050/SystemCleanerPro.git
cd SystemCleanerPro
```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Run the Application

```powershell
python main.py
```

> The app will automatically request **Administrator** permissions via UAC prompt.

---

## Build as EXE / بناء كملف EXE مستقل

To create a standalone `.exe` file that doesn't require Python:

```powershell
pip install pyinstaller
pyinstaller --onefile --uac-admin --windowed --name "SystemCleanerPro" main.py
```

The executable will be in: `dist\SystemCleanerPro.exe`

| Flag | Purpose |
|---|---|
| `--onefile` | Single EXE file |
| `--uac-admin` | Requests admin on launch |
| `--windowed` | No console window |

---

## Usage / طريقة الاستخدام

### 1. Language Toggle / تبديل اللغة

<div dir="rtl">

- اضغط زر **عربي** في أعلى اليمين للتبديل بين العربية والإنجليزية

</div>

- Click the **EN** button in the top-right corner to switch languages

### 2. Scan System / فحص النظام

<div dir="rtl">

1. حدد الفئات التي تريد فحصها (محددة مسبقاً جميعها)
2. اضغط زر **🔍 فحص النظام**
3. انتظر حتى يكتمل الفحص
4. ستظهر المساحة القابلة للاسترجاع بجانب كل فئة

</div>

1. Select the categories you want to scan (all selected by default)
2. Click **🔍 Scan System**
3. Wait for the scan to complete
4. Recoverable size appears next to each category

### 3. Categories / الفئات

| Icon | Category (EN) | الفئة (AR) | Description |
|---|---|---|---|
| 📁 | User Temp Files | ملفات المؤقت للمستخدم | `%TEMP%` folder |
| ⚙️ | Windows System Temp | ملفات مؤقت النظام | `C:\Windows\Temp` |
| ⚡ | Windows Prefetch | ملفات التنقل المسبق | `C:\Windows\Prefetch` |
| ⚠️ | Error Reports & Crash Dumps | تقارير الأخطاء وملفات العطل | Crash dumps, WER reports |
| 🗑️ | Recycle Bin | سلة المهملات | All deleted files |
| 🌐 | Google Chrome Cache | ذاكرة كروم المؤقتة | Chrome browser cache |
| 🔷 | Microsoft Edge Cache | ذاكرة إيدج المؤقتة | Edge browser cache |

### 4. Custom Paths / مسارات مخصصة

<div dir="rtl">

1. اضغط **＋ إضافة مجلد**
2. اختر المجلد من المتصفح
3. (اختياري) حدد عدد الأيام — الملفات الأقدم من هذا العدد فقط ستُحذف
4. اضغط **🧹 بدء المسح** للحذف

</div>

1. Click **＋ Add Folder**
2. Select a folder from the browser
3. (Optional) Set days filter — only files older than this will be deleted
4. Click **🧹 Start Cleaning** to delete

### 5. Clean / مسح الملفات

<div dir="rtl">

1. اضغط زر **🧹 بدء المسح**
2. ستظهر رسالة تأكيد — اضغط **Yes** للتأكيد
3. انتظر حتى يكتمل المسح
4. ستظهر النتيجة في سجل العمليات

</div>

1. Click **🧹 Start Cleaning**
2. A confirmation dialog appears — click **Yes** to confirm
3. Wait for the cleaning to complete
4. Results appear in the log console

---

## Safety / الأمان

<div dir="rtl">

- **الملفات المقفلة:** يتم تخطيها تلقائياً بدون إيقاف التطبيق
- **تأكيد قبل الحذف:** رسالة تأكيد تظهر قبل أي عملية مسح
- **صلاحيات المدير:** التطبيق يطلب صلاحيات المدير تلقائياً للوصول لملفات النظام
- **سجل العمليات:** كل عملية تُسجَّل في الكونسول السفلي

</div>

- **Locked files:** Automatically skipped without crashing
- **Confirmation dialog:** Appears before any cleaning operation
- **Admin privileges:** Requested automatically for system folder access
- **Operation log:** Every operation is logged in the bottom console

---

## Project Structure / هيكل المشروع

```
SystemCleanerPro/
├── main.py              # Application source code
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

---

## License / الترخيص

Free to use and modify.

---

## Author / المطور

**Ahmed Al-Qassabi**
- Website: [ahmed4050.github.io](https://ahmed4050.github.io/)
- GitHub: [ahmed4050](https://github.com/ahmed4050)
