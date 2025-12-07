"""Benchmark custom CSV reader/writer against Python's csv module."""

import time
import csv
from csv_parser import CustomCsvReader, CustomCsvWriter

DATA_FILE = "sample_10k.csv"


def benchmark_reader(reader_factory, label: str, repeats: int = 5) -> float:
    """Benchmark a reader implementation and print average time."""
    times = []

    for _ in range(repeats):
        start = time.perf_counter()
        with open(DATA_FILE, newline="", encoding="utf-8") as f:
            reader = reader_factory(f)
            for _ in reader:
                # We just iterate through all rows to measure speed.
                pass
        end = time.perf_counter()
        times.append(end - start)

    avg_time = sum(times) / len(times)
    print(f"{label} reader avg time over {repeats} runs: {avg_time:.6f} seconds")
    return avg_time


def benchmark_writer(writer_factory, label: str, rows, repeats: int = 5) -> float:
    """Benchmark a writer implementation and print average time."""
    times = []

    for i in range(repeats):
        filename = f"out_{label}_{i}.csv"
        start = time.perf_counter()
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = writer_factory(f)
            # For CustomCsvWriter we call .writerows, which we defined
            writer.writerows(rows)
        end = time.perf_counter()
        times.append(end - start)

    avg_time = sum(times) / len(times)
    print(f"{label} writer avg time over {repeats} runs: {avg_time:.6f} seconds")
    return avg_time


def main() -> None:
    # Load all rows once using the standard csv module
    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        std_rows = list(csv.reader(f))

    print("=== Reader benchmarks ===")
    custom_reader_time = benchmark_reader(
        lambda f: CustomCsvReader(f),
        "CustomCsv",
    )
    std_reader_time = benchmark_reader(
        lambda f: csv.reader(f),
        "StdCsv",
    )

    print("\n=== Writer benchmarks ===")
    custom_writer_time = benchmark_writer(
        lambda f: CustomCsvWriter(f),
        "CustomCsv",
        std_rows,
    )
    std_writer_time = benchmark_writer(
        lambda f: csv.writer(f),
        "StdCsv",
        std_rows,
    )

    print("\n=== Summary ===")
    print(f"Custom reader time: {custom_reader_time:.6f} s")
    print(f"Std    reader time: {std_reader_time:.6f} s")
    print(f"Custom writer time: {custom_writer_time:.6f} s")
    print(f"Std    writer time: {std_writer_time:.6f} s")


if __name__ == "__main__":
    main()
