from ray.rllib.algorithms.ppo import PPOConfig, PPO
from ray.rllib.algorithms.algorithm import Algorithm
from environment import GridWorldEnv
from ray_env_wrapper import AntiJamEnv
from ray.tune.registry import register_env


class TrainedAgent:
    def __init__(self, checkpoint_path):
        register_env("antijam", lambda config: AntiJamEnv(config))
        single_env = AntiJamEnv({})
        obs_space = single_env.observation_space
        act_space = single_env.action_space

        def gen_policy(_):
            return (None, obs_space, act_space, {})

        policies = {
            'policy_{}'.format(i): gen_policy(i) for i in range(1)
        }
        policy_ids = list(policies.keys())
        
        config = (
            PPOConfig()
            .environment('antijam', disable_env_checking=True)
            .framework('torch')
            .resources(num_gpus=1)
            .rollouts(num_rollout_workers=1)
            .multi_agent(
                policies=policies,
                policy_mapping_fn=lambda agent_id, episode, worker, **kwargs: policy_ids[0],
            )
            # .training(
            #     model={
            #         'custom_model': CustomModel,
            #     },
            # )
        )

        self.algo = config.build()
        self.algo.restore(checkpoint_path)

        self.env = AntiJamEnv({})

    def compute_actions(self, env: GridWorldEnv):
        # return: {"light_{i}": 0 or 1}
        self.env.env = env
        obs = {
            f'light_{i}': self.env.get_light_observation(i)
            for i in range(self.env.num_lights)
        }
        return self.algo.compute_actions(obs, policy_id='policy_0')
