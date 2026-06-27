import eventlet
import time

class RunnerLoop:
    def __init__(self, game, tick_hz=60, on_state=None):
        self.game = game
        self.tick_hz = tick_hz
        self.on_state = on_state
        self._running = False
        self._gt = None
        self._training = False;

    def start(self):
        if self._running:
            return
        self._running = True
        self._gt = eventlet.spawn(self._run)

    def trainStart(self):
        print("Train start works")
        if self._training:
            return
        print("is this the prob")
        self._training = True
        self._trainingRun()



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
        policy = self.game.Mike.policy
        policy.epsilon = 0
        try:
            dt = 1.0 / self.tick_hz
            while self._running:
                t0 = time.time()

                state = policy.get_state(self.game)

                action = policy.get_action(state)

                print(action)

                self.game.step(dt, action)


                if self.on_state:
                   self.on_state(self.game.get_state())
                elapsed = time.time() - t0
                eventlet.sleep(max(0, dt - elapsed))
        finally:
            self._running = False
            self._gt = None
            
    def _trainingRun(self): #TODO: Add all the runner policy changing
        policy = self.game.Mike.policy

        try:
            while self._training:

                self.game.gameReset()
                done = False

                while not done:

                    state_old = policy.get_state(self.game)

                    action = policy.get_action(state_old)

                    reward, done = self.game.train_step(action)

                    state_new = policy.get_state(self.game)

                    policy.train_short_memory(state_old, action, reward, state_new, done)

                    policy.remember(state_old, action, reward, state_new, done)


                print("episode completed")
                
                policy.train_long_memory()
                policy.n_games += 1

                policy.save("latest.pth")
                #TODO: In train.py add policy.load
                # Add policy.save right here
                # In policy create both functions which creates a file and saves weights and pams into it

        except KeyboardInterrupt:
            print("Training ended")

        finally:
            self._training = False
