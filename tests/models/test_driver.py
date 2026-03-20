import pytest

# --- Tests pour DriverStats.overall ---


def test_overall_base_stats(base_driver_stats):
    """Test overall calculation with all stats at 50."""
    # Expected: (50*0.25 + 50*0.15 + 50*0.15 + 50*0.20 + 50*0.15 + 50*0.10) = 50
    assert base_driver_stats.overall == 50


def test_overall_high_rated_stats(high_rated_driver_stats):
    """Test overall calculation with balanced high stats."""
    # Expected: (80*0.25 + 75*0.15 + 85*0.15 + 78*0.20 + 80*0.15 + 72*0.10)
    # = 20 + 11.25 + 12.75 + 15.6 + 12 + 7.2 = 78.8 -> 78
    assert high_rated_driver_stats.overall == 78


def test_overall_specialist_stats(specialist_driver_stats):
    """Test overall calculation with one dominant stat."""
    # Expected: (95*0.25 + 60*0.15 + 55*0.15 + 58*0.20 + 52*0.15 + 50*0.10)
    # = 23.75 + 9 + 8.25 + 11.6 + 7.8 + 5 = 65.4 -> 65
    assert specialist_driver_stats.overall == 65


# --- Tests pour DriverStats.get_stat_names ---


def test_get_stat_names(base_driver_stats):
    """Test that get_stat_names returns all six stats."""
    names = base_driver_stats.get_stat_names()
    assert len(names) == 6
    assert "pace" in names
    assert "overtaking" in names
    assert "defending" in names
    assert "consistency" in names
    assert "tire_management" in names
    assert "wet_skill" in names


# --- Tests pour DriverStats.upgrade_stat ---


def test_upgrade_stat_single_point(base_driver_stats):
    """Test upgrading a stat by one point."""
    base_driver_stats.upgrade_stat("pace", 1)
    assert base_driver_stats.pace == 51


def test_upgrade_stat_multiple_points(base_driver_stats):
    """Test upgrading a stat by multiple points."""
    base_driver_stats.upgrade_stat("pace", 5)
    assert base_driver_stats.pace == 55


def test_upgrade_stat_cap_at_99(base_driver_stats):
    """Test that upgrading is capped at 99."""
    base_driver_stats.pace = 95
    base_driver_stats.upgrade_stat("pace", 10)
    assert base_driver_stats.pace == 99


def test_upgrade_stat_cap_at_exactly_99(base_driver_stats):
    """Test that upgrading to exactly 99 works."""
    base_driver_stats.pace = 90
    base_driver_stats.upgrade_stat("pace", 9)
    assert base_driver_stats.pace == 99


def test_upgrade_different_stats(base_driver_stats):
    """Test upgrading different stats independently."""
    base_driver_stats.upgrade_stat("pace", 5)
    base_driver_stats.upgrade_stat("wet_skill", 3)
    assert base_driver_stats.pace == 55
    assert base_driver_stats.wet_skill == 53
    assert base_driver_stats.overtaking == 50


# --- Tests pour DriverStats.degrade_stat ---


def test_degrade_stat_single_point(base_driver_stats):
    """Test degrading a stat by one point."""
    base_driver_stats.pace = 70
    base_driver_stats.degrade_stat("pace", 1)
    assert base_driver_stats.pace == 69


def test_degrade_stat_multiple_points(base_driver_stats):
    """Test degrading a stat by multiple points."""
    base_driver_stats.pace = 70
    base_driver_stats.degrade_stat("pace", 5)
    assert base_driver_stats.pace == 65


def test_degrade_stat_minimum_50(base_driver_stats):
    """Test that degrading is floored at 50."""
    base_driver_stats.pace = 55
    base_driver_stats.degrade_stat("pace", 10)
    assert base_driver_stats.pace == 50


def test_degrade_stat_already_at_minimum(base_driver_stats):
    """Test degrading when already at minimum (50)."""
    assert base_driver_stats.pace == 50
    base_driver_stats.degrade_stat("pace", 5)
    assert base_driver_stats.pace == 50


def test_degrade_different_stats(base_driver_stats):
    """Test degrading different stats independently."""
    base_driver_stats.overtaking = 75
    base_driver_stats.wet_skill = 70
    base_driver_stats.degrade_stat("overtaking", 3)
    base_driver_stats.degrade_stat("wet_skill", 2)
    assert base_driver_stats.overtaking == 72
    assert base_driver_stats.wet_skill == 68
    assert base_driver_stats.pace == 50


