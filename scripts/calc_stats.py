import json

# Canonical name aliases
canonical_map = {
    "jeremy wachtel": "Jeremiah Wachtel",
    "jeremiah/jeremy wachtel": "Jeremiah Wachtel",
    "jeremiah wachtel": "Jeremiah Wachtel",
    "gabrielle cruz": "Gabby Cruz",
    "gabby cruz": "Gabby Cruz",
    "max zubiria": "Maximillian Zubiria",
    "maximillian zubiria": "Maximillian Zubiria",
    "alsx kwok": "Alex Kwok",
    "alex kwok": "Alex Kwok",
    "maya u": "Maya Umylny",
    "maya umylny": "Maya Umylny",
    "ben matsko": "Benjamin Matsko",
    "benjamin matsko": "Benjamin Matsko",
    "nich shelhoff": "Nick Shelhoff",
    "nick shelhoff": "Nick Shelhoff",
    "nicholas shelhoff": "Nick Shelhoff",
    "francis clyde gamil": "Francis Gamil",
    "francis gamil": "Francis Gamil",
    "joshua lim": "Josh Lim",
    "josh lim": "Josh Lim",
    "jordan  jimenez": "Jordan Jimenez",
    "jordan jimenez": "Jordan Jimenez",
    "christopher shuba": "Chris Shuba",
    "chris shuba": "Chris Shuba",
    "anna bryan jones": "Anna Bryan-Jones",
    "anna bryan-jones": "Anna Bryan-Jones",
    "anthony eames egidi": "Anthony Eames-Egidi",
    "anthony eames-egidi": "Anthony Eames-Egidi",
    "natalie detample": "Natalie Detample",
    "natalie de tample": "Natalie Detample",
    "natalie detample": "Natalie Detample",
    "sarah marlene goufo lontchi": "Sarah Marlene Goufo Lontchi"
}

def to_canon(name):
    norm = " ".join(name.strip().lower().split())
    if norm in canonical_map:
        return canonical_map[norm]
    return " ".join([p.capitalize() for p in name.strip().split()])

# Load comp roster
with open("data/roster.json", "r") as f:
    roster_data = json.load(f)

comp_roster = set([to_canon(m["name"]) for m in roster_data["members"]])
print(f"Loaded {len(comp_roster)} comp roster members.")

# Let's import the parsed data from scripts/parse_attendance.py
import sys
sys.path.append('.')
import scripts.parse_attendance as pa

# Also Fight Knight 11/22 attendees
from scripts.fk_check import fk_parsed

fk_attendees = set([to_canon(item[1]) for item in fk_parsed])
print(f"Loaded {len(fk_attendees)} Fight Knight attendees.")

# Let's verify Method attendees
method_attendees = set([to_canon(n) for n in pa.method_31_names])
print(f"Loaded {len(method_attendees)} Method attendees.")

# Build complete unified database of athletes
# athlete_id -> { fullName, team, records: { date: { status, eventType, note } } }
athletes = {}

for m_name in comp_roster:
    c_name = to_canon(m_name)
    athletes[c_name] = {
        "fullName": c_name,
        "team": "Comp Team",
        "records": {}
    }

for c_name, pdata in pa.people_records.items():
    canon = to_canon(c_name)
    if canon not in athletes:
        athletes[canon] = {
            "fullName": canon,
            "team": pdata["team"],
            "records": {}
        }
    else:
        if pdata["team"] == "Comp Team" or canon in comp_roster:
            athletes[canon]["team"] = "Comp Team"
    
    # Merge date records
    for d, status in pdata["attendance"].items():
        if status in ["Present", "Excused", "Absent"]:
            event_type = "regular"
            if d == "2026-10-11":
                event_type = "method_trip"
            elif d == "2026-11-22":
                event_type = "competition"
            athletes[canon]["records"][d] = {
                "status": status.lower(),
                "eventType": event_type
            }

