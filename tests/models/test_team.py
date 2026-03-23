import pytest

from src.models import Driver, DriverStats, Team

# --- Fixtures pour les tests Team ---


@pytest.fixture
def sample_driver_1(young_driver):
    """Returns the first sample driver for team tests (from shared fixtures)."""
    return young_driver


@pytest.fixture
def sample_driver_2():
    """Returns the second sample driver for team tests."""
    stats = DriverStats(
        pace=75,
        overtaking=70,
        defending=80,
        consistency=75,
        tire_management=72,
        wet_skill=78,
    )
    return Driver(
        name="George Russell",
        age=24,
        nationality="United Kingdom",
        stats=stats,
        salary=18,
        market_value=35,
    )


@pytest.fixture
def sample_driver_3():
    """Returns a third sample driver for team tests."""
    stats = DriverStats(
        pace=85,
        overtaking=80,
        defending=75,
        consistency=80,
        tire_management=78,
        wet_skill=82,
    )
    return Driver(
        name="Charles Leclerc",
        age=25,
        nationality="Monaco",
        stats=stats,
        salary=20,
        market_value=42,
    )


@pytest.fixture
def player_team(base_car):
    """Returns a player-controlled team with budget."""
    return Team(
        name="Player Racing",
        budget=150,
        car=base_car,
        is_player_team=True,
    )


@pytest.fixture
def ai_team(average_car):
    """Returns an AI-controlled team with budget."""
    return Team(
        name="AI Motors",
        budget=200,
        car=average_car,
        is_player_team=False,
    )


@pytest.fixture
def team_with_drivers(high_end_car, sample_driver_1, sample_driver_2):
    """Returns a team with two drivers already signed."""
    team = Team(
        name="Elite Racing",
        budget=100,
        car=high_end_car,
        is_player_team=False,
    )
    team.drivers = [sample_driver_1, sample_driver_2]
    sample_driver_1.sign_with_team("Elite Racing")
    sample_driver_2.sign_with_team("Elite Racing")
    return team


# --- Tests pour Team.__str__ ---


def test_team_str_representation(player_team):
    """Test string representation of team."""
    assert str(player_team) == "Player Racing"


def test_team_str_different_names(ai_team):
    """Test string representation with different team name."""
    assert str(ai_team) == "AI Motors"


# --- Tests pour Team.get_driver_names ---


def test_get_driver_names_no_drivers(player_team):
    """Test driver names when team has no drivers."""
    assert player_team.get_driver_names() == "No drivers signed"


def test_get_driver_names_single_driver(player_team, sample_driver_1):
    """Test driver names with single driver."""
    player_team.drivers.append(sample_driver_1)
    assert player_team.get_driver_names() == "Marcus Rivera"


def test_get_driver_names_two_drivers(player_team, sample_driver_1, sample_driver_2):
    """Test driver names with two drivers."""
    player_team.drivers = [sample_driver_1, sample_driver_2]
    assert player_team.get_driver_names() == "Marcus Rivera & George Russell"


def test_get_driver_names_format(team_with_drivers):
    """Test driver names format with existing team."""
    names = team_with_drivers.get_driver_names()
    assert "Marcus Rivera" in names
    assert "George Russell" in names
    assert " & " in names


# --- Tests pour Team.can_afford ---


def test_can_afford_sufficient_budget(player_team):
    """Test can_afford with sufficient budget."""
    assert player_team.can_afford(100) is True


def test_can_afford_exact_budget(player_team):
    """Test can_afford with exact budget amount."""
    assert player_team.can_afford(150) is True


def test_can_afford_insufficient_budget(player_team):
    """Test can_afford with insufficient budget."""
    assert player_team.can_afford(200) is False


def test_can_afford_zero_amount(player_team):
    """Test can_afford with zero amount."""
    assert player_team.can_afford(0) is True


def test_can_afford_small_amount(ai_team):
    """Test can_afford with small amount."""
    assert ai_team.can_afford(1) is True


# --- Tests pour Team.spend ---


def test_spend_successful(player_team):
    """Test successful spending."""
    initial_budget = player_team.budget
    result = player_team.spend(50)
    assert result is True
    assert player_team.budget == initial_budget - 50


