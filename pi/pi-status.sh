#!/bin/sh
# Publish the public health snapshot that luketye.dev's header strip reads.
#
# Reads three kernel-provided files, validates every value, then writes
# status.json into the webroot through a temp file and an atomic rename, so a
# reader never sees a half-written file. The webroot is bind-mounted read-only
# into the nginx container, so this script is its only writer.
#
# What this publishes is a positive allowlist: four numbers and a time. No
# hostname, no IP address, no kernel version, no container names, no tailnet
# address. Adding a field is a deliberate decision, never a side effect.
set -eu

WEB="$HOME/sites/luketye.dev"
OUT="$WEB/status.json"
TMP="$WEB/.status.json.new"

# Pacific is pinned here rather than inherited from the system. Changing the
# Pi's own timezone later therefore does not change this output.
TZ=America/Los_Angeles
export TZ

# Uptime is published in whole days. Finer granularity tells a reader more
# precisely how long the running kernel has gone unpatched, and buys the page
# nothing.
up_days=$(awk '{printf "%d", $1/86400}' /proc/uptime)
load1=$(awk '{print $1}' /proc/loadavg)
temp_c=$(awk '{printf "%.1f", $1/1000}' /sys/class/thermal/thermal_zone0/temp)

# generated drives the age calculation; the offset makes it unambiguous in
# every viewer's timezone. display is what the page shows when the data is
# stale, so the Pi stays the source of truth for its own clock.
generated=$(date +%Y-%m-%dT%H:%M:%S%:z)
display=$(date '+%-I:%M %p PT')

# Validate before publishing. A failed check exits without writing and leaves
# the last good file in place, rather than replacing it with something
# malformed. The page's staleness logic then surfaces the failure on its own.
fail() { echo "pi-status: $1" >&2; exit 1; }

echo "$up_days"   | grep -qE '^[0-9]+$'                              || fail "bad uptime: $up_days"
echo "$load1"     | grep -qE '^[0-9]+\.[0-9]+$'                      || fail "bad load: $load1"
echo "$temp_c"    | grep -qE '^[0-9]+\.[0-9]+$'                      || fail "bad temp: $temp_c"
echo "$generated" | grep -qE '^[0-9-]{10}T[0-9:]{8}[+-][0-9]{2}:[0-9]{2}$' || fail "bad timestamp: $generated"
echo "$display"   | grep -qE '^[0-9]{1,2}:[0-9]{2} (AM|PM) PT$'      || fail "bad display: $display"

cat > "$TMP" <<JSON
{"uptime_days":$up_days,"load1":$load1,"temp_c":$temp_c,"generated":"$generated","display":"$display"}
JSON

chmod 644 "$TMP"
mv "$TMP" "$OUT"
