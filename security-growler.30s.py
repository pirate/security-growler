#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Security Growler - xbar Plugin for macOS Security Monitoring

Monitors security events on macOS including SSH logins, sudo commands,
port scans, network connections, and more using the unified logging system.

<xbar.title>Security Growler</xbar.title>
<xbar.version>v2.0.0</xbar.version>
<xbar.author>Nick Sweeting</xbar.author>
<xbar.author.github>pirate</xbar.author.github>
<xbar.desc>Monitor security events on macOS: SSH, sudo, port scans, VNC, and network connections</xbar.desc>
<xbar.dependencies>python3,desktop-notifier</xbar.dependencies>
<xbar.abouturl>https://github.com/pirate/security-growler</xbar.abouturl>
<xbar.var>boolean(SHOW_NOTIFICATIONS=true): Show macOS notifications for alerts</xbar.var>
<xbar.var>boolean(MONITOR_SSH=true): Monitor SSH login events</xbar.var>
<xbar.var>boolean(MONITOR_SUDO=true): Monitor sudo command usage</xbar.var>
<xbar.var>boolean(MONITOR_PORTSCAN=true): Monitor for incoming port scans</xbar.var>
<xbar.var>boolean(MONITOR_VNC=true): Monitor VNC connections</xbar.var>
<xbar.var>boolean(MONITOR_PORTS=true): Monitor network port connections</xbar.var>
<xbar.var>string(MONITORED_PORTS="21,445,548,3306,3689,5432"): Comma-separated ports to monitor</xbar.var>
<xbar.var>boolean(MONITOR_LISTENING=true): Monitor new listening ports (21-9999)</xbar.var>
<xbar.var>boolean(MONITOR_DOTENV=true): Monitor new .env files in home directory</xbar.var>
<xbar.var>boolean(MONITOR_DANGEROUS_COMMANDS=true): Monitor npx, uvx, op commands</xbar.var>
<xbar.var>boolean(MONITOR_DNS=true): Monitor DNS resolver changes</xbar.var>
<xbar.var>boolean(MONITOR_PUBLIC_IP=true): Monitor public IP address changes</xbar.var>
<xbar.var>boolean(MONITOR_LOCAL_IP=true): Monitor local IP address changes</xbar.var>
<xbar.var>boolean(MONITOR_MDM=true): Monitor Kandji/MDM events</xbar.var>
"""

import os
import sys
import json
import asyncio
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Any

# Try to import desktop-notifier for rich notifications
try:
    from desktop_notifier import DesktopNotifier, Urgency, DEFAULT_SOUND
    DESKTOP_NOTIFIER_AVAILABLE = True
except ImportError:
    DESKTOP_NOTIFIER_AVAILABLE = False

# Configuration
APP_NAME = "Security Growler"
STATE_DIR = Path.home() / "Library" / "Application Support" / "SecurityGrowler"
STATE_FILE = STATE_DIR / "state.json"
LOG_FILE = Path.home() / "Library" / "Logs" / "SecurityGrowler.log"
MAX_EVENTS = 50
MAX_LOG_LINES = 1000

# Environment variable configuration (set by xbar)
SHOW_NOTIFICATIONS = os.environ.get("SHOW_NOTIFICATIONS", "true").lower() == "true"
MONITOR_SSH = os.environ.get("MONITOR_SSH", "true").lower() == "true"
MONITOR_SUDO = os.environ.get("MONITOR_SUDO", "true").lower() == "true"
MONITOR_PORTSCAN = os.environ.get("MONITOR_PORTSCAN", "true").lower() == "true"
MONITOR_VNC = os.environ.get("MONITOR_VNC", "true").lower() == "true"
MONITOR_PORTS = os.environ.get("MONITOR_PORTS", "true").lower() == "true"
MONITORED_PORTS = os.environ.get("MONITORED_PORTS", "21,445,548,3306,3689,5432")
MONITOR_LISTENING = os.environ.get("MONITOR_LISTENING", "true").lower() == "true"
MONITOR_DOTENV = os.environ.get("MONITOR_DOTENV", "true").lower() == "true"
MONITOR_DANGEROUS_COMMANDS = os.environ.get("MONITOR_DANGEROUS_COMMANDS", "true").lower() == "true"
MONITOR_DNS = os.environ.get("MONITOR_DNS", "true").lower() == "true"
MONITOR_PUBLIC_IP = os.environ.get("MONITOR_PUBLIC_IP", "true").lower() == "true"
MONITOR_LOCAL_IP = os.environ.get("MONITOR_LOCAL_IP", "true").lower() == "true"
MONITOR_MDM = os.environ.get("MONITOR_MDM", "true").lower() == "true"

# Listening port range to monitor
LISTENING_PORT_MIN = 21
LISTENING_PORT_MAX = 9999

# Dangerous commands to monitor
DANGEROUS_COMMANDS = ["npx", "uvx", "op"]

# Parse monitored ports
PORTS_TO_MONITOR = [int(p.strip()) for p in MONITORED_PORTS.split(",") if p.strip().isdigit()]

# Port names for display
PORT_NAMES = {
    21: "FTP",
    22: "SSH",
    445: "SMB",
    548: "AFP",
    3306: "MySQL",
    3689: "iTunes",
    5432: "PostgreSQL",
    5900: "VNC",
}

# Icons (base64 encoded for xbar)
# Shield icon for menubar
MENUBAR_ICON = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAADfSURBVDiNpZMxDoJAEEXfLhYWxsLCeLDtiIW9J/AAnoBb2HgDGwsv4A1sPIEHcAtja2VhYRxZd8YGWBDFn0wymZ3J/2+yM4qqEhIppyBJEtfKsuy7JwBEpANcAlfAHdD7AZ4DR+BaVV/D2QaQAg/ADXCuqrvvgD5wAfSADtB2zm2IyE5VJwFQVaKqTIAB0AFOVLUTxVH0DtAE9oB9YNc51wwFqCrrpkMRGQI14EBE2kALeP4JiIhI3Tl3EcVxPI7j+BlYB46Bs+/JC4BIYV+qapymaT+Koughjp9efQHoZ2F1jT7xOQAAAABJRU5ErkJggg=="

# Alert icon
ALERT_ICON = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAC0SURBVDiNY2AYBVQDjPgk//37x8DEyPAfH5uhQEBAIPTfv38f/v37x4CPDReMjIz/GRgYnmNTy4IuANOIzwv4xBkZGRlBXkBRy8jI+B+bGLIYTBwGmHAJwgC6l5CdCwMMDAz/GXB4AesLDAz/YHJE+oCBgQEyVhkYGP6DDIV5gYEB4gNUQJQXkBWCACM+SRYYgYGB4QMxlhNygpGR8T+MjRcQDBWcYYuNjeU/ExNTKDZxfGIMDADcxjhf0SF9tQAAAABJRU5ErkJggg=="


# =============================================================================
# State Management
# =============================================================================

def load_state() -> Dict[str, Any]:
    """Load persisted state from disk."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {
        "last_check": None,
        "seen_events": [],
        "known_connections": {},
        "events": [],
    }


