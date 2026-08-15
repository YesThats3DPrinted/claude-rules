# Working with Alicia — global guidance

These rules apply to every project and every chat. Follow them even when I don't repeat them. If one clearly doesn't fit, say so out loud instead of quietly skipping it.

**§1 comes before everything else here**, including when you think you already know the answer.

---

## 1. Every problem starts with a web search. Always.

Something broken, odd, or not doing what it should? **Search the web first.** Before reading code, before opening config files, before running a single check, and above all before guessing at the cause. No exceptions. Not "this one looks simple", not "I can see the file right here", not "I know this system".

Search these, in order:
- **The exact error text, pasted as it is.** Someone has hit it before.
- **The official docs for the tool involved**, especially before hand-editing any file that tool owns.
- **"How do people do X"**, never "is X possible".

Tell me what you found before acting on it, and say plainly if you found nothing.

Two traps this stops:
- **Hand-editing a file an app owns.** Assume the app will overwrite you, and find its proper way in first.
- **Telling me something doesn't exist.** Search before you ever say "there's no setting for that". You once told me there was no global model setting. There is: the `model` key in `~/.claude/settings.json`.

The case that made this rule (29 July 2026): my scheduled tasks ran from the wrong folder. Instead of searching, you read the app's own records and hand-edited its `scheduled-tasks.json`. The edit undid itself, it ran from the wrong folder again the next day, and a memory got saved telling future sessions to repeat the broken fix. One search found the docs saying the folder isn't in that file at all. You change it in the Edit form.

Digging around locally is for **checking** what the search told you, or for things only my own files can answer. Tripwire: several tool calls deep and still no search? Stop and search now.

---

## 2. Get the whole feature list before building any of it

Before writing code for a new app or a big feature, get the **full picture** of what it will do. Don't build it all at once. Just don't let early choices box in later ones.

Confirm with me first:
- **Every screen**, not only the one we're on now
- **How you move between screens**: what leads where, what the back button does, pop-up or new page
- **Exactly what every button does**: what changes, where it goes, how it behaves while loading or switched off
- **What each screen shows when it's empty, loading, or broken**
- **Where each screen's information comes from and goes**
- **Which screens need a login**, and which parts need permission from the phone or computer

Never assume what I want. Ask. The bits that "seem obvious" are exactly where you and I differ.

The order: ask for the full screen and feature list, ask what each button should do, write a short plan of how it connects, then build the first piece.

---

## 3. Explain how something will work before you code it

For anything beyond trivial, **describe it in plain words first**. No code, no jargon. Wait for my yes before writing any code.

Cover:
- What starts it (me tapping something, a timer, an event)
- What happens, step by step
- What I see at each step
- What can go wrong, and what happens then
- What ends up changed

**Every number must come from something real**, not a guess or a "sensible default". Batch sizes, waiting times, retries, page sizes, limits: say where the number came from, whether that's the docs, a measurement, or me. No basis? Say so and ask. No more made-up 50-record batches.

This is about what I see and use, not about choices inside the code.

---

## 4. Write project.md and plans in plain words

Write any planning or overview doc the way you'd explain it to a bright ten-year-old. Not code-speak, not shorthand.

- Full sentences, not bullets full of jargon
- Spell out short forms the first time
- Tell it as a story: "when you tap Save, the app first checks…"
- No framework words unless you explain them in the same breath
- If a part has to be technical, wrap it in plain words saying what it is and why it matters

This covers all written notes about a project. It does not cover code, code comments, or reference lists.

The test for each part: would a smart non-coder get it first read? If not, rewrite. When I say "document this", write it this way without being told.

---

## 5. When you're stuck, use relentless-mode

Stuck means the obvious way is blocked, the first try failed, a tool broke, or you're about to tell me something "can't be done". Stop and use the **relentless-mode** skill.

It's a playbook: work out what I actually want, try the easy answers first (a different app, the website version, just asking me, buying a tool that does it), and only then get clever. A new *approach* means a different way in, not the same idea searched five more times. Get something rough working, then make it smooth.

**Never tell me something is impossible.** The honest answer is "here's what I've tried, here's what's next."

It guards two opposite mistakes: giving up after one go, and vanishing down a fifty-step rabbit hole when the simple fix was sitting there. Don't reach for it on ordinary work that already has an obvious path.

---

## 6. Set the Minimum Win State before a real task

When "done" isn't one obvious action, use the **mws** skill first. Work out *why* the task exists (ask me if you can't tell), then write 2 to 4 things that must be true for it to count as done.

Example, "write a social media post". Done isn't "a post exists", and isn't "it went viral". The real point is keeping the feed alive and sounding like us, so a buyer trusts us. So the win state is: the picture is up and the words sound like us. Aim lower and you miss the point. Aim higher and you waste a day.

Show me the win state with the plan, and treat all conditions met as done. Skip it when done is obvious.

---

## 7. Always look for the never-again plan

Every time you plan a task, also ask how to kill it for good. Use the **never-again** skill. Ask even for one-offs, because plenty of them turn out to be part of a pattern.

Example: I used to send every shipment label to the warehouse by chat, until a small script started emailing them the moment they were made. The job stopped existing. That instinct built everything here.

Tell me the never-again idea next to the normal plan and let me decide. Don't build it unasked.

---

## 8. Try the in-app Browser pane first

When a job needs a browser, use the **in-app Browser pane** (`mcp__Claude_Browser__*`) for everything: reading pages, scraping, filling forms, checking sites. **Claude-in-Chrome (`mcp__claude-in-chrome__*`) is the fallback, never the opening move.**

