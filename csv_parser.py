"""
Custom CSV reader and writer implemented from scratch.

This module defines CustomCsvReader and CustomCsvWriter classes that mimic
the behaviour of Python's csv.reader and csv.writer for common cases.

Features:
- Comma-separated values
- Quoted fields using "
- Escaped quotes written as ""
- Newlines inside quoted fields
- Streaming reader: rows are produced one by one
"""

from typing import List, Iterable, TextIO, Optional


class CustomCsvReader:
    """Simple streaming CSV reader implemented from scratch.

    This class supports:
    - Comma-delimited CSV files
    - Fields enclosed in double quotes (")
    - Escaped double quotes ("") inside quoted fields
    - Newline characters inside quoted fields
    """

    def __init__(
        self,
        file_obj: TextIO,
        delimiter: str = ",",
        quotechar: str = '"',
    ) -> None:
        """Initialise the reader.

        Args:
            file_obj: An open text file object to read from.
            delimiter: The character that separates fields (default: comma).
            quotechar: The character used for quoting (default: ").
        """
        self.file = file_obj
        self.delimiter = delimiter
        self.quotechar = quotechar
        self._buffered_char: Optional[str] = None
        self._eof = False

    def __iter__(self) -> "CustomCsvReader":
        """Return the iterator object (self)."""
        return self

    # ---- internal helpers -------------------------------------------------

    def _read_char(self) -> str:
        """Read the next character, using buffered char if available."""
        if self._buffered_char is not None:
            ch = self._buffered_char
            self._buffered_char = None
            return ch
        return self.file.read(1)

    def _unread_char(self, ch: str) -> None:
        """Push a character back so it will be read again next time."""
        self._buffered_char = ch

    # ---- iterator protocol ------------------------------------------------

    def __next__(self) -> List[str]:
        """Parse and return the next row as a list of strings.

        Raises:
            StopIteration: When the end of the file is reached.
        """
        if self._eof:
            raise StopIteration

        row: List[str] = []
        field_chars: List[str] = []
        in_quotes = False

        while True:
            ch = self._read_char()

            if ch == "":
                # End of file
                if in_quotes:
                    # If file ends while inside quotes, treat as end of field.
                    in_quotes = False
                if field_chars or row:
                    # There is a last field / row to return.
                    row.append("".join(field_chars))
                    return row
                self._eof = True
                raise StopIteration

            if in_quotes:
                # We are inside a quoted field.
                if ch == self.quotechar:
                    # Could be end of quoted field or escaped quote.
                    next_ch = self._read_char()
                    if next_ch == self.quotechar:
                        # Escaped quote ("") -> literal " in the field.
                        field_chars.append(self.quotechar)
                    else:
                        # End of quoted field.
                        in_quotes = False
                        if next_ch != "":
                            # Put the next char back for normal processing.
                            self._unread_char(next_ch)
                else:
                    # Any other char (including newline) is part of field.
                    field_chars.append(ch)
            else:
                # We are NOT inside quotes.
                if ch == self.delimiter:
                    # End of field.
                    row.append("".join(field_chars))
                    field_chars = []
                elif ch == "\n":
                    # End of line with Unix newline.
                    row.append("".join(field_chars))
                    return row
                elif ch == "\r":
                    # Handle Windows-style \r\n newlines.
                    next_ch = self._read_char()
                    if next_ch != "\n" and next_ch != "":
                        self._unread_char(next_ch)
                    row.append("".join(field_chars))
                    return row
                elif ch == self.quotechar and not field_chars:
                    # Starting a quoted field (only valid at beginning of field).
                    in_quotes = True
                else:
                    # Normal character inside an unquoted field.
                    field_chars.append(ch)


class CustomCsvWriter:
    """Simple CSV writer implemented from scratch.

    This writer:
    - Writes lists of strings as CSV rows.
    - Automatically quotes fields that contain:
        * the delimiter
        * a double quote
        * a newline
    - Escapes internal quotes by doubling them (" -> "").
    """

    def __init__(
        self,
        file_obj: TextIO,
        delimiter: str = ",",
        quotechar: str = '"',
        lineterminator: str = "\n",
    ) -> None:
        """Initialise the writer.

        Args:
            file_obj: An open text file object to write to.
            delimiter: The character that separates fields.
            quotechar: The character used for quoting.
            lineterminator: Line ending used after each row.
        """
        self.file = file_obj
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.lineterminator = lineterminator

    # ---- internal helpers -------------------------------------------------

    def _escape_and_quote_field(self, field) -> str:
        """Return a field as a correctly escaped CSV string."""
        if field is None:
            field_str = ""
        else:
            field_str = str(field)

        needs_quote = (
            self.delimiter in field_str
            or self.quotechar in field_str
            or "\n" in field_str
            or "\r" in field_str
        )

        if needs_quote:
            # Escape existing quotes by doubling them.
            field_str = field_str.replace(self.quotechar, self.quotechar * 2)
            # Wrap the whole field in quotes.
            field_str = f"{self.quotechar}{field_str}{self.quotechar}"

        return field_str

    # ---- public API -------------------------------------------------------

    def write_row(self, row: Iterable[object]) -> None:
        """Write a single CSV row.

        Args:
            row: An iterable of values to write as one row.
        """
        escaped_fields = [self._escape_and_quote_field(f) for f in row]
        line = self.delimiter.join(escaped_fields) + self.lineterminator
        self.file.write(line)

    def write_rows(self, rows: Iterable[Iterable[object]]) -> None:
        """Write multiple CSV rows."""
        for row in rows:
            self.write_row(row)

    # For easier compatibility with csv.writer
    def writerows(self, rows: Iterable[Iterable[object]]) -> None:
        """Alias for write_rows to resemble csv.writer API."""
        self.write_rows(rows)


if __name__ == "__main__":
    # Small manual demo (optional).
    import io

    data = [
        ["a", "b", "c"],
        ["hello,world", "2", "3"],
        ["line1\nline2", "x", 'y"z'],
        ["", "", "empty"],
    ]

    buffer = io.StringIO()
    writer = CustomCsvWriter(buffer)
    writer.write_rows(data)

    csv_text = buffer.getvalue()
    print("Written CSV:")
    print(csv_text)

    print("Parsed back:")
    buffer.seek(0)
    reader = CustomCsvReader(buffer)
    for row in reader:
        print(row)
