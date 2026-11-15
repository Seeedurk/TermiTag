# AI Tag — Reinforcement Learning Pursuit & Evasion

<p align="center">
  <strong>A real-time pursuit-and-evasion environment featuring a Double DQN Runner and deterministic Tagger opponents.</strong>
</p>

<p align="center">
  <img src="assets/gameplay.gif" alt="AI Tag gameplay demonstration" width="800">
</p>

<p align="center">
  <a href="#overview">Overview</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#reinforcement-learning">Reinforcement Learning</a> •
  <a href="#tagger-ai">Tagger AI</a> •
  <a href="#training--evaluation">Training & Evaluation</a> •
  <a href="#results">Results</a> •
  <a href="#video-demo">Video Demo</a> •
  <a href="#setup">Setup</a>
</p>

---

## Overview

**TermiTag** is a real-time pursuit-and-evasion environment designed to explore reinforcement learning in a dynamic game setting.

The project features two competing agents:

* **Runner** — controlled by a Double Deep Q-Network (Double DQN)
* **Tagger** — controlled by deterministic pursuit algorithms with multiple difficulty levels

The Runner observes the game state and selects from four movement actions. During training, the Runner learns to maximize its survival time while maintaining distance from the Tagger and avoiding environmental hazards.

The primary experiment trains the Runner against a **medium-strength deterministic Tagger** and evaluates the resulting policy against both the training opponent and a **stronger Tagger that was not used during training**.

---

## Key Features

* Double DQN reinforcement-learning agent
* Experience replay
* Target network for stable Q-value learning
* Deterministic pursuit-based Tagger AI
* Multiple Tagger difficulty levels
* Real-time game environment
* Collision and boundary detection
* Reward shaping based on pursuit distance and environmental hazards
* Training and evaluation modes
* Browser-based visualization

---
## Development Process

### 1. Environment Design

When I created this project the goals I had in mind were learning to implement base level reinforcement learning AI, and testing 
whether that AI could successfully train against a tagger, then use what it learned to beat a higher level tagger

The rules are simple, the environment is a 600*800 px arena, by default there are a randomized number of walls 0 - 5
The tagger is tasked with touching the runner, and the runner must evade the tagger, winning when the timer reaches 0
Touching the wall or going out of bounds results in a point for the other player
Each game is first to 10 rounds

One important thing to notice is that the runner is controlled by the AI Policy, while the Tagger is deterministic. This is because
the tagger role is straight forward, while running is more open ended with various strategies. 

---

### 2. Deterministic Tagger Development

The Tagger was developed in multiple stages to create progressively more challenging opponents.

**Level 1 — Basic Pursuit**

The Level 1 Tagger accelerates toward the Runner's current position.

**Level 2 — Medium Pursuit**

The Level 2 Tagger checks candidate acceleration directions and chooses one expected to approach the Runner.

**Level 3 — Advanced Pursuit**

The Level 3 Tagger predicts the Runner's future position and aims to intercept it.

The Tagger difficulty was designed to increase through **decision-making complexity rather than simply increasing movement speed**.

---

### 3. Reinforcement Learning Agent

The Runner was chosen for reinforcement learning because evasion allows for a wider range of strategies than direct pursuit.

The Runner uses a **Double Deep Q-Network (Double DQN)** to select movement actions based on the current game state.

The state representation summarizes the positions and velocities of both agents, nearby walls, boundaries, and remaining time.

The four actions accelerate up, down, left, or right.

The network maps 23 state values through two 128-unit ReLU layers to four action-value outputs.

---

### 4. Reward & State Design

The observation includes agent motion, arena limits, remaining time, and nearby obstacles.

The state includes information about:

* Runner position and velocity
* Tagger position and velocity
* Relative Runner–Tagger position
* Boundary proximity
* Remaining time
* Nearby environmental obstacles

These features help the Runner estimate the threat direction and identify available space for evasive movement.

The reward system combines:

* Terminal rewards for survival, tagging, and collisions
* Distance-based reward shaping relative to the Tagger
* Penalties for environmental hazards