# --- Tests pour Driver.__str__ ---


def test_driver_str_representation(young_driver):
    """Test string representation of driver."""
    assert str(young_driver) == "Marcus Rivera (Spain, 21)"


def test_driver_str_different_drivers(prime_driver, veteran_driver):
    """Test string representation with different drivers."""
    assert str(prime_driver) == "Carlos Sainz (Spain, 25)"
    assert str(veteran_driver) == "Fernando Alonso (Spain, 34)"


# --- Tests pour Driver.get_stats_display ---


def test_get_stats_display_format(young_driver):
    """Test that stats display has the correct format with all components."""
    display = young_driver.get_stats_display()
    assert "Pace:" in display
    assert "Overtaking:" in display
    assert "Defending:" in display
    assert "Consistency:" in display
    assert "Tire Mgmt:" in display
    assert "Wet:" in display
    assert "Overall:" in display
    assert "Potential:" in display


def test_get_stats_display_no_rising_star(young_driver):
    """Test stats display without rising star status."""
    display = young_driver.get_stats_display()
    assert "[RISING STAR]" not in display


def test_get_stats_display_with_rising_star(young_driver):
    """Test stats display with rising star status."""
    young_driver.rising_star_races = 3
    display = young_driver.get_stats_display()
    assert "[RISING STAR]" in display


# --- Tests pour Driver.get_potential ---


def test_get_potential_explicit_set(young_driver):
    """Test get_potential returns explicit value when set."""
    young_driver.potential = 85
    assert young_driver.get_potential() == 85


def test_get_potential_auto_calculate_young_driver(young_driver):
    """Test potential auto-calculation for young driver (age 21)."""
    # Young driver (< 23) gets +8 to +15 bonus
    potential = young_driver.get_potential()
    assert potential > young_driver.stats.overall
    assert potential <= 99


def test_get_potential_caches_value(young_driver):
    """Test that potential is cached after auto-calculation."""
    first_call = young_driver.get_potential()
    second_call = young_driver.get_potential()
    assert first_call == second_call  # Should be same since it's cached


def test_get_potential_prime_driver(prime_driver):
    """Test potential calculation for prime driver (age 25)."""
    potential = prime_driver.get_potential()
    assert potential >= prime_driver.stats.overall


def test_get_potential_veteran_driver(veteran_driver):
    """Test potential calculation for veteran driver (age 34)."""
    # Veteran gets smaller bonus (+0 to +2)
    veteran_driver.potential = 0  # Reset to force auto-calculation
    initial_overall = veteran_driver.stats.overall
    potential = veteran_driver.get_potential()
    assert potential - initial_overall <= 2


# --- Tests pour Driver.reset_season_stats ---


def test_reset_season_stats_clears_points(young_driver):
    """Test that reset_season_stats clears season points."""
    young_driver.season_points = 100
    young_driver.reset_season_stats()
    assert young_driver.season_points == 0


def test_reset_season_stats_clears_wins(young_driver):
    """Test that reset_season_stats clears race wins."""
    young_driver.race_wins = 5
    young_driver.reset_season_stats()
    assert young_driver.race_wins == 0


def test_reset_season_stats_clears_podiums(young_driver):
    """Test that reset_season_stats clears podiums."""
    young_driver.podiums = 10
    young_driver.reset_season_stats()
    assert young_driver.podiums == 0


def test_reset_season_stats_clears_dnfs(young_driver):
    """Test that reset_season_stats clears DNFs."""
    young_driver.dnfs = 3
    young_driver.reset_season_stats()
    assert young_driver.dnfs == 0


def test_reset_season_stats_clears_finishes(young_driver):
    """Test that reset_season_stats clears total finishes."""
    young_driver.total_finishes = 10
    young_driver.total_positions = 95
    young_driver.reset_season_stats()
    assert young_driver.total_finishes == 0
    assert young_driver.total_positions == 0


def test_reset_season_stats_clears_season_best_finish(young_driver):
    """Test that reset_season_stats resets season best finish to 99."""
    young_driver.season_best_finish = 3
    young_driver.reset_season_stats()
    assert young_driver.season_best_finish == 99


def test_reset_season_stats_preserves_rising_star_races(young_driver):
    """Test that reset_season_stats does not reset rising_star_races."""
    young_driver.rising_star_races = 4
    young_driver.reset_season_stats()
    assert young_driver.rising_star_races == 4


