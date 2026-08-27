#!/usr/bin/env python3
"""Round-trip the site's prose through a plain-text file.

    python3 copy/copy-deck.py extract   # index.html  -> copy/copy-deck.md
    python3 copy/copy-deck.py apply     # copy/copy-deck.md -> index.html

extract writes every editable string into copy-deck.md, one labelled block
each, and records the exact source snippet it came from in copy-deck.lock.json.
apply reads the deck back and rewrites index.html.

Rewrite only the text under each `## [id]` heading. Do not edit the ids, and
do not reorder or delete blocks. Inline markup inside a block (for example
<span class="mono">) is part of the text -- keep it if you still want it.

apply matches on the exact snippet recorded at extract time, so it refuses to
run if index.html changed underneath the deck. Re-run extract if that happens.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, 'index.html')
DECK = os.path.join(ROOT, 'copy', 'copy-deck.md')
LOCK = os.path.join(ROOT, 'copy', 'copy-deck.lock.json')

# (kind, regex). The capture group is the editable text.
PATTERNS = [
    ('wordmark',   re.compile(r'(<div class="wordmark sans">)(.*?)(</div>)', re.S)),
    ('eyebrow',    re.compile(r'(<div class="label mono">)(.*?)(</div>)', re.S)),
    ('h1',         re.compile(r'(<h1>)(.*?)(</h1>)', re.S)),
    ('h2',         re.compile(r'(<h2>)(.*?)(</h2>)', re.S)),
    ('thesis',     re.compile(r'(<p class="thesis sans">)(.*?)(</p>)', re.S)),
    ('para',       re.compile(r'(<p class="body-text sans">)(.*?)(</p>)', re.S)),
    ('para',       re.compile(r'(<p class="body-text">)(.*?)(</p>)', re.S)),
    ('note',       re.compile(r'(<div class="margin-note sans">)(.*?)(</div>)', re.S)),
    ('projname',   re.compile(r'(<span class="project-name">)(.*?)(</span>)', re.S)),
    ('writeup',    re.compile(r'(<div class="writeup"><span>)(.*?)(</span>)', re.S)),
    ('phase',      re.compile(r'(<span class="name">)(.*?)(</span>)', re.S)),
    ('pending',    re.compile(r'(<span class="pending">)(.*?)(</span>)', re.S)),
]

ROLE = {
    'wordmark': 'site wordmark',
    'eyebrow': 'small mono label above the heading',
    'h1': 'the page-opening statement',
    'h2': 'section heading',
    'thesis': 'the opening paragraph -- who you are and what this site is',
    'para': 'body paragraph',
    'note': 'margin note -- the specific bug or detail behind the project',
    'projname': 'project name',
    'writeup': 'planned write-up title',
    'phase': 'roadmap item',
    'pending': 'placeholder link label',
}


def sections(src):
    """Map an offset in the source to the section id it falls inside."""
    marks = [(m.start(), m.group(1))
             for m in re.finditer(r'<section id="([^"]+)"', src)]
    marks += [(m.start(), m.group(1))
              for m in re.finditer(r'<(header|footer) class=', src)]
    marks.sort()

    def at(pos):
        cur = 'page'
        for start, name in marks:
            if start <= pos:
                cur = name
            else:
                break
        return cur
    return at


def extract():
    src = open(HTML).read()
    at = sections(src)
    found = []
    for kind, rx in PATTERNS:
        for m in rx.finditer(src):
            found.append({'pos': m.start(), 'kind': kind, 'section': at(m.start()),
                          'open': m.group(1), 'text': m.group(2).strip(),
                          'close': m.group(3), 'snippet': m.group(0)})
    found.sort(key=lambda b: b['pos'])

    seen = {}
    lock = {}
    lines = [
        '# Copy deck',
        '',
        'Rewrite the text under each `## [id]` heading, in your own voice.',
        'Leave the ids alone. Do not reorder or delete blocks.',
        'Inline markup inside a block is part of the text -- keep it if you want it.',
        '',
        'Then run:  `python3 copy/copy-deck.py apply`',
        '',
        '---',
        '',
    ]
    for b in found:
        key = '%s.%s' % (b['section'], b['kind'])
        seen[key] = seen.get(key, 0) + 1
        bid = key if seen[key] == 1 else '%s%d' % (key, seen[key])
        if src.count(b['snippet']) != 1:
            print('warn: snippet for %s is not unique, skipping' % bid, file=sys.stderr)
            continue
        lock[bid] = b['snippet']
        words = len(re.sub(r'<[^>]+>', '', b['text']).split())
        lines.append('## [%s]' % bid)
        lines.append('<!-- %s | currently %d words -->' % (ROLE.get(b['kind'], b['kind']), words))
        lines.append('')
        lines.append(b['text'])
        lines.append('')
    open(DECK, 'w').write('\n'.join(lines))
    json.dump(lock, open(LOCK, 'w'), indent=1)
    print('wrote %s (%d blocks) and %s' % (
        os.path.relpath(DECK, ROOT), len(lock), os.path.relpath(LOCK, ROOT)))


def apply():
    src = open(HTML).read()
    lock = json.load(open(LOCK))
    deck = open(DECK).read()

    blocks = {}
    cur = None
    buf = []
    for line in deck.splitlines():
        m = re.match(r'^## \[([^\]]+)\]\s*$', line)
        if m:
            if cur:
                blocks[cur] = '\n'.join(buf).strip()
            cur = m.group(1)
            buf = []
        elif cur is not None:
            if line.startswith('<!--') and line.rstrip().endswith('-->'):
                continue
            buf.append(line)
    if cur:
        blocks[cur] = '\n'.join(buf).strip()

    missing = [k for k in lock if k not in blocks]
    if missing:
        sys.exit('deck is missing blocks: %s' % ', '.join(missing))

    changed = 0
    for bid, snippet in lock.items():
        if src.count(snippet) != 1:
            sys.exit('index.html no longer matches the deck at [%s].\n'
                     'Re-run: python3 copy/copy-deck.py extract' % bid)
        m = None
        for _, rx in PATTERNS:
            m = rx.fullmatch(snippet)
            if m:
                break
        if not m:
            sys.exit('could not re-parse the snippet for [%s]' % bid)
        new_text = blocks[bid]
        if new_text == m.group(2).strip():
            continue
        src = src.replace(snippet, m.group(1) + new_text + m.group(3), 1)
        changed += 1
    open(HTML, 'w').write(src)
    print('updated %d block(s) in index.html' % changed)
    if changed:
        print('re-run `python3 copy/copy-deck.py extract` to re-sync the lock')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'extract':
        extract()
    elif cmd == 'apply':
        apply()
    else:
        sys.exit(__doc__)
