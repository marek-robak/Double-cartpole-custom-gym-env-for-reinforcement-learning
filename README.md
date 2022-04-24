# Double-cartpole-custom-gym-env-for-reinforcement-learning

This repository contains OpenAI Gym environment designed for teaching RL
agents the ability to balance double CartPole. To make this easy to use, the
environment has been packed into a Python package, which automatically registers
the environment in the Gym library when the package is included in the code.
As a result, it can be easily used in conjunction with reinforcement learning
libraries such as StableBaselines3. There is also a sample code for training
and evaluating agents in this environment.

<p align="center">
  <img src="media/double_cartpole_540.gif"/>
</p>

## Installation

These instructions will guide you through installation of the environment and
show you how to use it for your projects. Whichever method of installation you
choose I recommend running it in a virtual environment created by Miniconda.
This program is used to simplify package management and deployment.

So, to get started, install Miniconda, [here](https://docs.conda.io/en/latest/miniconda.html)
is the official installation guide along with a detailed description.

In the following way you can create and activate virtual environment:

```
conda create -n <environment_name> python=3.9
conda activate <environment_name>
```

### Installation via pip - package installer for Python

You just need to type

```
pip install double-cartpole-custom-gym-env
```

### Installation via source code from GitHub repository

If you want to make specific changes to the source code or extend it with your
own functionalities this method will suit you.

```
git clone https://github.com/mareo1208/Double-cartpole-custom-gym-env-for-reinforcement-learning.git
cd Double-cartpole-custom-gym-env-for-reinforcement-learning/double_cartpole_custom_gym_env_package
pip install -e .
```

### How to use it in your code

Now all you need to do to use this environment in your code is import the package.
After that, you can use it with Gym and StableBaselines3 library via its
id: double-cartpole-custom-v0.

```
from stable_baselines3 import PPO
import gym

import double_cartpole_custom_gym_env

env = gym.make('double-cartpole-custom-v0')

model = PPO("MlpPolicy", env)

model.learn(total_timesteps=1500000)
model.save('new_agent')
```

### Environment prerequisites

Environment to run needs Python3 with Gym, Pygame, Pymunk, Numpy and StableBaselines3
libraries. All of them are automatically installed when the package is installed.

## Environment details

This environment consists of a cart attached to a straight rail and a double pendulum
attached to the cart. The RL agent can control the force acting on the cart. This
force influences the movement of the cart, which affects the swing angle of the
pendulums. The pendulums and the cart separately are rigid bodies with the same
mass. The agent's goal is to learn how to stabilize this system so that the pendulums
stay vertical. Forces acting on the cart are marked with red lines. The permitted
ranges of pendulums swings are also marked in the environment with red lines. If any
pendulum crosses these lines, the episode will stop.

The physics engine for this environment runs at 60fps.

### Initial episode conditions

Each episode begins with the cart centered on the available space at zero speed
initial. Both pendulums point upwards with a random deviation from the vertical
from -10° up to 10°.

### Ending episode conditions

Each episode ends if any pendulum swings beyond the allowed area or if the cart
hits a wall. Additionally, the episode will end if the set number of timesteps
has passed.

### Agent action and observation space

The space of actions made available to the RL agent consists of one value from -1
to 1. It is correlated with the force acting on the cart, -1 and 1 are maximum forces,
0 is no force acting.

The observation space consists of six values, all ranging from -1 to 1.
- The first one carries information about the distance of the cart from the walls
and the center point. A 0 is returned when the cart is in the middle
and values -1 and 1 when the cart touches the left or right wall.
- The second and third numbers inform about the current swing angles of the pendulums.
It is scaled to return 0 for a vertically upward pendulum, and -1 and 1 when a pendulum
goes outside the permitted area.
- The fourth number contains information about the speed at which the cart is moving.
It has been graduated so that the values -1 and 1 represent the maximum possible
speed that the cart can develop in the available space.
- The fifth and sixth numbers contain information about the angular velocities of the pendulums.
It has been scaled so that the values -1 and 1 represent the maximum achievable values.

### Reward function

The reward function consists of linear dependence of the cart distance from
the center of the available space and a -50 penalty for premature termination of the episode.

<img src="https://render.githubusercontent.com/render/math?math={\large\color{black}R(x)=1%2B0.5(-|x|%2B1)}#gh-light-mode-only">
<img src="https://render.githubusercontent.com/render/math?math={\large\color{white}R(x)=1%2B0.5(-|x|%2B1)}#gh-dark-mode-only">

Variable x is the first value from the agent observation space.

### Environment parameters

This environment provides two parameters that can change the way it works.

- render_sim: (bool) if true, a graphic is generated
- n_steps: (int) number of time steps

```
env = gym.make('double-cartpole-custom-v0', render_sim=True, n_steps=1000)
```

## See also

Everything available in this repository was created for the needs of my bachelor thesis.
If you can read in Polish and you are interested in it, you can find it
[here](https://www.ap.uj.edu.pl/diplomas/151837/?_s=1). It includes details on the
training process for sample agents and a description of the reward function selection process.

You may also be interested in other environments I have created. Go to the repositories
where they are located by clicking on the gifs below.

<p align="center">
  <a href="https://github.com/mareo1208/Drone-2d-custom-gym-env-for-reinforcement-learning.git">
    <img src="media/drone_360.gif"/>
  </a>
  <a href="https://github.com/mareo1208/Single-cartpole-custom-gym-env-for-reinforcement-learning.git">
    <img src="media/cartpole_360.gif"/>
  </a>
</p>
