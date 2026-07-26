#!/usr/bin/env python3
"""Seed all three simulated client tracks."""

from __future__ import annotations

from seed_ironwood import seed as seed_ironwood
from seed_northwood import seed as seed_northwood
from seed_strata import seed as seed_strata


def main() -> None:
    seed_ironwood()
    seed_strata()
    seed_northwood()
    print("All clients seeded.")


if __name__ == "__main__":
    main()
