"""
Smart Home Single Model Trainer
Train ONE model to predict ALL device states at once
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.multioutput import MultiOutputClassifier
import joblib
import json
from datetime import datetime
import os

class SingleModelTrainer:
    """Train one model to predict all devices"""
    
    def __init__(self, data_file='training_data.csv'):
        self.data_file = data_file
        self.model = None
        self.scaler = None
        self.feature_columns = []
        self.device_columns = []
        
    def load_data(self):
        """Load training data"""
        print(f"📂 Loading data from {self.data_file}...")
        
        if not os.path.exists(self.data_file):
            print(f"❌ Error: {self.data_file} not found!")
            print("   Please run 'python data_generator.py' first")
            return None
        
        self.df = pd.read_csv(self.data_file)
        print(f"   ✓ Loaded {len(self.df):,} samples")
        print(f"   ✓ Columns: {len(self.df.columns)}")
        return self.df
    
    def prepare_features(self):
        """Prepare features for training"""
        print("\n🔧 Preparing features...")
        
        # Feature columns (inputs)
        self.feature_columns = [
            'hour', 'day_of_week', 'month', 'is_weekend',
            'temperature', 'humidity', 'motion_detected',
            'light_level', 'smoke_detected', 'user_present',
            'outdoor_temp', 'rain'
        ]
        
        # Device columns (outputs to predict)
        self.device_columns = [col for col in self.df.columns if col.endswith('_status')]
        
        print(f"   ✓ Features: {len(self.feature_columns)}")
        print(f"   ✓ Devices to predict: {len(self.device_columns)}")
        
        # Extract features
        X = self.df[self.feature_columns].values
        
        # Extract all device states as multi-output
        y = self.df[self.device_columns].values
        
        # Scale features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        return X_scaled, y
    
    def train_model(self, X, y, test_size=0.2):
        """Train ONE model for ALL devices"""
        print(f"\n🤖 Training SINGLE model for {len(self.device_columns)} devices...")
        print(f"   Test size: {test_size*100}%")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        print(f"   Training samples: {len(X_train):,}")
        print(f"   Test samples: {len(X_test):,}")
        
        # Create Multi-Output Random Forest
        print("\n   Training model (this may take a few minutes)...")
        
        base_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=10,
            min_samples_leaf=5,
            random_state=42,
            n_jobs=-1,
            verbose=0
        )
        
        # Multi-output wrapper
        self.model = MultiOutputClassifier(base_model, n_jobs=-1)
        
        # Train
        self.model.fit(X_train, y_train)
        
        print("   ✓ Training complete!")
        
        # Evaluate
        print("\n📊 Evaluating model...")
        y_pred = self.model.predict(X_test)
        
        # Calculate accuracy for each device
        accuracies = []
        print("\n   Device Accuracies:")
        for i, device_col in enumerate(self.device_columns):
            device_name = device_col.replace('_status', '')
            accuracy = accuracy_score(y_test[:, i], y_pred[:, i])
            accuracies.append(accuracy)
            print(f"      {device_name:20s}: {accuracy*100:6.2f}%")
        
        avg_accuracy = np.mean(accuracies)
        print(f"\n   ✓ Average Accuracy: {avg_accuracy*100:.2f}%")
        
        return avg_accuracy
    
    def save_model(self, output_dir='models'):
        """Save the single model"""
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\n💾 Saving model to {output_dir}/...")
        
        # Save the single model
        joblib.dump(self.model, f"{output_dir}/smart_home_model.pkl")
        print(f"   ✓ Saved smart_home_model.pkl")
        
        # Save scaler
        joblib.dump(self.scaler, f"{output_dir}/scaler.pkl")
        print(f"   ✓ Saved scaler.pkl")
        
        # Save metadata
        metadata = {
            'trained_at': datetime.now().isoformat(),
            'model_type': 'single_multi_output',
            'num_samples': len(self.df),
            'feature_columns': self.feature_columns,
            'device_columns': self.device_columns,
            'num_devices': len(self.device_columns)
        }
        
        with open(f"{output_dir}/metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"   ✓ Saved metadata.json")
    
    def test_prediction(self, X):
        """Test prediction on sample scenarios"""
        print("\n🧪 Testing predictions on sample scenarios:")
        print("=" * 70)
        
        # Test scenarios
        test_cases = [
            {
                'name': '🔥 Fire Emergency',
                'features': [12, 3, 6, 0, 35, 50, 1, 300, 1, 1, 30, 0]  # smoke=1
            },
            {
                'name': '☀️ Hot Day',
                'features': [14, 2, 7, 0, 32, 45, 1, 600, 0, 1, 35, 0]  # temp=32
            },
            {
                'name': '🌙 Night Mode',
                'features': [23, 4, 3, 0, 22, 50, 1, 50, 0, 1, 18, 0]  # hour=23
            },
            {
                'name': '🌅 Morning Routine',
                'features': [7, 1, 4, 0, 20, 55, 1, 200, 0, 1, 18, 0]  # hour=7
            }
        ]
        
        for test_case in test_cases:
            print(f"\n📍 Scenario: {test_case['name']}")
            
            # Prepare features
            features = np.array([test_case['features']])
            features_scaled = self.scaler.transform(features)
            
            # Predict ALL device states at once
            predictions = self.model.predict(features_scaled)[0]
            
            # Show devices that should be ON
            print(f"   Devices to turn ON:")
            on_count = 0
            for i, device_col in enumerate(self.device_columns):
                device_name = device_col.replace('_status', '')
                if predictions[i] == 1:
                    print(f"      ✓ {device_name}")
                    on_count += 1
            
            if on_count == 0:
                print(f"      (All devices OFF)")
        
        print("=" * 70)


def main():
    print("=" * 70)
    print("Smart Home SINGLE Model Training")
    print("=" * 70)
    print("\nThis will train ONE model to predict ALL devices")
    print("Instead of 23 separate models")
    print()
    
    # Initialize trainer
    trainer = SingleModelTrainer('training_data.csv')
    
    # Load data
    df = trainer.load_data()
    if df is None:
        return
    
    # Prepare features
    X, y = trainer.prepare_features()
    
    # Train single model
    avg_accuracy = trainer.train_model(X, y)
    
    # Test predictions
    trainer.test_prediction(X)
    
    # Save model
    trainer.save_model()
    
    print("\n" + "=" * 70)
    print("✅ Training Complete!")
    print(f"   Average Accuracy: {avg_accuracy*100:.2f}%")
    print(f"   Model saved: models/smart_home_model.pkl")
    print("\n   Next step: The AI system will automatically use this model")
    print("=" * 70)


if __name__ == "__main__":
    main()
