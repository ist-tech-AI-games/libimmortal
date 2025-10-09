#!/usr/bin/env bash
set -e

export DISPLAY=${DISPLAY:-:99}
export XVFB_RES=${XVFB_RES:-1280x720x24}
export VNC_PORT=${VNC_PORT:-5900}

Xvfb "$DISPLAY" -screen 0 "$XVFB_RES" -nolisten tcp -ac &
sleep 0.5

fluxbox >/dev/null 2>&1 &

x11vnc -display "$DISPLAY" -forever -shared -nopw -rfbport "$VNC_PORT" >/dev/null 2>&1 &

exec "$@"
