from double_cartpole_custom_gym_env.event_handler import *
from double_cartpole_custom_gym_env.Cartpole import *

import gym
from gym import spaces
from gym.utils import seeding
import numpy as np
import random
import os

class DoubleCartpoleEnv(gym.Env):
    """
    render_sim: (bool) if true, a graphic is generated
    n_steps: (int) number of time steps
    """

    def __init__(self, render_sim=False, n_steps=1000):

        self.render_sim = render_sim

        if self.render_sim is True:
            self.init_pygame()

        self.init_pymunk()

        #Parameters
        self.max_time_steps = n_steps
        self.force_scale = 1200

        #Initial values
        self.force = 0
        self.done = False
        self.current_time_step = 0

        #Defining spaces for action and observation
        self.min_action = np.array([-1], dtype=np.float32)
        self.max_action = np.array([1], dtype=np.float32)
        self.action_space = spaces.Box(low=self.min_action, high=self.max_action, dtype=np.float32)

        self.min_observation = np.array([-1, -1, -1, -1, -1, -1], dtype=np.float32)
        self.max_observation = np.array([1, 1, 1, 1, 1, 1], dtype=np.float32)
        self.observation_space = spaces.Box(low=self.min_observation, high=self.max_observation, dtype=np.float32)

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Double Cartpole Environment")
        self.clock = pygame.time.Clock()

        script_dir = os.path.dirname(__file__)
        icon_path = os.path.join("img", "icon.png")
        icon_path = os.path.join(script_dir, icon_path)
        pygame.display.set_icon(pygame.image.load(icon_path))

    def init_pymunk(self):
        self.space = pymunk.Space()
        self.space.gravity = Vec2d(0, -1000)

        if self.render_sim is True:
            self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
            self.draw_options.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES
            pymunk.pygame_util.positive_y_is_up = True

        initial_x = 400
        initial_y = 400
        self.target = 400

        self.track = Track(0, 400, 800, 400, 0, self.space)

        self.cart_mass = 1
        self.cart = Cart(initial_x, initial_y, 80, 40, self.cart_mass, (33, 93, 191), self.space)

        #pole 1
        self.pole_1_mass = 1
        self.pole_1_length = 160
        pole_1_thickness = 15

        alpha = random.uniform(17*np.pi/36, 19*np.pi/36)

        pole_1_x = initial_x + self.pole_1_length * np.cos(alpha)
        pole_1_y = initial_y + self.pole_1_length * np.sin(alpha)
        self.pole_1 = Pole(pole_1_x, pole_1_y, initial_x, initial_y, pole_1_thickness, self.pole_1_mass, (66, 135, 245), self.space)

        #pole 2
        self.pole_2_mass = 1
        self.pole_2_length = 160
        pole_2_thickness = 15

        betha = random.uniform(17*np.pi/36, 19*np.pi/36)

        pole_2_x = pole_1_x + self.pole_2_length * np.cos(betha)
        pole_2_y = pole_1_y + self.pole_2_length * np.sin(betha)
        self.pole_2 = Pole(pole_2_x, pole_2_y, pole_1_x, pole_1_y, pole_2_thickness, self.pole_2_mass, (119, 169, 248), self.space)

        self.left_slider = pymunk.GrooveJoint(self.track.body, self.cart.body, (0, 400), (800, 400), (-20, 0))
        self.left_slider.error_bias = 0
        self.left_slider.collide_bodies = False
        self.space.add(self.left_slider)

        self.right_slider = pymunk.GrooveJoint(self.track.body, self.cart.body, (0, 400), (800, 400), (20, 0))
        self.right_slider.error_bias = 0
        self.right_slider.collide_bodies = False
        self.space.add(self.right_slider)

        self.pivot_1 = pymunk.PivotJoint(self.cart.body, self.pole_1.body, (0, 0), (-self.pole_1_length/2, 0))
        self.pivot_1.error_bias = 0
        self.pivot_1.collide_bodies = False
        self.space.add(self.pivot_1)

        self.pivot_2 = pymunk.PivotJoint(self.pole_1.body, self.pole_2.body, (self.pole_1_length/2, 0), (-self.pole_2_length/2, 0))
        self.pivot_2.error_bias = 0
        self.pivot_2.collide_bodies = False
        self.space.add(self.pivot_2)

    def step(self, action):
        self.force = action[0] * self.force_scale
        self.cart.body.apply_force_at_local_point((self.force, 0), (0, 0))

        #Friction
        pymunk.Body.update_velocity(self.pole_1.body, Vec2d(0, 0), 0.999, 1/60.0)
        pymunk.Body.update_velocity(self.pole_2.body, Vec2d(0, 0), 0.999, 1/60.0)
        pymunk.Body.update_velocity(self.cart.body, Vec2d(0, 0), 0.9999, 1/60.0)

        self.space.step(1 / 60.0)
        self.current_time_step += 1

        #Reward function
        obs = self.get_observation()
        reward = 1 + 0.5*(-np.abs(obs[5])+1)

        #Penalty for loss of balance
        if np.abs(obs[1]) == 1 or np.abs(obs[2]) == 1:
            self.done = True
            reward = -50

        #Stops episode when cart hits wall
        if np.abs(obs[5]) == 1:
            self.done = True
            reward = -50

        #Stops episode, when time is up
        if self.current_time_step == self.max_time_steps:
            self.done = True

        return obs, reward, self.done, {}

    def get_observation(self):
        cart_velocity = np.clip(self.cart.body.velocity_at_local_point((0, 0))[0]/610, -1, 1)
        pole_1_angle = -9*self.pole_1.body.angle/np.pi + 4.5
        pole_1_angle = np.clip(pole_1_angle, -1, 1)
        pole_2_angle = -9*self.pole_2.body.angle/np.pi + 4.5
        pole_2_angle = np.clip(pole_2_angle, -1, 1)
        pole_1_angular_velocity = np.clip(self.pole_1.body.angular_velocity/15, -1, 1)
        pole_2_angular_velocity = np.clip(self.pole_2.body.angular_velocity/15, -1, 1)

        #calculatng distance from target line
        x = self.cart.body.position[0]
        if x < self.target:
            distance_x = np.clip((x/(self.target-40) - self.target/(self.target-40)) , -1, 0)
        else:
            distance_x = np.clip((-x/(self.target-760) + self.target/(self.target-760)) , 0, 1)

        return np.array([cart_velocity, pole_1_angle, pole_2_angle, pole_1_angular_velocity, pole_2_angular_velocity, distance_x])

    def render(self, mode='human', close=False):
        x, y = self.cart.body.position
        pivot_point = self.pole_1.body.local_to_world([self.pole_1_length/2, 0])
        scale = 1.0/12

        pygame_events()

        self.screen.fill((243, 243, 243))
        pygame.draw.line(self.screen, (149, 165, 166), (400, 0), (400, 800), 1)

        x_prim = x + (self.pole_1_length+25) * np.cos(7*np.pi/18)
        y_prim = y + (self.pole_1_length+25) * np.sin(7*np.pi/18)
        pygame.draw.line(self.screen, (255, 26, 26), (x, y), (x_prim, 800-y_prim), 4)
        x_prim = x + (self.pole_1_length+25) * np.cos(11*np.pi/18)
        y_prim = y + (self.pole_1_length+25) * np.sin(11*np.pi/18)
        pygame.draw.line(self.screen, (255, 26, 26), (x, y), (x_prim, 800-y_prim), 4)

        x_prim = pivot_point[0] + (self.pole_2_length+25) * np.cos(7*np.pi/18)
        y_prim = pivot_point[1] + (self.pole_2_length+25) * np.sin(7*np.pi/18)
        pygame.draw.line(self.screen, (255, 26, 26), (pivot_point[0], 800-pivot_point[1]), (x_prim, 800-y_prim), 4)
        x_prim = pivot_point[0] + (self.pole_2_length+25) * np.cos(11*np.pi/18)
        y_prim = pivot_point[1] + (self.pole_2_length+25) * np.sin(11*np.pi/18)
        pygame.draw.line(self.screen, (255, 26, 26), (pivot_point[0], 800-pivot_point[1]), (x_prim, 800-y_prim), 4)

        self.space.debug_draw(self.draw_options)

        pygame.draw.circle(self.screen, (33, 93, 191), (x, y), 5)
        pygame.draw.circle(self.screen, (66, 135, 245), (pivot_point[0], 800-pivot_point[1]), 5)
        pygame.draw.line(self.screen, (179,179,179), (x-scale*self.force_scale, 399), (x+scale*self.force_scale, 399), 4)

        if self.force != 0:
            pygame.draw.line(self.screen, (255,0,0), (x, 399), (x+scale*self.force, 399), 4)

        pygame.display.flip()
        self.clock.tick(60)

    def reset(self):
        self.__init__(self.render_sim, self.max_time_steps)
        return self.get_observation()

    def close(self):
        pygame.quit()
