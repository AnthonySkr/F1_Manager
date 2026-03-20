"""Configuration pytest et fixtures partagées."""

import pytest

from src.models import Track, TrackType


@pytest.fixture
def street_track():
    """Returns a Track instance for a street circuit."""
    return Track(
        name="Monaco GP",
        country="Monaco",
        city="Monte Carlo",
        track_type=TrackType.STREET,
        laps=78,
        base_lap_time=75.0,
        pit_loss_time=25.0,
        overtaking_difficulty=9,  # Hard
        tire_degradation=1.0,  # Medium
        drs_zones=1,
    )


@pytest.fixture
def high_downforce_track():
    """Returns a Track instance for a high downforce circuit."""
    return Track(
        name="Hungaroring",
        country="Hungary",
        city="Budapest",
        track_type=TrackType.HIGH_DOWNFORCE,
        laps=70,
        base_lap_time=78.0,
        pit_loss_time=22.0,
        overtaking_difficulty=7,  # Hard
        tire_degradation=1.3,  # High
        drs_zones=2,
    )


@pytest.fixture
def power_track():
    """Returns a Track instance for a power circuit."""
    return Track(
        name="Monza",
        country="Italy",
        city="Monza",
        track_type=TrackType.POWER,
        laps=53,
        base_lap_time=83.0,
        pit_loss_time=28.0,
        overtaking_difficulty=2,  # Easy
        tire_degradation=0.8,  # Low
        drs_zones=2,
    )


@pytest.fixture
def balanced_track():
    """Returns a Track instance for a balanced circuit."""
    return Track(
        name="Silverstone",
        country="United Kingdom",
        city="Silverstone",
        track_type=TrackType.BALANCED,
        laps=52,
        base_lap_time=90.0,
        pit_loss_time=26.0,
        overtaking_difficulty=5,  # Medium
        tire_degradation=1.1,  # Medium
        drs_zones=2,
    )
