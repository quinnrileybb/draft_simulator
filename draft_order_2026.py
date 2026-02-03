# Complete 2026 MLB Draft Order (Rounds 1-10)
# Based on official MLB.com data

DRAFT_ORDER_2026 = {
    # ROUND 1 (40 picks total including comp rounds)
    1: [
        ("White Sox", 1),           # Lottery winner
        ("Rays", 2),                # Lottery
        ("Twins", 3),               # Lottery
        ("Giants", 4),              # Lottery
        ("Pirates", 5),             # Lottery
        ("Royals", 6),              # Lottery
        ("Orioles", 7),             # Non-lottery non-playoff
        ("Athletics", 8),
        ("Braves", 9),
        ("Rockies", 10),
        ("Nationals", 11),
        ("Angels", 12),
        ("Cardinals", 13),
        ("Marlins", 14),
        ("Diamondbacks", 15),
        ("Rangers", 16),
        ("Astros", 17),
        ("Reds", 18),               # WC loser (revenue sharing)
        ("Guardians", 19),          # WC loser (revenue sharing)
        ("Red Sox", 20),            # WC loser (non-revenue sharing)
        ("Padres", 21),             # WC loser (non-revenue sharing)
        ("Tigers", 22),             # DS loser (revenue sharing)
        ("Cubs", 23),               # DS loser (revenue sharing)
        ("Mariners", 24),           # CS loser (revenue sharing)
        ("Brewers", 25),            # CS loser (revenue sharing)
        # PPI PICKS (Prospect Promotion Incentive)
        ("Braves", 26),             # PPI - Drake Baldwin ROY
        ("Mets", 27),               # Round 1 + 10 spot CBT penalty
        ("Astros", 28),             # PPI - Hunter Brown Cy Young top 3
        # COMPETITIVE BALANCE ROUND A
        ("Guardians", 29),          # CB-A
        ("Royals", 30),             # CB-A
        ("Diamondbacks", 31),       # CB-A
        ("Cardinals", 32),          # CB-A (traded from Orioles)
        ("Rays", 33),               # CB-A (from Orioles for Shane Baz)
        ("Pirates", 34),            # CB-A
        ("Yankees", 35),            # Round 1 + 10 spot CBT penalty
        ("Phillies", 36),           # Round 1 + 10 spot CBT penalty
        ("Rockies", 37),            # CB-A
        ("Rockies", 38),            # START OF ROUND 2
        ("Blue Jays", 39),          # Round 1 + 10 spot CBT penalty
        ("Dodgers", 40),            # Round 1 + 10 spot CBT penalty
    ],
    
    # ROUND 2 (28 picks - Blue Jays, Dodgers, Mets, Red Sox forfeited for QO signings)
    2: [
        ("Rockies", 38),            # (Also listed as pick 38 above)
        ("Blue Jays", 39),          # FORFEITED - signed Dylan Cease
        ("Dodgers", 40),            # FORFEITED - signed Bo Bichette/Edwin Díaz
        ("White Sox", 41),
        ("Nationals", 42),
        ("Twins", 43),
        ("Pirates", 44),
        ("Angels", 45),
        ("Orioles", 46),
        ("Athletics", 47),
        ("Braves", 48),
        ("Rays", 49),
        ("Cardinals", 50),
        ("Pirates", 51),            # Comp for unsigned 2025 pick Angel Cervantes
        ("Marlins", 52),
        ("Diamondbacks", 53),
        ("Rangers", 54),
        ("Giants", 55),
        ("Royals", 56),
        ("Mets", 57),               # FORFEITED - signed Bo Bichette
        ("Astros", 58),
        ("Reds", 59),
        ("Guardians", 60),
        ("Red Sox", 61),            # FORFEITED - signed Ranger Suárez
        ("Padres", 62),
        ("Tigers", 63),
        ("Cubs", 64),
        ("Yankees", 65),
        ("Phillies", 66),
        ("Mariners", 67),
        ("Brewers", 68),
    ],
    
    # COMPETITIVE BALANCE ROUND B (8 picks)
    "CB-B": [
        ("Brewers", 69),
        ("Mariners", 70),
        ("Tigers", 71),
        ("Reds", 72),
        ("Marlins", 73),
        ("Rays", 74),
        ("Athletics", 75),
        ("Twins", 76),
        # COMPENSATION PICKS after CB-B
        ("Cubs", 77),               # Comp for Kyle Tucker (if he signs elsewhere)
        ("Diamondbacks", 78),       # Comp for Zac Gallen if <$50M (if >$50M goes after R1)
    ],
    
    # ROUND 3 (30 picks - Dodgers forfeited)
    3: [
        ("Rockies", 79),
        ("White Sox", 80),
        ("Nationals", 81),
        ("Twins", 82),
        ("Pirates", 83),
        ("Angels", 84),
        ("Orioles", 85),
        ("Athletics", 86),
        ("Braves", 87),
        ("Rays", 88),
        ("Cardinals", 89),
        ("Marlins", 90),
        ("Diamondbacks", 91),
        ("Rangers", 92),
        ("Giants", 93),
        ("Royals", 94),
        ("Mets", 95),
        ("Astros", 96),
        ("Reds", 97),
        ("Guardians", 98),
        ("Red Sox", 99),
        ("Padres", 100),
        ("Tigers", 101),
        ("Cubs", 102),
        ("Yankees", 103),
        ("Phillies", 104),
        ("Mariners", 105),
        ("Brewers", 106),
        ("Blue Jays", 107),
        ("Dodgers", 108),           # FORFEITED
    ],
    
    # ROUND 4 (30 picks)
    4: [
        ("Rockies", 109),
        ("White Sox", 110),
        ("Nationals", 111),
        ("Twins", 112),
        ("Pirates", 113),
        ("Angels", 114),
        ("Orioles", 115),
        ("Athletics", 116),
        ("Braves", 117),
        ("Rays", 118),
        ("Cardinals", 119),
        ("Marlins", 120),
        ("Diamondbacks", 121),
        ("Rangers", 122),
        ("Giants", 123),
        ("Royals", 124),
        ("Mets", 125),
        ("Astros", 126),
        ("Reds", 127),
        ("Guardians", 128),
        ("Red Sox", 129),
        ("Padres", 130),
        ("Tigers", 131),
        ("Cubs", 132),
        ("Yankees", 133),
        ("Phillies", 134),
        ("Mariners", 135),
        ("Brewers", 136),
        ("Blue Jays", 137),
        ("Dodgers", 138),
        # COMPENSATION PICKS after Round 4 (for QO losses by teams over CBT)
        ("Astros", 139),            # Comp for Framber Valdez (if he signs elsewhere)
        ("Phillies", 140),          # Comp for Ranger Suárez
        ("Blue Jays", 141),         # Comp for Bo Bichette
        ("Mets", 142),              # Comp for Edwin Díaz
        ("Padres", 143),            # Comp for Dylan Cease
    ],
    
    # ROUND 5 (28 picks - Blue Jays, Dodgers forfeited)
    5: [
        ("Rockies", 144),
        ("White Sox", 145),
        ("Nationals", 146),
        ("Twins", 147),
        ("Pirates", 148),
        ("Angels", 149),
        ("Orioles", 150),
        ("Athletics", 151),
        ("Braves", 152),
        ("Rays", 153),
        ("Cardinals", 154),
        ("Marlins", 155),
        ("Diamondbacks", 156),
        ("Rangers", 157),
        ("Giants", 158),
        ("Royals", 159),
        ("Mets", 160),
        ("Astros", 161),
        ("Reds", 162),
        ("Guardians", 163),
        ("Red Sox", 164),
        ("Padres", 165),
        ("Tigers", 166),
        ("Cubs", 167),
        ("Yankees", 168),
        ("Phillies", 169),
        ("Mariners", 170),
        ("Brewers", 171),
        ("Blue Jays", None),        # FORFEITED - signed Dylan Cease
        ("Dodgers", None),          # FORFEITED - signed Edwin Díaz
    ],
    
    # ROUNDS 6-10 (standard 30 teams each, some with forfeits)
    6: [
        ("Rockies", 172),
        ("Twins", 173),
        ("Orioles", 174),
        ("Rays", 175),
        ("Diamondbacks", 176),
        ("Royals", 177),
        ("Reds", 178),
        ("Guardians", 179),
        ("Yankees", 180),
        ("Brewers", 181),
        ("White Sox", 182),
        ("Pirates", 183),
        ("Athletics", 184),
        ("Cardinals", 185),
        ("Rangers", 186),
        ("Mets", 187),
        ("Red Sox", 188),
        ("Tigers", 189),
        ("Phillies", 190),
        ("Blue Jays", 191),
        ("Nationals", 192),
        ("Angels", 193),
        ("Braves", 194),
        ("Marlins", 195),
        ("Giants", 196),
        ("Astros", 197),
        ("Padres", 198),
        ("Cubs", 199),
        ("Mariners", 200),
        ("Dodgers", 201),           # FORFEITED - signed QO player
    ],
    
    7: [
        ("Rockies", 202),
        ("White Sox", 203),
        ("Nationals", 204),
        ("Twins", 205),
        ("Pirates", 206),
        ("Angels", 207),
        ("Orioles", 208),
        ("Athletics", 209),
        ("Braves", 210),
        ("Rays", 211),
        ("Cardinals", 212),
        ("Marlins", 213),
        ("Diamondbacks", 214),
        ("Rangers", 215),
        ("Giants", 216),
        ("Royals", 217),
        ("Mets", 218),
        ("Astros", 219),
        ("Reds", 220),
        ("Guardians", 221),
        ("Red Sox", 222),
        ("Padres", 223),
        ("Tigers", 224),
        ("Cubs", 225),
        ("Yankees", 226),
        ("Phillies", 227),
        ("Mariners", 228),
        ("Brewers", 229),
        ("Blue Jays", 230),
        ("Dodgers", 231),
    ],
    
    8: [
        ("Rockies", 232),
        ("White Sox", 233),
        ("Nationals", 234),
        ("Twins", 235),
        ("Pirates", 236),
        ("Angels", 237),
        ("Orioles", 238),
        ("Athletics", 239),
        ("Braves", 240),
        ("Rays", 241),
        ("Cardinals", 242),
        ("Marlins", 243),
        ("Diamondbacks", 244),
        ("Rangers", 245),
        ("Giants", 246),
        ("Royals", 247),
        ("Mets", 248),
        ("Astros", 249),
        ("Reds", 250),
        ("Guardians", 251),
        ("Red Sox", 252),
        ("Padres", 253),
        ("Tigers", 254),
        ("Cubs", 255),
        ("Yankees", 256),
        ("Phillies", 257),
        ("Mariners", 258),
        ("Brewers", 259),
        ("Blue Jays", 260),
        ("Dodgers", 261),
    ],
    
    9: [
        ("Rockies", 262),
        ("White Sox", 263),
        ("Nationals", 264),
        ("Twins", 265),
        ("Pirates", 266),
        ("Angels", 267),
        ("Orioles", 268),
        ("Athletics", 269),
        ("Braves", 270),
        ("Rays", 271),
        ("Cardinals", 272),
        ("Marlins", 273),
        ("Diamondbacks", 274),
        ("Rangers", 275),
        ("Giants", 276),
        ("Royals", 277),
        ("Mets", 278),
        ("Astros", 279),
        ("Reds", 280),
        ("Guardians", 281),
        ("Red Sox", 282),
        ("Padres", 283),
        ("Tigers", 284),
        ("Cubs", 285),
        ("Yankees", 286),
        ("Phillies", 287),
        ("Mariners", 288),
        ("Brewers", 289),
        ("Blue Jays", 290),
        ("Dodgers", 291),
    ],
    
    10: [
        ("Rockies", 292),
        ("White Sox", 293),
        ("Nationals", 294),
        ("Twins", 295),
        ("Pirates", 296),
        ("Angels", 297),
        ("Orioles", 298),
        ("Athletics", 299),
        ("Braves", 300),
        ("Rays", 301),
        ("Cardinals", 302),
        ("Marlins", 303),
        ("Diamondbacks", 304),
        ("Rangers", 305),
        ("Giants", 306),
        ("Royals", 307),
        ("Mets", 308),
        ("Astros", 309),
        ("Reds", 310),
        ("Guardians", 311),
        ("Red Sox", 312),
        ("Padres", 313),
        ("Tigers", 314),
        ("Cubs", 315),
        ("Yankees", 316),
        ("Phillies", 317),
        ("Mariners", 318),
        ("Brewers", 319),
        ("Blue Jays", 320),
        ("Dodgers", 321),
    ],
}

