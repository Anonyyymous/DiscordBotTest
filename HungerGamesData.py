environments = {  # 
    "swamp": {
        "players": [],
        "deaths": [["(v) was eaten by an alligator", "(v) slipped and fell into the swamps"], 
              ["(k) threw an alligator at (v)", "(k) told (v) to eat a toad, it was poisonous"]],
        "has events": False,
        "events": [""]
    },
    "volcano": {
        "players": [],
        "deaths": [["(v) fell into a lava stream", "(v) died from a rock fall"],
                   ["(k) pushed (v) into the lava", "(k) roasted (v) like a marshmellow"]],
        "has events": True,
        "events": ["The volcano errupted"],
        "event deaths": -1
    },
    "planes": {
        "players": [],
        "deaths": [["(v) was trampled by a horse", "(v) was mauled by a tiger"], 
              ["(v) was torn to shreds by a hoard of monkeys controlled by (k)", "(k) sexxed (v) to death against a tree", "(k) vored (v) and (v) liked it too much"]],
        "has events": True,
        "events": ["a stampede of horses ran all over the planes"]
    }
}
possible_environments = ["planes", "swamp", "volcano"]
actions = [
    ("(v) made a spear", 2),
    ("(v) found a sword", 3),
    ("(v) found a gun", 5),
    ("(v) awakened Star Platinum", 10),
    ("(v) slipped on a bannana peel and broke their leg", -2),
    ("(v) got fined for tax fraud", 4),
    ("(v) is wanted by the FBI", 2),
    ("(v) is wanted in 16 states", 1),
]
pvps = [
    "(k) punched (v) to death",
    "(k) stranged (v)",
    "(k) stepped on (v) and (v) liked it so much they died",
    "(k) smothered (v) with their ass",
    "(k) forced (v) to commit seppuku",
    "(k) pegged (v) too hard",
    "(v) got vored by (v)",
    "(k) stabbed (v) while they watched jojos",
]
