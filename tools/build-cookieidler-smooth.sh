#!/usr/bin/env bash
set -euo pipefail

ORIGINAL_URL='https://raw.githubusercontent.com/KS-Sainen/Custom-Theory-Cookie-Idler/main/CookieIdler%20-%20Redux.js'
PATCH_FILE='patches/cookieidler-smooth-counter.patch'
OUTPUT_FILE='CookieIdler-Redux.smooth-counter.js'
TMP_ORIGINAL='CookieIdler - Redux.js'

curl -fsSL "$ORIGINAL_URL" -o "$TMP_ORIGINAL"
cp "$TMP_ORIGINAL" "$OUTPUT_FILE"
git apply --unsafe-paths --whitespace=nowarn --directory=. "$PATCH_FILE"

# git apply modifies the path named in the patch. Normalize final file name.
if [[ -f 'CookieIdler - Redux.smooth-counter.js' ]]; then
  mv 'CookieIdler - Redux.smooth-counter.js' "$OUTPUT_FILE"
fi

node --check "$OUTPUT_FILE"
rm -f "$TMP_ORIGINAL"
