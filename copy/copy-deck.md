# Copy deck

Rewrite the text under each `## [id]` heading, in your own voice.
Leave the ids alone. Do not reorder or delete blocks.
Inline markup inside a block is part of the text -- keep it if you want it.

Then run:  `python3 copy/copy-deck.py apply`

---

## [header.wordmark]
<!-- site wordmark | currently 2 words -->

Luke Tye

## [about.eyebrow]
<!-- small mono label above the heading | currently 1 words -->

about

## [about.h1]
<!-- the page-opening statement | currently 13 words -->

I build the systems, then I build the software that runs on them.

## [about.thesis]
<!-- the opening paragraph -- who you are and what this site is | currently 67 words -->

I'm a second-year CS student at Oregon State — one intro Python course down, CS 162 this fall. The next section came from the other direction: a Raspberry Pi 5 I administer myself, an MCP server I wrote for it, and a scraper that's been running since June. This site is that gap in the open — what shipped, what broke, and the bug I never root-caused.

## [projects.eyebrow]
<!-- small mono label above the heading | currently 1 words -->

projects

## [projects.h2]
<!-- section heading | currently 3 words -->

What's actually running.

## [projects.projname]
<!-- project name | currently 1 words -->

pi-mcp

## [projects.para]
<!-- body paragraph | currently 51 words -->

A Model Context Protocol server that hands an assistant three tools against my own hardware: a read-only health snapshot, a shell exec with a clamped timeout and capped output, and a Docker container restart. 273 lines of Python, two transports, two execution modes, behind a bearer token and a tailnet-only bind.

## [projects.note]
<!-- margin note -- the specific bug or detail behind the project | currently 27 words -->

This is also the tool that let Claude check the Pi's real uptime and load while we built this page — the numbers above came from it.

## [projects.projname2]
<!-- project name | currently 2 words -->

Price monitor

## [projects.para2]
<!-- body paragraph | currently 48 words -->

Eleven products across Amazon and Uniqlo, scraped straight from the page — no vendor API — and checked three times a day. Request, extract, parse the price, compare, then a Slack alert and a row written to Notion. Roughly 1,100 scrape-and-parse runs since it went up in June.

## [projects.note2]
<!-- margin note -- the specific bug or detail behind the project | currently 38 words -->

It ran for weeks firing nothing. I assumed Amazon was blocking me — the execution log showed prices arriving fine. One trailing space outside a <span class="mono">{{ }}</span> made n8n read the condition as text instead of evaluating it.

## [projects.projname3]
<!-- project name | currently 1 words -->

Homelab

## [projects.para3]
<!-- body paragraph | currently 49 words -->

One Raspberry Pi 5 running Raspberry Pi OS. No hypervisor, no rack. Docker for the services, systemd user units with linger for anything that has to survive a reboot, Tailscale for access and TLS. It isn't a project so much as the thing both projects above are deployed on.

## [projects.note3]
<!-- margin note -- the specific bug or detail behind the project | currently 28 words -->

The uptime monitor sits on a Docker bridge; pi-mcp binds loopback. No container-side address reaches that socket, so the check had to push out rather than poll in.

## [skills.eyebrow]
<!-- small mono label above the heading | currently 1 words -->

skills

## [skills.h2]
<!-- section heading | currently 4 words -->

What I reach for.

## [skills.para]
<!-- body paragraph | currently 36 words -->

Everything on this wall is something I've shipped with or broken and fixed — nothing aspirational. Two honest asterisks: Java is AP coursework I haven't touched since, and my JavaScript lives entirely inside n8n code nodes.

## [path.eyebrow]
<!-- small mono label above the heading | currently 4 words -->

path — summer 2026

## [path.h2]
<!-- section heading | currently 13 words -->

Two of these shipped. The one you're reading is the one that's late.

## [path.para]
<!-- body paragraph | currently 31 words -->

The summer plan, tracked in the open — including the dates I missed. This site was supposed to be answering on a real domain by July 26. It's still a mockup.

## [path.phase]
<!-- roadmap item | currently 4 words -->

pi-mcp on the Pi

## [path.phase2]
<!-- roadmap item | currently 2 words -->

Price monitor

## [path.phase3]
<!-- roadmap item | currently 7 words -->

This site, live on its own domain

## [path.phase4]
<!-- roadmap item | currently 4 words -->

Résumé + repo cleanup

## [path.phase5]
<!-- roadmap item | currently 3 words -->

Summer 2027 applications

## [writing.eyebrow]
<!-- small mono label above the heading | currently 1 words -->

writing

## [writing.h2]
<!-- section heading | currently 6 words -->

The two bugs worth writing up.

## [writing.writeup]
<!-- planned write-up title | currently 9 words -->

The 421 that only happened over the public URL

## [writing.writeup2]
<!-- planned write-up title | currently 9 words -->

A trailing space that made every price check false

## [contact.eyebrow]
<!-- small mono label above the heading | currently 1 words -->

contact

## [contact.h2]
<!-- section heading | currently 2 words -->

Let's talk.

## [contact.para]
<!-- body paragraph | currently 42 words -->

Email's fastest if you actually want a reply — I check it more than GitHub notifications. GitHub is where the receipts are: pi-mcp and the price-monitor workflow are both public. The résumé link goes up when there's a résumé worth linking to.

## [contact.pending]
<!-- placeholder link label | currently 4 words -->

résumé — not yet