def save_state(state: Dict[str, Any]) -> None:
    """Save state to disk."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    # Trim events to prevent unbounded growth
    state["events"] = state["events"][-MAX_EVENTS:]
    state["seen_events"] = state["seen_events"][-500:]
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, default=str)


def log_event(event_type: str, title: str, body: str) -> None:
    """Append event to log file."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%m/%d %H:%M")
    prefix = "!!" if event_type == "alert" else ">>"
    line = f"[{timestamp}] {prefix} {title}: {body}\n"

    # Append to log, but keep it trimmed
    try:
        existing = LOG_FILE.read_text().splitlines() if LOG_FILE.exists() else []
        existing.append(line.strip())
        LOG_FILE.write_text("\n".join(existing[-MAX_LOG_LINES:]) + "\n")
    except IOError:
        pass


# =============================================================================
# Notifications
# =============================================================================

# Global notifier instance (initialized lazily)
_notifier: Optional["DesktopNotifier"] = None


def _get_notifier() -> Optional["DesktopNotifier"]:
    """Get or create the desktop notifier instance."""
    global _notifier
    if DESKTOP_NOTIFIER_AVAILABLE and _notifier is None:
        _notifier = DesktopNotifier(
            app_name=APP_NAME,
            notification_limit=10,
        )
    return _notifier


async def _send_notification_async(title: str, message: str, is_alert: bool = False) -> None:
    """Send notification using desktop-notifier (async)."""
    notifier = _get_notifier()
    if notifier is None:
        return

    try:
        await notifier.send(
            title=title,
            message=message,
            urgency=Urgency.Critical if is_alert else Urgency.Normal,
            sound=DEFAULT_SOUND if is_alert else None,
        )
    except Exception:
        pass


def _send_notification_osascript(title: str, message: str, is_alert: bool = False) -> None:
    """Fallback: Send a macOS notification using osascript."""
    # Escape quotes for AppleScript
    title_escaped = title.replace('"', '\\"').replace("'", "\\'")
    message_escaped = message.replace('"', '\\"').replace("'", "\\'")

    sound = 'sound name "Sosumi"' if is_alert else ""
    script = f'''
    display notification "{message_escaped}" with title "{APP_NAME}" subtitle "{title_escaped}" {sound}
    '''

    try:
        subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            timeout=5
        )
    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        pass


def send_notification(title: str, message: str, is_alert: bool = False) -> None:
    """Send a macOS notification using desktop-notifier or fallback to osascript."""
    if not SHOW_NOTIFICATIONS:
        return

    if DESKTOP_NOTIFIER_AVAILABLE:
        try:
            asyncio.run(_send_notification_async(title, message, is_alert))
        except Exception:
            # Fallback to osascript if async fails
            _send_notification_osascript(title, message, is_alert)
    else:
        _send_notification_osascript(title, message, is_alert)


# =============================================================================
# Unified Log Reader
# =============================================================================

