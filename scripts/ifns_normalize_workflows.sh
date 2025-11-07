#!/usr/bin/env bash
set -e
mkdir -p .github/workflows
# انقل أي YAML من مسارات متداخلة إلى المسار القياسي
for f in $(git ls-files | grep -E '\.github/.+/workflows/.+\.(yml|yaml)$' || true); do
  base="$(basename "$f")"
  dest=".github/workflows/$base"
  if [ "$f" != "$dest" ]; then
    git mv -f "$f" "$dest"
  fi
done
# حذف مجلدات workflows الفارغة
find .github -type d -name workflows -not -path "./.github/workflows" -empty -delete || true
