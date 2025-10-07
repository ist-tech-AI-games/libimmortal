import numpy as np
from mlagents_envs.environment import UnityEnvironment, ActionTuple
from mlagents_envs.side_channel.engine_configuration_channel import EngineConfigurationChannel
from mlagents_envs.side_channel.environment_parameters_channel import EnvironmentParametersChannel
from mlagents_envs.envs.unity_gym_env import UnityToGymWrapper

class ImmortalSufferingEnv:
    def __init__(
        self, 
        game_path: str,  # Path to the Unity executable
        port: int,  # Port number for the Unity environment and python api to communicate
        time_scale: float,  # Speed of the simulation, maximum 2.0
        seed: int,  # Seed that controls enemy spawn
        width: int = 720,  # Visualized game screen width
        height: int = 480,  # Visualized game screen height
        verbose: bool = False  # Whether to print logs
    ) -> None:
        self.verbose = verbose
        self._create_env(game_path, port, time_scale, seed, width, height)

    def _create_env(
        self, 
        game_path: str, 
        port: int, 
        time_scale: float, 
        seed: int, 
        width: int, 
        height: int
    ) -> None:
        
        if self.verbose:
            print(f"[INFO] Launching Unity Environment from: {game_path}")
            print(f"       Port: {port}, Time Scale: {time_scale}, Seed: {seed}")
            print("[Info] Setting up side channels...")
            
        self._engine_channel = EngineConfigurationChannel()
        self._env_parameter_channel = EnvironmentParametersChannel()
        
        if self.verbose:
            print("[INFO] Starting Unity Environment...")
        
        self._unity_env = UnityEnvironment(
            file_name=game_path,
            base_port=port,
            no_graphics=False,
            side_channels=[self._engine_channel, self._env_parameter_channel],  # <-- 여기 중요!
        )

        if self.verbose:
            print("[INFO] Configuring environment parameters...")
        
        self._engine_channel.set_configuration_parameters(
            time_scale=time_scale,
            target_frame_rate=-1,
            capture_frame_rate=0,
            width=width,
            height=height,
            quality_level=0
        )

        if self.verbose:
            print(f"[INFO] Setting environment seed to {seed}...")
        self._env_parameter_channel.set_float_parameter("seed", float(seed))

        if self.verbose:
            print("[INFO] Wrapping Unity Environment with Gym Wrapper...")
        
        self.env = UnityToGymWrapper(
            self._unity_env,
            uint8_visual=True,
            flatten_branched=False,
            allow_multiple_obs=True  # To get graphic observation and vector observation together
        )
        
    def reset(self) -> np.ndarray:
        if self.verbose:
            print("[INFO] Resetting environment...")
            
        return self.env.reset()
    
    def parse_observation(self, observation: np.ndarray) -> np.ndarray:
        return {
            "graphic": observation[0],  # Graphic observation
            "vector": observation[1]    # Vector observation
        }

    def step(self, action: np.ndarray) -> tuple[dict[str, np.ndarray], float, bool, dict]:
        observation, reward, done, info = self.env.step(action)
        observation = self.parse_observation(observation)
        
        return observation, reward, done, info

    def close(self) -> None:
        if self.verbose:
            print("[INFO] Closing environment...")
            
        self.env.close()