def get_log_entries(predicate: str, since_minutes: int = 1) -> List[Dict[str, str]]:
    """
    Query the macOS unified logging system using /usr/bin/log.

    Args:
        predicate: Log predicate filter string
        since_minutes: How many minutes back to query

    Returns:
        List of log entries as dictionaries
    """
    # Calculate start time
    start_time = (datetime.now() - timedelta(minutes=since_minutes)).strftime("%Y-%m-%d %H:%M:%S")

    cmd = [
        "/usr/bin/log", "show",
        "--predicate", predicate,
        "--start", start_time,
        "--style", "json",
        "--info",
        "--debug",
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            return []

        # Parse JSON output
        output = result.stdout.strip()
        if not output:
            return []

        # The log command outputs JSON array
        try:
            entries = json.loads(output)
            return entries if isinstance(entries, list) else []
        except json.JSONDecodeError:
            # Sometimes output is line-delimited JSON
            entries = []
            for line in output.splitlines():
                line = line.strip()
                if line.startswith("{"):
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
            return entries

    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        return []


# =============================================================================
# SSH Parser
# =============================================================================

def parse_ssh_events(state: Dict[str, Any]) -> List[Tuple[str, str, str]]:
    """Parse SSH events from unified log."""
    if not MONITOR_SSH:
        return []

    events = []

    # Query for sshd events
    predicate = '(process == "sshd") AND (eventMessage CONTAINS "Accepted" OR eventMessage CONTAINS "Failed" OR eventMessage CONTAINS "error")'

    entries = get_log_entries(predicate)

    for entry in entries:
        event_id = entry.get("eventID", entry.get("traceID", str(entry)))
        if event_id in state["seen_events"]:
            continue

        message = entry.get("eventMessage", "")
        timestamp = entry.get("timestamp", "")

        if "Accepted publickey" in message or "Accepted keyboard" in message:
            # Successful login
            user = ""
            src = ""
            if " for " in message:
                user = message.split(" for ", 1)[-1].split(" ", 1)[0]
            if " from " in message:
                src = message.split(" from ", 1)[-1].split(" ", 1)[0]

            method = "Public Key" if "publickey" in message else "Password"
            title = f"SSH LOGIN: {user}"
            body = f"from {src} via {method}"
            events.append(("alert", title, body))
            state["seen_events"].append(event_id)

        elif "Failed" in message or "error" in message.lower():
            # Failed attempt or error
            user = ""
            src = ""
            if " for " in message:
                user = message.split(" for ", 1)[-1].split(" ", 1)[0]
            if " from " in message:
                src = message.split(" from ", 1)[-1].split(" ", 1)[0]
            elif " by " in message:
                src = message.split(" by ", 1)[-1].split(" ", 1)[0]

            summary = message[:50] + "..." if len(message) > 50 else message
            title = f"SSH EVENT: {user or 'unknown'}"
            body = f"from {src}: {summary}"
            events.append(("alert", title, body))
            state["seen_events"].append(event_id)

    return events


# =============================================================================
# Sudo Parser
# =============================================================================

def parse_sudo_events(state: Dict[str, Any]) -> List[Tuple[str, str, str]]:
    """Parse sudo events from unified log."""
    if not MONITOR_SUDO:
        return []

    events = []

    # Query for sudo events
    predicate = '(process == "sudo") AND (eventMessage CONTAINS "COMMAND")'

    entries = get_log_entries(predicate)

    # Exclusion patterns to prevent self-monitoring loops
    exclude_patterns = ["/usr/sbin/lsof", "/usr/bin/log show", "security-growler"]

    for entry in entries:
        event_id = entry.get("eventID", entry.get("traceID", str(entry)))
        if event_id in state["seen_events"]:
            continue

        message = entry.get("eventMessage", "")

        # Skip self-monitoring commands
        if any(pattern in message for pattern in exclude_patterns):
            continue

        # Parse sudo log format:
        # user : TTY=ttys001 ; PWD=/Users/user ; USER=root ; COMMAND=/usr/bin/whoami
        try:
            if " ; " in message:
                parts = message.split(" ; ")
                user_part = parts[0] if parts else ""
                user = user_part.split(":")[-1].strip().split()[-1] if user_part else "unknown"

                tty = ""
                pwd = ""
                command = ""

                for part in parts:
                    if "TTY=" in part:
                        tty = part.split("TTY=", 1)[-1].strip()
                    elif "PWD=" in part:
                        pwd = part.split("PWD=", 1)[-1].strip()
                    elif "COMMAND=" in part:
                        command = part.split("COMMAND=", 1)[-1].strip()

                if command:
                    title = f"SUDO: {user}"
                    # Truncate long commands
                    cmd_display = command[:60] + "..." if len(command) > 60 else command
                    body = f"{cmd_display}"
                    events.append(("alert", title, body))
                    state["seen_events"].append(event_id)
        except (IndexError, ValueError):
            continue

    return events


# =============================================================================
# Port Scan Parser
# =============================================================================

def parse_portscan_events(state: Dict[str, Any]) -> List[Tuple[str, str, str]]:
    """Parse port scan detection events from unified log."""
    if not MONITOR_PORTSCAN:
        return []

    events = []

    # Query for kernel port scan detection messages
    predicate = '(process == "kernel") AND (eventMessage CONTAINS "Limiting closed port RST")'

    entries = get_log_entries(predicate)

    for entry in entries:
        event_id = entry.get("eventID", entry.get("traceID", str(entry)))
        if event_id in state["seen_events"]:
            continue

        message = entry.get("eventMessage", "")

        if "Limiting closed port RST response" in message:
            # Extract rate limit info
            rate_info = message.split("response ", 1)[-1] if "response " in message else message
            title = "PORT SCAN DETECTED"
            body = f"Limiting {rate_info}"
            events.append(("alert", title, body))
            state["seen_events"].append(event_id)

    return events


# =============================================================================
# FTP Parser
# =============================================================================

def parse_ftp_events(state: Dict[str, Any]) -> List[Tuple[str, str, str]]:
    """Parse FTP events from unified log."""
    events = []

    # Query for ftpd events
    predicate = '(process == "ftpd")'

    entries = get_log_entries(predicate)

    for entry in entries:
        event_id = entry.get("eventID", entry.get("traceID", str(entry)))
        if event_id in state["seen_events"]:
            continue

        message = entry.get("eventMessage", "")

        if message:
            title = "FTP Access"
            body = message[:80] + "..." if len(message) > 80 else message
            events.append(("notify", title, body))
            state["seen_events"].append(event_id)

    return events


# =============================================================================
# Network Connection Monitor
# =============================================================================

def get_port_connections(port: int) -> List[Dict[str, str]]:
    """Get current connections on a specific port using lsof."""
    cmd = f"lsof +c 0 -i:{port} 2>/dev/null | grep -v '^COMMAND' | grep -v '^launchd '"

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )

        connections = []
        for line in result.stdout.strip().splitlines():
            parts = line.split()
            if len(parts) >= 9:
                # Parse lsof output
                # PROCESS PID USER FD TYPE DEVICE SIZE/OFF NODE NAME
                conn = {
                    "process": parts[0],
                    "pid": parts[1],
                    "user": parts[2],
                    "name": parts[-1] if len(parts) > 8 else "",
                    "port": port,
                }

                # Parse connection details from NAME field
                name = parts[-1] if parts else ""
                if "->" in name:
                    local, remote = name.split("->", 1)
                    conn["local"] = local
                    conn["remote"] = remote
                else:
                    conn["local"] = name
                    conn["remote"] = ""

                connections.append(conn)

        return connections

    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        return []


