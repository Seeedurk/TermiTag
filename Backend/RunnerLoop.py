import eventlet
import time

class RunnerLoop:
    def __init__(self, game, tick_hz=60, on_state=None):
        self.game = game
        self.tick_hz = tick_hz
        self.on_state = on_state
        self._running = False
        self._gt = None

    def start(self):
        if self._running:
            return
        self._running = True
        self._gt = eventlet.spawn(self._run)

    def stop(self, timeout=2.0):
        self._running = False
        if not self._gt:
            return
        try:
            eventlet.with_timeout(timeout, self._gt.wait)
        except Exception:
            try:
                self._gt.kill()
            except Exception:
                pass
        finally:
            self._gt = None

    def _run(self):
        try:
            dt = 1.0 / self.tick_hz
            while self._running:
                t0 = time.time()

                self.game.step(dt)


                if self.on_state:
                   self.on_state(self.game.get_state())
                elapsed = time.time() - t0
                eventlet.sleep(max(0, dt - elapsed))
        finally:
            self._running = False
            self._gt = None 