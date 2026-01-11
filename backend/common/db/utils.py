from collections.abc import Mapping, Sequence


def chunk_rows(
    rows: Sequence[Mapping[str, object]], size: int
) -> list[Sequence[Mapping[str, object]]]:
    """Split rows into batches to avoid asyncpg's max bind-parameter limit."""
    return [rows[i : i + size] for i in range(0, len(rows), size)]