def test_spend_exact_budget(player_team):
    """Test spending exact budget."""
    result = player_team.spend(150)
    assert result is True
    assert player_team.budget == 0


def test_spend_insufficient_budget(player_team):
    """Test spending with insufficient budget."""
    result = player_team.spend(200)
    assert result is False
    assert player_team.budget == 150  # Budget unchanged


def test_spend_multiple_times(player_team):
    """Test multiple spending transactions."""
    player_team.spend(50)
    player_team.spend(40)
    assert player_team.budget == 60


def test_spend_zero_amount(player_team):
    """Test spending zero amount."""
    initial_budget = player_team.budget
    result = player_team.spend(0)
    assert result is True
    assert player_team.budget == initial_budget


# --- Tests pour Team.add_income ---


def test_add_income_simple(player_team):
    """Test adding income to budget."""
    initial_budget = player_team.budget
    player_team.add_income(50)
    assert player_team.budget == initial_budget + 50


def test_add_income_multiple_times(player_team):
    """Test adding income multiple times."""
    player_team.add_income(30)
    player_team.add_income(20)
    assert player_team.budget == 200


def test_add_income_after_spending(player_team):
    """Test adding income after spending."""
    player_team.spend(100)
    assert player_team.budget == 50
    player_team.add_income(100)
    assert player_team.budget == 150


def test_add_income_zero(player_team):
    """Test adding zero income."""
    initial_budget = player_team.budget
    player_team.add_income(0)
    assert player_team.budget == initial_budget


def test_add_income_large_amount(player_team):
    """Test adding large income."""
    player_team.add_income(1000)
    assert player_team.budget == 1150


# --- Tests pour Team.sign_driver ---


def test_sign_driver_successful(player_team, sample_driver_1):
    """Test successfully signing a driver."""
    result = player_team.sign_driver(sample_driver_1, 25)
    assert result is True
    assert sample_driver_1 in player_team.drivers
    assert sample_driver_1.team_name == "Player Racing"
    assert player_team.budget == 125


def test_sign_driver_second_driver(player_team, sample_driver_1, sample_driver_2):
    """Test signing a second driver."""
    player_team.sign_driver(sample_driver_1, 25)
    result = player_team.sign_driver(sample_driver_2, 20)
    assert result is True
    assert len(player_team.drivers) == 2
    assert sample_driver_2 in player_team.drivers


def test_sign_driver_max_drivers(
    player_team,
    sample_driver_1,
    sample_driver_2,
    sample_driver_3,
):
    """Test that team cannot sign more than 2 drivers."""
    player_team.sign_driver(sample_driver_1, 25)
    player_team.sign_driver(sample_driver_2, 20)
    result = player_team.sign_driver(sample_driver_3, 30)
    assert result is False
    assert len(player_team.drivers) == 2
    assert sample_driver_3 not in player_team.drivers


def test_sign_driver_insufficient_budget(player_team, sample_driver_1):
    """Test signing driver with insufficient budget."""
    result = player_team.sign_driver(sample_driver_1, 200)
    assert result is False
    assert sample_driver_1 not in player_team.drivers
    assert player_team.budget == 150  # Budget unchanged


def test_sign_driver_exact_fee(player_team, sample_driver_1):
    """Test signing driver for exact team budget."""
    result = player_team.sign_driver(sample_driver_1, 150)
    assert result is True
    assert player_team.budget == 0


def test_sign_driver_free_transfer(player_team, sample_driver_1):
    """Test signing driver for free (fee = 0)."""
    result = player_team.sign_driver(sample_driver_1, 0)
    assert result is True
    assert player_team.budget == 150


# --- Tests pour Team.release_driver ---


def test_release_driver_success(team_with_drivers, sample_driver_1):
    """Test successfully releasing a driver."""
    result = team_with_drivers.release_driver(sample_driver_1)
    assert result is True
    assert sample_driver_1 not in team_with_drivers.drivers
    assert sample_driver_1.is_free_agent() is True


def test_release_driver_not_on_team(player_team, sample_driver_1):
    """Test releasing a driver not on the team."""
    result = player_team.release_driver(sample_driver_1)
    assert result is False