Together, these rewards encourage survival and separation from the Tagger while discouraging collisions.

---

### 5. Training Process

The Runner was trained through repeated games against the medium Tagger using Double DQN.

Training was performed against the **medium-strength deterministic Tagger**.

The training configuration is not documented here.

State transitions were stored in replay memory and sampled for training.

The online network selects the next action, and the target network evaluates that action when calculating the update.

---

### 6. Development & Iteration

Development focused on representing the game state, shaping rewards for evasion, and comparing the Runner against Taggers with different strategies.

---

### 7. Evaluation Strategy

After training, the Runner was evaluated against:

1. **The medium Tagger used during training**
2. **The stronger Tagger that was not used during training**

This was intended to determine whether the learned Runner policy could perform against an opponent with a more sophisticated pursuit strategy.

Evaluation compares the Runner against the medium and advanced Taggers. The number of games and measured outcomes have not been recorded here.

---

### 8. Final Development Outcome

The final system combines a real-time game environment, deterministic Taggers, and a Double DQN Runner.

Measured performance results are not included yet.

Testing against additional opponents and environments would be needed to establish how well the learned policy generalizes.


---

## Architecture

```mermaid
flowchart TD
    UI["Game Interface<br/>React / Canvas"]
    ENV["Game Environment<br/>State • Physics • Collision • Reward"]

    RUNNER["Runner<br/>Double DQN"]
    TAGGER["Tagger<br/>Deterministic AI"]

    STATE["23-Dimensional<br/>State Representation"]
    QNET["Q-Network<br/>23 → 128 → 128 → 4"]
    TRAIN["QTrainer<br/>Double DQN Update"]
    MEMORY["Replay Memory"]

    UI --> ENV

    ENV --> STATE
    STATE --> QNET
    QNET --> RUNNER

    ENV --> TAGGER

    RUNNER --> ENV
    TAGGER --> ENV

    ENV -->|"State transition<br/>Reward + Next State"| MEMORY
    MEMORY --> TRAIN
    TRAIN --> QNET
```

### Training Loop

```mermaid
flowchart LR
    S["Current State"] --> A["Double DQN"]
    A --> ACT["Select Action"]
    ACT --> ENV["Game Environment"]
    ENV --> R["Reward"]
    ENV --> NS["Next State"]
    R --> MEM["Replay Memory"]
    NS --> MEM
    MEM --> TRAIN["QTrainer"]
    TRAIN --> UPDATE["Update Q-Network"]
    UPDATE --> A
```

---

## Reinforcement Learning

### State Representation

The Runner receives a normalized **23-dimensional state representation** containing information about:

| Category          | Information                          |
| ----------------- | ------------------------------------ |
| Runner            | Position and velocity                |
| Tagger            | Position and velocity                |
| Relative Position | Runner-to-Tagger displacement        |
| Boundaries        | Distance to each arena boundary      |
| Time              | Remaining episode time               |
| Environment       | Relative Position of 2 closest walls |

This allows the agent to make decisions based on both the Tagger's current state and the surrounding environment.

### Action Space

The Runner has four discrete actions:

| Action | Behavior         |
| ------ | ---------------- |
| `0`    | Accelerate Up    |
| `1`    | Accelerate Down  |
| `2`    | Accelerate Left  |
| `3`    | Accelerate Right |

### Neural Network

```text
Input: 23 state values
        │
        ▼
   Fully Connected
      128 units
        │
       ReLU
        │
        ▼
   Fully Connected
      128 units
        │
       ReLU
        │
        ▼
   4 Q-values
```

The output represents the estimated value of each available action.

### Double DQN

The training process uses Double DQN to reduce overestimation of action values.

The online network selects the best next action, while the target network evaluates that selected action.

Conceptually:

```text
Online Network
      │
      ├── Select best next action
      │
      ▼
Target Network
      │
      └── Evaluate selected action
```

---

## Reward Function

The Runner receives both terminal and intermediate rewards.

### Terminal Rewards

| Event                       | Reward |
| --------------------------- | -----: |
| Runner survives the episode |    +30 |
| Runner is tagged            |    -30 |
| Runner leaves bounds        |    -30 |
| Runner collides with a wall |    -30 |

