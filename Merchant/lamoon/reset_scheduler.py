"""Runs a persistent 30-day order-data reset schedule."""

from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from threading import Event, Thread


class DataResetScheduler:
    def __init__(self, order_service, state_path, interval_days=30, check_seconds=60):
        if interval_days < 1:
            raise ValueError("interval_days must be at least 1")
        self.order_service = order_service
        self.state_path = Path(state_path)
        self.interval = timedelta(days=interval_days)
        self.check_seconds = check_seconds
        self._stop = Event()
        self._thread = None

    @staticmethod
    def _now():
        return datetime.now(timezone.utc)

    def _write_state(self, state):
        temporary = self.state_path.with_suffix(self.state_path.suffix + ".tmp")
        temporary.write_text(json.dumps(state, indent=2), encoding="utf-8")
        temporary.replace(self.state_path)

    def _read_state(self):
        try:
            state = json.loads(self.state_path.read_text(encoding="utf-8"))
            next_reset = datetime.fromisoformat(state["next_reset_at"])
            if next_reset.tzinfo is None:
                next_reset = next_reset.replace(tzinfo=timezone.utc)
            return state, next_reset
        except FileNotFoundError:
            return None, None
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            # A broken schedule file should not unexpectedly erase customer orders.
            print("Warning: reset schedule file is invalid; starting a new 30-day period.")
            return None, None

    def _check_and_reset(self):
        now = self._now()
        state, next_reset = self._read_state()
        if state is None:
            state = {
                "last_reset_at": None,
                "next_reset_at": (now + self.interval).isoformat(),
            }
            self._write_state(state)
            print(f"Order data will first reset at {state['next_reset_at']}.")
            return

        if now < next_reset:
            return

        removed = self.order_service.reset_orders()
        state = {
            "last_reset_at": now.isoformat(),
            "next_reset_at": (now + self.interval).isoformat(),
        }
        try:
            self._write_state(state)
        except OSError as error:
            # Stop retrying, so a storage error cannot repeatedly erase new orders.
            self._stop.set()
            print(f"Order data reset completed, but schedule could not be saved: {error}")
            return
        print(f"Automatic 30-day reset removed {removed} orders; next reset at {state['next_reset_at']}.")

    def _run(self):
        while not self._stop.wait(self.check_seconds):
            try:
                self._check_and_reset()
            except OSError as error:
                print(f"Order data reset failed; will retry: {error}")

    def start(self):
        # Check at startup as well as periodically, so an overdue reset happens
        # before the HTTP server starts accepting new orders.
        self._check_and_reset()
        self._thread = Thread(target=self._run, name="data-reset-scheduler", daemon=True)
        self._thread.start()

    def stop(self):
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=2)
