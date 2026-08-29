#!/bin/bash
# Checks the runbooks hook speaks where it should and stays quiet everywhere else.
#
# Run it after ANY change to writing-runbooks-reminder.py. A hook that is too noisy gets
# switched off, and a hook that is too quiet is not there at all — and both look exactly
# like success from the outside, which is why this exists.
#
#   ./writing-runbooks-reminder.test.sh

HOOK="$(dirname "$0")/writing-runbooks-reminder.py"
pass=0; fail=0

# say <what it should do> <name of the check> <the payload>
say() {
  local want="$1" name="$2" payload="$3"
  # A fresh session id every time, so the once-per-file mark never hides a real answer.
  payload="${payload//SESSION/probe-$RANDOM$RANDOM$RANDOM}"
  local got; got="$(printf '%s' "$payload" | /usr/bin/python3 "$HOOK")"
  local heard="quiet"; [ -n "$got" ] && heard="speaks"
  if [ "$heard" = "$want" ]; then
    pass=$((pass+1)); printf '  ok    %-52s %s\n' "$name" "$heard"
  else
    fail=$((fail+1)); printf '  FAIL  %-52s wanted %s, got %s\n' "$name" "$want" "$heard"
  fi
}

# A page of instructions, used wherever the writing itself is what is being tested.
PAGE='# Booking a shipment

Read this whole page before starting.

## 1. Check the numbers

**Never invent a quantity.** If the sheet has no figure, ask.

## 2. Send it

Otherwise the booking goes out with a number nobody can vouch for, and it fails
silently — the shipment looks booked and no one finds out for a week.

If it refuses → report it and stop.
'
# Ordinary code, the same length, with a couple of the same words in comments.
CODE='import os

def load(path):
    """Read the file. Never returns None."""
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    with open(path) as fh:
        text = fh.read()
    if not text:
        raise ValueError("empty")
    return text


def save(path, text):
    """Write it back. Always writes the whole file."""
    with open(path, "w") as fh:
        fh.write(text)
    return len(text)
'
esc() { /usr/bin/python3 -c 'import json,sys; print(json.dumps(sys.stdin.read())[1:-1])'; }
PAGE_J="$(printf '%s' "$PAGE" | esc)"
CODE_J="$(printf '%s' "$CODE" | esc)"

echo "Where pages live — the name or the folder is enough"
say speaks "SKILL.md anywhere"            '{"session_id":"SESSION","tool_name":"Write","tool_input":{"file_path":"/p/SKILL.md","content":"x"}}'
say speaks "RECIPE.md anywhere"           '{"session_id":"SESSION","tool_name":"Write","tool_input":{"file_path":"/p/RECIPE.md","content":"x"}}'
say speaks "a page under /docs/"          '{"session_id":"SESSION","tool_name":"Write","tool_input":{"file_path":"/p/docs/how.md","content":"x"}}'
say speaks "another page in a skill"      '{"session_id":"SESSION","tool_name":"Write","tool_input":{"file_path":"/h/.claude/skills/shopify/stock-switch.md","content":"x"}}'
say speaks "an agent recipe"              '{"session_id":"SESSION","tool_name":"Write","tool_input":{"file_path":"/p/scheduled-tasks/x/agents/stock-agent.md","content":"x"}}'

echo
echo "The writing itself, whatever the file is called"
say speaks "instructions in a plainly-named page"  "{\"session_id\":\"SESSION\",\"tool_name\":\"Write\",\"tool_input\":{\"file_path\":\"/p/notes.md\",\"content\":\"$PAGE_J\"}}"
say speaks "instructions added by an edit"         "{\"session_id\":\"SESSION\",\"tool_name\":\"Edit\",\"tool_input\":{\"file_path\":\"/p/notes.md\",\"new_string\":\"$PAGE_J\"}}"
say quiet  "the same words inside source code"     "{\"session_id\":\"SESSION\",\"tool_name\":\"Write\",\"tool_input\":{\"file_path\":\"/p/loader.py\",\"content\":\"$CODE_J\"}}"
say quiet  "a short note, not a page"              '{"session_id":"SESSION","tool_name":"Write","tool_input":{"file_path":"/p/notes.md","content":"# Monday\n\nRan it again. Never mind, it works now."}}'
say quiet  "a one-line tweak to a plain page"      '{"session_id":"SESSION","tool_name":"Edit","tool_input":{"file_path":"/p/notes.md","new_string":"the total, not the subtotal"}}'

echo
echo "Bash writes"
say speaks "sed -i on a page in a skill"  '{"session_id":"SESSION","tool_name":"Bash","tool_input":{"command":"sed -i '"''"' 5d /h/.claude/skills/shopify/sold-out.md"}}'
say speaks "a heredoc into /docs/"        '{"session_id":"SESSION","tool_name":"Bash","tool_input":{"command":"cat > /p/docs/how.md <<EOF"}}'
say quiet  "reading a page"               '{"session_id":"SESSION","tool_name":"Bash","tool_input":{"command":"grep -n foo /p/docs/how.md"}}'
say quiet  "writing code, not a page"     '{"session_id":"SESSION","tool_name":"Bash","tool_input":{"command":"cat > /p/scripts/main.py <<EOF"}}'
# The folder is the only thing that says where a bare name lands.
say speaks "cd into a skill, then sed"    '{"session_id":"SESSION","tool_name":"Bash","tool_input":{"command":"cd /h/.claude/skills/shopify && sed -i '"''"' 5d sold-out.md"}}'
say quiet  "cd into a skill, then grep"   '{"session_id":"SESSION","tool_name":"Bash","tool_input":{"command":"cd /h/.claude/skills/shopify && grep -n foo sold-out.md"}}'
say quiet  "cd into code, then sed"       '{"session_id":"SESSION","tool_name":"Bash","tool_input":{"command":"cd /p/scripts && sed -i '"''"' 5d main.py"}}'

echo
echo "Never speaks twice about the same file"
FIXED='{"session_id":"same-session","tool_name":"Write","tool_input":{"file_path":"/p/docs/twice.md","content":"x"}}'
rm -f "$TMPDIR"claude-runbook-reminder-* 2>/dev/null
first="$(printf '%s' "$FIXED" | /usr/bin/python3 "$HOOK")"
second="$(printf '%s' "$FIXED" | /usr/bin/python3 "$HOOK")"
if [ -n "$first" ] && [ -z "$second" ]; then
  pass=$((pass+1)); printf '  ok    %-52s speaks then quiet\n' "second edit to one file"
else
  fail=$((fail+1)); printf '  FAIL  %-52s wanted speaks then quiet\n' "second edit to one file"
fi

echo
echo "$pass passed, $fail failed"
[ "$fail" -eq 0 ]