def parse_port_events(state: Dict[str, Any]) -> List[Tuple[str, str, str]]:
    """Monitor network connections on configured ports."""
    if not MONITOR_PORTS:
        return []

    events = []
    known = state.get("known_connections", {})

    for port in PORTS_TO_MONITOR:
        port_key = str(port)
        connections = get_port_connections(port)

        # Create connection identifiers
        current_conns = set()
        for conn in connections:
            conn_id = f"{conn['process']}:{conn['pid']}:{conn.get('remote', '')}"
            current_conns.add(conn_id)

            # Check if this is a new connection
            if port_key not in known:
                known[port_key] = []

            if conn_id not in known[port_key]:
                known[port_key].append(conn_id)

                port_name = PORT_NAMES.get(port, str(port))
                title = f"PORT {port} ({port_name})"
                body = f"{conn['user']} {conn['process']} (PID {conn['pid']})"
                if conn.get("remote"):
                    body += f" <- {conn['remote']}"

                events.append(("notify", title, body))

        # Clean up old connections
        if port_key in known:
            known[port_key] = [c for c in known[port_key] if c in current_conns]

    state["known_connections"] = known
    return events


def parse_vnc_events(state: Dict[str, Any]) -> List[Tuple[str, str, str]]:
    """Monitor VNC connections specifically (elevated to alert level)."""
    if not MONITOR_VNC:
        return []

    events = []
    known = state.get("known_connections", {})
    port = 5900
    port_key = "vnc_5900"

    connections = get_port_connections(port)

    current_conns = set()
    for conn in connections:
        conn_id = f"{conn['process']}:{conn['pid']}:{conn.get('remote', '')}"
        current_conns.add(conn_id)

        if port_key not in known:
            known[port_key] = []

        if conn_id not in known[port_key]:
            known[port_key].append(conn_id)

            title = "VNC CONNECTION"
            body = f"{conn['user']} {conn['process']} (PID {conn['pid']})"
            if conn.get("remote"):
                body += f" from {conn['remote']}"

            # VNC connections are alerts, not just notifications
            events.append(("alert", title, body))

    # Clean up old connections
    if port_key in known:
        known[port_key] = [c for c in known[port_key] if c in current_conns]

    state["known_connections"] = known
    return events


# =============================================================================
# New Listening Ports Monitor
# =============================================================================

def get_listening_ports() -> Dict[int, Dict[str, str]]:
    """Get all listening ports and their processes using lsof."""
    cmd = "lsof -i -P -n 2>/dev/null | grep LISTEN"

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=15
        )

        listening = {}
        for line in result.stdout.strip().splitlines():
            parts = line.split()
            if len(parts) >= 9:
                process = parts[0]
                pid = parts[1]
                user = parts[2]
                name = parts[-2] if parts[-1] == "(LISTEN)" else parts[-1]

                # Extract port from name (e.g., "*:8080" or "127.0.0.1:3000")
                if ":" in name:
                    port_str = name.rsplit(":", 1)[-1]
                    try:
                        port = int(port_str)
                        if LISTENING_PORT_MIN < port < LISTENING_PORT_MAX:
                            listening[port] = {
                                "process": process,
                                "pid": pid,
                                "user": user,
                                "address": name,
                            }
                    except ValueError:
                        continue

        return listening

    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        return {}


