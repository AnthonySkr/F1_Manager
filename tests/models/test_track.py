# --- Tests pour la méthode __str__ ---


def test_track_str_representation(street_track):
    """Test the string representation of a Track object."""
    assert str(street_track) == "Monaco GP - Monte Carlo, Monaco"


# --- Tests pour la méthode get_info_display ---


def test_get_info_display_street(street_track):
    """Test get_info_display for a street track."""
    expected_output = (
        "=======================================================\n"
        "  Monaco GP\n"
        "  Monte Carlo, Monaco\n"
        "=======================================================\n"
        "  Type: Street\n"
        "  Laps: 78\n"
        "  DRS Zones: 1\n"
        "  Overtaking: Hard\n"
        "  Tire Wear: Medium\n"
        "  Key Attributes: CHASSIS crucial, Downforce important"
    )
    assert street_track.get_info_display() == expected_output


def test_get_info_display_high_downforce(high_downforce_track):
    """Test get_info_display for a high downforce track."""
    expected_output = (
        "=======================================================\n"
        "  Hungaroring\n"
        "  Budapest, Hungary\n"
        "=======================================================\n"
        "  Type: Highdownforce\n"
        "  Laps: 70\n"
        "  DRS Zones: 2\n"
        "  Overtaking: Hard\n"
        "  Tire Wear: High\n"
        "  Key Attributes: DOWNFORCE crucial, Chassis important"
    )
    assert high_downforce_track.get_info_display() == expected_output


def test_get_info_display_power(power_track):
    """Test get_info_display for a power track."""
    expected_output = (
        "=======================================================\n"
        "  Monza\n"
        "  Monza, Italy\n"
        "=======================================================\n"
        "  Type: Power\n"
        "  Laps: 53\n"
        "  DRS Zones: 2\n"
        "  Overtaking: Easy\n"
        "  Tire Wear: Low\n"
        "  Key Attributes: POWER UNIT crucial, Aero Efficiency helps"
    )
    assert power_track.get_info_display() == expected_output


def test_get_info_display_balanced(balanced_track):
    """Test get_info_display for a balanced track."""
    expected_output = (
        "=======================================================\n"
        "  Silverstone\n"
        "  Silverstone, United Kingdom\n"
        "=======================================================\n"
        "  Type: Balanced\n"
        "  Laps: 52\n"
        "  DRS Zones: 2\n"
        "  Overtaking: Medium\n"
        "  Tire Wear: Medium\n"
        "  Key Attributes: All-round car needed, Aero Efficiency key"
    )
    assert balanced_track.get_info_display() == expected_output


# --- Tests pour la méthode get_downforce_bonus ---


def test_get_downforce_bonus_street(street_track):
    """Test downforce bonus for a street track."""
    assert street_track.get_downforce_bonus() == 1.2


def test_get_downforce_bonus_high_downforce(high_downforce_track):
    """Test downforce bonus for a high downforce track."""
    assert high_downforce_track.get_downforce_bonus() == 1.3


def test_get_downforce_bonus_power(power_track):
    """Test downforce bonus for a power track."""
    assert power_track.get_downforce_bonus() == 0.8


def test_get_downforce_bonus_balanced(balanced_track):
    """Test downforce bonus for a balanced track."""
    assert balanced_track.get_downforce_bonus() == 1.0


# --- Tests pour la méthode get_power_bonus ---


def test_get_power_bonus_street(street_track):
    """Test power bonus for a street track."""
    assert street_track.get_power_bonus() == 0.8


def test_get_power_bonus_high_downforce(high_downforce_track):
    """Test power bonus for a high downforce track."""
    assert high_downforce_track.get_power_bonus() == 0.9


def test_get_power_bonus_power(power_track):
    """Test power bonus for a power track."""
    assert power_track.get_power_bonus() == 1.3


def test_get_power_bonus_balanced(balanced_track):
    """Test power bonus for a balanced track."""
    assert balanced_track.get_power_bonus() == 1.0
