#!/usr/bin/env bash
#
# scaffold-structure.sh — ساخت اسکلت پوشه‌های فریمورک تَوان
#
# این اسکریپت ساختار پوشه‌ای مطابق docs/04-structure/folder-structure.md (DOC-080)
# را می‌سازد تا کدنویسی هسته و موتورها آغاز شود. هیچ کدی تولید نمی‌کند؛
# فقط پوشه‌ها + فایل‌های .gitkeep + فایل‌های پایهٔ خالی.
#
# استفاده:  bash tools/scripts/scaffold-structure.sh [مسیر_مقصد]
#           مسیر پیش‌فرض: ریشهٔ پروژه (یک سطح بالاتر از tools/)
#
set -euo pipefail

TARGET="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
cd "$TARGET"

echo "🏗️  ساخت اسکلت تَوان در: $TARGET"

# ── پوشه‌ها ────────────────────────────────────────────────────────────────
dirs=(
  bin
  public/assets public/media
  core/Application core/Autoloading core/Bootstrap core/Container core/Context
  core/Error core/Exceptions core/Events core/Facade/Facades core/Module
  core/Pipeline core/Provider core/Kernel
  core/Support/ValueObject core/Support/Math core/Support/Id core/Support/Time
  core/Support/Enum core/Support/Attributes
  core/Contracts/{Container,Config,Events,Http,Routing,Database,ORM,Validation,Cache,Queue,Auth,Authorization,Filesystem,Log,Mail,Notification,I18n,Encryption,Console,Observability,Workflow,Payment,Search,Support}
  engines
  config/schema
  app/src/{Http,Console,Application,Domain,Infrastructure,Providers,Policies,Support}
  app/config app/routes app/views app/lang/fa app/lang/en
  modules kits plugins
  database/{migrations,seeders,factories,schema}
  routes
  resources/{views,lang/fa,lang/en,css,js,fonts,images,stubs}
  storage/{app/public,app/private,cache,framework/sessions,framework/views,framework/testing,logs,backups,temp}
  tests/{Unit,Feature,Integration,Benchmark,Architecture,Security,Contract,Fixtures}
  docs deploy/{docker,nginx,apache,php,k8s,systemd,cron} tools/{phpstan,cs-fixer,scripts} examples
)

for d in "${dirs[@]}"; do
  mkdir -p "$d"
done

# ── موتورها (پوشهٔ خالی با ساختار استاندارد) ──────────────────────────────
engines=(
  container config event pipeline error log compat optimizer module
  http router session cookie view api realtime cors
  database schema migration orm validation search pagination
  crypt hash auth rbac security audit
  cache queue schedule console filesystem http-client mail notification observability backup
  i18n jalali
  workflow report payment media feature-flag tenancy
  scaffold admin plugin test upgrade
)

for e in "${engines[@]}"; do
  mkdir -p "engines/$e"/{src,config,lang/fa,lang/en,tests/Unit,tests/Feature,benchmarks,docs,examples}
  touch "engines/$e/src/.gitkeep"
done

# ── فایل‌های .gitkeep برای پوشه‌های خالی ───────────────────────────────────
find storage public/uploads modules kits plugins database -type d -empty -exec touch {}/.gitkeep \; 2>/dev/null || true

# ── فایل‌های پایه ──────────────────────────────────────────────────────────
[ -f .gitignore ] || cat > .gitignore <<'EOF'
.env
.env.local
.env.*.local
!.env.example
/storage/*
!/storage/**/.gitignore
/vendor/
/tools/vendor/
/public/assets/*
!/public/assets/.gitignore
/node_modules/
.phpunit.result.cache
.php-cs-fixer.cache
/.idea/
/.vscode/
*.swp
.DS_Store
EOF

[ -f .editorconfig ] || cat > .editorconfig <<'EOF'
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 4

[*.{json,yml,yaml,md,css,js,ts}]
indent_size = 2

[*.md]
trim_trailing_whitespace = false
EOF

[ -f .env.example ] || cat > .env.example <<'EOF'
# ── اپلیکیشن ───────────────────────────────────────────
TVN_APP_NAME=Tavaan
TVN_APP_ENV=local
TVN_APP_DEBUG=true
TVN_APP_URL=http://localhost:8000
TVN_APP_KEY=
TVN_APP_LOCALE=fa
TVN_FALLBACK_LOCALE=en
TVN_TIMEZONE=Asia/Tehran

# ── پایگاه داده ────────────────────────────────────────
TVN_DB_CONNECTION=mysql
TVN_DB_HOST=127.0.0.1
TVN_DB_PORT=3306
TVN_DB_DATABASE=tavaan
TVN_DB_USERNAME=root
TVN_DB_PASSWORD=

# ── کش / صف / نشست ─────────────────────────────────────
TVN_CACHE_DRIVER=file
TVN_QUEUE_CONNECTION=database
TVN_SESSION_DRIVER=file
TVN_SESSION_LIFETIME=120

# ── رمزنگاری ───────────────────────────────────────────
TVN_AUDIT_KEY=
TVN_BACKUP_KEY=

# ── بهینه‌سازی ─────────────────────────────────────────
TVN_AUTOLOAD_CACHE=false
TVN_CONFIG_CACHE=false
TVN_ROUTE_CACHE=false
TVN_VIEW_CACHE=false
EOF

[ -f bin/tvn ] || cat > bin/tvn <<'EOF'
#!/usr/bin/env php
<?php
//Entry point — پس از ساخت هسته، به bin/tvn.php متصل می‌شود.
declare(strict_types=1);
fwrite(STDERR, "Tavaan CLI not yet implemented. See docs/00-overview/quickstart.md\n");
exit(1);
EOF
chmod +x bin/tvn

[ -f public/index.php ] || cat > public/index.php <<'EOF'
<?php
// public/index.php — ساخته می‌شود در M2 (DOC-025 §2 P1)
declare(strict_types=1);
http_response_code(503);
echo 'Tavaan is not bootstrapped yet. See docs/02-architecture/bootstrapping.md';
EOF

# ── گزارش ──────────────────────────────────────────────────────────────────
total_dirs=$(find . -type d -not -path '*/.git*' | wc -l | tr -d ' ')
total_engines=${#engines[@]}
echo ""
echo "✅ اسکلت ساخته شد:"
echo "   📁 پوشه‌ها:      $total_dirs"
echo "   ⚙️  موتورها:      $total_engines (پوشهٔ استاندارد)"
echo "   📄 فایل‌های پایه: .gitignore, .editorconfig, .env.example, bin/tvn, public/index.php"
echo ""
echo "گام بعدی: core/bootstrap.php را طبق docs/02-architecture/bootstrapping.md §10 بنویسید."
echo "         سپس اولین موتور (container) را طبق docs/03-engines/container.md بسازید."