def parse_listening_port_events(state: Dict[str, Any]) -> List[Tuple[str, str, str]]:
    """Monitor for new listening ports."""
    if not MONITOR_LISTENING:
        return []

    events = []
    known_listening = set(state.get("known_listening_ports", []))
    current_listening = get_listening_ports()

    for port, info in current_listening.items():
        if port not in known_listening:
            title = f"NEW LISTENING PORT: {port}"
            body = f"{info['user']} {info['process']} (PID {info['pid']}) on {info['address']}"
            events.append(("alert", title, body))

    # Update known listening ports
    state["known_listening_ports"] = list(current_listening.keys())
    return events


# =============================================================================
# .env File Monitor (using find)
# =============================================================================

def find_recent_dotenv_files() -> List[str]:
    """Find .env files modified in the last 2 minutes using find, excluding ~/Library."""
    home = str(Path.home())

    # Use find to locate .env files modified in last 2 minutes
    # -mmin -2 means modified within last 2 minutes
    # -name matches both .env and *.env files
    # -not -path excludes ~/Library
    # -type f ensures we only get files
    cmd = f'''find "{home}" -maxdepth 6 -type f \\( -name ".env" -o -name "*.env" \\) -mmin -2 -not -path "*/Library/*" -not -path "*/.git/*" -not -path "*/node_modules/*" 2>/dev/null'''

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=15
        )

        files = []
        for line in result.stdout.strip().splitlines():
            path = line.strip()
            if path:
                files.append(path)

        return files

    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        return []


def parse_dotenv_events(state: Dict[str, Any]) -> List[Tuple[str, str, str]]:
    """Monitor for new .env files in home directory."""
    if not MONITOR_DOTENV:
        return []

    events = []
    known_dotenv = set(state.get("known_dotenv_files", []))
    current_dotenv = find_recent_dotenv_files()

    for filepath in current_dotenv:
        if filepath not in known_dotenv:
            # Get relative path from home
            try:
                rel_path = str(Path(filepath).relative_to(Path.home()))
            except ValueError:
                rel_path = filepath

            title = "NEW .ENV FILE"
            body = f"~/{rel_path}"
            events.append(("alert", title, body))
            known_dotenv.add(filepath)

    state["known_dotenv_files"] = list(known_dotenv)
    return events


# =============================================================================
# Dangerous Commands Monitor (npx, uvx, op) - uses shell history + ps polling
# =============================================================================

def get_shell_history_commands() -> List[Dict[str, str]]:
    """
    Read recent commands from shell history files.
    Works with zsh, bash, and fish shells.
    """
    home = Path.home()
    commands = []

    # Shell history file locations and their formats
    history_files = [
        (home / ".zsh_history", "zsh"),
        (home / ".bash_history", "bash"),
        (home / ".local/share/fish/fish_history", "fish"),
    ]

    for hist_file, shell_type in history_files:
        if not hist_file.exists():
            continue

        try:
            # Read last 50 lines of history (recent commands)
            with open(hist_file, "rb") as f:
                # Seek to end and read backwards to get recent lines
                try:
                    f.seek(0, 2)  # End of file
                    size = f.tell()
                    # Read last 8KB or whole file if smaller
                    read_size = min(8192, size)
                    f.seek(max(0, size - read_size))
                    content = f.read().decode("utf-8", errors="ignore")
                except Exception:
                    continue

            lines = content.splitlines()[-50:]  # Last 50 commands

            for line in lines:
                # Parse based on shell type
                cmd = ""
                if shell_type == "zsh":
                    # zsh format: ": timestamp:0;command" or just "command"
                    if line.startswith(":"):
                        parts = line.split(";", 1)
                        if len(parts) > 1:
                            cmd = parts[1]
                    else:
                        cmd = line
                elif shell_type == "bash":
                    cmd = line
                elif shell_type == "fish":
                    # fish format: "- cmd: command"
                    if line.startswith("- cmd:"):
                        cmd = line[6:].strip()

                cmd = cmd.strip()
                if not cmd:
                    continue

                # Check if command starts with or contains dangerous commands
                cmd_lower = cmd.lower()
                cmd_parts = cmd.split()

                for dangerous_cmd in DANGEROUS_COMMANDS:
                    # Check if it's the command itself or run via path
                    first_word = cmd_parts[0].lower() if cmd_parts else ""
                    if (first_word == dangerous_cmd or
                        first_word.endswith(f"/{dangerous_cmd}") or
                        cmd_lower.startswith(f"{dangerous_cmd} ")):
                        commands.append({
                            "command": dangerous_cmd,
                            "full_cmd": cmd[:100],
                            "shell": shell_type,
                            "source": "history",
                        })
                        break

        except (IOError, OSError):
            continue

    return commands


