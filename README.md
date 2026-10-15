# تَوان | Tavaan

> فریمورک کاملاً اختصاصی، صفر‌وابستگی (Zero-Dependency) برای PHP 8.2+ — با معماری ترکیبی
> **HMVC + Modular Monolith + Event-Driven + Layered + Microservice-Ready (Hexagonal)**

این مخزن در فاز کنونی **فقط مستندات تحلیلی و معماری** است؛ یعنی «نقشهٔ راه کدنویسی» که یک تیم انسانی یا
مجموعه‌ای از ایجنت‌های هوش مصنوعی بتوانند **بدون ابهام**، جزء به جزء، هسته و موتورها را پیاده‌سازی کنند.

---

## چرا این مستندات؟

| مشکل رایج در فریمورک‌های دست‌ساز | پاسخ تَوان |
|---|---|
| معماری تک‌لایه و درهم (Spaghetti MVC) | HMVC سلسله‌مراتبی + ماژول‌های خودبسنده با مرز دسترسی |
| وابستگی سنگین به کامپوزر/پکیج‌ها | هستهٔ صفر‌وابستگی + **موتورهای خودنوشته** با قرارداد کامپوزرِ اختیاری |
| کدهای Deprecated و منسوخ | سند الزامات PHP 8.2+ و چک‌لیست «ممنوعه‌ها» + ابزار بررسی خودکار |
| توسعهٔ کُند برای دامنه‌های بزرگ (ERP/BPMS) | موتورهای دامنه‌ای آماده: Workflow، Report، Audit، Payment، Media |
| امنیت پس‌رو (Afterthought) | لایهٔ امنیتی درون‌ذاتی در هر موتور + نقش‌ها و سطوح دسترسی استاندارد |

---

## نقشهٔ مستندات (Docs Map)

