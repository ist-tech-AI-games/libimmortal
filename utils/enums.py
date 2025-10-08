class ActionIndex:
    MOVE_UP = 0
    MOVE_LEFT = 1
    MOVE_DOWN = 2
    MOVE_RIGHT = 3
    ATTACK_UP = 4
    ATTACK_LEFT = 5
    ATTACK_DOWN = 6
    ATTACK_RIGHT = 7

class ObservationIndex:
    GRAPHIC = 0
    VECTOR = 1

class VectorObservationPlayerIndex:
    PLAYER_POSITION_X = 0
    PLAYER_POSITION_Y = 1
    PLAYER_VELOCITY_X = 2
    PLAYER_VELOCITY_Y = 3
    PLAYER_CULULATED_DAMAGE = 4
    PLAYER_IS_ACTIONABLE = 5
    PLAYER_IS_HITTING = 6
    PLAYER_IS_DOBBLE_JUMP_AVAILABLE = 7
    PLAYER_IS_ATTACKABLE = 8
    GOAL_POSITION_X = 9
    GOAL_POSITION_Y = 10
    GOAL_PLAYER_DISTANCE = 11
    TIME_ELAPSED = 12

class VectorObservationEnemyIndex:
    ENEMY_TYPE_SKELETON = 0
    ENEMY_TYPE_BOMBKID = 1
    ENEMY_TYPE_TURRET = 2
    ENEMY_POSITION_X = 3
    ENEMY_POSITION_Y = 4
    ENEMY_VELOCITY_X = 5
    ENEMY_VELOCITY_Y = 6
    ENEMY_HEALTH = 7
    ENEMY_STATE = 8

class GraphicObservationColorMap:
    BLANK = [0, 0, 0]               # Black
    WALL = [0, 0, 255]              # Blue
    PLATFORM = [113, 69, 1]         # Purple
    TURRET = [179, 0, 255]          # Magenta
    BOMBKID = [255, 2, 0]           # Red
    SKELETON = [255, 255, 255]      # White
    ARROW = [255, 255, 0]           # Yellow
    EXPLOSION = [255, 127, 0]       # Orange
    KNIGHT = [4, 255, 210]          # Cyan
    GOAL = [2, 255, 0]              # Green
    KNIGHT_ATTACK = [128, 128, 204] # Light Blue

__all__ = [
    "ActionIndex",
    "ObservationIndex",
    "VectorObservationPlayerIndex",
    "VectorObservationEnemyIndex",
    "GraphicObservationColorMap",
]