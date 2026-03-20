import pytest

from src.models import Car

# --- Tests pour la propriété overall ---


def test_overall_base_car(base_car):
    """Test overall calculation for a base car."""
    assert base_car.overall == 51


def test_overall_high_end_car(high_end_car):
    """Test overall calculation for a high-end car."""
    assert high_end_car.overall == 93


# --- Tests pour la propriété performance ---


def test_performance_base_car(base_car):
    """Test performance calculation for a base car."""
    assert base_car.performance == pytest.approx(50.0)


def test_performance_high_end_car(high_end_car):
    """Test performance calculation for a high-end car."""
    assert high_end_car.performance == pytest.approx(93.9)


# --- Tests pour la propriété tire_wear_factor ---


def test_tire_wear_factor_excellent_cooling(base_car):
    """Test tire wear factor with excellent tire cooling."""
    base_car.tire_cooling = 100
    assert base_car.tire_wear_factor == pytest.approx(0.5)


def test_tire_wear_factor_average_cooling(base_car):
    """Test tire wear factor with average tire cooling (default)."""
    base_car.tire_cooling = 65
    assert base_car.tire_wear_factor == pytest.approx(0.85)


def test_tire_wear_factor_poor_cooling(base_car):
    """Test tire wear factor with poor tire cooling."""
    base_car.tire_cooling = 30
    assert base_car.tire_wear_factor == pytest.approx(1.2)


def test_tire_wear_factor_min_cooling(base_car):
    """Test tire wear factor with minimum tire cooling."""
    base_car.tire_cooling = 1
    assert base_car.tire_wear_factor == pytest.approx(1.49)


def test_tire_wear_factor_intermediate_cooling(base_car):
    """Test tire wear factor with an intermediate tire cooling value."""
    base_car.tire_cooling = 80
    assert base_car.tire_wear_factor == pytest.approx(0.7)


# --- Tests pour la méthode get_upgrade_cost ---


def calculate_expected_cost(start_value, points, cost_tiers):
    """Helper for cost calculation."""
    total_cost = 0
    for i in range(points):
        stat_value = start_value + i + 1
        cost_per_point = 0
        for threshold, cost in cost_tiers:
            if stat_value <= threshold:
                cost_per_point = cost
                break
        total_cost += cost_per_point
    return total_cost


def test_get_upgrade_cost_single_point_low_stat(base_car):
    """Test single point upgrade cost for a low stat."""
    assert base_car.get_upgrade_cost("downforce", 1) == 2  # 50 -> 51


def test_get_upgrade_cost_multiple_points_low_stat(base_car):
    """Test multiple points upgrade cost for a low stat."""
    assert base_car.get_upgrade_cost("downforce", 5) == 11


def test_get_upgrade_cost_across_tier_boundary(base_car):
    """Test upgrade cost crossing a tier boundary (e.g., 54 to 55)."""
    base_car.downforce = 54
    assert base_car.get_upgrade_cost("downforce", 1) == 3  # 54 -> 55


def test_get_upgrade_cost_high_stat(average_car):
    """Test upgrade cost for a high stat (e.g., 70 to 71)."""
    average_car.power_unit = 70
    assert average_car.get_upgrade_cost("power_unit", 1) == 10  # 70 -> 71


def test_get_upgrade_cost_very_high_stat(high_end_car):
    """Test upgrade cost for a very high stat (e.g., 95 to 96)."""
    high_end_car.chassis = 95
    assert high_end_car.get_upgrade_cost("chassis", 1) == 45  # 95 -> 96


def test_get_upgrade_cost_multiple_points_spanning_tiers(base_car):
    """Test upgrade cost for multiple points spanning multiple tiers."""
    expected_cost = calculate_expected_cost(
        50,
        11,
        [
            (54, 2),
            (59, 3),
            (64, 5),
            (69, 7),
            (74, 10),
            (79, 14),
            (84, 18),
            (89, 24),
            (94, 32),
            (float("inf"), 45),
        ],
    )
    assert base_car.get_upgrade_cost("downforce", 11) == expected_cost
    assert base_car.get_upgrade_cost("downforce", 11) == (2 * 4 + 3 * 5 + 5 * 2)


# --- Tests pour la méthode upgrade_stat ---


def test_upgrade_stat_successful_increment(base_car):
    """Test successful single point stat upgrade."""
    base_car.upgrade_stat("downforce", 1)
    assert base_car.downforce == 51


def test_upgrade_stat_multiple_points(base_car):
    """Test successful multiple points stat upgrade."""
    base_car.upgrade_stat("chassis", 10)
    assert base_car.chassis == 60


def test_upgrade_stat_caps_at_100(high_end_car):
    """Test that stat upgrade does not exceed 100."""
    high_end_car.power_unit = 99
    high_end_car.upgrade_stat("power_unit", 5)  # Try to upgrade by 5 points
    assert high_end_car.power_unit == 100


def test_upgrade_stat_at_100_stays_100(high_end_car):
    """Test that stat at 100 remains 100."""
    high_end_car.aero_efficiency = 100
    high_end_car.upgrade_stat("aero_efficiency", 5)
    assert high_end_car.aero_efficiency == 100


# --- Tests pour la méthode get_stats_display ---


def test_get_stats_display_base_car(base_car):
    """Test the display format for a base car."""
    expected_display = (
        "  Downforce:      50  |  Aero Efficiency:     50\n"
        "  Chassis:        50  |  Power Unit:          50\n"
        "  Reliability:    50  |  Tire Cooling:        65\n"
        "  Overall Performance:    51"
    )
    assert base_car.get_stats_display() == expected_display


def test_get_stats_display_high_end_car(high_end_car):
    """Test the display format for a high-end car."""
    expected_display = (
        "  Downforce:      95  |  Aero Efficiency:     90\n"
        "  Chassis:        98  |  Power Unit:          92\n"
        "  Reliability:    85  |  Tire Cooling:        95\n"
        "  Overall Performance:    93"
    )
    assert high_end_car.get_stats_display() == expected_display


# --- Tests pour la méthode get_stat_names ---


def test_get_stat_names():
    """Test that get_stat_names returns the correct list of stat names."""
    expected_names = [
        "downforce",
        "aero_efficiency",
        "chassis",
        "power_unit",
        "reliability",
        "tire_cooling",
    ]
    assert Car.get_stat_names() == expected_names
