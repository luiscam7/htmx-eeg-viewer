"""Serve synthetic raw EEG data for testing."""

from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import Dict, List

from synthesis import SyntheticEDFWriter


class EEGDataEpoch(BaseModel):
    data: Dict[str, List[float]]
    epoch: int
    total_epochs: int


app = FastAPI()

@app.get("/eeg-epoch", response_model=EEGDataEpoch)
async def get_eeg_epoch(epoch: int = Query(1, ge=1)):
    synth = SyntheticEDFWriter(n_seconds=600, fs=100)
    synth.generate_synthetic_eeg()
    
    df = synth.df
    fs = 100  # Sampling frequency
    epoch_duration = 30  # 30-second epochs
    samples_per_epoch = fs * epoch_duration
    total_records = len(df)
    total_epochs = total_records // samples_per_epoch
    
    if epoch > total_epochs:
        raise HTTPException(status_code=404, detail="Epoch out of range")
    
    # Calculate the start and end indices for the given epoch
    start = (epoch - 1) * samples_per_epoch
    end = start + samples_per_epoch

    # Slice the dataframe based on start and end indices
    epoch_df = df.iloc[start:end]

    # Convert the epoch to dictionary
    epoch_data = epoch_df.to_dict(orient="list")
    
    return EEGDataEpoch(
        data=epoch_data,
        epoch=epoch,
        total_epochs=total_epochs
    )