def get_running_dangerous_commands() -> List[Dict[str, str]]:
    """Find running instances of dangerous commands using ps."""
    cmd = "ps -eo pid,user,comm,args 2>/dev/null"

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=5
        )

        processes = []
        for line in result.stdout.strip().splitlines()[1:]:  # Skip header
            parts = line.split(None, 3)
            if len(parts) >= 3:
                pid = parts[0]
                user = parts[1]
                comm = parts[2]
                args = parts[3] if len(parts) > 3 else comm

                comm_lower = comm.lower()
                args_lower = args.lower()

                for dangerous_cmd in DANGEROUS_COMMANDS:
                    if comm_lower == dangerous_cmd or comm_lower.endswith(f"/{dangerous_cmd}"):
                        processes.append({
                            "pid": pid,
                            "user": user,
                            "command": dangerous_cmd,
                            "full_cmd": args[:100],
                            "source": "process",
                        })
                        break
                    elif f"/{dangerous_cmd}" in args_lower or f" {dangerous_cmd} " in f" {args_lower} ":
                        processes.append({
                            "pid": pid,
                            "user": user,
                            "command": dangerous_cmd,
                            "full_cmd": args[:100],
                            "source": "process",
                        })
                        break

        return processes

    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        return []


def parse_dangerous_command_events(state: Dict[str, Any]) -> List[Tuple[str, str, str]]:
    """Monitor for npx, uvx, op command execution using history + ps polling."""
    if not MONITOR_DANGEROUS_COMMANDS:
        return []

    events = []
    seen_commands = set(state.get("seen_dangerous_commands", []))
    seen_pids = set(state.get("seen_dangerous_pids", []))

    # Check shell history for completed commands
    history_commands = get_shell_history_commands()
    for cmd_info in history_commands:
        # Create a unique key for this command (use full command to dedupe)
        cmd_key = f"hist:{cmd_info['full_cmd']}"
        if cmd_key not in seen_commands:
            seen_commands.add(cmd_key)

            title = f"COMMAND: {cmd_info['command']}"
            full_cmd = cmd_info["full_cmd"]
            if len(full_cmd) > 55:
                full_cmd = full_cmd[:52] + "..."
            body = f"[{cmd_info['shell']}] {full_cmd}"
            events.append(("alert", title, body))

    # Check for currently running processes
    running_processes = get_running_dangerous_commands()
    current_pids = set()

    for proc in running_processes:
        pid = proc.get("pid", "")
        current_pids.add(pid)

        if pid and pid not in seen_pids:
            seen_pids.add(pid)

            title = f"COMMAND: {proc['command']}"
            full_cmd = proc["full_cmd"]
            if len(full_cmd) > 50:
                full_cmd = full_cmd[:47] + "..."
            body = f"PID {pid} by {proc.get('user', '?')}: {full_cmd}"
            events.append(("alert", title, body))

    # Keep only recent history entries (last 100) to prevent unbounded growth
    if len(seen_commands) > 100:
        # Convert to list, keep last 100, convert back to set
        seen_commands = set(list(seen_commands)[-100:])

    # Clean up PIDs no longer running
    seen_pids = seen_pids & current_pids

    state["seen_dangerous_commands"] = list(seen_commands)
    state["seen_dangerous_pids"] = list(seen_pids)

    return events


# =============================================================================
# DNS Resolver Monitor
# =============================================================================

def get_dns_resolvers() -> List[str]:
    """Get current DNS resolver addresses using scutil."""
    cmd = "scutil --dns 2>/dev/null | grep 'nameserver\\[' | awk '{print $3}' | sort -u"

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=5
        )

        resolvers = [
            line.strip()
            for line in result.stdout.strip().splitlines()
            if line.strip()
        ]
        return resolvers

    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        return []


def parse_dns_events(state: Dict[str, Any]) -> List[Tuple[str, str, str]]:
    """Monitor for DNS resolver changes."""
    if not MONITOR_DNS:
        return []

    events = []
    known_dns = set(state.get("known_dns_resolvers", []))
    current_dns = set(get_dns_resolvers())

    # Check for changes (both additions and removals indicate a change)
    if known_dns and current_dns != known_dns:
        added = current_dns - known_dns
        removed = known_dns - current_dns

        if added or removed:
            title = "DNS RESOLVERS CHANGED"
            parts = []
            if added:
                parts.append(f"added: {', '.join(added)}")
            if removed:
                parts.append(f"removed: {', '.join(removed)}")
            body = "; ".join(parts)
            events.append(("alert", title, body))

    # Always update to current (including first run)
    state["known_dns_resolvers"] = list(current_dns)
    return events


# =============================================================================
# Public IP Monitor
# =============================================================================

def get_public_ip() -> Optional[str]:
    """Get public IP address using external service."""
    # Try multiple methods
    methods = [
        ["curl", "--max-time", "3", "--silent", "http://whatismyip.akamai.com/"],
        ["curl", "--max-time", "3", "--silent", "https://api.ipify.org"],
        ["dig", "-4", "+short", "myip.opendns.com", "@resolver1.opendns.com"],
    ]

    for cmd in methods:
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=5
            )
            ip = result.stdout.strip()
            # Basic validation - should look like an IP
            if ip and "." in ip and len(ip) <= 15:
                return ip
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
            continue

    return None


def parse_public_ip_events(state: Dict[str, Any]) -> List[Tuple[str, str, str]]:
    """Monitor for public IP address changes."""
    if not MONITOR_PUBLIC_IP:
        return []

    events = []
    known_ip = state.get("known_public_ip")
    current_ip = get_public_ip()

    if current_ip and known_ip and current_ip != known_ip:
        title = "PUBLIC IP CHANGED"
        body = f"{known_ip} → {current_ip}"
        events.append(("alert", title, body))

    if current_ip:
        state["known_public_ip"] = current_ip

    return events


