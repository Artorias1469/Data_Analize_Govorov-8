#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sqlite3
import typing as t
from pathlib import Path

DATABASE_FILE = "flights.db"

def add_flight(database_path: Path, destination: str, flight_number: str, aircraft_type: str) -> None:
    """
    Добавить новый рейс в базу данных.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO flights (destination, flight_number, aircraft_type)
        VALUES (?, ?, ?)
        """,
        (destination, flight_number, aircraft_type),
    )
    conn.commit()
    conn.close()

def print_flights(database_path: Path) -> None:
    """
    Вывести список всех рейсов из базы данных.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT destination, flight_number, aircraft_type FROM flights
        """
    )
    rows = cursor.fetchall()
    conn.close()

    line = "+-{}-+-{}-+-{}-+".format("-" * 30, "-" * 20, "-" * 15)
    print(line)
    print("| {:^30} | {:^20} | {:^15} |".format("Название пункта назначения", "Номер рейса", "Тип самолета"))
    print(line)

    for row in rows:
        print("| {:<30} | {:<20} | {:<15} |".format(row[0], row[1], row[2]))

    print(line)

def search_flights_by_aircraft_type(database_path: Path, search_aircraft_type: str) -> None:
    """
    Найти рейсы по типу самолета.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT destination, flight_number, aircraft_type FROM flights
        WHERE aircraft_type = ?
        """,
        (search_aircraft_type,),
    )
    rows = cursor.fetchall()
    conn.close()

    if rows:
        line = "+-{}-+-{}-+-{}-+".format("-" * 30, "-" * 20, "-" * 15)
        print(f"\nРейсы, обслуживаемые самолетом типа {search_aircraft_type}: ")
        print(line)
        print("| {:^30} | {:^20} | {:^15} |".format("Название пункта назначения", "Номер рейса", "Тип самолета"))
        print(line)

        for row in rows:
            print("| {:<30} | {:<20} | {:<15} |".format(row[0], row[1], row[2]))

        print(line)
    else:
        print(f"\nРейсов, обслуживаемых самолетом типа {search_aircraft_type}, не найдено.")

def create_tables(database_path: Path) -> None:
    """
    Создать таблицы в базе данных.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS flights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destination TEXT NOT NULL,
            flight_number TEXT NOT NULL,
            aircraft_type TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS aircraft_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL
        )
        """
    )

    conn.close()

def main():
    parser = argparse.ArgumentParser(description="Flight Information Management System")
    parser.add_argument("-a", "--add-flight", action="store_true", help="Add a new flight")
    parser.add_argument("-p", "--print-flights", action="store_true", help="Print the list of flights")
    parser.add_argument("-s", "--search-by-type", help="Search flights by aircraft type")
    args = parser.parse_args()

    database_path = Path(DATABASE_FILE)
    create_tables(database_path)

    if args.add_flight:
        destination = input("Введите название пункта назначения: ")
        flight_number = input("Введите номер рейса: ")
        aircraft_type = input("Введите тип самолета: ")
        add_flight(database_path, destination, flight_number, aircraft_type)

    elif args.print_flights:
        print_flights(database_path)

    elif args.search_by_type:
        search_flights_by_aircraft_type(database_path, args.search_by_type)

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
