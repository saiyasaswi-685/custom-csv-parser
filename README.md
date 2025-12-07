# Custom CSV Parser in Python  
**Author: Sai Yasaswi Bandaru**

---

## Overview

This project implements a **custom CSV reader and writer from scratch in Python**.

The goal is to understand:

- How CSV parsing works internally  
- How to handle tricky CSV edge cases:
  - Fields wrapped in double quotes (`"`)
  - Escaped quotes (`""` → `"`)
  - Commas inside fields
  - Newlines inside quoted fields  

The project also includes a **benchmark** comparing the custom parser with Python's built-in `csv` module.

---

## Project Structure

```
custom_csv_parser/
├── csv_parser.py             # CustomCsvReader and CustomCsvWriter classes
├── generate_data.py          # Script to generate sample_10k.csv
├── benchmark_csv_parser.py   # Benchmark against Python's csv module
└── README.md                 # Project documentation
```

---

## Custom CSV Reader

The **CustomCsvReader**:

- Processes the file **character-by-character** (streaming)
- Uses a **state machine**:
  - `in_quotes = True` → inside a quoted field
  - `in_quotes = False` → normal parsing mode
- Correctly handles:
  - Commas inside quoted fields (`"hello,world"`)
  - Escaped quotes (`""` → `"`)
  - Newlines inside quoted fields
  - Empty fields (`,,`)

The reader is implemented as an **iterator**, using:

```python
__iter__()
__next__()
```

Example:

```python
with open("sample_10k.csv") as f:
    reader = CustomCsvReader(f)
    for row in reader:
        print(row)
```

---

## Custom CSV Writer

The **CustomCsvWriter**:

- Automatically wraps fields in quotes if they contain commas, quotes, or newlines  
- Escapes internal quotation marks (`"` → `""`)  
- Produces valid CSV files readable by any standard CSV reader  

Example:

```python
with open("output.csv", "w") as f:
    writer = CustomCsvWriter(f)
    writer.write_rows([
        ["name", "comment"],
        ["Alice", "hello,world"],
        ["Bob", "line1\nline2"],
        ["Charlie", "He said \"ok\""]
    ])
```

---

## Setup & Usage

### 1️⃣ Generate sample CSV file (10,000 rows)

Run:

```bash
python generate_data.py
```

This creates:

```
sample_10k.csv
```

### 2️⃣ Reading a CSV file

```python
from csv_parser import CustomCsvReader

with open("sample_10k.csv", encoding="utf-8") as f:
    reader = CustomCsvReader(f)
    for row in reader:
        print(row)
```

### 3️⃣ Writing a CSV file

```python
from csv_parser import CustomCsvWriter

rows = [
    ["name", "comment"],
    ["Alice", "hello,world"],
    ["Bob", "line1\nline2"]
]

with open("output.csv", "w", newline="", encoding="utf-8") as f:
    writer = CustomCsvWriter(f)
    writer.write_rows(rows)
```

---

## Benchmark Results (Actual Output)

These results were produced by running:

```bash
python benchmark_csv_parser.py
```

**Actual measured times:**

```
=== Reader benchmarks ===
CustomCsv reader avg time over 5 runs: 0.070599 seconds
StdCsv reader avg time over 5 runs: 0.006542 seconds

=== Writer benchmarks ===
CustomCsv writer avg time over 5 runs: 0.016942 seconds
StdCsv writer avg time over 5 runs: 0.009597 seconds

=== Summary ===
Custom reader time: 0.070599 s
Std    reader time: 0.006542 s
Custom writer time: 0.016942 s
Std    writer time: 0.009597 s
```

**Observations:**

- Python's built-in `csv` module is faster (written in C).
- The custom CSV reader/writer works correctly and handles all edge cases.
- Performance is reasonable for a pure Python implementation.

---

## Key Concepts Learned

- **File I/O**  
- **String manipulation**  
- **State machine design for parsing**  
- **Handling escaped and quoted fields**  
- **Benchmarking using time.perf_counter()**  
- **Streaming data processing**  

---

## Conclusion

This project demonstrates:

- A fully functional CSV parser built manually from scratch  
- Correct handling of CSV complexities like commas, quotes, and newlines  
- Clean and readable Python implementation  
- Measured performance compared to the standard csv module  

The project meets all requirements, including:

✔ CustomCsvReader  
✔ CustomCsvWriter  
✔ Benchmarking  
✔ Edge-case handling  
✔ Documentation  


