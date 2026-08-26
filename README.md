# 🧹 SystemCleanerPro

[![Python](https://img.shields.io/badge/Python-3.x-blue)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-CustomTkinter-orange)](https://github.com/TomSchimansky/CustomTkinter)
[![Windows](https://img.shields.io/badge/Platform-Windows-0078D4)](https://www.microsoft.com/windows/)

## 📋 نظرة عامة

تطبيق تنظيف نظام حديث لنظام **Windows** مبني بلغة **Python**. يمسح وينظف 7 أنواع من الملفات غير الضرورية بواجهة عربية/إنجليزية سهلة الاستخدام.

## 🧹 أنواع التنظيف

| النوع | الوصف |
|-------|-------|
| 🗑️ ملفات مؤقتة المستخدم | %TEMP% |
| 🗑️ ملفات مؤقتة Windows | Windows\Temp |
| ⚡ Prefetch | ملفات التشغيل المسبقة |
| ❌ تقارير الأخطاء | Windows Error Reports |
| ♻️ سلة المهملات | Recycle Bin |
| 🌐 كاش Chrome | Google Chrome Cache |
| 🌐 كاش Edge | Microsoft Edge Cache |

## ⭐ المميزات

### 🌍 اللغات
- **العربية** (RTL)
- **الإنجليزية**
- تبديل فوري بين اللغات

### 🎨 الواجهة
- تصميم عصري مع **CustomTkinter**
- الوضع الداكن
- سجل العمليات

### 🔒 الأمان
- ترقية تلقائية UAC للصلاحيات
- حذف آمن (يتجاوز الملفات المستخدمة)
- نافذة تأكيد قبل التنظيف

### 📊 الميزات
- فلتر عمر الملفات
- مسارات مخصصة
- إحصائيات مفصلة
- تصدير كـ EXE (PyInstaller)

## 🚀 التشغيل

```bash
# استنساخ المستودع
git clone https://github.com/ahmed4050/SystemCleanerPro.git

# تثبيت المتطلبات
pip install customtkinter

# التشغيل
python main.py
```

## 📦 التصدير كـ EXE

```bash
# تثبيت PyInstaller
pip install pyinstaller

# التصدير
pyinstaller --onefile --windowed --name "SystemCleanerPro" main.py
```

## 📱 الواجهة

```
┌────────────────────────────────┐
│     🧹 SystemCleanerPro        │
├────────────────────────────────┤
│  اللغة: [العربية | English]    │
├────────────────────────────────┤
│  ☑ ملفات مؤقتة المستخدم       │
│  ☑ ملفات مؤقتة Windows        │
│  ☐ Prefetch                   │
│  ☐ تقارير الأخطاء             │
│  ☐ سلة المهملات               │
│  ☐ كاش Chrome                 │
│  ☐ كاش Edge                   │
├────────────────────────────────┤
│  عمر الملفات: [≥ 7 أيام ▼]   │
│  مسار مخصص: [ browsing... ]   │
├────────────────────────────────┤
│  [🔍 مسح]  [🧹 تنظيف]         │
├────────────────────────────────┤
│  النتائج:                      │
│  • تم العثور على 250 ملف       │
│  • الحجم: 1.2 GB              │
│  • تم التنظيف بنجاح ✓         │
└────────────────────────────────┘
```

## 📁 هيكل الملفات

```
SystemCleanerPro/
├── main.py           # الكود الرئيسي
├── ui.py             # واجهة المستخدم
├── cleaner.py        # منطق التنظيف
├── requirements.txt  # المتطلبات
└── README.md         # هذه الملفات
```

## ⚙️ الإعدادات

```python
# الإعدادات الافتراضية
DEFAULT_AGE_DAYS = 7
DEFAULT_ENCODING = 'utf-8'
SUPPORTED_LANGUAGES = ['ar', 'en']
```

## 🛠️ المتطلبات

- Python 3.8+
- CustomTkinter
- Windows 10/11
- صلاحيات Administrator

## 📚 المراجع

- [CustomTkinter Documentation](https://github.com/TomSchimansky/CustomTkinter)
- [PyInstaller Documentation](https://pyinstaller.org/)

## 👨‍💻 المؤلف

**Ahmed Al-Qassabi** - [GitHub](https://github.com/ahmed4050)

## 📄 الرخصة

هذا المشروع مرخص بموجب رخصة MIT.