# =============================================================================
# Local IP Monitor
# =============================================================================

def get_local_ips() -> Dict[str, str]:
    """Get local IP addresses for all interfaces."""
    interfaces = ["en0", "en1", "en2", "en3", "en4", "utun0", "utun1", "utun2"]
    ips = {}

    for iface in interfaces:
        try:
            result = subprocess.run(
                ["ipconfig", "getifaddr", iface],
                capture_output=True,
                text=True,
                timeout=2
            )
            ip = result.stdout.strip()
            if ip:
                ips[iface] = ip
        except (subprocess.TimeoutExpired, subprocess.SubprocessError):
            continue

    return ips


def parse_local_ip_events(state: Dict[str, Any]) -> List[Tuple[str, str, str]]:
    """Monitor for local IP address changes."""
    if not MONITOR_LOCAL_IP:
        return []

    events = []
    known_ips = state.get("known_local_ips", {})
    current_ips = get_local_ips()

    # Check for changes
    for iface, ip in current_ips.items():
        old_ip = known_ips.get(iface)
        if old_ip and old_ip != ip:
            title = f"LOCAL IP CHANGED: {iface}"
            body = f"{old_ip} → {ip}"
            events.append(("notify", title, body))

    # Check for new interfaces
    for iface, ip in current_ips.items():
        if iface not in known_ips:
            title = f"NEW INTERFACE: {iface}"
            body = f"IP: {ip}"
            events.append(("notify", title, body))

    # Check for removed interfaces
    for iface in known_ips:
        if iface not in current_ips:
            title = f"INTERFACE DOWN: {iface}"
            body = f"was {known_ips[iface]}"
            events.append(("notify", title, body))

    state["known_local_ips"] = current_ips
    return events


# =============================================================================
# Kandji/MDM Events Monitor
# =============================================================================

def parse_mdm_events(state: Dict[str, Any]) -> List[Tuple[str, str, str]]:
    """Monitor for Kandji/MDM events."""
    if not MONITOR_MDM:
        return []

    events = []

    # Query for MDM-related processes
    predicate = '''(
        process == "Kandji" OR
        process == "kandji-daemon" OR
        process == "mdmclient" OR
        process == "profiles" OR
        process == "ManagedClient" OR
        process == "softwareupdated" OR
        subsystem == "com.apple.ManagedClient" OR
        subsystem CONTAINS "kandji" OR
        eventMessage CONTAINS "MDM" OR
        eventMessage CONTAINS "Configuration Profile"
    )'''

    entries = get_log_entries(predicate)

    # Filter for interesting events
    interesting_keywords = [
        "install", "remove", "profile", "command", "push", "enroll",
        "policy", "restrict", "allow", "block", "update", "compliance"
    ]

    for entry in entries:
        event_id = entry.get("eventID", entry.get("traceID", str(entry)))
        if event_id in state["seen_events"]:
            continue

        process = entry.get("process", "MDM")
        message = entry.get("eventMessage", "")
        message_lower = message.lower()

        # Only alert on interesting MDM events
        if any(kw in message_lower for kw in interesting_keywords):
            title = f"MDM: {process}"
            body = message[:60] + "..." if len(message) > 60 else message
            events.append(("alert", title, body))
            state["seen_events"].append(event_id)

    return events


# =============================================================================
# Main Plugin Logic
# =============================================================================

def collect_all_events(state: Dict[str, Any]) -> List[Tuple[str, str, str]]:
    """Collect events from all sources."""
    all_events = []

    # Log-based events
    all_events.extend(parse_ssh_events(state))
    all_events.extend(parse_sudo_events(state))
    all_events.extend(parse_portscan_events(state))
    all_events.extend(parse_ftp_events(state))
    all_events.extend(parse_dangerous_command_events(state))
    all_events.extend(parse_mdm_events(state))

    # Network connection events
    all_events.extend(parse_port_events(state))
    all_events.extend(parse_vnc_events(state))
    all_events.extend(parse_listening_port_events(state))

    # File monitoring
    all_events.extend(parse_dotenv_events(state))

    # Network configuration monitoring
    all_events.extend(parse_dns_events(state))
    all_events.extend(parse_public_ip_events(state))
    all_events.extend(parse_local_ip_events(state))

    return all_events


