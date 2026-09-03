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
        self._training = False
        self.paused = False

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
        self.paused = False

        gt = self._gt
        self._gt = None

        if not gt:
            return

        try:
            gt.kill()
        except Exception:
            pass

    def _run(self):
        policy = self.game.Mike.policy

        # Deployment should use the same simulation timestep
        # that was used during training.
        policy.epsilon = 0

        SIM_DT = 1.0 / 60.0

        try:
            # This controls real-time pacing.
            # The actual game physics always receives SIM_DT = 1/60.
            next_tick = time.monotonic()

            while self._running:

                # Get the current state.
                state = policy.get_state(self.game)

                # Get the trained agent's action.
                action = policy.get_action(state)

                # Advance the game using the exact same timestep
                # used by training.
                self.game.step(SIM_DT, action)

                # Send the latest state to the frontend.
                if self.on_state:
                    self.on_state(self.game.get_state())

                # Wait until the next 60 Hz simulation tick.
                next_tick += SIM_DT

                sleep_time = next_tick - time.monotonic()

                if sleep_time > 0:
                    eventlet.sleep(sleep_time)
                else:
                    # If the server falls behind, don't execute a
                    # large batch of simulation steps immediately.
                    next_tick = time.monotonic()

        finally:
            self._running = False
            self._gt = None

    def _trainingRun(self):
        # TODO: Add all the runner policy changing

        policy = self.game.Mike.policy

        survival_history = []
        reward_history = []

        component_totals = {
            "potential": 0.0,
            "terminal": 0.0
        }

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

                    # policy.train_short_memory(
                    #     state_old,
                    #     action,
                    #     reward,
                    #     state_new,
                    #     done
                    # )

                    policy.remember(
                        state_old,
                        action,
                        reward,
                        state_new,
                        done
                    )

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

                    avg_survival = (
                        sum(survival_history)
                        / len(survival_history)
                    )

                    avg_reward = (
                        sum(reward_history)
                        / len(reward_history)
                    )

                    n = max(1, n_since_print)

                    print(
                        f"[stats] "
                        f"ep={policy.n_games} "
                        f"avg_survival={avg_survival:.1f} "
                        f"avg_reward={avg_reward:.2f} | "
                        f"avg components: "
                        f"terminal="
                        f"{component_totals['terminal'] / n:.2f} "
                        f"potential="
                        f"{component_totals['potential'] / n:.2f}"
                    )

                    component_totals = {
                        k: 0.0 for k in component_totals
                    }

                    movement_sum = 0
                    n_since_print = 0

                for i in range(5):
                    policy.train_long_memory()

                policy.n_games += 1

                # if policy.n_games % 10 == 0:
                #     self._log_fixed_state_action(policy)

                if policy.n_games % 50 == 0:
                    policy.save("model.pth")

        except KeyboardInterrupt:
            print("Training ended")

        finally:
            self._training = False