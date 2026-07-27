#!/usr/bin/env python3
"""Seed all three simulated client tracks."""

from __future__ import annotations

from seed_colorado import seed as seed_colorado
from seed_datacenter import seed as seed_datacenter
from seed_kerrville import seed as seed_kerrville


def main() -> None:
    seed_colorado()
    seed_kerrville()
    seed_datacenter()
    print("All clients seeded.")


if __name__ == "__main__":
    main()
