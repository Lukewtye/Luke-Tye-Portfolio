## Luke-Tye-Portfolio

The source for luketye.dev. One self-contained `index.html`, no build step and no dependencies.

Fonts are inlined as base64 woff2 and every graphic is inline SVG, so the page makes no external requests and the repo carries no asset directory.

## Hosting

Served from a Raspberry Pi on a home network rather than a static host.

nginx runs in a container bound to 127.0.0.1:8081. A Cloudflare Tunnel is the only ingress: no ports are forwarded, and the origin is unreachable from the LAN and from the tailnet. DNS and TLS terminate at Cloudflare, so the nameservers are there while the registrar stays at Name.com.

## Deployment

Manual. `update-portfolio.sh` runs on the Pi: fetch origin, hard reset to origin/main, then copy index.html into the webroot by writing a temporary file and renaming it, so a reader never sees a half-written page.

The webroot holds index.html and nothing else.

## What it does not do

No CI, so have to push to git then run the script on pi to push changes live. 

No uptime monitoring (yet)

Status bar is not live with status updates from the pi (yet)

## Status

Live at https://luketye.dev. Automated deployment is the next thing to build.
