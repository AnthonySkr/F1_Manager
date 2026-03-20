from models import Track, TrackType


def main() -> None:
    """Entry point for F1 manager game."""
    paul = Track(
        "Paul Ricard",
        "France",
        "Vierzon",
        TrackType.STREET,
        72,
        90,
        20,
        5,
        1,
        2,
    )
    print(paul)


if __name__ == "__main__":
    main()