```
docs/
├── README.md                      ← شاخص کل + راهنمای مطالعه برای انسان و ایجنت
├── 00-overview/
│   ├── goals-vision.md            ← اهداف کلان، چشم‌انداز، شاخص‌های موفقیت (OKR/KPI)
│   ├── principles.md              ← اصول بنیادین ۱۲گانه و قواعد تصمیم‌گیری معماری
│   ├── requirements.md            ← الزامات عملکردی/غیرعملکردی با شناسه (FR-/NFR-)
│   └── quickstart.md              ← 🚀 راهنمای شروع سریع (از صفر تا اولین ماژول)
├── 01-standards/
│   ├── php82-strict.md            ← قواعد اجباری PHP 8.2/8.3/8.4 و جلوی Deprecated
│   ├── coding-style.md            ← سبک کد، PSR-1/12، قالب‌بندی، مستندسازی
│   ├── naming-conventions.md      ← نام‌گذاری: namespace، کلاس، فایل، جدول، روت، کلید تنظیمات
│   ├── error-handling.md          ← سلسله‌مراتب استثناها، کد خطا، بازیابی
│   ├── contracts-interfaces.md    ← قراردادهای هسته (Interface Catalog)
│   ├── documentation-standard.md  ← استاندارد مستندسازی (همین قالب) + PHPDoc
│   └── security-policy.md         ← سیاست امنیتی، مدل تهدید، کنترل‌ها
├── 02-architecture/
│   ├── overview.md                ← نمای کلان، ترکیب معماری‌ها، نمودار C4
│   ├── layered-hmvc.md            ← معماری لایه‌ای + HMVC سلسله‌مراتبی
│   ├── modular-monolith.md        ← مرز ماژول، Public API، ممنوعیت نفوذ متقابل
│   ├── event-driven.md            ← Event Bus، Outbox، CQRS، Event Sourcing، DLQ
│   ├── microservice-ready.md      ← استراتژی تجزیه، Saga، قراردادها، Observability توزیعی
│   ├── request-lifecycle.md       ← چرخهٔ عمر درخواست، ۱۴ فاز، Pipeline
│   ├── container-di.md            ← تزریق وابستگی، Contextual Binding، Lazy Proxy
│   ├── bootstrapping.md           ← راه‌اندازی، Autoloader خودنوشته، Preload، Cache
│   └── multi-tenancy.md           ← چنداجاره‌ای (Shared/DB-per-tenant/Schema-per-tenant)
├── 03-engines/
│   ├── README.md                  ← رجیستری موتورها، ماتریس وابستگی، اولویت ساخت
│   └── <engine>.md                ← ۵۳ سند موتور (هر کدام جزء‌به‌جزء)
├── 04-structure/
│   ├── folder-structure.md        ← ساختار کامل پوشه/فایل با توضیح هر قلم
│   ├── file-conventions.md        ← قرارداد محتوای فایل‌ها (هدر، ترتیب اعضا)
│   ├── composer-mapping.md        ← نگاشت Autoloader ↔ composer.json ↔ PSR-4
│   ├── cli-reference.md           ← 🔧 مرجع کامل ۱۰۵ دستور tvn
│   ├── config-reference.md        ← ⚙️ مرجع کامل ۴۸ فایل config + ۱۱۱ کلید ENV
│   └── database-schema-catalog.md ← 🗄️ دیکشنری دادهٔ جداول هسته (tvn_*)
├── 05-applications/
│   ├── README.md                  ← الگوی ساخت اپلیکیشن و ماتریس ماژول‌ها
│   ├── blog.md / shop.md / forum.md / lms.md / news-portal.md
│   └── erp.md / bpms.md / crm.md
├── 06-roles-access/
│   ├── roles-matrix.md            ← نقش‌های سیستمی و سازمانی + ماتریس دسترسی
│   ├── permission-catalog.md      ← کاتالوگ مجوزها با کلید استاندارد
│   └── duties-workflow.md         ← وظایف، گردش‌کار تصویب، تفویض اختیار
├── 07-quality/
│   ├── testing-strategy.md        ← هرم تست، Test Engine، پوشش کد
│   ├── static-analysis-ci.md      ← PHPStan/CS-Fixer/CI پایپ‌لاین
│   ├── benchmark-targets.md       ← اهداف عملکرد و روش اندازه‌گیری
│   └── definition-of-done.md      ← تعریف «تمام‌شده» برای هر تیکت
├── 08-roadmap/
│   ├── milestones.md              ← فازها M0..M9 با خروجی و معیار پذیرش
│   └── agent-backlog.md           ← بک‌لاگ تیکت‌های آمادهٔ ایجنت (machine-readable)
├── 09-references/
│   ├── benchmarks.md              ← مراجع: Laravel/Symfony/CodeIgniter/Yii/Drupal/Odoo/…
│   └── glossary.md                ← واژه‌نامهٔ فارسی↔لاتین
├── adr/                           ← تصمیم‌های معماری (ADR-0001 …) + README.md (ایندکس)
├── schemas/                       ← 🧩 JSON Schemaهای اعتبارسنجی
│   ├── module.v1.json             ← schema فایل module.json
│   ├── project.v1.json            ← schema فایل tavaan.json
│   ├── integration-event.v1.json  ← schema رویداد بین‌سرویسی
│   └── docs-manifest.v1.json      ← schema خودِ manifest
├── manifest.json                  ← 🤖 فهرست ماشین‌خوان همهٔ اسناد (برای ایجنت‌ها)
└── templates/                     ← قالب مستند موتور / ماژول / ADR

tools/scripts/
├── verify-docs.py                 ← بررسی سلامت مستندات (لینک‌ها، DOC-ID، JSON، manifest)
└── scaffold-structure.sh          ← ساخت اسکلت پوشه‌های واقعی فریمورک (۵۳ موتور)

INDEX.html                         ← 📊 داشبورد بصری و ناوبری همهٔ مستندات
```

---

## شروع سریع برای ایجنت‌های هوش مصنوعی

**ترتیب اجباری مطالعه:**

1. `docs/00-overview/goals-vision.md` — بدان چه می‌سازی و چرا.
2. `docs/00-overview/quickstart.md` — 🚀 نقشهٔ عملی شروع.
3. `docs/01-standards/php82-strict.md` — **قوانین سفت‌وسخت زبانی**؛ نقض = ریجکت.
4. `docs/02-architecture/request-lifecycle.md` — مدل ذهنی اجرا.
5. `docs/04-structure/folder-structure.md` — کجا بنویسی.
6. `docs/03-engines/README.md` — رجیستری موتورها و ترتیب ساخت.
7. `docs/08-roadmap/agent-backlog.md` — تیکت خودت را بردار.
8. `docs/07-quality/definition-of-done.md` — کی تمام است.