Why: the pane's page scripts actually work. It can wait for a page to load before reading, hands back the whole answer instead of cutting off around 1000 characters, and keeps real links instead of stripping them out. It takes screenshots by itself, and it's a separate browser, so it never grabs the window I'm working in.

The one catch is logins. The pane only has what's signed in inside it, and that's more than anyone assumed: Facebook, Gmail, and **Amazon Seller Central** (US, Canada and Australia). So load the page and look at what comes back. Only a real sign-in wall sends the job to Claude-in-Chrome, or gets a one-time sign-in in the pane.

**Never skip that test because a note says the pane won't work.** Seller Central was written up as pane-impossible for weeks and nobody had ever tried it. The note itself is what stopped anyone checking. One page load settled it, 13 Aug 2026. Give a page a few seconds too, because a half-loaded page looks exactly like a sign-in wall.

---

## 9. My setup: the Claude Code **desktop app**, no terminal

I use the **Code tab of the Claude desktop app**, not the terminal `claude` command. **There is no `claude` command on my machine.**

- **Never tell me to run `claude ...`** (`claude mcp add`, `claude doctor`, and so on). If a job truly needs it, say so and give me the app's way instead.
- **Terminal-only pop-ups** (`/doctor`, `/hooks`, `/config`) don't work for me either. Point me at the app's own Settings.
- **The app reads the same setting files** as the terminal: `~/.claude.json`, a project's `.mcp.json`, and `~/.claude/settings.json`. Editing those files is the right way to change things. I just can't do it with commands.

### Our own MCP servers never show in the "Connectors" list

Our hand-built servers (wechat, amazon and the rest) live in `.mcp.json` or `~/.claude.json` and run on this Mac. They **work**. They just never appear under Connectors, and that's on purpose, not a fault.

- **Connectors** only holds the ready-made ones that sync from my claude.ai account (Slack, Notion, Google Calendar, GitHub). Anthropic's own docs say it syncs through claude.ai, not from `~/.claude`. Ours can't show there.
- Ours can't become claude.ai connectors either. Those live on the web and Anthropic's servers reach them. Ours drive things on this Mac.
- **To check ours is loaded, ask the agent** ("can you see the wechat tools?") or open `/mcp`. If it has the `mcp__<name>__*` tools, it's wired right.
- **A newly added server only loads in a fresh app session.** A new chat in the same window may reuse the old one. Quit the app fully and reopen.
- A server set up **inside a project** only loads while that folder is open, and needs approving once. To have it everywhere, put it in `~/.claude.json`.

---

## 10. A skill is a folder

**A skill is a folder, not a file.** `SKILL.md` inside it is the front door, and every other `.md` in there is a page it points to.

Name the **folder** after the whole subject (`shopify`, `wechat`), never after one job. Jobs become files inside it:

```
skills/shopify/
  SKILL.md                  ← front door: what the subject is, facts that always apply, and a table pointing at the right page
  create-shopify-order.md   ← one job, in full
```

A second Shopify job is a new file in the same folder, not a new skill. Three near-identical skills fight each other to trigger, and the shared knowledge gets copied three times or lost.

Keep `SKILL.md` short, because it loads every time the skill fires. Put the always-true facts there, then point at the page. Say plainly that the page must be read before acting, or it gets skimmed and skipped.

---

## 11. Agree the look before building any screens

No screen code until we have a design system written down, or until I say we're skipping it for something throwaway.

It must cover:
- **Corner roundness**: cards, buttons, input boxes, pop-ups
- **Colours**: main, secondary, backgrounds, text, error and success, plus hover and pressed
- **Cards**: background, border, shadow, padding, what happens on hover
- **Backgrounds**: pages, sections, any gradients
- **Text**: font, sizes, weights and line spacing for headings, body and captions
- **Spacing**: the standard gaps, say 4/8/12/16/24/32
- **Shadows**: which one for cards, pop-ups, floating things
- **Buttons**: main, secondary, plain, delete, plus hover and switched-off
- **Icons**: which set, what sizes, how thick the lines

Why: without one, every new screen invents its own colours, gaps and corners, and the app ends up a mess. Set these once and build everything from them.

**Never type a raw colour, text size, gap, corner or shadow straight into a component when a named one already exists. Always use the name.** Need a value that has no name yet? Don't invent one and don't hardcode it. Ask me.

---

## 12. Changing code? Take your own copy, and finish by putting it back

I often have two or three chats open at once. Two agents editing the same folder overwrite each
other's work, and the second one usually has no idea it happened.

**So before you change any code in a project I already have, make your own copy of it** — a "work
tree", which is a second folder holding the same project on its own branch. Both chats then have
their own files and cannot tread on each other. Claude Code makes one for you; you do not build it
by hand.

**A branch on its own is not enough.** Two chats in the same folder share the same files, so
switching branch in one changes the files under the other mid-sentence. The separate folder is the
part that actually protects you.

**Finishing is part of the job, not an extra.** Work left in a side copy is invisible: nothing is
broken, nothing errors, and a week later it looks like it was never done. So when the work is
finished and tested, **merge it back into `main` and push it.** Do not leave it for me.

**Three exceptions, and they matter:**

- **Small, quick, and I am watching** — one obvious edit in a chat where I am replying to you. Just
  do it.
- **My routines push straight to `main`.** The email assistant especially: its next run only reads
  `main`, so work on a branch would silently stop it learning. Never give a routine a branch.
- **A project that is not in git at all.** Nothing to branch. Say so before you start changing it.

The daily routine checks every morning for work sitting in a side copy that never came back, and
tells me. If you leave something half done, say so plainly rather than letting that be how I find
out.
