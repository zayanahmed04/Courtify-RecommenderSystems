"""
Script: train_model.py
Trains the matchmaking Random Forest model. Generates data first if needed.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path


DATASET_PATH = "data/processed/matchmaking_dataset.csv"
MODEL_PATH = "data/models/matcher_model.pkl"
ENCODERS_PATH = "data/models/label_encoders.pkl"
SCALER_PATH = "data/models/scaler.pkl"


def main():
    if not Path(DATASET_PATH).exists():
        print(f"[train] Dataset not found at {DATASET_PATH}. Generating...")
        from app.services.matchmaking.dataset_generator import generate_dataset
        generate_dataset(output_path=DATASET_PATH)

    from app.services.matchmaking.trainer import ModelTrainer

    print("[train] Starting training pipeline...")
    trainer = ModelTrainer()
    metrics = trainer.train(
        dataset_path=DATASET_PATH,
        model_output_path=MODEL_PATH,
        encoders_output_path=ENCODERS_PATH,
        scaler_output_path=SCALER_PATH,
    )

    print(f"\n✅  Training complete.")
    print(f"    Accuracy : {metrics['accuracy']:.4f}")
    print(f"    Model    : {metrics['model_path']}")


if __name__ == "__main__":
    main()
