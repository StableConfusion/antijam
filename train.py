import argparse
import gym
from gym.spaces import Discrete, Box
import numpy as np

import ray
from ray import air, tune
from ray.air.integrations.wandb import WandbLoggerCallback
from ray.rllib.env.env_context import EnvContext
from ray.tune.registry import get_trainable_cls


parser = argparse.ArgumentParser()
parser.add_argument(
    "--run", type=str, default="PPO", help="The RLlib-registered algorithm to use."
)
parser.add_argument(
    "--framework",
    choices=["tf", "tf2", "torch"],
    default="torch",
    help="The DL framework specifier.",
)


class SimpleCorridor(gym.Env):
    def __init__(self, config: EnvContext):
        self.end_pos = config["corridor_length"]
        self.cur_pos = 0
        self.action_space = Discrete(2)
        self.observation_space = Box(0.0, self.end_pos, shape=(1,), dtype=np.float32)

    def reset(self):
        self.cur_pos = 0
        return [self.cur_pos]

    def step(self, action):
        assert action in [0, 1], action
        if action == 0 and self.cur_pos > 0:
            self.cur_pos -= 1
        elif action == 1:
            self.cur_pos += 1
        done = self.cur_pos >= self.end_pos
        return [self.cur_pos], 1 if done else -0.1, done, {}


if __name__ == "__main__":
    args = parser.parse_args()
    print(f"Running with following CLI options: {args}")

    ray.init()

    config = (
        get_trainable_cls(args.run)
        .get_default_config()
        .environment(SimpleCorridor, env_config={"corridor_length": 5})
        .framework(args.framework)
        .rollouts(num_rollout_workers=8)
        .resources(num_gpus=1)
    )

    print("Training automatically with Ray Tune")
    tuner = tune.Tuner(
        args.run,
        param_space=config.to_dict(),
        run_config=air.RunConfig(
            local_dir='./ray_results',
            callbacks=[
                WandbLoggerCallback(project='antijam'),
            ],
        ),
    )
    results = tuner.fit()

    ray.shutdown()
