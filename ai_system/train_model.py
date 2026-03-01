"""
AI Model Training for Smart Home
Trains ML model on generated data to predict device actions
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import json
from datetime import datetime

class SmartHomeModelTrainer:
    def __init__(self, data_file='training_data.csv'):
        self.data_file = data_file
        self.models = {}
        self.scalers = {}
        self.feature_columns = []
        self.device_columns = []
        
    def load_data(self):
        """Load training data"""
        print(f"📂 Loading data from {self.data_file}...")
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
        
        # Scale features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        return X_scaled
    
    def train_models(self, X, test_size=0.2):
        """Train separate model for each device"""
        print(f"\n🤖 Training models for {len(self.device_columns)} devices...")
        print(f"   Test size: {test_size*100}%")
        
        results = {}
        
        for i, device_col in enumerate(self.device_columns):
            device_name = device_col.replace('_status', '')
            print(f"\n   [{i+1}/{len(self.device_columns)}] Training model for: {device_name}")
            
            # Get target
            y = self.df[device_col].values
            
            # Check class distribution
            unique, counts = np.unique(y, return_counts=True)
            print(f"      Class distribution: OFF={counts[0]:,}, ON={counts[1]:,}")
            
            # Skip if only one class
            if len(unique) < 2:
                print(f"      ⚠️  Skipping (only one class)")
                continue
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42, stratify=y
            )
            
            # Train Random Forest
            model = RandomForestClassifier(
                n_estimators=100,
                max_depth=15,
                min_samples_split=10,
                min_samples_leaf=5,
                random_state=42,
                n_jobs=-1
            )
            
            model.fit(X_train, y_train)
            
            # Evaluate
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            print(f"      ✓ Accuracy: {accuracy*100:.2f}%")
            
            # Store model
            self.models[device_name] = model
            
            # Store results
            results[device_name] = {
                'accuracy': accuracy,
                'train_samples': len(X_train),
                'test_samples': len(X_test)
            }
        
        return results
    
    def train_scenario_classifier(self, X):
        """Train model to classify scenarios"""
        print("\n🎯 Training scenario classifier...")
        
        y = self.df['scenario'].values
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train Gradient Boosting
        model = GradientBoostingClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"   ✓ Scenario classifier accuracy: {accuracy*100:.2f}%")
        
        self.scenario_model = model
        
        return accuracy
    
    def save_models(self, output_dir='models'):
        """Save trained models"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\n💾 Saving models to {output_dir}/...")
        
        # Save device models
        for device_name, model in self.models.items():
            filename = f"{output_dir}/{device_name}_model.pkl"
            joblib.dump(model, filename)
        
        # Save scenario model
        if hasattr(self, 'scenario_model'):
            joblib.dump(self.scenario_model, f"{output_dir}/scenario_model.pkl")
        
        # Save scaler
        joblib.dump(self.scaler, f"{output_dir}/scaler.pkl")
        
        # Save metadata
        metadata = {
            'trained_at': datetime.now().isoformat(),
            'num_samples': len(self.df),
            'feature_columns': self.feature_columns,
            'device_columns': self.device_columns,
            'num_models': len(self.models)
        }
        
        with open(f"{output_dir}/metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"   ✓ Saved {len(self.models)} device models")
        print(f"   ✓ Saved scenario model")
        print(f"   ✓ Saved scaler and metadata")
    
    def evaluate_models(self, X):
        """Evaluate all models"""
        print("\n📊 Model Evaluation Summary:")
        print("=" * 70)
        
        total_accuracy = 0
        count = 0
        
        for device_name, model in self.models.items():
            device_col = f"{device_name}_status"
            y = self.df[device_col].values
            
            # Split for evaluation
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            total_accuracy += accuracy
            count += 1
            
            print(f"   {device_name:20s}: {accuracy*100:6.2f}%")
        
        avg_accuracy = total_accuracy / count if count > 0 else 0
        print("=" * 70)
        print(f"   Average Accuracy: {avg_accuracy*100:.2f}%")
        
        return avg_accuracy
    
    def test_prediction(self, X):
        """Test prediction on sample data"""
        print("\n🧪 Testing predictions on sample scenarios:")
        print("=" * 70)
        
        # Test scenarios
        test_cases = [
            {
                'name': 'Fire Emergency',
                'features': [12, 3, 6, 0, 35, 50, 1, 300, 1, 1, 30, 0]  # smoke=1
            },
            {
                'name': 'Hot Day',
                'features': [14, 2, 7, 0, 32, 45, 1, 600, 0, 1, 35, 0]  # temp=32
            },
            {
                'name': 'Night Mode',
                'features': [23, 4, 3, 0, 22, 50, 1, 50, 0, 1, 18, 0]  # hour=23
            },
            {
                'name': 'Morning Routine',
                'features': [7, 1, 4, 0, 20, 55, 1, 200, 0, 1, 18, 0]  # hour=7
            }
        ]
        
        for test_case in test_cases:
            print(f"\n📍 Scenario: {test_case['name']}")
            
            # Prepare features
            features = np.array([test_case['features']])
            features_scaled = self.scaler.transform(features)
            
            # Predict scenario
            if hasattr(self, 'scenario_model'):
                scenario = self.scenario_model.predict(features_scaled)[0]
                print(f"   Detected scenario: {scenario}")
            
            # Predict device states
            print(f"   Recommended device states:")
            for device_name, model in list(self.models.items())[:10]:  # Show first 10
                prediction = model.predict(features_scaled)[0]
                if prediction == 1:
                    print(f"      ✓ {device_name}: ON")
        
        print("=" * 70)


def main():
    print("=" * 70)
    print("Smart Home AI Model Training")
    print("=" * 70)
    print()
    
    # Initialize trainer
    trainer = SmartHomeModelTrainer('training_data.csv')
    
    # Load data
    df = trainer.load_data()
    
    # Prepare features
    X = trainer.prepare_features()
    
    # Train device models
    results = trainer.train_models(X)
    
    # Train scenario classifier
    trainer.train_scenario_classifier(X)
    
    # Evaluate models
    avg_accuracy = trainer.evaluate_models(X)
    
    # Test predictions
    trainer.test_prediction(X)
    
    # Save models
    trainer.save_models()
    
    print("\n" + "=" * 70)
    print("✅ Training Complete!")
    print(f"   Average Model Accuracy: {avg_accuracy*100:.2f}%")
    print(f"   Models saved in: models/")
    print("\n   Next step: Run 'python ai_engine_ml.py' to use the trained models")
    print("=" * 70)


if __name__ == "__main__":
    main()
