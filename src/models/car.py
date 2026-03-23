from dataclasses import dataclass


@dataclass
class Car:
    """Dataclass Car."""

    downforce: int  # Cornering grip (1-100)
    aero_efficiency: int  # Straight-line + corners balance (1-100)
    chassis: int  # Overall car handling (1-100)
    power_unit: int  # Engine power (1-100)
    reliability: int  # DNF chances reduction (1-100)
    tire_cooling: int = 65  # Tire temperature management (1-100) - affects tire wear

    @property
    def overall(self) -> int:
        """Calculate overall car stats."""
        return int(
            (self.downforce * 0.18)
            + (self.aero_efficiency * 0.18)
            + (self.chassis * 0.22)
            + (self.power_unit * 0.18)
            + (self.reliability * 0.12)
            + (self.tire_cooling * 0.12),
        )

    @property
    def performance(self) -> float:
        """Calculate overall car performance for race simulation."""
        return (
            (self.downforce * 0.22)
            + (self.aero_efficiency * 0.22)
            + (self.chassis * 0.28)
            + (self.power_unit * 0.28)
        )

    @property
    def tire_wear_factor(self) -> float:
        """Calculate tire wear multiplier based on tire cooling.

        100 tire_cooling = 0.5x wear (excellent cooling)
        65 tire_cooling = 0.85x wear (average)
        30 tire_cooling = 1.2x wear (poor cooling, tires overheat).
        """
        # Linear scale: 100 -> 0.5, 65 -> 0.85, 30 -> 1.2
        return 1.5 - (self.tire_cooling / 100)

    def get_upgrade_cost(self, stat_name: str, points: int = 1) -> int:
        """Calculate cost to upgrade a stat by specified points (in millions)."""
        current = getattr(self, stat_name)
        total_cost = 0

        # Define threshold and costs by points
        # (threshold_max, cost_by_points)
        cost_tiers = [
            (54, 2),  # Up to and including 54, the cost is 2
            (59, 3),  # Up to and including 59, the cost is 3
            (64, 5),
            (69, 7),
            (74, 10),
            (79, 14),
            (84, 18),
            (89, 24),
            (94, 32),
            (float("inf"), 45),  # For all over 94
        ]

        for i in range(points):
            stat_value = current + i + 1
            cost_per_point = 0
            for threshold, cost in cost_tiers:
                if stat_value <= threshold:
                    cost_per_point = cost
                    break
            total_cost += cost_per_point

        return total_cost

    def upgrade_stat(self, stat_name: str, points: int = 1) -> bool:
        """Upgrade a stat by specified points. Returns True if successful."""
        current = getattr(self, stat_name)
        new_value = min(100, current + points)
        setattr(self, stat_name, new_value)
        return True

    def get_stats_display(self) -> str:
        """Return performance display."""
        return (
            f"  Downforce:      {self.downforce}  |  Aero Efficiency:     {self.aero_efficiency}\n"
            f"  Chassis:        {self.chassis}  |  Power Unit:          {self.power_unit}\n"
            f"  Reliability:    {self.reliability}  |  Tire Cooling:        {self.tire_cooling}\n"
            f"  Overall Performance:    {self.overall}"
        )

    @staticmethod
    def get_stat_names() -> list:
        """Return list of stats names."""
        return [
            "downforce",
            "aero_efficiency",
            "chassis",
            "power_unit",
            "reliability",
            "tire_cooling",
        ]
