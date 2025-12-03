# Security Growler

<img src="https://pirate.github.io/security-growler/alert.png" height="20px"/> [![Github Stars](https://img.shields.io/github/stars/pirate/security-growler.svg)](https://github.com/pirate/security-growler)

A lightweight [xbar](https://xbarapp.com/) plugin for macOS that monitors security events and sends notifications. Detects SSH logins, sudo commands, port scans, VNC connections, and network activity on configurable ports.

<img src="http://pirate.github.io/security-growler/screenshots/portscan_event.PNG" width="45%"/>
<img src="http://pirate.github.io/security-growler/screenshots/vnc_event.PNG" width="45%"/>

## Features

- **SSH Monitoring**: Alerts on successful and failed SSH login attempts
- **Sudo Tracking**: Notifications when sudo commands are executed
- **Port Scan Detection**: Detects incoming port scans (nmap-style)
- **VNC Connections**: High-priority alerts for remote desktop connections
- **Network Ports**: Monitor connections on FTP, SMB, AFP, MySQL, PostgreSQL, iTunes Sharing, and custom ports
- **FTP Access**: Track FTP daemon activity
- **Native Notifications**: Uses [desktop-notifier](https://github.com/samschott/desktop-notifier) for rich macOS notifications with fallback to osascript

## Requirements

- macOS 10.15+ (Catalina or later) - uses unified logging system
- [xbar](https://xbarapp.com/) (formerly BitBar)
- Python 3.8+
- `desktop-notifier` (recommended, for rich notifications): `pip3 install desktop-notifier`

## Installation

### Quick Install

1. Install [xbar](https://xbarapp.com/) if you haven't already
2. Install the notification library:
   ```bash
   pip3 install desktop-notifier
   ```
3. Copy `security-growler.30s.py` to your xbar plugins folder:
   ```bash
   cp security-growler.30s.py ~/Library/Application\ Support/xbar/plugins/
   chmod +x ~/Library/Application\ Support/xbar/plugins/security-growler.30s.py
   ```
4. Refresh xbar or click the xbar icon and select "Refresh all"

### Manual Install

1. Download `security-growler.30s.py` from this repository
2. Move it to `~/Library/Application Support/xbar/plugins/`
3. Make it executable: `chmod +x security-growler.30s.py`
4. Refresh xbar

## Configuration

Configuration is done through xbar's plugin variables. Click on the plugin in xbar, then go to the xbar app preferences to modify these settings:

| Variable | Default | Description |
|----------|---------|-------------|
| `SHOW_NOTIFICATIONS` | `true` | Enable/disable macOS notifications |
| `MONITOR_SSH` | `true` | Monitor SSH login events |
| `MONITOR_SUDO` | `true` | Monitor sudo command usage |
| `MONITOR_PORTSCAN` | `true` | Detect incoming port scans |
| `MONITOR_VNC` | `true` | Monitor VNC (port 5900) connections |
| `MONITOR_PORTS` | `true` | Monitor network connections on specified ports |
| `MONITORED_PORTS` | `21,445,548,3306,3689,5432` | Comma-separated list of ports to monitor |

### Monitored Ports

Default ports monitored:
- **21**: FTP
- **445**: SMB (Windows file sharing)
- **548**: AFP (Apple file sharing)
- **3306**: MySQL
- **3689**: iTunes Sharing
- **5432**: PostgreSQL
- **5900**: VNC (always monitored separately as high-priority)

## How It Works

Security Growler uses the macOS **unified logging system** (`/usr/bin/log`) to query security-relevant events. This is the modern approach that works on macOS Catalina and later, replacing the deprecated `/var/log/system.log` file.

The plugin:
1. Queries the unified log for SSH, sudo, port scan, and FTP events
2. Monitors network connections using `lsof` for configured ports
3. Tracks seen events to avoid duplicate notifications
4. Outputs a menu showing recent events and monitoring status
5. Sends native macOS notifications for new security events

### Event Persistence

State is stored in `~/Library/Application Support/SecurityGrowler/state.json` to track:
- Previously seen log events (prevents duplicate alerts)
- Known network connections (alerts only on new connections)
- Recent event history (shown in the menu)

Logs are written to `~/Library/Logs/SecurityGrowler.log`.

## Responding to Alerts

| Alert Type | Recommended Action |
|------------|-------------------|
| SSH Connection | Check `System Preferences > Sharing > Remote Login`. Review with `w` command. |
| VNC Connection | Check `System Preferences > Sharing > Screen Sharing`. |
| Port Scan | Enable firewall stealth mode: `sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setstealthmode on` |
| Sudo Command | Review with `last` and check Activity Monitor for unexpected processes |
| Port Connection | Ensure the service (MySQL, PostgreSQL, etc.) is properly secured with authentication |

## Troubleshooting

### No events appearing?

1. **Check unified log access**: The unified log may require specific entitlements. Run manually to test:
   ```bash
   /usr/bin/log show --predicate 'process == "sshd"' --last 5m
   ```

2. **Refresh the plugin**: Click the shield icon and select "Refresh Now"

3. **Check for Python errors**: Look at the plugin output for error messages

### Notifications not working?

1. Install desktop-notifier: `pip3 install desktop-notifier`
2. Check System Preferences > Notifications > Script Editor (or Terminal) permissions
3. The fallback uses osascript which should work without additional setup

### Plugin not appearing in xbar?

1. Ensure the file is executable: `chmod +x security-growler.30s.py`
2. Check the file is in the correct location
3. Verify Python 3 is available: `which python3`

## Related Tools

- [Lulu](https://objective-see.com/products/lulu.html) - Free, open-source firewall
- [Little Snitch](https://www.obdev.at/products/littlesnitch/index.html) - Comprehensive firewall solution
- [KnockKnock](https://objective-see.com/products/knockknock.html) - Detect persistent malware

## License

MIT License - See source file for full license text.

Copyright (c) Nick Sweeting

Permission is hereby granted, free of charge, to any person obtaining a copy of this software to deal in the Software without restriction, including the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies.