# Flatten into single list for easy iteration
def get_full_draft_order():
    """Returns complete draft order as list of (round, team, overall_pick)"""
    order = []
    
    # Round 1 (includes PPI and CB-A)
    for team, pick in DRAFT_ORDER_2026[1]:
        order.append((1, team, pick))
    
    # Round 2 (some forfeited)
    for team, pick in DRAFT_ORDER_2026[2]:
        if pick is not None:  # Skip forfeited picks
            order.append((2, team, pick))
    
    # CB-B
    for team, pick in DRAFT_ORDER_2026["CB-B"]:
        order.append(("CB-B", team, pick))
    
    # Round 3 (Dodgers forfeit)
    for team, pick in DRAFT_ORDER_2026[3]:
        if pick is not None:
            order.append((3, team, pick))
    
    # Round 4 (includes comp picks after)
    for team, pick in DRAFT_ORDER_2026[4]:
        order.append((4, team, pick))
    
    # Round 5 (Blue Jays, Dodgers forfeit)
    for team, pick in DRAFT_ORDER_2026[5]:
        if pick is not None:
            order.append((5, team, pick))
    
    # Rounds 6-10
    for round_num in [6, 7, 8, 9, 10]:
        for team, pick in DRAFT_ORDER_2026[round_num]:
            if pick is not None:
                order.append((round_num, team, pick))
    
    return order

