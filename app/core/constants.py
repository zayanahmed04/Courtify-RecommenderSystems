SUPPORTED_SPORTS = [
    "Cricket",
    "Football",
    "Padel",
    "Badminton",
    "Basketball",
]

PLAY_STYLES = ["Aggressive", "Defensive", "Balanced"]

AGE_GROUPS = ["Teen", "Young Adult", "Adult", "Senior"]

LOCATION_ZONES = ["North", "South", "Central", "East", "West"]

# Heuristic weight defaults
HEURISTIC_WEIGHT_DISTANCE = 0.5
HEURISTIC_WEIGHT_PRICE = 0.3
HEURISTIC_WEIGHT_RATING = 0.2

# A* search
ASTAR_MAX_RESULTS = 5
ASTAR_MAX_DISTANCE_KM = 50.0

# ML
DATASET_SIZE = 1000
RANDOM_STATE = 42
TEST_SIZE = 0.2
RF_N_ESTIMATORS = 200
RF_MAX_DEPTH = 10

# Compatibility classes
COMPATIBILITY_LOW = 0
COMPATIBILITY_MID = 1
COMPATIBILITY_HIGH = 2

COMPATIBILITY_LABELS = {
    COMPATIBILITY_LOW: "Low",
    COMPATIBILITY_MID: "Mid",
    COMPATIBILITY_HIGH: "High",
}