def format_xbar_output(state: Dict[str, Any], new_events: List[Tuple[str, str, str]]) -> None:
    """Format and print xbar-compatible output."""

    # Process new events
    for event_type, title, body in new_events:
        timestamp = datetime.now().strftime("%H:%M")
        state["events"].append({
            "type": event_type,
            "title": title,
            "body": body,
            "time": timestamp,
            "date": datetime.now().isoformat(),
        })

        # Log event
        log_event(event_type, title, body)

        # Send notification for alerts
        if event_type == "alert":
            send_notification(title, body, is_alert=True)
        elif SHOW_NOTIFICATIONS:
            send_notification(title, body, is_alert=False)

    # Count recent alerts
    recent_alerts = sum(1 for e in state["events"][-20:] if e["type"] == "alert")

    # Menubar display
    if recent_alerts > 0:
        print(f"🛡️{recent_alerts} | templateImage={MENUBAR_ICON}")
    else:
        print(f"🛡️ | templateImage={MENUBAR_ICON}")

    print("---")

    # Status section
    print(f"Security Growler v2.0 | color=#666666 size=11")
    print(f"Last check: {datetime.now().strftime('%H:%M:%S')} | color=#666666 size=11")
    print("---")

    # Active monitors
    print("Active Monitors | color=#333333")
    monitors = []
    if MONITOR_SSH:
        monitors.append("SSH")
    if MONITOR_SUDO:
        monitors.append("Sudo")
    if MONITOR_PORTSCAN:
        monitors.append("Port Scans")
    if MONITOR_VNC:
        monitors.append("VNC")
    if MONITOR_PORTS:
        port_list = ", ".join(str(p) for p in PORTS_TO_MONITOR[:3])
        if len(PORTS_TO_MONITOR) > 3:
            port_list += f" (+{len(PORTS_TO_MONITOR) - 3})"
        monitors.append(f"Ports: {port_list}")
    if MONITOR_LISTENING:
        monitors.append(f"Listening ({LISTENING_PORT_MIN}-{LISTENING_PORT_MAX})")
    if MONITOR_DOTENV:
        monitors.append(".env Files")
    if MONITOR_DANGEROUS_COMMANDS:
        monitors.append(f"Commands: {', '.join(DANGEROUS_COMMANDS)}")
    if MONITOR_DNS:
        monitors.append("DNS Resolvers")
    if MONITOR_PUBLIC_IP:
        public_ip = state.get("known_public_ip", "?")
        monitors.append(f"Public IP ({public_ip})")
    if MONITOR_LOCAL_IP:
        monitors.append("Local IPs")
    if MONITOR_MDM:
        monitors.append("Kandji/MDM")

    for m in monitors:
        print(f"--✓ {m} | color=#228B22 size=12")

    print("---")

    # Recent events section
    events = state["events"][-20:]
    events.reverse()  # Most recent first

    if events:
        print("Recent Events | color=#333333")
        for event in events:
            icon = "🔴" if event["type"] == "alert" else "🔵"
            title = event["title"][:40]
            time = event["time"]
            color = "#CC0000" if event["type"] == "alert" else "#333333"
            print(f"--{icon} [{time}] {title} | color={color} size=12")
            if event.get("body"):
                body = event["body"][:50]
                print(f"----{body} | color=#666666 size=11")
    else:
        print("No recent events | color=#999999")

    print("---")

    # Actions
    print(f"View Log File | bash=/usr/bin/open param1={LOG_FILE} terminal=false")
    print(f"Open Plugin Folder | bash=/usr/bin/open param1=-R param2={os.path.abspath(__file__)} terminal=false")
    print("Refresh Now | refresh=true")

    print("---")

    # Configuration hints
    print("Configure... | color=#666666")
    print("--Edit plugin variables in xbar preferences | color=#999999 size=11")
    print("-----")
    print("--Core Monitors | color=#666666 size=11")
    print(f"----MONITOR_SSH={MONITOR_SSH} | color=#999999 size=11")
    print(f"----MONITOR_SUDO={MONITOR_SUDO} | color=#999999 size=11")
    print(f"----MONITOR_PORTSCAN={MONITOR_PORTSCAN} | color=#999999 size=11")
    print(f"----MONITOR_VNC={MONITOR_VNC} | color=#999999 size=11")
    print(f"----MONITOR_PORTS={MONITOR_PORTS} | color=#999999 size=11")
    print(f"----MONITORED_PORTS={MONITORED_PORTS} | color=#999999 size=11")
    print("-----")
    print("--New Monitors | color=#666666 size=11")
    print(f"----MONITOR_LISTENING={MONITOR_LISTENING} | color=#999999 size=11")
    print(f"----MONITOR_DOTENV={MONITOR_DOTENV} | color=#999999 size=11")
    print(f"----MONITOR_DANGEROUS_COMMANDS={MONITOR_DANGEROUS_COMMANDS} | color=#999999 size=11")
    print(f"----MONITOR_DNS={MONITOR_DNS} | color=#999999 size=11")
    print(f"----MONITOR_PUBLIC_IP={MONITOR_PUBLIC_IP} | color=#999999 size=11")
    print(f"----MONITOR_LOCAL_IP={MONITOR_LOCAL_IP} | color=#999999 size=11")
    print(f"----MONITOR_MDM={MONITOR_MDM} | color=#999999 size=11")
    print("-----")
    print(f"--SHOW_NOTIFICATIONS={SHOW_NOTIFICATIONS} | color=#999999 size=11")


def main():
    """Main entry point for the xbar plugin."""
    try:
        # Load state
        state = load_state()

        # Collect new events
        new_events = collect_all_events(state)

        # Update last check time
        state["last_check"] = datetime.now().isoformat()

        # Output xbar format
        format_xbar_output(state, new_events)

        # Save state
        save_state(state)

    except Exception as e:
        # Show error in menubar
        print(f"🛡️❌ | color=#CC0000")
        print("---")
        print(f"Error: {str(e)[:50]} | color=#CC0000")
        print(f"--{type(e).__name__}: {str(e)} | color=#999999 size=11")
        print("---")
        print("Refresh | refresh=true")


if __name__ == "__main__":
    main()
