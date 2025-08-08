from Function.iRail_API import IRailAPI
from pprint import pprint

api = IRailAPI(lang="en")

# 🔹 LIVEBOARD
print("\n📍 🔹 LIVEBOARD (Brussels-Central)")
liveboard = api.get_liveboard(station="Brussels-Central")
pprint(liveboard)

# 🔹 CONNECTIONS
print("\n🔁 🔹 CONNECTIONS (Brussels-Central → Gent-Sint-Pieters)")
connections = api.get_connections(from_station="Brussels-Central", to_station="Gent-Sint-Pieters")
pprint(connections)

# 🔹 VEHICLE (on prend le 1er vehicle du liveboard pour exemple)
print("\n🚂 🔹 VEHICLE (détails du train)")


from datetime import datetime

# 1. Récupérer ID propre
vehicle_raw = liveboard['departures']['departure'][0]['vehicle']
vehicle_id = vehicle_raw.split(".")[-1]

# 2. Extraire date correcte
timestamp = int(liveboard['departures']['departure'][0]['time'])
date_str = datetime.fromtimestamp(timestamp).strftime("%d%m%y")

# 3. Appel correct



if vehicle_id:
    vehicle_data = api.get_vehicle(vehicle_id, date=date_str)
    pprint(vehicle_data)
else:
    print("❌ Aucun vehicle ID trouvé dans liveboard")

# 🔹 DISTURBANCES
print("\n⚠️ 🔹 DISTURBANCES (perturbations actuelles)")
disturbances = api.get_disturbances()
pprint(disturbances)
