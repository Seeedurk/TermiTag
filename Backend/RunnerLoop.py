import eventlet
import time
import torch
import numpy as np

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


                self.game.step(dt, action)


                if self.on_state:
                   self.on_state(self.game.get_state())
                elapsed = time.time() - t0
                eventlet.sleep(max(0, dt - elapsed))
        finally:
            self._running = False
            self._gt = None

    def _log_fixed_state_action(self, policy):
        # Fixed diagnostic state: runner at start pos (100,300), tagger at start pos (700,300),
        # both stationary, distance_x=600, distance_y=0.
        # NOTE: must match whatever feature order/scaling DQNPolicy.get_state currently uses.
        # If you normalize get_state later, normalize this the same way or the comparison is meaningless.
        fixed_state = np.array([
            400/800,   # runner_x
            300/600,   # runner_y
            0,         # runner_vx
            0,         # runner_vy

            # ---------- Tagger (approaching from the right) ----------
            600/800,   # tagger_x
            300/600,   # tagger_y
            0,         # tagger_vx
            0,         # tagger_vy

            # ---------- Relative distance ----------
            (600-400)/800,  # distance_x
            0,              # distance_y

            # ---------- Border distances ----------
            400/800,        # left
            (800-400)/800,  # right
            300/600,        # top
            (600-300)/600,  # bottom

            # ---------- Wall 1 (none nearby) ----------
            0, 0, 0, 0,

            # ---------- Wall 2 (none nearby) ----------
            0, 0, 0, 0,

            1


        ], dtype=np.float32)
        state_tensor = torch.tensor(fixed_state, dtype=torch.float32)
        with torch.no_grad():
            q_values = policy.model(state_tensor)
        action = torch.argmax(q_values).item()
        print(f"[diag] n_games={policy.n_games} fixed_state_action={action} q={q_values.tolist()}")
            
    def _trainingRun(self): #TODO: Add all the runner policy changing
        policy = self.game.Mike.policy
        survival_history = []
        reward_history = []
        component_totals = {"potential": 0.0, "terminal": 0.0}
        movement_sum = 0
        n_since_print = 0

        try:
            while self._training:

                self.game.gameReset()
                step_counter = 0
                done = False
                episode_reward_sum = 0

                while not done:

                    state_old = policy.get_state(self.game)

                    action = policy.get_action(state_old)

                    reward, done = self.game.train_step(action)

                    episode_reward_sum += reward

                    state_new = policy.get_state(self.game)

                    #policy.train_short_memory(state_old, action, reward, state_new, done)

                    policy.remember(state_old, action, reward, state_new, done)

                    step_counter += 1

                    movement_sum += self.game.total_movement

                for key in component_totals:
                    component_totals[key] += self.game.reward_components[key]
                n_since_print += 1

                survival_history.append(step_counter) 

                if len(survival_history) > 50: 
                    survival_history.pop(0)

                reward_history.append(episode_reward_sum)
                if len(reward_history) > 50:
                    reward_history.pop(0)

                if policy.n_games % 50 == 0:
                    avg_survival = sum(survival_history) / len(survival_history)
                    avg_reward = sum(reward_history) / len(reward_history)
                    n = max(1, n_since_print)
                    print(f"[stats] ep={policy.n_games} avg_survival={avg_survival:.1f} avg_reward={avg_reward:.2f} | "
                        f"avg components: terminal={component_totals['terminal']/n:.2f} potential={component_totals['potential']/n:.2f} ")
                    component_totals = {k: 0.0 for k in component_totals}
                    movement_sum = 0
                    n_since_print = 0
                
                for i in range(5):
                    policy.train_long_memory()

                policy.n_games += 1

                #if policy.n_games % 10 == 0:
                    #self._log_fixed_state_action(policy)

                if policy.n_games % 50 == 0:
                    policy.save("model.pth")
  

        except KeyboardInterrupt:
            print("Training ended")

        finally:
            self._training = False
