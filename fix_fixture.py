"""
Run this script once from your project root:
    python fix_fixture.py

It rewrites cinema_service_db_data.json so all auth.user
entries use email instead of username, making it compatible
with the custom User model.
"""
from __future__ import annotations

import json
import pathlib


FIXTURE_PATH = pathlib.Path("cinema_service_db_data.json")


def fix_fixture(path: pathlib.Path) -> None:
    data: list[dict] = json.loads(path.read_text(encoding="utf-8"))

    for obj in data:
        if obj.get("model") != "user.user":
            continue

        fields: dict = obj["fields"]

        # Promote username value to email if email is missing
        if not fields.get("email"):
            fields["email"] = fields.get("username", "")

        # Remove fields the custom User model no longer has
        fields.pop("username", None)

    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Done — fixture rewritten: {path}")


if __name__ == "__main__":
    fix_fixture(FIXTURE_PATH)
