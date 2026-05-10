"""
Script: seed_courts.py
Seeds a JSON file of sample courts for use in dev/testing.
In production this would seed a database.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from pathlib import Path


COURTS = [
    {"id": 1, "name": "Padel Arena DHA", "sport": "Padel", "latitude": 24.7966, "longitude": 67.0681, "price_per_hour": 2500, "rating": 4.7, "available_slots": ["6PM", "7PM", "8PM"]},
    {"id": 2, "name": "Clifton Sports Complex", "sport": "Padel", "latitude": 24.8121, "longitude": 67.0299, "price_per_hour": 2000, "rating": 4.2, "available_slots": ["5PM", "6PM"]},
    {"id": 3, "name": "Green Court Badminton", "sport": "Badminton", "latitude": 24.8607, "longitude": 67.0011, "price_per_hour": 5000, "rating": 4.5, "available_slots": ["7AM", "8AM", "5PM", "6PM"]},
    {"id": 4, "name": "Korangi Cricket Ground", "sport": "Cricket", "latitude": 24.8324, "longitude": 67.1282, "price_per_hour": 4000, "rating": 3.9, "available_slots": ["6AM", "7AM"]},
    {"id": 5, "name": "North Nazimabad Football Club", "sport": "Football", "latitude": 24.9239, "longitude": 67.0621, "price_per_hour": 2000, "rating": 4.1, "available_slots": ["4PM", "5PM", "6PM"]},
    {"id": 6, "name": "Elite Basketball Academy", "sport": "Basketball", "latitude": 24.8715, "longitude": 67.0421, "price_per_hour": 3000, "rating": 4.6, "available_slots": ["3PM", "4PM", "7PM"]},
    {"id": 7, "name": "Gulshan Badminton Hall", "sport": "Badminton", "latitude": 24.9215, "longitude": 67.0931, "price_per_hour": 5000, "rating": 4.0, "available_slots": ["6AM", "8PM", "9PM"]},
    {"id": 8, "name": "Defence Padel Club", "sport": "Padel", "latitude": 24.8221, "longitude": 67.0711, "price_per_hour": 2000, "rating": 4.9, "available_slots": ["9AM", "10AM", "6PM", "7PM"]},
    {"id": 9, "name": "Gulshan Cricket Hub", "sport": "Cricket", "latitude": 24.9100, "longitude": 67.0800, "price_per_hour": 2000, "rating": 4.3, "available_slots": ["6AM", "7AM", "5PM"]},
    {"id": 10, "name": "PECHS Basketball Court", "sport": "Basketball", "latitude": 24.8780, "longitude": 67.0580, "price_per_hour": 1000, "rating": 4.4, "available_slots": ["4PM", "5PM", "6PM", "7PM"]},
    {"id": 11, "name": "Landhi Football Ground", "sport": "Football", "latitude": 24.8400, "longitude": 67.1600, "price_per_hour": 2000, "rating": 3.7, "available_slots": ["5PM", "6PM"]},
    {"id": 12, "name": "Malir Cricket Ground", "sport": "Cricket", "latitude": 24.8900, "longitude": 67.2000, "price_per_hour": 5000, "rating": 3.5, "available_slots": ["6AM", "7AM"]},
]


def seed():
    output_path = Path("data/raw/courts.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(COURTS, f, indent=2)
    print(f"✅  Seeded {len(COURTS)} courts → {output_path}")


if __name__ == "__main__":
    seed()
