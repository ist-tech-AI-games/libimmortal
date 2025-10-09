# libimmortal: 2025 IST-TECH AI Video Game Project

## Introduction
This is the Python Gym-like API for video game **"Immortal suffering"**
Make an AI Agent that take out various enemies and reach the goalpoint as fast as possible.

## Installation

### For windows

1. Download window build of [immortal suffering](https://github.com/ist-tech-AI-games/immortal_suffering/releases/download/v.1.0/immortal_suffering_windows_x86_64.zip)

2. Unzip the immortal_suffering_windows_x86_64.zip

3. Import conda virtual environment (this might take a while...)
```
conda env create -f libimmortal.yaml -n <env_name_here>
```

4. Install libimmortal
```
pip install -e .
```

5. Install pytorch that are compatible with you local gpu

### For Linux
1. Build docker image
```sh
docker build -t libimmortal:1.0 .
```

2. create docker container
```sh
docker compose up -d
```

3. Access docker container
## Content
```sh
.
├── docker
│   └── start_xvfb.sh
├── docker-compose.yml
├── Dockerfile
├── env.py  # This is the environment file
├── __init__.py
├── libimmortal.yaml
├── README.md
├── requirements.txt
├── samples
│   ├── agents.py  # Sample agent will be located here (WIP)
│   └── __init__.py
└── utils
    ├── aux_func.py  # auxilary functions such as feature extraction or finding free ports are located here
    ├── enums.py  # enums that are useful for feature extraction are located here
    ├── __init__.py
    └── obs_limits.py  # limit values for normailization are located here
```
## How to run
```python
from libimmortal import ImmortalSufferingEnv
from libimmortal.utils import colormap_to_ids_and_onehot

env = ImmortalSufferingEnv(
    game_path=args.game_path,  # Put you game path here. (For windows, <path -for-Immortal Suffering.exe>. For linux, <path-for immortal_suffering_linux_build.x86_64>)
    port=args.port,  # you can use immortal_suffering.utils.aux_func.find_free_tcp_port() to find free usable port 
    time_scale=args.time_scale,  # 1.0~2.0 is recommended
    seed=args.seed,  # integer seed that determines enemy spawn position and type
    width=args.width,  # Game play screen width (only for visualization)
    height=args.height,  # Game play screen height (only for visualization)
    verbose=args.verbose,  # Whether to print logs or not
)

MAX_STEPS = args.max_steps
obs = env.reset()
graphic_obs, vector_obs = obs["graphic"], obs["vector"]
    id_map, graphic_obs = colormap_to_ids_and_onehot(
        graphic_obs
    )  # one-hot encoded graphic observation

for _ in tqdm.tqdm(range(MAX_STEPS), desc="Stepping through environment"):
    action = env.env.action_space.sample()  # Change here with your AI agent
    obs, reward, done, info = env.step(action)
    graphic_obs, vector_obs = obs["graphic"], obs["vector"]
    id_map, graphic_obs = colormap_to_ids_and_onehot(
        graphic_obs
    )  # one-hot encoded graphic observation

env.close()
```

## Tips for Reinforcement Learning
1. **Parallel episode collection**  
Included parallel processing library **"ray"**.  
Immortal suffering supports parallel running.
2. **Reward shaping**  
The default reward only gives 1 when goal is reached, else 0.  
Modify reward fucntion using given observations.
3. **Feature extraction**  
Both graphic observation and vector observation are provided in obs.
4. **Monitor training process with visualization**  
Included training visualizing library "tensorflow" and "wandb"