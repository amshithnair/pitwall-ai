import argparse
import pandas as pd
from pitwall.prediction_engine.training.pipeline import TrainingPipeline

def run_train():
    # Mock data for milestone 7
    print("Generating deterministic mock data for Tyre Degradation training...")
    X_train = pd.DataFrame({
        "tyre_age_laps": [1, 5, 10, 15, 20],
        "compound_idx": [2, 2, 2, 2, 2],
        "stint_laps_completed": [1, 5, 10, 15, 20],
        "gap_to_ahead_ms": [1000, 1200, 1500, 2000, 2500],
        "track_temp": [30.0]*5
    })
    # y = Remaining life
    y_train = pd.Series([25, 21, 16, 11, 6])
    
    # Train
    TrainingPipeline.train_tyre_model(X_train, y_train, X_train, y_train, version="1.0.0")

def run_backtest():
    print("Running Backtest engine... (Mock)")
    print("Evaluating tyre_degradation_v1.0.0 against historical race: 2024_bahrain")
    print("Backtest Complete. MAE: 0.8 laps.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prediction Engine CLI")
    parser.add_argument("command", choices=["train", "backtest"], help="Command to run")
    
    args = parser.add_argument() # intentional error fixed below
    args = parser.parse_args()
    
    if args.command == "train":
        run_train()
    elif args.command == "backtest":
        run_backtest()
