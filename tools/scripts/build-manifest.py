#!/usr/bin/env python3
"""
build-manifest.py — تولید فهرست ماشین‌خوان مستندات تَوان (docs/manifest.json)

پس از افزودن/ویرایش هر سند، این اسکریپت را اجرا کنید تا manifest.json
با وضعیت واقعی همگام بماند:

    python3 tools/scripts/build-manifest.py

سپس با `python3 tools/scripts/verify-docs.py` سازگاری را بررسی کنید.
خروجی مطابق schema در docs/schemas/docs-manifest.v1.json است.
"""
import re
import json
import hashlib
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
DOCS = ROOT / "docs"

SECTIONS = {
    "": "شاخص",
    "00-overview": "نمای کلی و اهداف",
    "01-standards": "استانداردها و قواعد",
    "02-architecture": "معماری",
    "03-engines": "موتورها",
    "04-structure": "ساختار پوشه و فایل",
    "05-applications": "کاربردها (Kits)",
    "06-roles-access": "نقش‌ها و دسترسی",
    "07-quality": "کیفیت",
    "08-roadmap": "نقشهٔ راه",
    "09-references": "مراجیع و واژه‌نامه",
    "adr": "تصمیم‌های معماری",
    "templates": "قالب‌ها",
}


def doc_id(text: str):
    m = re.search(r"DOC-ID\s*\|\s*([A-Z0-9\-]+)", text)
    return m.group(1) if m else None


def title_of(text: str, path: pathlib.Path) -> str:
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if m:
        return re.sub(r"^DOC-[0-9A-Z]+\s*[—-]\s*", "", m.group(1).strip())
    return path.stem


def build_catalog() -> list[dict]:
    catalog = []
    for sec, label in SECTIONS.items():
        base = DOCS / sec if sec else DOCS
        for md in sorted(base.glob("*.md")):          # فقط همین سطح
            text = md.read_text(encoding="utf-8")
            catalog.append({
                "section": sec or "index",
                "section_label": label,
                "doc_id": doc_id(text),
                "title": title_of(text, md),
                "path": str(md.relative_to(ROOT)),
                "machine_readable": "machine-readable:" in text,
                "sha256": hashlib.sha256(text.encode()).hexdigest()[:16],
            })
    return catalog


def build_engines() -> list[dict]:
    engines = []
    for md in sorted((DOCS / "03-engines").glob("*.md")):
        if md.name == "README.md":
            continue
        text = md.read_text(encoding="utf-8")
        b = re.search(r"# machine-readable: tavaan\.engine\.([a-z\-]+)\.v1", text)
        slug = b.group(1) if b else md.stem
        ns = re.search(r"namespace:\s*(\S+)", text)
        pr = re.search(r"priority:\s*(\S+)", text)
        ph = re.search(r"phase:\s*(\S+)", text)
        engines.append({
            "engine_id": f"tavaan.engine.{slug}",
            "slug": slug,
            "namespace": ns.group(1) if ns else None,
            "priority": pr.group(1) if pr else None,
            "phase": ph.group(1) if ph else None,
            "doc": f"docs/03-engines/{md.name}",
        })
    return engines


def main() -> None:
    catalog = build_catalog()
    engines = build_engines()
    schemas = len(list((DOCS / "schemas").glob("*.json"))) if (DOCS / "schemas").exists() else 0

    manifest = {
        "$schema": "https://docs.tavaan.dev/schemas/docs-manifest.v1.json",
        "framework": {
            "name": "Tavaan", "name_fa": "تَوان", "version": "1.0.0", "php_min": "8.2.0",
            "dependency_policy": "zero-external",
            "architectures": ["layered", "hmvc", "modular-monolith", "event-driven", "hexagonal"],
        },
        "generated_note": "فهرست ماشین‌خوان همهٔ مستندات — برای پیمایش خودکار ایجنت‌ها",
        "totals": {"documents": len(catalog), "engines": len(engines), "schemas": schemas, "adrs": 16},
        "entry_points": {
            "human_dashboard": "INDEX.html", "index": "docs/README.md", "readme": "README.md",
            "quickstart": "docs/00-overview/quickstart.md",
            "engine_registry": "docs/03-engines/README.md",
            "agent_backlog": "docs/08-roadmap/agent-backlog.md", "adr_index": "docs/adr/README.md",
        },
        "reading_paths": {
            "engine_builder": ["DOC-010", "DOC-011", "DOC-012", "DOC-013", "DOC-014", "DOC-030", "DOC-110", "DOC-113"],
            "architect": ["DOC-001", "DOC-002", "DOC-020", "DOC-021", "DOC-022", "DOC-023", "DOC-024", "DOC-025"],
            "app_builder": ["DOC-021", "DOC-022", "DOC-080", "DOC-090", "DOC-100", "DOC-101"],
            "qa_reviewer": ["DOC-010", "DOC-016", "DOC-110", "DOC-111", "DOC-112", "DOC-113"],
        },
        "engines": engines,
        "catalog": catalog,
    }

    out = DOCS / "manifest.json"
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ {out.relative_to(ROOT)} تولید شد: {len(catalog)} سند، {len(engines)} موتور، {schemas} schema")


if __name__ == "__main__":
    main()
