#!/bin/bash
# Does the work-tree hook speak when it should, and stay quiet when it should?
#
# Run it after ANY change to worktree-reminder.py:
#     ./worktree-reminder.test.sh
#
# A hook that is too noisy gets switched off, and a hook that is too quiet is not there at all.
# Both failures look like success from the outside, which is why this exists.
HOOK="$(dirname "$0")/worktree-reminder.py"
M="$HOME/Adam work/Claude Code/daily-mentions-monitor"    # any shared checkout on main
fails=0

try () {  # try "<what>" "<json-quoted command>" SPEAK|QUIET
  out=$(python3 - "$HOOK" <<EOF
import json,subprocess,sys
p=json.dumps({"session_id":"t-$RANDOM$RANDOM","tool_name":"Bash","tool_input":{"command":$2}})
r=subprocess.run([sys.executable,sys.argv[1]],input=p,capture_output=True,text=True)
print("SPEAK" if r.stdout.strip() else "QUIET")
EOF
)
  if [ "$out" = "$3" ]; then echo "  ok    $out  $1"
  else echo "  FAIL  got $out, wanted $3 — $1"; fails=$((fails+1)); fi
}

echo "It must SPEAK — a file landing in the shared folder:"
try "python heredoc"            "\"cd '$M' && python3 - <<'PY'\nopen('docs/x.md','w').write(s)\nPY\"" SPEAK
try "sed -i, mac style"         "\"sed -i '' 's/a/b/' '$M/scripts/main.py'\"" SPEAK
try "sed -i, no suffix"         "\"cd '$M' && sed -i 's/a/b/' scripts/main.py\"" SPEAK
try "redirect"                  "\"echo hi > '$M/docs/notes.md'\"" SPEAK
try "append"                    "\"echo hi >> '$M/docs/notes.md'\"" SPEAK
try "cp"                        "\"cp /tmp/x.md '$M/docs/x.md'\"" SPEAK
try "tee"                       "\"echo hi | tee '$M/docs/n.md'\"" SPEAK

echo "It must stay QUIET — nothing is being written where it matters:"
try "reading a file"            "\"cat '$M/scripts/main.py'\"" QUIET
try "grep"                      "\"grep -rn foo '$M/scripts'\"" QUIET
try "git log"                   "\"cd '$M' && git log --oneline -5\"" QUIET
try "running the tests"         "\"cd '$M' && ./.venv/bin/python -m pytest -q\"" QUIET
try "writing to /tmp"           "\"echo hi > /tmp/scratch.txt\"" QUIET
try "redirect to /dev/null"     "\"cd '$M' && ls > /dev/null\"" QUIET
try "stderr only"               "\"cd '$M' && ls 2>/dev/null\"" QUIET
try "writing inside a worktree" "\"echo hi > '$M/.claude/worktrees/x/docs/n.md'\"" QUIET
try "git commit"                "\"cd '$M' && git commit -q -m 'x'\"" QUIET
try "curl to a temp file"       "\"curl -s http://x/y -o /tmp/z\"" QUIET

echo
[ $fails -eq 0 ] && echo "all good" || { echo "$fails failed"; exit 1; }