### Reward Shaping

Intermediate rewards incorporate a potential function using a telescopic reward shaping based primarily on:

* Distance from the Tagger
* Proximity to environmental hazards

This encourages the Runner to maintain separation while avoiding dangerous areas of the environment.

---

## Tagger AI

AI Tag includes multiple deterministic Tagger strategies with increasing levels of decision-making complexity.

### Difficulty Progression

```mermaid
flowchart LR
    L1["Level 1<br/>Direct Pursuit"]
    L2["Level 2<br/>Candidate Direction Search"]
    L3["Level 3<br/>Predictive Pursuit"]

    L1 --> L2 --> L3
```

### Level 1 — Direct Pursuit

The Tagger accelerates toward the Runner's current position.

### Level 2 — Search-Based Pursuit

The Tagger evaluates multiple possible acceleration directions and selects the direction that produces the strongest predicted approach toward the Runner.

### Level 3 — Predictive Pursuit

The strongest Tagger uses prediction of the Runner's future position to make its pursuit decisions.

This creates a natural difficulty progression without simply relying on increased movement speed.

---

## Training & Evaluation

The primary training experiment uses the following setup:

```mermaid
flowchart TD
    L1["Level 1<br/>Basic Tagger"]
    L2["Level 2<br/>Medium Tagger"]
    L3["Level 3<br/>Advanced Tagger"]

    L2 -->|"TRAIN"| DQN["Double DQN Runner"]

    DQN -->|"EVALUATE"| L2
    DQN -->|"EVALUATE"| L3
```

The Runner is trained against the **medium Tagger** and subsequently evaluated against:

1. The Tagger it trained against
2. A stronger Tagger that was not used during training

This provides a simple test of whether the learned policy can generalize beyond its training opponent.

---

## Results

Measured evaluation results have not been recorded yet.

### Interpretation

When results are available, performance against the stronger Tagger can indicate how well the learned evasion policy transfers to a more challenging opponent.

---

## Video Demo

Export the Screencastify recording as an H.264 MP4 and add it to the repository as `assets/demo.mp4`. The embedded player below loads that file from the `main` branch.

<video src="https://raw.githubusercontent.com/Seeedurk/TermiTank/main/assets/demo.mp4" controls width="100%">
  Your browser does not support embedded video.
</video>

---

## Project Structure

```text
TermiTank/
├── Client/
│   ├── Components/
│   ├── Root/
│   └── Styles/
├── Backend/
│   ├── Models/
│   ├── Policy/
│   ├── Game.py
│   ├── Runner.py
│   ├── RunnerLoop.py
│   ├── Tagger.py
│   ├── Train.py
│   └── main.py
├── package.json
└── README.md
```

---

## Tech Stack

* **Python** — reinforcement learning and game logic
* **PyTorch** — neural network and Double DQN
* **React** — game interface
* **Flask** — backend/API
* **Socket.IO** — real-time communication
* **Git/GitHub** — version control and project documentation

---

## What I Learned

Through AI Tag, I explored:

* Reinforcement learning fundamentals
* Double Deep Q-Networks
* Experience replay
* Target networks
* Reward shaping
* State representation
* Deterministic pursuit algorithms
* Real-time interaction between an ML model and a game environment
* Evaluating learned policies against previously unseen opponents

---

## Limitations & Future Work

Current limitations include:

* The Runner is trained against a specific deterministic opponent.
* Performance can vary depending on the opponent strategy and environment configuration.
* The current action space is limited to four directional acceleration actions.

Potential future improvements include:

* Self-play reinforcement learning
* Additional opponent strategies
* More complex environments
* Larger action/state spaces
* More extensive evaluation across randomized environments

---

## Installation

```bash
git clone https://github.com/Seeedurk/TermiTank.git
cd TermiTank
npm install
python -m pip install -r Backend/requirements.txt
npm run dev
```

In a second terminal, start the backend:

```bash
cd Backend
python main.py
```

---

## License

This project is licensed under the [MIT License](LICENSE).
