from __future__ import annotations

import sqlite3
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "donations.db"

app = Flask(__name__)


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS donations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                donor_name TEXT NOT NULL,
                amount_cents INTEGER NOT NULL,
                message TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def parse_amount_to_cents(amount_text: str) -> int:
    try:
        amount_decimal = Decimal(amount_text).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except InvalidOperation as exc:
        raise ValueError("Amount must be a valid number.") from exc

    if amount_decimal <= 0:
        raise ValueError("Amount must be greater than 0.")

    return int(amount_decimal * 100)


def get_donations_and_total() -> tuple[list[sqlite3.Row], int]:
    with get_connection() as conn:
        donations = conn.execute(
            """
            SELECT donor_name, amount_cents, message, created_at
            FROM donations
            ORDER BY id DESC
            """
        ).fetchall()

        total_cents = conn.execute("SELECT COALESCE(SUM(amount_cents), 0) AS total FROM donations").fetchone()[
            "total"
        ]

    return donations, int(total_cents)


@app.template_filter("money")
def format_money(cents: int) -> str:
    dollars = Decimal(cents) / Decimal(100)
    return f"${dollars:,.2f}"


@app.route("/", methods=["GET", "POST"])
def index():
    error = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        amount_text = request.form.get("amount", "").strip()
        message = request.form.get("message", "").strip()

        if not name:
            error = "Name is required."
        elif not message:
            error = "Message is required."
        else:
            try:
                amount_cents = parse_amount_to_cents(amount_text)
            except ValueError as exc:
                error = str(exc)
            else:
                with get_connection() as conn:
                    conn.execute(
                        """
                        INSERT INTO donations (donor_name, amount_cents, message)
                        VALUES (?, ?, ?)
                        """,
                        (name, amount_cents, message),
                    )
                return redirect(url_for("index"))

    donations, total_cents = get_donations_and_total()
    return render_template("index.html", donations=donations, total_cents=total_cents, error=error)


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
