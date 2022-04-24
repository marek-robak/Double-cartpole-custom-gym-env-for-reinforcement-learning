from double_cartpole_custom_gym_env.double_cartpole_env import *
from gym.envs.registration import register

register(
    id='double-cartpole-custom-v0',
    entry_point='double_cartpole_custom_gym_env:DoubleCartpoleEnv',
    kwargs={'render_sim': False, 'n_steps': 1000}
)
