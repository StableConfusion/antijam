import ray
from ray import tune
from ray.air.integrations.wandb import WandbLoggerCallback
from ray.tune.registry import register_env
from ray.rllib.algorithms.ppo import PPOConfig

from ray_env_wrapper import AntiJamEnv


if __name__ == "__main__":
    ray.init()

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

    tune.run(
        'PPO',
        config=(
            PPOConfig()
            .environment('antijam', disable_env_checking=True)
            .framework('torch')
            .resources(num_gpus=0)
            .rollouts(num_rollout_workers=4)
            .multi_agent(
                policies=policies,
                policy_mapping_fn=lambda agent_id, episode, worker, **kwargs: policy_ids[0],
            )
        ).to_dict(),
        callbacks=[WandbLoggerCallback(project='antijam')],
        local_dir='./ray_results',
        checkpoint_at_end=True,
        checkpoint_freq=1,
    )

    ray.shutdown()