**قواعد طلایی (Hard Rules):**

```
R1  هر فایل PHP با declare(strict_types=1); شروع می‌شود.
R2  هیچ require/include دستی در کد کاربردی؛ فقط Autoloader هسته.
R3  هیچ پکیج خارجی (composer require) در core/ و engines/ ممنوع است.
R4  هیچ Property پویا؛ کلاس‌ها یا readonly یا typed و تعریف‌شده.
R5  هر خروجی عمومی باید Interface داشته باشد؛ پیاده‌سازی پشت قرارداد.
R6  هر موتور: Provider + Interface + Tests + Docs + Benchmark. هیچ‌کدام اختیاری نیست.
R7  نام namespace فقط از ریشهٔ ثبت‌شده در docs/04-structure/composer-mapping.md.
R8  خطاها استثنا هستند با کد عددی و MessageId ترجمه‌پذیر (نه متن خام).
R9  هیچ کوئری با الحاق رشته؛ فقط Prepared Statement / Query Builder.
R10 قبل از Merge: php -l + PHPStan level max + تست‌ها سبز + Benchmark بدون افت.
```

---

## ابزارهای همراه (Companion Tools)

دو اسکریپت در `tools/scripts/` برای شروع عملی ارائه شده است:

| ابزار | دستور | کاربرد |
|---|---|---|
| **ساخت اسکلت** | `bash tools/scripts/scaffold-structure.sh` | ساخت همهٔ پوشه‌های فریمورک (۵۳ موتور + ساختار DOC-080) با فایل‌های پایه |
| **اعتبارسنج مستندات** | `python3 tools/scripts/verify-docs.py` | بررسی لینک‌ها، یکتایی DOC-ID، JSON، همگامی manifest، سلامت بلوک‌های کد |
| **تولید manifest** | `python3 tools/scripts/build-manifest.py` | بازتولید `docs/manifest.json` (فهرست ماشین‌خوان برای ایجنت‌ها) |

> 🤖 **ورود برنامه‌ای ایجنت‌ها:** `docs/manifest.json` فهرست ماشین‌خوان همهٔ ۱۲۱ سند و ۵۳ موتور
> (با DOC-ID، مسیر، hash و مسیرهای مطالعه) را فراهم می‌کند؛ `docs/schemas/*.json` برای اعتبارسنجی
> `module.json` / `tavaan.json` / رویدادهای بین‌سرویسی‌اند.
>
> 💡 داشبورد بصری `INDEX.html` نمای ناوبری همهٔ اسناد را فراهم می‌کند (در مرورگر باز کنید).

---

## وضعیت فاز فعلی

| فاز | محتوا | وضعیت |
|---|---|---|
| M0 | تحلیل، معماری، مستندات (این مخزن) | ✅ تکمیل |
| M1 | هستهٔ صفر‌وابستگی (Autoloader, Container, Config, Events) | ⬜ آمادهٔ شروع |
| M2 | موتور HTTP + Router + View | ⬜ |
| M3 | موتور Database + ORM + Migration | ⬜ |
| M4 | Auth/RBAC/Validation/Cache/Log | ⬜ |
| M5 | Queue/Schedule/Mail/Notification/Media/Filesystem | ⬜ |
| M6 | API/Observability/Search/Workflow/Report | ⬜ |
| M7 | اپلیکیشن‌های پایه (Blog/Shop/Forum/LMS) | ⬜ |
| M8 | اپلیکیشن‌های حرفه‌ای (ERP/BPMS/CRM) | ⬜ |
| M9 | ابزارها، Scaffold، Admin، Docs Site، Release 1.0 | ⬜ |

---

## پروانه و هویت

- نام: **تَوان** / **Tavaan** — ریشهٔ فارسی به معنای «قدرت، توانایی، توانمندسازی».
- شعار: *صفر وابستگی، بی‌نهایت امکان* / **Zero Dependency. Infinite Capability.**
- پروانهٔ پیشنهادی: MIT (هسته) + مجوز تجاری برای موتورهای Enterprise (تصمیم در ADR-0002).