# --- Tests pour Driver.get_average_position ---


def test_get_average_position_no_finishes(young_driver):
    """Test average position returns 99 when no finishes recorded."""
    assert young_driver.get_average_position() == 99.0


def test_get_average_position_single_finish(young_driver):
    """Test average position with single finish."""
    young_driver.record_finish(5)
    assert young_driver.get_average_position() == 5.0


def test_get_average_position_multiple_finishes(young_driver):
    """Test average position with multiple finishes."""
    young_driver.record_finish(3)
    young_driver.record_finish(5)
    young_driver.record_finish(4)
    # (3 + 5 + 4) / 3 = 12 / 3 = 4.0
    assert young_driver.get_average_position() == 4.0


def test_get_average_position_consistent(young_driver):
    """Test average position calculation consistency."""
    for _ in range(5):
        young_driver.record_finish(8)
    assert young_driver.get_average_position() == 8.0


# --- Tests pour Driver.record_finish ---


def test_record_finish_increments_total_finishes(young_driver):
    """Test that recording a finish increments total_finishes."""
    young_driver.record_finish(5)
    assert young_driver.total_finishes == 1


def test_record_finish_accumulates_positions(young_driver):
    """Test that recording finishes accumulates positions."""
    young_driver.record_finish(3)
    young_driver.record_finish(7)
    assert young_driver.total_positions == 10


def test_record_finish_updates_season_best_finish(young_driver):
    """Test that better finish updates season_best_finish."""
    young_driver.record_finish(8)
    assert young_driver.season_best_finish == 8
    young_driver.record_finish(3)
    assert young_driver.season_best_finish == 3


def test_record_finish_does_not_worsen_season_best(young_driver):
    """Test that worse finish does not update season_best_finish."""
    young_driver.record_finish(5)
    young_driver.record_finish(10)
    assert young_driver.season_best_finish == 5


def test_record_finish_invalid_position_zero(young_driver):
    """Test that position 0 or negative is not recorded."""
    initial_finishes = young_driver.total_finishes
    young_driver.record_finish(0)
    assert young_driver.total_finishes == initial_finishes


# --- Tests pour Driver.check_rising_star ---


def test_check_rising_star_not_triggered_old_driver(veteran_driver):
    """Test that rising star is never triggered for drivers >= 27."""
    assert veteran_driver.check_rising_star(1, 90) is False
    assert veteran_driver.check_rising_star(3, 70) is False


def test_check_rising_star_win_young_driver(young_driver):
    """Test that a win triggers rising star for young drivers."""
    assert young_driver.check_rising_star(1, 90) is True
    assert young_driver.rising_star_races == 5


def test_check_rising_star_podium_low_car(young_driver):
    """Test that podium in low-rated car triggers rising star."""
    assert young_driver.check_rising_star(2, 70) is True
    assert young_driver.rising_star_races == 5


def test_check_rising_star_podium_high_car(young_driver):
    """Test that podium in high-rated car does not trigger rising star."""
    assert young_driver.check_rising_star(3, 90) is False


def test_check_rising_star_outperforming_car(young_driver):
    """Test that significantly outperforming car triggers rising star."""
    # Car rating 65, expected position ~14, finishing P10 is outperforming by 4
    assert young_driver.check_rising_star(10, 65) is True


def test_check_rising_star_not_outperforming_enough(young_driver):
    """Test that not outperforming enough does not trigger rising star."""
    # Car rating 75, expected position ~10, finishing P8 is only outperforming by 2
    assert young_driver.check_rising_star(8, 75) is False


# --- Tests pour Driver.tick_rising_star ---


def test_tick_rising_star_decrements_counter(young_driver):
    """Test that tick_rising_star decrements the counter."""
    young_driver.rising_star_races = 3
    young_driver.tick_rising_star()
    assert young_driver.rising_star_races == 2


def test_tick_rising_star_stops_at_zero(young_driver):
    """Test that counter does not go below zero."""
    young_driver.rising_star_races = 1
    young_driver.tick_rising_star()
    assert young_driver.rising_star_races == 0
    young_driver.tick_rising_star()
    assert young_driver.rising_star_races == 0


# --- Tests pour Driver team management ---


def test_is_free_agent_initially_true(young_driver):
    """Test that a new driver is initially a free agent."""
    assert young_driver.is_free_agent() is True


