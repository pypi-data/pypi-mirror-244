import os
import numpy as np
import gymnasium as gym
from gymnasium import Wrapper, spaces
import gymize

from paiagym import PAIAGame, PAIAWrapper, GameData
from paiagym.config import ENV, bool_ENV

def kart_env(file_name: str=None, render_mode: str=None):
    observation_space = spaces.Dict(
        {
            # The RaySensor is composed of the distance to the hit object and hit object
			# The item that Raycast hit, record it will a specific item number.
			# RayHit
			# 0: No hit
			# 1: Wall
			# 2: Car
			# 3: Gas
			# 4: Wheel
			# 5: Nitro
			# 6: Turtle
			# 7: Banana
            'RaySensor': spaces.Dict(
                {
                    'Front': spaces.Dict(
                        {
                            'Distance': spaces.Box(low=0, high=np.inf, shape=(1,), dtype=np.float32),
                            'Hit': spaces.Discrete(8)
                        }
                    ),
                    'FrontRight': spaces.Dict(
                        {
                            'Distance': spaces.Box(low=0, high=np.inf, shape=(1,), dtype=np.float32),
                            'Hit': spaces.Discrete(8)
                        }
                    ),
                    'FrontLeft': spaces.Dict(
                        {
                            'Distance': spaces.Box(low=0, high=np.inf, shape=(1,), dtype=np.float32),
                            'Hit': spaces.Discrete(8)
                        }
                    ),
                    'Left': spaces.Dict(
                        {
                            'Distance': spaces.Box(low=0, high=np.inf, shape=(1,), dtype=np.float32),
                            'Hit': spaces.Discrete(8)
                        }
                    ),
                    'Right': spaces.Dict(
                        {
                            'Distance': spaces.Box(low=0, high=np.inf, shape=(1,), dtype=np.float32),
                            'Hit': spaces.Discrete(8)
                        }
                    ),
                    'Back': spaces.Dict(
                        {
                            'Distance': spaces.Box(low=0, high=np.inf, shape=(1,), dtype=np.float32),
                            'Hit': spaces.Discrete(8)
                        }
                    ),
                    'BackRight': spaces.Dict(
                        {
                            'Distance': spaces.Box(low=0, high=np.inf, shape=(1,), dtype=np.float32),
                            'Hit': spaces.Discrete(8)
                        }
                    ),
                    'BackLeft': spaces.Dict(
                        {
                            'Distance': spaces.Box(low=0, high=np.inf, shape=(1,), dtype=np.float32),
                            'Hit': spaces.Discrete(8)
                        }
                    )
                }
                
            ),
            # The image that camera captures, include front and back:
            'CameraFront': spaces.Box(low=0, high=255, shape=(112, 252, 3), dtype=np.uint8),
            'CameraBack': spaces.Box(low=0, high=255, shape=(112, 252, 3), dtype=np.uint8),
            # A floating point number that shows the current progress:
			'Progress': spaces.Box(low=-1, high=1, shape=(1,), dtype=np.float32),
			# A floating point number that shows how much time has been used:
			'UsedTime': spaces.Box(low=0, high=np.inf, shape=(1,), dtype=np.float32),
			# A floating point number that shows current velocity:
			'Velocity': spaces.Box(low=0, high=np.inf, shape=(1,), dtype=np.float32),
			# The amount of refill remains, refills = (gas, wheels):
			'RefillRemaining': spaces.Box(low=0, high=1, shape=(2,), dtype=np.float32),
			# The number of effect remains, effects = (nitro, banana, turtle):
			'EffectRemaining': spaces.Box(low=0, high=np.iinfo(np.int32).max, shape=(3,), dtype=np.int32)
        }
    )

    action_space = spaces.Dict(
        {
            'Acceleration': spaces.Box(low=0, high=1, dtype=np.bool_),
            'Brake': spaces.Box(low=0, high=1, dtype=np.bool_),
            'Steering': spaces.Box(low=-1, high=1, dtype=np.float32),
        }
    )

    env = gym.make('gymize/Unity-v0', env_name='kart3d', file_name=file_name, observation_space=observation_space, action_space=action_space, render_mode=render_mode)
    
    return env


