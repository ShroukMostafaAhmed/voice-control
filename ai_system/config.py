"""
Configuration for ML Training
Customize these settings for your needs
"""

# ==================== DATA GENERATION ====================

# Number of training samples to generate
NUM_SAMPLES = 50000  # Increase for better accuracy (100k, 200k, etc.)

# Output file for training data
TRAINING_DATA_FILE = 'training_data.csv'

# Scenario probabilities (must sum to ~1.0)
SCENARIO_PROBABILITIES = {
    'fire_emergency': 0.01,        # 1% - Critical
    'extreme_heat': 0.02,          # 2% - High danger
    'possible_gas_leak': 0.005,    # 0.5% - High danger
    'intrusion_detected': 0.02,    # 2% - High danger
    'morning_routine': 0.10,       # 10% - Normal
    'hot_weather': 0.15,           # 15% - Normal
    'cold_weather': 0.10,          # 10% - Normal
    'night_mode': 0.10,            # 10% - Normal
    'no_activity': 0.15,           # 15% - Normal
    'dark_room_activity': 0.10,    # 10% - Normal
    'high_humidity': 0.08,         # 8% - Normal
    'energy_saving': 0.10,         # 10% - Normal
    'rain_weather': 0.05,          # 5% - Normal
    'normal_operation': 0.02,      # 2% - Low
}

# Temperature ranges (Celsius)
TEMP_MIN = 15
TEMP_MAX = 40
TEMP_COMFORTABLE = 24

# Humidity ranges (%)
HUMIDITY_MIN = 30
HUMIDITY_MAX = 70

# Light level ranges (lux)
LIGHT_DAY_MIN = 300
LIGHT_DAY_MAX = 800
LIGHT_NIGHT_MIN = 10
LIGHT_NIGHT_MAX = 100

# ==================== MODEL TRAINING ====================

# Test/Train split
TEST_SIZE = 0.2  # 20% for testing, 80% for training

# Random Forest parameters
RF_N_ESTIMATORS = 100      # Number of trees (increase for better accuracy)
RF_MAX_DEPTH = 15          # Maximum depth of trees
RF_MIN_SAMPLES_SPLIT = 10  # Minimum samples to split
RF_MIN_SAMPLES_LEAF = 5    # Minimum samples in leaf
RF_RANDOM_STATE = 42       # For reproducibility

# Gradient Boosting parameters (for scenario classifier)
GB_N_ESTIMATORS = 100
GB_MAX_DEPTH = 10
GB_RANDOM_STATE = 42

# Confidence threshold for predictions
CONFIDENCE_THRESHOLD = 0.6  # Only act if confidence > 60%

# Models directory
MODELS_DIR = 'models'

# ==================== DEVICES ====================

# All devices in the smart home
DEVICES = [
    'bath_light', 'bath_heater', 'bath_fan',
    'corr_main_light', 'corr_spots',
    'rec_light', 'rec_window', 'rec_sound', 'rec_ac',
    'out_camera', 'out_light', 'out_door',
    'r1_ac', 'r1_tv', 'r1_light', 'r1_window', 'r1_sound',
    'kit_light', 'kit_window', 'kit_fan',
    'r2_ac', 'r2_sound', 'r2_light'
]

# Device energy consumption (watts)
DEVICE_ENERGY = {
    'light': 60,
    'ac': 1500,
    'heater': 2000,
    'fan': 75,
    'window': 10,
    'sound': 50,
    'tv': 150,
    'camera': 15,
    'door': 20
}

# ==================== SCENARIOS ====================

# Danger levels
DANGER_LEVELS = {
    'low': 0,
    'normal': 1,
    'high': 2,
    'critical': 3
}

# Action priorities (1-10, 10 is highest)
ACTION_PRIORITIES = {
    'fire_emergency': 10,
    'extreme_heat': 9,
    'possible_gas_leak': 9,
    'intrusion_detected': 8,
    'morning_routine': 5,
    'hot_weather': 6,
    'cold_weather': 5,
    'night_mode': 4,
    'no_activity': 3,
    'dark_room_activity': 5,
    'high_humidity': 4,
    'energy_saving': 3,
    'rain_weather': 4,
    'normal_operation': 1
}

# ==================== FEATURES ====================

# Feature columns for ML model
FEATURE_COLUMNS = [
    'hour',
    'day_of_week',
    'month',
    'is_weekend',
    'temperature',
    'humidity',
    'motion_detected',
    'light_level',
    'smoke_detected',
    'user_present',
    'outdoor_temp',
    'rain'
]

# ==================== LOGGING ====================

# Enable verbose logging
VERBOSE = True

# Log file
LOG_FILE = 'ai_training.log'

# ==================== ADVANCED ====================

# Use parallel processing
USE_PARALLEL = True  # Set to False if you have memory issues

# Number of CPU cores to use (-1 = all cores)
N_JOBS = -1

# Memory optimization
LOW_MEMORY_MODE = False  # Set to True for large datasets

# Feature scaling method
SCALER_METHOD = 'standard'  # 'standard', 'minmax', or 'robust'

# Cross-validation folds
CV_FOLDS = 5

# Early stopping for gradient boosting
EARLY_STOPPING = True
EARLY_STOPPING_ROUNDS = 10

# ==================== VALIDATION ====================

# Minimum accuracy threshold
MIN_ACCURACY = 0.70  # 70% minimum

# Warn if accuracy is below this
WARN_ACCURACY = 0.85  # 85%

# ==================== EXPORT ====================

# Export format for models
MODEL_FORMAT = 'pkl'  # 'pkl' or 'joblib'

# Compress models
COMPRESS_MODELS = True

# Include metadata
INCLUDE_METADATA = True

# ==================== HELPER FUNCTIONS ====================

def get_device_type(device_id):
    """Get device type from device ID"""
    if 'light' in device_id:
        return 'light'
    elif 'ac' in device_id:
        return 'ac'
    elif 'heater' in device_id:
        return 'heater'
    elif 'fan' in device_id:
        return 'fan'
    elif 'window' in device_id:
        return 'window'
    elif 'sound' in device_id:
        return 'sound'
    elif 'tv' in device_id:
        return 'tv'
    elif 'camera' in device_id:
        return 'camera'
    elif 'door' in device_id:
        return 'door'
    return 'unknown'

def get_device_energy(device_id):
    """Get energy consumption for device"""
    device_type = get_device_type(device_id)
    return DEVICE_ENERGY.get(device_type, 0)

def validate_config():
    """Validate configuration"""
    errors = []
    
    # Check probabilities sum to ~1.0
    prob_sum = sum(SCENARIO_PROBABILITIES.values())
    if not (0.95 <= prob_sum <= 1.05):
        errors.append(f"Scenario probabilities sum to {prob_sum:.2f}, should be ~1.0")
    
    # Check temperature ranges
    if TEMP_MIN >= TEMP_MAX:
        errors.append("TEMP_MIN must be less than TEMP_MAX")
    
    # Check test size
    if not (0 < TEST_SIZE < 1):
        errors.append("TEST_SIZE must be between 0 and 1")
    
    # Check confidence threshold
    if not (0 < CONFIDENCE_THRESHOLD < 1):
        errors.append("CONFIDENCE_THRESHOLD must be between 0 and 1")
    
    if errors:
        print("❌ Configuration errors:")
        for error in errors:
            print(f"   - {error}")
        return False
    
    return True

# Validate on import
if __name__ == "__main__":
    if validate_config():
        print("✅ Configuration is valid")
    else:
        print("❌ Configuration has errors")