def test_is_free_agent_after_signing(young_driver):
    """Test that driver is not free agent after signing."""
    young_driver.sign_with_team("Ferrari")
    assert young_driver.is_free_agent() is False


def test_sign_with_team_sets_team_name(young_driver):
    """Test that signing sets the team name."""
    young_driver.sign_with_team("Mercedes")
    assert young_driver.team_name == "Mercedes"


def test_release_from_team(young_driver):
    """Test that releasing from team makes driver free agent."""
    young_driver.sign_with_team("Red Bull")
    young_driver.release_from_team()
    assert young_driver.is_free_agent() is True
    assert young_driver.team_name is None


def test_sign_with_team_overwrites_previous_team(young_driver):
    """Test that signing with new team overwrites previous team."""
    young_driver.sign_with_team("Ferrari")
    young_driver.sign_with_team("McLaren")
    assert young_driver.team_name == "McLaren"


# --- Tests pour Driver.age_up ---


def test_age_up_increments_age(young_driver):
    """Test that age_up increments driver age."""
    assert young_driver.age == 21
    young_driver.age_up()
    assert young_driver.age == 22


def test_age_up_multiple_times(young_driver):
    """Test aging up multiple times."""
    for _ in range(5):
        young_driver.age_up()
    assert young_driver.age == 26


# --- Tests pour Driver.develop_stats ---


def test_develop_stats_young_driver_good_season(young_driver):
    """Test stat development for young driver after good season."""
    changes = young_driver.develop_stats(had_good_season=True)
    # Young drivers should have high chance to improve
    # Just verify list is returned (some changes may occur)
    assert isinstance(changes, list)


def test_develop_stats_returns_list(young_driver):
    """Test that develop_stats returns a list of tuples."""
    changes = young_driver.develop_stats()
    assert isinstance(changes, list)
    for change in changes:
        assert isinstance(change, tuple)
        assert len(change) == 3  # (stat_name, old_value, new_value)


def test_develop_stats_updates_market_value(young_driver):
    """Test that develop_stats updates market value."""
    young_driver.develop_stats(had_good_season=True)
    # Market value should be recalculated (may be same or different)
    assert isinstance(young_driver.market_value, int)


# --- Tests pour Driver.apply_rising_star_growth ---


def test_apply_rising_star_growth_no_effect_if_inactive(young_driver):
    """Test that no growth occurs when rising_star_races is 0."""
    young_driver.rising_star_races = 0
    changes = young_driver.apply_rising_star_growth()
    assert changes == []


def test_apply_rising_star_growth_no_effect_if_too_old(veteran_driver):
    """Test that no growth occurs for drivers >= 27."""
    veteran_driver.rising_star_races = 5
    changes = veteran_driver.apply_rising_star_growth()
    assert changes == []


def test_apply_rising_star_growth_returns_list(young_driver):
    """Test that apply_rising_star_growth returns a list."""
    young_driver.rising_star_races = 3
    changes = young_driver.apply_rising_star_growth()
    assert isinstance(changes, list)


# --- Tests pour intégration complet ---


def test_driver_complete_season_scenario(young_driver):
    """Test a complete season scenario with multiple operations."""
    # Start of season
    assert young_driver.is_free_agent() is True

    # Sign with team
    young_driver.sign_with_team("Alpine")
    assert young_driver.team_name == "Alpine"

    # Record some races
    young_driver.record_finish(8)  # Not a great start
    young_driver.record_finish(5)  # Improving
    young_driver.record_finish(3)  # Podium!

    # Check average position
    assert young_driver.get_average_position() == pytest.approx(5.333, rel=0.01)

    # Age up at season end
    initial_age = young_driver.age
    young_driver.age_up()
    assert young_driver.age == initial_age + 1

    # Reset season stats
    young_driver.reset_season_stats()
    assert young_driver.season_points == 0
    assert young_driver.get_average_position() == 99.0


def test_driver_rising_star_full_scenario(young_driver):
    """Test complete rising star scenario."""
    # Not triggered initially
    assert young_driver.rising_star_races == 0

    # Trigger rising star with a win
    triggered = young_driver.check_rising_star(1, 80)
    assert triggered is True
    assert young_driver.rising_star_races == 5

    # Apply growth and tick counter
    young_driver.apply_rising_star_growth()
    young_driver.tick_rising_star()
    assert young_driver.rising_star_races == 4

    # After 5 ticks, should be exhausted
    for _ in range(4):
        young_driver.tick_rising_star()
    assert young_driver.rising_star_races == 0