class KartWrapper(Wrapper):
    def __init__(self, env):
        super().__init__(env)

        self.observation_space = spaces.Dict(
            {
                # Rays: Front 0, FrontRight 1, FrontLeft 2, Left 3, Right 4, Back 5, BackRight 6, BackLeft 7
                'RaySensor': spaces.Box(low=0, high=np.inf, shape=(8,), dtype=np.float32),
                # The image that camera captures, include front and back:
                'CameraFront': spaces.Box(low=0, high=255, shape=(112, 252, 3), dtype=np.uint8),
                'CameraBack': spaces.Box(low=0, high=255, shape=(112, 252, 3), dtype=np.uint8),
                # A floating point number that shows the current progress:
                'Progress': spaces.Box(low=-1, high=1, shape=(1,), dtype=np.float32),
                # A floating point number that shows how much time has been used:
                'UsedTime': spaces.Box(low=0, high=np.inf, shape=(1,), dtype=np.float32),
                # A floating point number that shows current velocity:
                'Velocity': spaces.Box(low=0, high=np.inf, shape=(1,), dtype=np.float32),
                # The amount of refill remains, refills = (gas, wheels):
                'RefillRemaining': spaces.Box(low=0, high=1, shape=(2,), dtype=np.float32),
                # The number of effect remains, effects = (nitro, banana, turtle):
                'EffectRemaining': spaces.Box(low=0, high=np.iinfo(np.int32).max, shape=(3,), dtype=np.int32)
            }
        )
        self.action_space = spaces.Discrete(3) # 0: Left, 1: Foward, 2: Right

        self.action_mapping = [
            { 'Acceleration': False, 'Brake': False, 'Steering': -1.0 },
            { 'Acceleration': True, 'Brake': False, 'Steering': 0.0 },
            { 'Acceleration': False, 'Brake': False, 'Steering': 1.0 }
        ]
    
    def reset(self, *, seed=None, options=None):
        observation, info = self.env.reset(seed=seed, options=options)
        obs = self._obs(observation)
        return obs, info
    
    def step(self, action):
        observation, reward, terminated, truncated, info = self.env.step(self.action_mapping[action])
        obs = self._obs(observation)
        return obs, reward, terminated, truncated, info
    
    def _obs(self, observation):
        obs = { key: value for key, value in observation.items() }
        ray_sensor = [
            observation['RaySensor']['Front']['Distance'][0],
            observation['RaySensor']['FrontRight']['Distance'][0],
            observation['RaySensor']['FrontLeft']['Distance'][0],
            observation['RaySensor']['Left']['Distance'][0],
            observation['RaySensor']['Right']['Distance'][0],
            observation['RaySensor']['Back']['Distance'][0],
            observation['RaySensor']['BackRight']['Distance'][0],
            observation['RaySensor']['BackLeft']['Distance'][0]
        ]
        obs['RaySensor'] = np.array(ray_sensor, dtype=np.float32)
        return obs


class KartInfoWrapper(Wrapper):
    def reset(self, *, seed=None, options=None):
        observation, info = self.env.reset(seed=seed, options=options)

        random_seed = ''
        if not bool_ENV('IS_PICKUP', False):
            random_seed = None
        else:
            random_seed = ENV.get('PICKUP_MAP', '')
        self.env.unwrapped.send_info(agent='', info=random_seed) # info: seed in string format, if is None: not using PickUps, if is '': using PickUps with auto random seed, if is string number, then its the fixed seed

        kart_name = ENV.get('1P_NAME', 'KART')
        self.env.unwrapped.send_info(agent='agent', info=kart_name) # info: kart name

        return observation, info


class Game(PAIAGame):
    def __init__(self, *args, **kwargs):
        self.name = 'kart3d' # for unity_path

    def make_env(self):
        env = kart_env(file_name=self.unity_path(), render_mode='video')
        env = KartWrapper(env)
        env = KartInfoWrapper(env)
        env = PAIAWrapper(env, on_step=self.on_step)
        return env
    
    def unity_path(self):
        return super().unity_path(os.path.dirname(__file__))
    
    def on_step(self, env, game_data: GameData):
        # return the game result
        if game_data.observation is not None:
            return {
                'progress': float(game_data.observation['Progress']),
                'used_time': float(game_data.observation['UsedTime'])
            }
        else:
            return None