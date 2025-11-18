
#!/usr/bin/env bash
# verify_checksums.sh
INDEX_JSON="${1:-IFNS_Indicators_Packs_Index_v0_18.json}"
if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required"; exit 2
fi
all_ok=0
count=$(jq '.items | length' "$INDEX_JSON")
for ((i=0; i<count; i++)); do
  fname=$(jq -r ".items[$i].filename" "$INDEX_JSON")
  expect=$(jq -r ".items[$i].sha256" "$INDEX_JSON")
  if [ ! -f "$fname" ]; then
    echo "MISSING: $fname"; all_ok=1; continue
  fi
  if command -v sha256sum >/dev/null 2>&1; then
    actual=$(sha256sum "$fname" | awk '{print $1}')
  else
    actual=$(shasum -a 256 "$fname" | awk '{print $1}')
  fi
  if [ "$actual" != "$expect" ]; then
    echo "MISMATCH: $fname"
    echo " expected: $expect"
    echo " actual  : $actual"
    all_ok=1
  else
    echo "OK: $fname"
  fi
done
if [ $all_ok -eq 0 ]; then echo "ALL OK"; else exit 2; fi
