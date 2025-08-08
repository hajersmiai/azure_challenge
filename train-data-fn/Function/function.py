from datetime import datetime
from Function.Train_repository import TrainDataRepository
from Function.iRail_API import IRailAPI

def ingest_all_data(max_from: int = None, max_to: int = None):
    # Connect to Azure SQL
    repo = TrainDataRepository(
        server="train-sql-serve-hajer.database.windows.net",
        database="train-data-db",
        uid="sqladmin",
        pwd="Th021008...."
    )

    # -------------------------
    # 1. Insert Train Departures
    # -------------------------
    print("\n Fetching train departures...")
    stations_dict = repo.api.get_stations()
    station_names = [s["name"] for s in stations_dict.values() if s.get("name")]

    # Appliquer la limite si max_from est défini
    from_list = station_names if max_from is None else station_names[:max_from]

    for station in from_list:
        repo.insert_train_departures(station)

    # -------------------------
    # 2. Insert Disturbances
    # -------------------------
    print("\n Fetching disturbances...")
    disturbances = repo.api.get_disturbances()
    for d in disturbances:
        repo.insert_disturbance(
            disturbance_id=d["id"],
            title=d.get("title"),
            description=d.get("description"),
            type=d.get("type"),
            timestamp=d.get("timestamp", datetime.now()),
            link=d.get("link"),
            attachment=d.get("attachment")
        )

    # -------------------------
    # 3. Insert Train Connections
    # -------------------------
    print("\n Building connection pairs dynamically...")

    # Appliquer la limite si max_to est défini
    to_list = station_names if max_to is None else station_names[:max_to]

    connection_pairs = [
        (from_station, to_station)
        for from_station in from_list
        for to_station in to_list
        if from_station != to_station
    ]

    print(f" Generated {len(connection_pairs)} connection pairs from API")

    for from_station, to_station in connection_pairs:
        try:
            connections = repo.api.get_connections(from_station=from_station, to_station=to_station)
            for c in connections:
                departure_ts = int(c["departure"]["time"])
                arrival_ts = int(c["arrival"]["time"])
                repo.insert_train_connections(
                    departure_station=from_station,
                    arrival_station=to_station,
                    departure_time=datetime.fromtimestamp(departure_ts),
                    arrival_time=datetime.fromtimestamp(arrival_ts),
                    duration=c.get("duration", ""),
                    train_vehicle=c.get("vehicle", ""),
                    number_of_vias=len(c.get("vias", {}).get("via", []))
                )
        except Exception as e:
            print(f" Failed to insert connection {from_station} → {to_station}: {e}")

    print("\n Data ingestion completed.")
