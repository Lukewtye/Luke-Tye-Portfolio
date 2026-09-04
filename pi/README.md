# Pi-side pieces for the header status strip

The strip at the top of the site reads `/status.json`, which a systemd timer on
the Pi rewrites once a minute. These files are the Pi half of that. They are not
deployed by `update-portfolio.sh`, which copies only `index.html`; install them
by hand.

| File | Installs to | Notes |
| --- | --- | --- |
| `pi-status.sh` | `~/sites/pi-status.sh` | mode 755 |
| `pi-status.service` | `~/.config/systemd/user/` | user unit, no sudo |
| `pi-status.timer` | `~/.config/systemd/user/` | 60s interval |
| `portfolio.conf` | `~/sites/portfolio.conf` | needs a container restart |
| `run-portfolio.sh` | `~/sites/run-portfolio.sh` | recreates the nginx container |

Install:

```sh
# install(1) sets the mode in the same step as the copy, so the temp file is
# never briefly world-writable.
install -m 755 pi-status.sh      ~/sites/pi-status.sh
install -m 644 pi-status.service ~/.config/systemd/user/pi-status.service
install -m 644 pi-status.timer   ~/.config/systemd/user/pi-status.timer
systemctl --user daemon-reload
systemctl --user enable --now pi-status.timer
```

Applying a change to `portfolio.conf` means recreating the container, because
the config is a read-only bind mount that nginx reads only at start:

```sh
# DESTRUCTIVE: removes and recreates the running container. The site is down
# for roughly a second. Nothing persistent is lost -- the webroot is a host
# directory, not container state. The image pull runs first, so a bad tag
# aborts before anything is removed.
~/sites/run-portfolio.sh
```

## Notes

- **Pacific is pinned inside `pi-status.sh`.** It does not read the system
  timezone, so changing the Pi's own timezone does not change this output.
- **The image tag is pinned.** `nginx:alpine` resolves at pull time and is not
  evidence of currency; the previous image was built 2026-07-15 and had drifted
  a mainline release behind.
- **What gets published is a positive allowlist**: uptime in whole days, 1-minute
  load, SoC temperature, and a timestamp. No hostname, IP, kernel version,
  container name, or tailnet address. Adding a field is a deliberate decision.
- **The page reads the `generated` field, not the fetch's success**, so a cached
  copy still renders as stale. That is what makes edge caching safe here.
