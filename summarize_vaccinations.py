import argparse
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable
import csv

DOSE_COLUMNS = [
    "Primera Dosis",
    "Segunda Dosis",
    "Dosis Refuerzo",
    "Cuarta Dosis",
    "Dosis Única",
]


def load_vaccination_data(csv_path: Path) -> Iterable[Dict[str, str]]:
    """Yield rows from the vaccination CSV file as dictionaries."""
    with csv_path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            yield row


def total_doses_by_manufacturer(rows: Iterable[Dict[str, str]]) -> Dict[str, Dict[str, float]]:
    """Compute total doses per manufacturer using only the standard library."""
    totals: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for row in rows:
        manufacturer = row.get("Fabricante", "Desconocido") or "Desconocido"
        for col in DOSE_COLUMNS:
            try:
                value = float(row.get(col, 0) or 0)
            except ValueError:
                value = 0.0
            totals[manufacturer][col] += value
    return totals


def main(csv_path: Path) -> None:
    rows = load_vaccination_data(csv_path)
    totals = total_doses_by_manufacturer(rows)
    # Sort manufacturers by first dose count in descending order
    sorted_manufacturers = sorted(
        totals.items(), key=lambda item: item[1]["Primera Dosis"], reverse=True
    )
    header = ["Fabricante"] + DOSE_COLUMNS
    print(",".join(header))
    for manufacturer, counts in sorted_manufacturers:
        values = [f"{counts[col]:.0f}" for col in DOSE_COLUMNS]
        print(",".join([manufacturer] + values))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Summarize Chile COVID-19 vaccination dataset by manufacturer."
    )
    parser.add_argument(
        "csv_path",
        nargs="?",
        default="Vacunas.csv",
        type=Path,
        help="Path to the Vacunas.csv dataset.",
    )
    args = parser.parse_args()
    main(args.csv_path)
