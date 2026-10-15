#!/usr/bin/env python3
"""
verify-docs.py — بررسی سلامت مستندات تَوان (Tavaan Docs Verifier)

این اسکریپت یکپارچگی مجموعهٔ مستندات را بررسی می‌کند:
  1. هر سند موتور دارای DOC-ID و بلوک machine-readable است
  2. لینک‌های داخلی .md شکسته نیستند
  3. DOC-IDها یکتا هستند (تداخل ندارند)
  4. هر موتور فهرست‌شده در رجیستری، فایل مستند دارد
  5. بلوک‌های کد ``` بسته شده‌اند
  6. کاراکترهای ناخواسته (CJK/سیریلیک) وارد نشده‌اند
  7. همهٔ فایل‌های JSON (schemaها + manifest) معتبرند
  8. manifest.json با واقعیت همگام است (تعداد سند/موتور + مسیرها)
  9. هر ADR ارجاع‌شده در ایندکس، فایل مستقل دارد (جلوگیری از گروه‌بندی)
 10. هر الزام FR/NFR/CON ارجاع‌شده، در requirements.md تعریف شده است
 11. هر کد خطای T<Area>NNN ارجاع‌شده، در رجیستری DOC-013 ثبت شده است
 12. هیچ سند یتیمی وجود ندارد (هر فایل از یک ایندکس قابل دسترسی است)

بررسی‌های ۹/۱۰/۱۱ «ارجاع به شناسهٔ تعریف‌نشده» را می‌گیرند و #۱۲ «فایل بدون لینک»
را — همان کلاس نقصی که در ممیزی ساختار یافت شد. همه با آزمون منفی تأیید شده‌اند.

استفاده:  python3 tools/scripts/verify-docs.py
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
DOCS = ROOT / "docs"
errors: list[str] = []
warnings: list[str] = []


def read(p: pathlib.Path) -> str:
    return p.read_text(encoding="utf-8")


# ── ۱) DOC-ID و machine-readable برای اسناد موتور ──────────────────────────
for doc in sorted((DOCS / "03-engines").glob("*.md")):
    if doc.name == "README.md":
        continue
    text = read(doc)
    if not re.search(r"DOC-ID\s*\|", text):
        errors.append(f"{doc.relative_to(ROOT)}: DOC-ID ندارد")
    if "machine-readable:" not in text:
        errors.append(f"{doc.relative_to(ROOT)}: بلوک machine-readable ندارد")
    if "معیار پذیرش" not in text and "Acceptance" not in text:
        warnings.append(f"{doc.relative_to(ROOT)}: بخش معیار پذیرش ندارد")


# ── ۲) لینک‌های داخلی شکسته ────────────────────────────────────────────────
for md in DOCS.rglob("*.md"):
    text = read(md)
    for link in re.findall(r"\]\(([^)]+\.md)\)", text):
        if link.startswith("http"):
            continue
        target = (md.parent / link).resolve()
        if not target.exists():
            errors.append(f"{md.relative_to(ROOT)}: لینک شکسته → {link}")


# ── ۳) یکتایی DOC-ID ───────────────────────────────────────────────────────
seen: dict[str, pathlib.Path] = {}
for md in DOCS.rglob("*.md"):
    text = read(md)
    for m in re.findall(r"DOC-ID\s*\|\s*(DOC-[0-9A-Z]+)", text):
        if m == "DOC-0XX":  # قالب خالی
            continue
        if m in seen:
            errors.append(f"DOC-ID تکراری {m}: {seen[m].name} و {md.name}")
        seen[m] = md


# ── ۴) هر موتور رجیستری فایل دارد ──────────────────────────────────────────
registry = read(DOCS / "03-engines" / "README.md")
for m in re.findall(r"\]\(([a-z0-9\-]+\.md)\)", registry):
    if not (DOCS / "03-engines" / m).exists():
        errors.append(f"رجیستری به فایل ناموجود اشاره می‌کند: {m}")


# ── ۵) بلوک‌های کد بسته‌شده ────────────────────────────────────────────────
for md in DOCS.rglob("*.md"):
    text = read(md)
    fences = text.count("```")
    if fences % 2 != 0:
        errors.append(f"{md.relative_to(ROOT)}: بلوک کد نابسته (``` = {fences})")


# ── ۶) کاراکترهای ناخواسته (CJK / سیریلیک / عربیِ خارج از محدودهٔ فارسی) ─────
# دامنهٔ مجاز: فارسی/عربی مشترک (U+0600–U+06FF) + لاتین + ارقام فارسی (U+06F0–U+06F9)
# ممنوع: CJK (U+4E00–U+9FFF)، سیریلیک (U+0400–U+04FF)
CJK = re.compile(r"[\u4e00-\u9fff]+")
CYRILLIC = re.compile(r"[\u0400-\u04ff]+")
for md in DOCS.rglob("*.md"):
    text = read(md)
    cjk = CJK.findall(text)
    if cjk:
        errors.append(f"{md.relative_to(ROOT)}: کاراکتر چینی یافت شد: {cjk[:3]}")
    cyr = CYRILLIC.findall(text)
    if cyr:
        errors.append(f"{md.relative_to(ROOT)}: کاراکتر سیریلیک یافت شد: {cyr[:3]}")


# ── ۷) اعتبار JSON (schemaها + manifest) ──────────────────────────────────
import json
for jf in list(DOCS.rglob("*.json")):
    try:
        json.loads(read(jf))
    except json.JSONDecodeError as e:
        errors.append(f"{jf.relative_to(ROOT)}: JSON نامعتبر — {e}")

# ── ۸) manifest با واقعیت هم‌خوان باشد ───────────────────────────────────
manifest_path = DOCS / "manifest.json"
if manifest_path.exists():
    try:
        manifest = json.loads(read(manifest_path))
        real_md = len(list(DOCS.rglob("*.md")))
        if manifest.get("totals", {}).get("documents") != real_md:
            errors.append(f"manifest.json: تعداد اسناد ({manifest['totals']['documents']}) "
                          f"با واقعیت ({real_md}) نمی‌خواند — آن را بازتولید کنید")
        real_eng = len([p for p in (DOCS / "03-engines").glob("*.md") if p.name != "README.md"])
        if manifest.get("totals", {}).get("engines") != real_eng:
            errors.append(f"manifest.json: تعداد موتورها با واقعیت نمی‌خواند")
        # هر doc در manifest باید وجود داشته باشد
        for entry in manifest.get("catalog", []):
            if not (ROOT / entry["path"]).exists():
                errors.append(f"manifest.json: مسیر ناموجود {entry['path']}")
    except (json.JSONDecodeError, KeyError) as e:
        errors.append(f"manifest.json: خوانده نشد — {e}")
else:
    warnings.append("docs/manifest.json وجود ندارد (برای ایجنت‌ها توصیه می‌شود)")


# ── ۹) هر ADR ارجاع‌شده فایل مستقل دارد (جلوگیری از بازگشت گروه‌بندی) ────────
adr_dir = DOCS / "adr"
if adr_dir.exists():
    adr_files = {m.group(0) for f in adr_dir.glob("ADR-*.md")
                 for m in [re.match(r"ADR-\d{4}", f.name)] if m}
    # ADRهای واقعی (۰۰۰۱..۰۰۱۶) — نه backlog پیشنهادی (۰۰۱۷+)
    referenced_adr = set()
    for md in DOCS.rglob("*.md"):
        for a in re.findall(r"ADR-(\d{4})", read(md)):
            referenced_adr.add("ADR-" + a)
    # فقط ADRهایی که «پذیرفته/پیشنهادی» هستند (در فهرست ایندکس) باید فایل داشته باشند
    index_txt = read(adr_dir / "README.md") if (adr_dir / "README.md").exists() else ""
    listed = set(re.findall(r"ADR-\d{4}", index_txt))
    for a in sorted(listed):
        num = int(a.split("-")[1])
        if num > 16:          # backlog آینده، فایل لازم نیست
            continue
        if a not in adr_files:
            errors.append(f"ADR ارجاع‌شده در ایندکس ولی فایل ندارد: {a} (باید docs/adr/{a}-<slug>.md باشد)")


# ── ۱۰) الزامات FR/NFR/CON: هر ارجاع باید در requirements.md تعریف شده باشد ──
req_file = DOCS / "00-overview" / "requirements.md"
if req_file.exists():
    defined_req = set(re.findall(r"\b(?:FR|NFR|CON)-[A-Z]+-\d+\b", read(req_file)))
    for md in DOCS.rglob("*.md"):
        if md == req_file:
            continue
        for r in re.findall(r"\b(?:FR|NFR|CON)-[A-Z]+-\d+\b", read(md)):
            if "XXX" in r:            # placeholder قالب
                continue
            if r not in defined_req:
                errors.append(f"{md.relative_to(ROOT)}: ارجاع به الزام تعریف‌نشده {r}")


# ── ۱۱) کدهای خطا T<Area>NNN: هر ارجاع باید در رجیستری DOC-013 باشد ─────────
err_file = DOCS / "01-standards" / "error-handling.md"
if err_file.exists():
    defined_err = set(re.findall(r"\bT[A-Z]{2,3}\d{3}\b", read(err_file)))
    for md in DOCS.rglob("*.md"):
        if md == err_file or md.name == "engine-spec-template.md":
            continue
        for c in re.findall(r"\bT[A-Z]{2,3}\d{3}\b", read(md)):
            if "TXX" in c:            # placeholder قالب
                continue
            if c not in defined_err:
                errors.append(f"{md.relative_to(ROOT)}: کد خطای {c} در DOC-013 ثبت نشده")


# ── ۱۲) اسناد یتیم: هر فایل باید از حداقل یک ایندکس قابل دسترسی باشد ────────
# ایندکس‌های مجاز (باید هر سند را با نام فایل لینک کنند):
INDEX_FILES = [
    ROOT / "README.md",
    ROOT / "INDEX.html",
    DOCS / "README.md",
    DOCS / "adr" / "README.md",
    DOCS / "manifest.json",
]
index_blob = "\n".join(read(f) for f in INDEX_FILES if f.exists())
for md in DOCS.rglob("*.md"):
    # ایندکس‌های بخش‌ها (README.md) خود ناوبری‌اند، نه سند محتوایی
    if md.name == "README.md":
        continue
    # سند باید با نام فایلش در یکی از ایندکس‌ها آمده باشد
    if md.name not in index_blob:
        errors.append(f"{md.relative_to(ROOT)}: سند یتیم — از هیچ ایندکسی لینک نشده")


# ── گزارش ──────────────────────────────────────────────────────────────────
total_md = len(list(DOCS.rglob("*.md")))
words = sum(len(read(p).split()) for p in DOCS.rglob("*.md"))
print(f"📊 بررسی {total_md} فایل مستند (~{words:,} کلمه)")
print(f"   DOC-IDهای یکتا: {len(seen)}")

if warnings:
    print(f"\n⚠️  {len(warnings)} هشدار:")
    for w in warnings:
        print(f"   - {w}")

if errors:
    print(f"\n❌ {len(errors)} خطا:")
    for e in errors:
        print(f"   - {e}")
    sys.exit(1)

print("\n✅ همهٔ بررسی‌ها پاس شد — مستندات سالم است.")
sys.exit(0)
