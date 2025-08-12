from pathlib import Path


def read_increment_write_counter(file_path: Path) -> int:
    """
    Reads an integer from file_path, increments it by 1, and writes it back.
    If the file does not exist or contains invalid data, starts from 0.

    Returns the new value after incrementing.
    """
    current = 0

    try:
        if file_path.exists():
            raw = file_path.read_text(encoding="utf-8").strip()
            if raw:
                try:
                    current = int(raw)
                except ValueError:
                    # If content isn't a valid integer, reset to 0
                    current = 0
    except Exception:
        # If reading fails for any reason, keep current at 0
        current = 0

    new_value = current + 1

    # Write the updated value (with trailing newline for POSIX friendliness)
    file_path.write_text(f"{new_value}\n", encoding="utf-8")

    return new_value


def main() -> None:
    # Place the counter file next to this script
    counter_file = Path(__file__).with_suffix(".txt")  # keep_github_live.txt
    new_value = read_increment_write_counter(counter_file)
    # Print for logging/CI visibility
    print(new_value)


if __name__ == "__main__":
    main()