def test_release_both_drivers(team_with_drivers, sample_driver_1, sample_driver_2):
    """Test releasing both drivers from team."""
    team_with_drivers.release_driver(sample_driver_1)
    result = team_with_drivers.release_driver(sample_driver_2)
    assert result is True
    assert len(team_with_drivers.drivers) == 0


def test_release_driver_makes_free_agent(team_with_drivers, sample_driver_1):
    """Test that released driver becomes free agent."""
    team_with_drivers.release_driver(sample_driver_1)
    assert sample_driver_1.team_name is None


# --- Tests pour Team.reset_season_stats ---


def test_reset_season_stats_clears_points(player_team):
    """Test that reset clears season points."""
    player_team.season_points = 100
    player_team.reset_season_stats()
    assert player_team.season_points == 0


def test_reset_season_stats_clears_wins(player_team):
    """Test that reset clears race wins."""
    player_team.race_wins = 10
    player_team.reset_season_stats()
    assert player_team.race_wins == 0


def test_reset_season_stats_clears_finishes(player_team):
    """Test that reset clears race finishes."""
    player_team.total_finishes = 15
    player_team.total_positions = 120
    player_team.reset_season_stats()
    assert player_team.total_finishes == 0
    assert player_team.total_positions == 0


def test_reset_season_stats_resets_drivers(team_with_drivers):
    """Test that reset resets drivers' season stats."""
    driver = team_with_drivers.drivers[0]
    driver.season_points = 50
    driver.race_wins = 2
    team_with_drivers.reset_season_stats()
    assert driver.season_points == 0
    assert driver.race_wins == 0


# --- Tests pour Team.get_average_position ---


def test_get_average_position_no_finishes(player_team):
    """Test average position returns 99 when no finishes."""
    assert player_team.get_average_position() == 99.0


def test_get_average_position_single_finish(player_team):
    """Test average position with single finish."""
    player_team.record_finish(5)
    assert player_team.get_average_position() == 5.0


def test_get_average_position_multiple_finishes(player_team):
    """Test average position with multiple finishes."""
    player_team.record_finish(3)
    player_team.record_finish(8)
    player_team.record_finish(6)
    # (3 + 8 + 6) / 3 = 17 / 3 ≈ 5.67
    assert player_team.get_average_position() == pytest.approx(5.666, rel=0.01)


def test_get_average_position_consistent_finishes(player_team):
    """Test average position with consistent finishing positions."""
    for _ in range(4):
        player_team.record_finish(10)
    assert player_team.get_average_position() == 10.0


# --- Tests pour Team.record_finish ---


def test_record_finish_increments_total(player_team):
    """Test that recording finish increments total_finishes."""
    player_team.record_finish(5)
    assert player_team.total_finishes == 1


def test_record_finish_accumulates_positions(player_team):
    """Test that positions accumulate correctly."""
    player_team.record_finish(3)
    player_team.record_finish(7)
    assert player_team.total_positions == 10


def test_record_finish_invalid_position(player_team):
    """Test that invalid position (0 or negative) is not recorded."""
    initial_finishes = player_team.total_finishes
    player_team.record_finish(0)
    assert player_team.total_finishes == initial_finishes


def test_record_finish_multiple_races(player_team):
    """Test recording multiple race finishes."""
    positions = [3, 5, 2, 8, 1]
    for pos in positions:
        player_team.record_finish(pos)
    assert player_team.total_finishes == 5
    assert player_team.total_positions == sum(positions)


# --- Tests pour Team.get_season_prize_money ---


def test_get_season_prize_money_first_place(player_team):
    """Test prize money for 1st place finish."""
    assert player_team.get_season_prize_money(1) == 80


def test_get_season_prize_money_fifth_place(player_team):
    """Test prize money for 5th place finish."""
    assert player_team.get_season_prize_money(5) == 48


def test_get_season_prize_money_tenth_place(player_team):
    """Test prize money for 10th place finish."""
    assert player_team.get_season_prize_money(10) == 30


def test_get_season_prize_money_eleventh_place(player_team):
    """Test prize money for 11th place finish."""
    assert player_team.get_season_prize_money(11) == 28


def test_get_season_prize_money_outside_table(player_team):
    """Test prize money for position outside table (defaults to 25)."""
    assert player_team.get_season_prize_money(15) == 25
    assert player_team.get_season_prize_money(20) == 25


