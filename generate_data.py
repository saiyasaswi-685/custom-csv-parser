"""Generate a synthetic CSV file with 10,000 rows and 5 columns.

The generated file is called sample_10k.csv and is used for benchmarking.
"""

import csv
import random
import string


def random_field() -> str:
    """Create a random field with some chances of commas, quotes and newlines."""
    base = "".join(random.choices(string.ascii_letters, k=5))
    kind = random.randint(0, 4)

    if kind == 0:
        # Simple word
        return base
    if kind == 1:
        # Contains a comma
        return base + "," + base
    if kind == 2:
        # Contains a double quote
        return base + '"' + base
    if kind == 3:
        # Contains a newline
        return base + "\n" + base
    # Empty string
    return ""


def generate_csv(
    filename: str = "sample_10k.csv",
    num_rows: int = 10_000,
    num_cols: int = 5,
    seed: int = 42,
) -> None:
    """Generate a CSV file with the given shape."""
    random.seed(seed)

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for _ in range(num_rows):
            row = [random_field() for _ in range(num_cols)]
            writer.writerow(row)

    print(f"Generated {filename} with {num_rows} rows and {num_cols} columns.")


if __name__ == "__main__":
    generate_csv()
