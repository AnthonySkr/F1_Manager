from models import Car


def main() -> None:
    """Entry point for F1 manager game."""
    car = Car(90, 92, 91, 89, 90, 92)

    stats = car.get_stats_display()
    print(stats)


if __name__ == "__main__":
    main()
