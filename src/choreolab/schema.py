from __future__ import annotations

from typing import Dict, List
from pydantic import BaseModel, Field


class MovementFeatures(BaseModel):
    torso_initiation: float = Field(ge=0, le=1)
    spiral: float = Field(ge=0, le=1)
    asymmetry: float = Field(ge=0, le=1)
    weight_transfer: float = Field(ge=0, le=1)
    extension_amplitude: float = Field(ge=0, le=1)
    floorwork: float = Field(ge=0, le=1)
    level_changes: float = Field(ge=0, le=1)
    off_axis_balance: float = Field(ge=0, le=1)
    curved_arm_pathways: float = Field(ge=0, le=1)
    limb_lag: float = Field(ge=0, le=1)
    suspension: float = Field(ge=0, le=1)
    collapse: float = Field(ge=0, le=1)
    rebound: float = Field(ge=0, le=1)
    acceleration_change: float = Field(ge=0, le=1)
    travelling: float = Field(ge=0, le=1)
    momentum_causality: float = Field(ge=0, le=1)
    groove: float = Field(ge=0, le=1)
    eccentricity: float = Field(ge=0, le=1)
    gesture_evolution: float = Field(ge=0, le=1)
    virtuosity: float = Field(ge=0, le=1)


class StyleProfile(BaseModel):
    name: str
    features: MovementFeatures
    dialects: Dict[str, float] = Field(default_factory=dict)
    avoid: List[str] = Field(default_factory=list)


class Candidate(BaseModel):
    id: str
    features: MovementFeatures
    flags: List[str] = Field(default_factory=list)


class CandidateEvaluation(BaseModel):
    candidate_id: str
    score: float
    accepted: bool
    component_scores: Dict[str, float]
    penalties: Dict[str, float]
    reasons: List[str]