# Now inject Method on 2026-10-11 for method_attendees
for m_name in method_attendees:
    canon = to_canon(m_name)
    if canon not in athletes:
        athletes[canon] = {
            "fullName": canon,
            "team": "Comp Team" if canon in comp_roster else "Rec Team",
            "records": {}
        }
    athletes[canon]["records"]["2026-10-11"] = {
        "status": "present",
        "eventType": "method_trip",
        "practiceName": "Method Trip"
    }

# Now inject Fight Knight on 2026-11-22
for fk_name in fk_attendees:
    canon = to_canon(fk_name)
    if canon not in athletes:
        athletes[canon] = {
            "fullName": canon,
            "team": "Comp Team" if canon in comp_roster else "Rec Team",
            "records": {}
        }
    athletes[canon]["records"]["2026-11-22"] = {
        "status": "present",
        "eventType": "competition",
        "practiceName": "Fight Knight Volume 2 (Competition)"
    }

# All practice dates across the semester
all_dates = sorted(list(set(pa.date_cols + ["2026-10-11", "2026-11-22"])))
print(f"Total semester practice dates ({len(all_dates)}): {all_dates}")

# Calculate stats per athlete
# Rules:
# - Eligible regular practice dates for counting missed:
#   Regular practices are mandatory for Comp team.
#   2026-10-11 (Method) is NOT a missed practice if absent!
#   2026-11-22 (Fight Knight) is NOT a missed practice if absent!
# - Points: +1 point for each Present (including regular practices, Method trip, and Fight Knight).
# - Fight Knight Allowance:
#   If athlete attended Fight Knight (2026-11-22 present):
#     They are granted 1 Excused Absence allowance.
#     If they had unexcused missed practices (missed > 0):
#       1 missed practice is excused (missed -= 1, excused += 1).
#     Even if missed == 0, their comp allowance is noted!

print("\n" + "=" * 95)
print(f"{'Athlete':<24} | {'Team':<10} | {'Points':<7} | {'Missed':<7} | {'Excused':<7} | {'Method':<7} | {'FK Vol 2':<8}")
print("=" * 95)

summary_results = []

for a_name, adata in sorted(athletes.items(), key=lambda x: (x[1]['team'] != 'Comp Team', x[0])):
    team = adata["team"]
    recs = adata["records"]
    
    points = 0
    raw_missed = 0
    excused = 0
    attended_method = (recs.get("2026-10-11", {}).get("status") == "present")
    attended_fk = (recs.get("2026-11-22", {}).get("status") == "present")
    
    # Evaluate dates
    for d in all_dates:
        r = recs.get(d)
        is_method = (d == "2026-10-11")
        is_comp = (d == "2026-11-22")
        
        if r and r["status"] == "present":
            points += 1
        elif r and r["status"] == "excused":
            excused += 1
        else:
            # Absent or not recorded
            # If it's Method or Comp, NOT a missed practice!
            if not is_method and not is_comp:
                if team == "Comp Team":
                    raw_missed += 1
                else:
                    # For rec team, if explicitly recorded as absent
                    if r and r["status"] == "absent":
                        raw_missed += 1

    # Apply Fight Knight 1 excused absence allowance
    final_missed = raw_missed
    effective_excused = excused
    if attended_fk:
        if final_missed > 0:
            final_missed -= 1
            effective_excused += 1

    summary_results.append({
        "name": a_name,
        "team": team,
        "points": points,
        "raw_missed": raw_missed,
        "missed": final_missed,
        "excused": effective_excused,
        "attended_method": attended_method,
        "attended_fk": attended_fk
    })
    
    if team == "Comp Team":
        fk_str = "Yes (+1)" if attended_fk else "No"
        m_str = "Yes" if attended_method else "No"
        print(f"{a_name:<24} | {team:<10} | {points:<7} | {final_missed:<7} | {effective_excused:<7} | {m_str:<7} | {fk_str:<8}")