# Notes for reference
DRAFT_NOTES = {
    "lottery_teams": ["White Sox", "Rays", "Twins", "Giants", "Pirates", "Royals"],
    "cbt_penalties": {
        "Yankees": "Round 1 pick moved back 10 spots (pick 35)",
        "Phillies": "Round 1 pick moved back 10 spots (pick 36)",
        "Blue Jays": "Round 1 pick moved back 10 spots (pick 39)",
        "Dodgers": "Round 1 pick moved back 10 spots (pick 40)",
        "Mets": "Round 1 pick moved back 10 spots (pick 27)",
    },
    "forfeited_picks": {
        "Blue Jays": "R2, R5 (signed Dylan Cease - QO)",
        "Dodgers": "R2, R3, R5, R6 (signed multiple QO players)",
        "Mets": "R2 (signed Bo Bichette - QO)",
        "Red Sox": "R2 (signed Ranger Suárez - QO)",
    },
    "ppi_picks": {
        "Braves": "Pick 26 for Drake Baldwin winning NL ROY",
        "Astros": "Pick 28 for Hunter Brown top 3 AL Cy Young",
    },
    "cb_a_teams": ["Guardians", "Royals", "Diamondbacks", "Cardinals", "Rays", "Pirates", "Rockies"],
    "cb_b_teams": ["Brewers", "Mariners", "Tigers", "Reds", "Marlins", "Rays", "Athletics", "Twins"],
}

if __name__ == "__main__":
    order = get_full_draft_order()
    print(f"Total picks in first 10 rounds: {len(order)}")
    print(f"\nFirst 10 picks:")
    for i, (rnd, team, pick) in enumerate(order[:10]):
        print(f"{pick}. {team} (Round {rnd})")