def test_get_season_prize_money_all_positions(player_team):
    """Test all positions in the prize table."""
    prize_table = {
        1: 80,
        2: 70,
        3: 62,
        4: 55,
        5: 48,
        6: 42,
        7: 38,
        8: 35,
        9: 32,
        10: 30,
        11: 28,
    }
    for position, expected_prize in prize_table.items():
        assert player_team.get_season_prize_money(position) == expected_prize


# --- Tests pour Team.get_info_display ---


def test_get_info_display_format(player_team):
    """Test that info display has correct format."""
    display = player_team.get_info_display()
    assert "Team:" in display
    assert "Player Racing" in display
    assert "Budget:" in display
    assert "Drivers:" in display
    assert "Season Points:" in display
    assert "Car Performance:" in display


def test_get_info_display_no_drivers(player_team):
    """Test info display with no drivers."""
    display = player_team.get_info_display()
    assert "No drivers signed" in display


def test_get_info_display_with_drivers(team_with_drivers):
    """Test info display with drivers."""
    display = team_with_drivers.get_info_display()
    assert "Marcus Rivera" in display
    assert "George Russell" in display


def test_get_info_display_budget(ai_team):
    """Test that info display shows correct budget."""
    display = ai_team.get_info_display()
    assert "200" in display  # Budget amount


def test_get_info_display_season_points(ai_team):
    """Test that info display shows season points."""
    ai_team.season_points = 42
    display = ai_team.get_info_display()
    assert "42" in display


# --- Tests d'intégration ---


def test_team_complete_scenario(player_team, sample_driver_1, sample_driver_2):
    """Test a complete team scenario with multiple operations."""
    # Initial state
    assert player_team.is_player_team is True
    initial_budget = player_team.budget

    # Sign first driver
    player_team.sign_driver(sample_driver_1, 30)
    assert len(player_team.drivers) == 1
    assert player_team.budget == initial_budget - 30

    # Sign second driver
    player_team.sign_driver(sample_driver_2, 25)
    assert len(player_team.drivers) == 2

    # Record some race finishes
    player_team.record_finish(3)
    player_team.record_finish(8)

    # Check average position
    assert player_team.get_average_position() == pytest.approx(5.5)

    # Reset season
    player_team.reset_season_stats()
    assert player_team.total_finishes == 0
    assert player_team.get_average_position() == 99.0


def test_team_driver_management_scenario(
    player_team,
    sample_driver_1,
    sample_driver_2,
    sample_driver_3,
):
    """Test complete driver management scenario."""
    budget = player_team.budget

    # Sign two drivers
    player_team.sign_driver(sample_driver_1, 20)
    player_team.sign_driver(sample_driver_2, 20)
    assert len(player_team.drivers) == 2

    # Cannot sign third driver (full roster)
    result = player_team.sign_driver(sample_driver_3, 20)
    assert result is False
    assert player_team.budget == budget - 40

    # Release first driver and sign third
    player_team.release_driver(sample_driver_1)
    assert len(player_team.drivers) == 1

    result = player_team.sign_driver(sample_driver_3, 20)
    assert result is True
    assert len(player_team.drivers) == 2


def test_team_budget_management_scenario(ai_team, sample_driver_1):
    """Test budget management scenario."""
    initial = ai_team.budget

    # Add income from sponsorship
    ai_team.add_income(50)
    assert ai_team.budget == initial + 50

    # Sign driver
    ai_team.sign_driver(sample_driver_1, 40)
    current = ai_team.budget

    # Check can afford
    assert ai_team.can_afford(current) is True
    assert ai_team.can_afford(current + 1) is False

    # Add prize money
    prize = ai_team.get_season_prize_money(3)  # 3rd place
    ai_team.add_income(prize)

    # Verify budget
    assert ai_team.budget == current + prize


def test_team_with_no_drivers_scenario(player_team):
    """Test team operations with no drivers."""
    # Get driver names
    assert player_team.get_driver_names() == "No drivers signed"

    # Reset season stats (should work with no drivers)
    player_team.season_points = 50
    player_team.reset_season_stats()
    assert player_team.season_points == 0

    # Info display
    info = player_team.get_info_display()
    assert "No drivers signed" in info
