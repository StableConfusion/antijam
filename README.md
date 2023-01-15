# AntiJam Project

This is a Reinforcement Learning system that trains
a traffic light agent to optimally switch based on
real time traffic observations.

The optimization goal is the minimization
of wasted fuel - fuel used while stuck in traffic.

Each traffic light sees cars in the entire city,
other traffic light states and it's own position.

The PPO (Proximal Policy Optimization) agent has
been trained in such an environment.

Results have been compared with a baseline
model (switching lights every X ticks).
The learned PPO agent outperforms the baseline.

# Demo

Baseline agent on the left, trained PPO on the right.

The reward is fuel use efficiency (100% means no fuel was wasted while not moving).

![image](docs/im1.png)

![video](docs/demo1.webm)

# Training report

![report](docs/training.png)

Total computational time was 6 h.

# Installation

- install python 3.10 and pytorch
- `pip install -r requirements.txt`

# Training

With enough RAM, VRAM, CPU cores and a good GPU run:
- `python train.py`

A pretrained checkpoint is provided in [checkpoints/](checkpoints).

# Simulation

Specify the trained checkpoint path in `simulation.py` and run:
- `python simulation.py`

# Environment specification

## Step function

The step function takes an action mapping of
traffic light ids to their requested states.

Each traffic light has a switching frequency limit.
This is to stop rapid state changes.

It returns the environment observation and reward.
The environment never terminates by itself.

## Observation

The observation is designed for a convolutional neural network.
It contains 6 channels, each NxM (size of grid):
- the map (1 where road)
- car positions (1 where car)
- this agent position (1 where this agent junction)
- 1 where lights are in state 0
- 1 where lights are in state 1
- all available junctions

To speed up training, the map was removed from
the observation and the CNN was replaced with
a simple FCN.

# Reward

The reward in each step is calculated
as (number of cars that moved / total cars).

The reward is summed over all agents and environment
steps.

For simulation evaluation, an average of
100 step rewards is taken.
