import json
import sys
sys.path.append('.')
import scripts.calc_stats as cs

athletes_export = []
for a_name, adata in sorted(cs.athletes.items(), key=lambda x: (x[1]['team'] != 'Comp Team', x[0])):
    norm_key = cs.to_canon(a_name).lower()
    athletes_export.append({
        "nameKey": norm_key,
        "fullName": a_name,
        "team": adata["team"],
        "records": adata["records"]
    })

data_file = {
    "specialEvents": {
        "2026-10-11": {
            "type": "trip",
            "name": "Method Trip",
            "noMissedPenalty": True,
            "grantExcusedAllowance": False
        },
        "2026-11-22": {
            "type": "competition",
            "name": "Fight Knight Volume 2 (Competition)",
            "noMissedPenalty": True,
            "grantExcusedAllowance": True
        }
    },
    "canonicalAliases": cs.canonical_map,
    "athletes": athletes_export
}

with open("data/historical_attendance.json", "w", encoding="utf-8") as f:
    json.dump(data_file, f, indent=2)

print(f"Successfully exported {len(athletes_export)} athletes to data/historical_attendance.json")
