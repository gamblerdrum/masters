import pandas as pd
import requests
import streamlit as st
from io import StringIO

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Masters Fantasy League",
    page_icon="⛳",
    layout="wide",
)

# ── ESPN Leaderboard URL ──────────────────────────────────────────────────────
URL = "https://www.espn.co.uk/golf/leaderboard/_/tournamentId/401811941"

# ── League participants and picks ─────────────────────────────────────────────
LEAGUE = [
    ("David Spencer",        "Jon Rahm",            "Ludvig Åberg",        "Patrick Reed",        "Dustin Johnson",    "Bryson DeChambeau"),
    ("Sam Quarlena",         "Rory McIlroy",         "Akshay Bhatia",       "Justin Rose",         "Sungjae Im",        "Patrick Reed"),
    ("Chris Hare",           "Scottie Scheffler",    "Ludvig Åberg",        "Justin Rose",         "Dustin Johnson",    "Bryson DeChambeau"),
    ("Aliff Turner",         "Jon Rahm",             "Matt Fitzpatrick",    "Justin Rose",         "Dustin Johnson",    "Robert MacIntyre"),
    ("Phil Chatman",         "Tommy Fleetwood",      "Bryson DeChambeau",   "Justin Rose",         "Brooks Koepka",     "Patrick Reed"),
    ("Greg Melville",        "Xander Schauffele",    "Bryson DeChambeau",   "Patrick Reed",        "Brooks Koepka",     "Justin Rose"),
    ("John Stout",           "Xander Schauffele",    "Bryson DeChambeau",   "Justin Rose",         "Brooks Koepka",     "Patrick Reed"),
    ("Taylor Brady",         "Xander Schauffele",    "Ludvig Åberg",        "Justin Rose",         "Brooks Koepka",     "Jordan Spieth"),
    ("Dominic Wade",         "Tommy Fleetwood",      "Matt Fitzpatrick",    "Chris Gotterup",      "Aaron Rai",         "Marco Penge"),
    ("Dan Collins",          "Jon Rahm",             "Ludvig Åberg",        "Sepp Straka",         "Brooks Koepka",     "Justin Rose"),
    ("Bruce Varga",          "Tommy Fleetwood",      "Robert MacIntyre",    "Shane Lowry",         "Aaron Rai",         "Tyrrell Hatton"),
    ("Hugo Barton",          "Tommy Fleetwood",      "Bryson DeChambeau",   "Patrick Reed",        "Rasmus Højgaard",   "Gary Woodland"),
    ("Simon Jones",          "Scottie Scheffler",    "Hideki Matsuyama",    "Patrick Reed",        "Sungjae Im",        "Bryson DeChambeau"),
    ("Carl Lee",             "Xander Schauffele",    "Robert MacIntyre",    "Justin Thomas",       "Andrew Novak",      "Justin Rose"),
    ("Charlotte Peck",       "Jon Rahm",             "Ludvig Åberg",        "Justin Rose",         "Brooks Koepka",     "J.J. Spaun"),
    ("Rachel Martin",        "Scottie Scheffler",    "Maverick McNealy",    "Harris English",      "Wyndham Clark",     "Justin Rose"),
    ("Richard Main",         "Jon Rahm",             "Robert MacIntyre",    "Patrick Reed",        "Sungjae Im",        "Bryson DeChambeau"),
    ("Andy Riley",           "Jon Rahm",             "Ludvig Åberg",        "Patrick Reed",        "Brooks Koepka",     "Bryson DeChambeau"),
    ("Craig Roberts",        "Jon Rahm",             "Bryson DeChambeau",   "Patrick Reed",        "Sungjae Im",        "Cameron Young"),
    ("Nick Meek",            "Scottie Scheffler",    "Akshay Bhatia",       "Justin Rose",         "Brooks Koepka",     "Bryson DeChambeau"),
    ("Graeme Wilson",        "Tommy Fleetwood",      "Ludvig Åberg",        "Justin Rose",         "Brooks Koepka",     "Min Woo Lee"),
    ("Luca Cappuccini",      "Jon Rahm",             "Cameron Young",       "Patrick Reed",        "Brooks Koepka",     "Bryson DeChambeau"),
    ("Ashley Rishavy",       "Rory McIlroy",         "Matt Fitzpatrick",    "Corey Conners",       "Brooks Koepka",     "Jacob Bridgeman"),
    ("David Black",          "Tommy Fleetwood",      "Ludvig Åberg",        "Justin Rose",         "Michael Brennan",   "Bryson DeChambeau"),
    ("Dan Garrigan",         "Jon Rahm",             "Ludvig Åberg",        "Corey Conners",       "Sungjae Im",        "Bryson DeChambeau"),
    ("Ollie Amann",          "Jon Rahm",             "Ludvig Åberg",        "Patrick Reed",        "Brooks Koepka",     "Cameron Young"),
    ("Ollie Nettleingham",   "Jon Rahm",             "Ludvig Åberg",        "Jordan Spieth",       "Brooks Koepka",     "Bryson DeChambeau"),
    ("Blane Sweeney",        "Scottie Scheffler",    "Matt Fitzpatrick",    "Chris Gotterup",      "Brooks Koepka",     "Shane Lowry"),
    ("Vince Moore",          "Scottie Scheffler",    "Bryson DeChambeau",   "Patrick Reed",        "Brooks Koepka",     "Matt Fitzpatrick"),
    ("Matt Pegg",            "Scottie Scheffler",    "Collin Morikawa",     "Justin Rose",         "Sungjae Im",        "Ludvig Åberg"),
    ("Ollie Read",           "Jon Rahm",             "Hideki Matsuyama",    "Justin Rose",         "Sungjae Im",        "Ludvig Åberg"),
    ("Matt Chapman",         "Tommy Fleetwood",      "Ludvig Åberg",        "Justin Rose",         "Brooks Koepka",     "Bryson DeChambeau"),
    ("Sam Browne",           "Tommy Fleetwood",      "Ludvig Åberg",        "Justin Rose",         "Brooks Koepka",     "Bryson DeChambeau"),
    ("Alex Morgan",          "Jon Rahm",             "Ludvig Åberg",        "Corey Conners",       "Sungjae Im",        "Cameron Young"),
    ("Harriet Hughes",       "Rory McIlroy",         "Hideki Matsuyama",    "Justin Rose",         "Brooks Koepka",     "Ludvig Åberg"),
    ("Archie Smith",         "Jon Rahm",             "Cameron Young",       "Patrick Reed",        "Brooks Koepka",     "Matt Fitzpatrick"),
    ("Jon Brant",            "Scottie Scheffler",    "Hideki Matsuyama",    "Jordan Spieth",       "Brooks Koepka",     "Cameron Young"),
    ("Martyn Neaves",        "Scottie Scheffler",    "Hideki Matsuyama",    "Adam Scott",          "Wyndham Clark",     "Shane Lowry"),
    ("Ben Lee",              "Jon Rahm",             "Jake Knapp",          "Shane Lowry",         "Brooks Koepka",     "Bryson DeChambeau"),
    ("Luke Billington-Brooks","Jon Rahm",            "Robert MacIntyre",    "Corey Conners",       "Brooks Koepka",     "Ludvig Åberg"),
    ("Ian Swarbrick",        "Rory McIlroy",         "Bryson DeChambeau",   "Patrick Reed",        "Gary Woodland",     "Justin Rose"),
    ("Callum Evans",         "Jon Rahm",             "Ludvig Åberg",        "Justin Rose",         "Brooks Koepka",     "Bryson DeChambeau"),
    ("Sion Rathkey",         "Jon Rahm",             "Ludvig Åberg",        "Justin Rose",         "Brooks Koepka",     "Bryson DeChambeau"),
    ("Will Mitchell",        "Jon Rahm",             "Min Woo Lee",         "Shane Lowry",         "Brooks Koepka",     "Bryson DeChambeau"),
    ("Chris Powell",         "Scottie Scheffler",    "Ludvig Åberg",        "Justin Rose",         "Brooks Koepka",     "Bryson DeChambeau"),
    ("James Eighteen",       "Scottie Scheffler",    "Ludvig Åberg",        "Justin Rose",         "Brooks Koepka",     "Bryson DeChambeau"),
    ("Jamie Tucker",         "Scottie Scheffler",    "Bryson DeChambeau",   "Justin Rose",         "Brooks Koepka",     "Ludvig Åberg"),
    ("James Tweed",          "Rory McIlroy",         "Ludvig Åberg",        "Justin Rose",         "Sungjae Im",        "Matt Fitzpatrick"),
    ("Ollie Peck",           "Tommy Fleetwood",      "Ludvig Åberg",        "Justin Rose",         "Brooks Koepka",     "Matt Fitzpatrick"),
    ("Simon",                "Scottie Scheffler",    "Robert MacIntyre",    "Justin Rose",         "Brooks Koepka",     "Hideki Matsuyama"),
    ("Pat Lee",              "Rory McIlroy",         "Matt Fitzpatrick",    "Alex Noren",          "Wyndham Clark",     "Justin Rose"),
    ("Mark Baker",           "Tommy Fleetwood",      "Ludvig Åberg",        "Patrick Reed",        "Brian Harman",      "Bryson DeChambeau"),
    ("Steve Bell",           "Tommy Fleetwood",      "Matt Fitzpatrick",    "Justin Rose",         "Sungjae Im",        "Cameron Young"),
    ("Adam Franks",          "Rory McIlroy",         "Matt Fitzpatrick",    "Nicolai Højgaard",    "Sungjae Im",        "Akshay Bhatia"),
    ("Christopher Sanders",  "Jon Rahm",             "Robert MacIntyre",    "Justin Rose",         "Brooks Koepka",     "Ludvig Åberg"),
    ("Will Murphy 1",        "Jon Rahm",             "Bryson DeChambeau",   "Justin Rose",         "Brooks Koepka",     "Cameron Young"),
    ("Richard Tucker",       "Xander Schauffele",    "Matt Fitzpatrick",    "Justin Rose",         "Gary Woodland",     "Patrick Reed"),
    ("Tom Fraser",           "Xander Schauffele",    "Bryson DeChambeau",   "Sepp Straka",         "Brooks Koepka",     "Matt Fitzpatrick"),
    ("Adam Ranford",         "Tommy Fleetwood",      "Matt Fitzpatrick",    "Justin Rose",         "Brooks Koepka",     "Robert MacIntyre"),
    ("Sam Goold",            "Jon Rahm",             "Ludvig Åberg",        "Justin Rose",         "Brooks Koepka",     "Cameron Young"),
    ("Paul Buchanan",        "Jon Rahm",             "Bryson DeChambeau",   "Justin Rose",         "Brooks Koepka",     "Matt Fitzpatrick"),
    ("Louis Smith",          "Xander Schauffele",    "Bryson DeChambeau",   "Corey Conners",       "Tyrrell Hatton",    "Patrick Reed"),
    ("Hamish Barton",        "Rory McIlroy",         "Robert MacIntyre",    "Justin Rose",         "Brooks Koepka",     "Cameron Young"),
    ("Arun Jeyarajah",       "Scottie Scheffler",    "Matt Fitzpatrick",    "Justin Rose",         "Brooks Koepka",     "Bryson DeChambeau"),
    ("Abid Qayum",           "Rory McIlroy",         "Akshay Bhatia",       "Justin Rose",         "Brian Harman",      "Bryson DeChambeau"),
    ("Sam Mahon",            "Rory McIlroy",         "Matt Fitzpatrick",    "Patrick Reed",        "Wyndham Clark",     "Ludvig Åberg"),
    ("Tony Philpott",        "Tommy Fleetwood",      "Ludvig Åberg",        "Justin Thomas",       "Aaron Rai",         "Adam Scott"),
    ("Greg Rowe",            "Tommy Fleetwood",      "Bryson DeChambeau",   "Patrick Reed",        "Tyrrell Hatton",    "Justin Rose"),
    ("James Bennett",        "Tommy Fleetwood",      "Bryson DeChambeau",   "Justin Rose",         "Tyrrell Hatton",    "Patrick Reed"),
    ("Paddy Forster",        "Tommy Fleetwood",      "Bryson DeChambeau",   "Patrick Reed",        "Tyrrell Hatton",    "Justin Rose"),
    ("Denis O'Shea",         "Xander Schauffele",    "Matt Fitzpatrick",    "Justin Rose",         "Tom McKibbin",      "Ludvig Åberg"),
    ("Ben Green",            "Scottie Scheffler",    "Hideki Matsuyama",    "Chris Gotterup",      "Sungjae Im",        "Cameron Young"),
    ("Stephen Hooper",       "Scottie Scheffler",    "Matt Fitzpatrick",    "Justin Rose",         "Brooks Koepka",     "Cameron Young"),
    ("Ed Poole",             "Rory McIlroy",         "Ludvig Åberg",        "Justin Rose",         "Tom McKibbin",      "Matt Fitzpatrick"),
    ("Nick Glenday",         "Xander Schauffele",    "Ludvig Åberg",        "Jason Day",           "Brian Harman",      "Hideki Matsuyama"),
    ("Craig Press",          "Jon Rahm",             "Robert MacIntyre",    "Nicolai Højgaard",    "Sungjae Im",        "Bryson DeChambeau"),
    ("Louis Langedijk",      "Scottie Scheffler",    "Collin Morikawa",     "Corey Conners",       "Wyndham Clark",     "Cameron Young"),
    ("Patrick Fox",          "Rory McIlroy",         "Hideki Matsuyama",    "J.J. Spaun",          "Sungjae Im",        "Matt Fitzpatrick"),
    ("Lauren O'Hare",        "Rory McIlroy",         "Matt Fitzpatrick",    "Chris Gotterup",      "Brooks Koepka",     "Bryson DeChambeau"),
    ("Fleur Riley",          "Scottie Scheffler",    "Bryson DeChambeau",   "Patrick Reed",        "Tyrrell Hatton",    "Justin Rose"),
    ("Flynn Dempsey",        "Jon Rahm",             "Matt Fitzpatrick",    "Shane Lowry",         "Brooks Koepka",     "Robert MacIntyre"),
    ("Allys Ceraldi",        "Rory McIlroy",         "Bryson DeChambeau",   "Justin Rose",         "Wyndham Clark",     "Ludvig Åberg"),
    ("Matt Wrench",          "Jon Rahm",             "Bryson DeChambeau",   "Shane Lowry",         "Aaron Rai",         "Justin Rose"),
    ("Alfie Pickering",      "Jon Rahm",             "Min Woo Lee",         "Corey Conners",       "Tyrrell Hatton",    "Justin Rose"),
    ("Luke Gilbert",         "Scottie Scheffler",    "Ludvig Åberg",        "Patrick Reed",        "Tyrrell Hatton",    "Justin Rose"),
    ("Alex Carter",          "Jon Rahm",             "Matt Fitzpatrick",    "Chris Gotterup",      "Brooks Koepka",     "Ludvig Åberg"),
    ("Richard Langedijk",    "Jon Rahm",             "Bryson DeChambeau",   "J.J. Spaun",          "Brooks Koepka",     "Robert MacIntyre"),
    ("William Dowling",      "Rory McIlroy",         "Maverick McNealy",    "Patrick Reed",        "Gary Woodland",     "Bryson DeChambeau"),
    ("Bob",                  "Tommy Fleetwood",      "Matt Fitzpatrick",    "Justin Rose",         "Aaron Rai",         "Shane Lowry"),
    ("Paul Franks",          "Rory McIlroy",         "Matt Fitzpatrick",    "Sam Burns",           "Aaron Rai",         "Patrick Reed"),
    ("Greg Martin",          "Rory McIlroy",         "Patrick Cantlay",     "Harris English",      "Gary Woodland",     "Shane Lowry"),
    ("Nic Ventress",         "Xander Schauffele",    "Ludvig Åberg",        "Justin Rose",         "Gary Woodland",     "Shane Lowry"),
    ("Sam Stout",            "Rory McIlroy",         "Robert MacIntyre",    "J.J. Spaun",          "Sungjae Im",        "Matt Fitzpatrick"),
    ("Phill Rannow",         "Jon Rahm",             "Ludvig Åberg",        "Corey Conners",       "Aaron Rai",         "J.J. Spaun"),
    ("Mark McKenzie",        "Scottie Scheffler",    "Hideki Matsuyama",    "Shane Lowry",         "Gary Woodland",     "Justin Rose"),
    ("Fran Garrigan",        "Scottie Scheffler",    "Cameron Young",       "Patrick Reed",        "Tyrrell Hatton",    "Justin Rose"),
    ("Dominic Korobowicz",   "Scottie Scheffler",    "Robert MacIntyre",    "Chris Gotterup",      "Brooks Koepka",     "Matt Fitzpatrick"),
    ("Michael Kilcullen",    "Rory McIlroy",         "Robert MacIntyre",    "Shane Lowry",         "Tom McKibbin",      "Matt Fitzpatrick"),
    ("Paul Knight",          "Xander Schauffele",    "Matt Fitzpatrick",    "Justin Rose",         "Wyndham Clark",     "Ludvig Åberg"),
    ("Marc Dendy-Sadler",    "Rory McIlroy",         "Matt Fitzpatrick",    "Justin Rose",         "Wyndham Clark",     "Bryson DeChambeau"),
    ("Andy Dempsey",         "Tommy Fleetwood",      "Ludvig Åberg",        "Adam Scott",          "Brian Harman",      "Bryson DeChambeau"),
    ("Mark Nugent",          "Tommy Fleetwood",      "Matt Fitzpatrick",    "Justin Rose",         "Brian Harman",      "Bryson DeChambeau"),
    ("Dave Finch",           "Tommy Fleetwood",      "Cameron Young",       "Corey Conners",       "Brian Harman",      "Matt Fitzpatrick"),
    ("Mark Knight",          "Jon Rahm",             "Cameron Young",       "Justin Thomas",       "Marco Penge",       "Justin Rose"),
    ("Benjamin Greaves",     "Xander Schauffele",    "Hideki Matsuyama",    "Viktor Hovland",      "Brian Harman",      "Jacob Bridgeman"),
    ("Sean O'Carroll",       "Scottie Scheffler",    "Robert MacIntyre",    "Jason Day",           "Wyndham Clark",     "Matt Fitzpatrick"),
    ("Harry Gray",           "Scottie Scheffler",    "Matt Fitzpatrick",    "Justin Rose",         "Wyndham Clark",     "Bryson DeChambeau"),
    ("Jack Rolfe",           "Jon Rahm",             "Bryson DeChambeau",   "Justin Rose",         "Brian Harman",      "Cameron Young"),
    ("Andy Hammerton",       "Xander Schauffele",    "Matt Fitzpatrick",    "Chris Gotterup",      "Aaron Rai",         "Justin Rose"),
    ("Will Clark Smith",     "Tommy Fleetwood",      "Collin Morikawa",     "Patrick Reed",        "Gary Woodland",     "Ludvig Åberg"),
    ("Matt Salmon",          "Tommy Fleetwood",      "Matt Fitzpatrick",    "Justin Rose",         "Tyrrell Hatton",    "Corey Conners"),
    ("Will Murphy 2",        "Rory McIlroy",         "Min Woo Lee",         "Patrick Reed",        "Daniel Berger",     "Justin Rose"),
    ("Pete Stillings",       "Scottie Scheffler",    "Bryson DeChambeau",   "Jordan Spieth",       "Cameron Smith",     "Brooks Koepka"),
    ("Danny Mahon",          "Tommy Fleetwood",      "Cameron Young",       "Justin Rose",         "Cameron Smith",     "Tyrrell Hatton"),
    ("Sam Stinton",          "Scottie Scheffler",    "Ludvig Åberg",        "Justin Rose",         "Cameron Smith",     "Tyrrell Hatton"),
    ("Elliott Peck",         "Jon Rahm",             "Russell Henley",      "Justin Rose",         "Max Homa",          "Sepp Straka"),
    ("Bradley Hill",         "Rory McIlroy",         "Bryson DeChambeau",   "Shane Lowry",         "Haotong Li",        "Justin Rose"),
    ("Chris C",              "Scottie Scheffler",    "Collin Morikawa",     "Justin Thomas",       "Cameron Smith",     "Sam Burns"),
    ("Matt Goforth",         "Scottie Scheffler",    "Cameron Young",       "Nicolai Højgaard",    "Cameron Smith",     "Corey Conners"),
    ("Tom Ward",             "Xander Schauffele",    "Matt Fitzpatrick",    "Chris Gotterup",      "Cameron Smith",     "Justin Rose"),
    ("Michael Rees",         "Xander Schauffele",    "Ludvig Åberg",        "Patrick Reed",        "Cameron Smith",     "Bryson DeChambeau"),
    ("William Peck",         "Scottie Scheffler",    "Cameron Young",       "Justin Thomas",       "Max Homa",          "Ludvig Åberg"),
    ("Quino",                "Scottie Scheffler",    "Hideki Matsuyama",    "Corey Conners",       "Cameron Smith",     "Collin Morikawa"),
    ("Richard Hawkes",       "Xander Schauffele",    "Ludvig Åberg",        "Shane Lowry",         "Max Homa",          "Cameron Young"),
    ("Aaron Roberts",        "Jon Rahm",             "Cameron Young",       "Patrick Reed",        "Cameron Smith",     "Bryson DeChambeau"),
    ("Ross Mander",          "Scottie Scheffler",    "Bryson DeChambeau",   "Justin Rose",         "Cameron Smith",     "Ludvig Åberg"),
    ("Edwin Grant",          "Tommy Fleetwood",      "Ludvig Åberg",        "Justin Rose",         "Cameron Smith",     "Cameron Young"),
    ("Mark Tisshaw",         "Xander Schauffele",    "Ludvig Åberg",        "Shane Lowry",         "Cameron Smith",     "Hideki Matsuyama"),
    ("Miles Wakeling",       "Jon Rahm",             "Ludvig Åberg",        "Viktor Hovland",      "Max Homa",          "Matt Fitzpatrick"),
    ("Hadleigh C",           "Rory McIlroy",         "Ludvig Åberg",        "Viktor Hovland",      "Cameron Smith",     "Patrick Cantlay"),
    ("Stuart Clark",         "Rory McIlroy",         "Ludvig Åberg",        "Justin Rose",         "Cameron Smith",     "Matt Fitzpatrick"),
    ("Tim O'Sullivan",       "Scottie Scheffler",    "Hideki Matsuyama",    "Shane Lowry",         "Cameron Smith",     "Ludvig Åberg"),
    ("Robin Illingworth",    "Scottie Scheffler",    "Si Woo Kim",          "Chris Gotterup",      "Nico Echavarria",   "Harris English"),
    ("Damian Harvey",        "Scottie Scheffler",    "Matt Fitzpatrick",    "Justin Rose",         "Cameron Smith",     "Ludvig Åberg"),
    ("Felix Shepherd",       "Jon Rahm",             "Matt Fitzpatrick",    "Sepp Straka",         "Cameron Smith",     "Bryson DeChambeau"),
    ("Liam Barker",          "Jon Rahm",             "Cameron Young",       "Sam Burns",           "Max Homa",          "Matt Fitzpatrick"),
    ("Chris Montgomery",     "Rory McIlroy",         "Cameron Young",       "Patrick Reed",        "Nico Echavarria",   "Bryson DeChambeau"),
    ("Stephen Quinn",        "Jon Rahm",             "Matt Fitzpatrick",    "Shane Lowry",         "Cameron Smith",     "Bryson DeChambeau"),
    ("Conor Lynch",          "Rory McIlroy",         "Matt Fitzpatrick",    "Keegan Bradley",      "Tyrrell Hatton",    "Shane Lowry"),
    ("Max Barton",           "Scottie Scheffler",    "Matt Fitzpatrick",    "J.J. Spaun",          "Tyrrell Hatton",    "Ryan Fox"),
]

HOLE_IN_ONES = []
PAR_PER_ROUND = 72

# ── Helpers ───────────────────────────────────────────────────────────────────

def parse_score(val):
    if pd.isna(val):
        return None
    s = str(val).strip()
    if s in ("--", "", "nan", "CUT", "WD", "DQ", "MDF", "MC"):
        return None
    if s == "E":
        return 0
    try:
        return int(s)
    except ValueError:
        return None

def fuzzy_match(a, b):
    return a.strip().lower() in b.strip().lower() or b.strip().lower() in a.strip().lower()

def missed_cut(pos_str):
    return any(t in str(pos_str).upper() for t in ("CUT", "WD", "DQ", "MDF", "MC"))

def parse_position(pos_str):
    s = str(pos_str).strip().upper().lstrip("T")
    try:
        return int(s)
    except ValueError:
        return None

# ── Leaderboard fetch (cached so refresh button controls it) ──────────────────

@st.cache_data(ttl=120)  # cache for 2 minutes
def get_leaderboard():
    headers = {"User-Agent": "Mozilla/5.0 (compatible)"}
    resp = requests.get(URL, headers=headers, timeout=15)
    resp.raise_for_status()
    tables = pd.read_html(StringIO(resp.text))
    df = tables[0].copy()
    df.columns = [str(c).strip() for c in df.columns]
    return df

def available_rounds(df):
    """A round is only 'complete' once at least 75% of players have a score in that column."""
    total = len(df)
    return [
        r for r in ["R1", "R2", "R3", "R4"]
        if r in df.columns
        and df[r].apply(lambda v: parse_score(v) is not None).sum() >= total * 0.75
    ]

def detect_current_round(df):
    if "TODAY" not in df.columns:
        return None
    if df["TODAY"].apply(parse_score).notna().sum() < 5:
        return None
    completed = available_rounds(df)
    for r in ["R1", "R2", "R3", "R4"]:
        if r not in completed:
            return r
    return None

def cumulative_to_par(df, rounds, current_round=None):
    cum = pd.DataFrame(index=df.index)
    running = pd.Series(0, index=df.index)
    for r in rounds:
        strokes = df[r].apply(parse_score)
        to_par = strokes.apply(lambda s: (s - PAR_PER_ROUND) if s is not None else None)
        running = running + to_par.fillna(0)
        cum[r] = running.where(strokes.notna(), other=None)
    if current_round and "TODAY" in df.columns:
        today_tp = df["TODAY"].apply(parse_score)
        running_live = running + today_tp.fillna(0)
        cum[current_round] = running_live.where(today_tp.notna(), other=None)
    return cum

def get_round_leaders(df, rounds, current_round=None):
    cum = cumulative_to_par(df, rounds, current_round)
    rounds_to_check = list(rounds) + ([current_round] if current_round and current_round not in rounds else [])
    leaders = {}
    for r in rounds_to_check:
        if r not in cum.columns:
            continue
        col = cum[r].dropna()
        if col.empty:
            continue
        best = col.min()
        leaders[r] = set(df.loc[col[col == best].index, "PLAYER"].values)
    return leaders

def get_low_round_scorers(df, rounds, current_round=None):
    low = {}
    for r in rounds:
        strokes = df[r].apply(parse_score).dropna()
        if strokes.empty:
            continue
        best = strokes.min()
        low[r] = set(df.loc[strokes[strokes == best].index, "PLAYER"].values)
    if current_round and "TODAY" in df.columns:
        today_tp = df["TODAY"].apply(parse_score)
        today_strokes = today_tp.apply(lambda v: (PAR_PER_ROUND + v) if v is not None else None).dropna()
        if not today_strokes.empty:
            best = today_strokes.min()
            low[current_round] = set(df.loc[today_strokes[today_strokes == best].index, "PLAYER"].values)
    return low

def is_tournament_complete(df):
    if "R4" not in df.columns:
        return False
    if detect_current_round(df) == "R4":
        return False
    return df["R4"].apply(parse_score).notna().sum() > 10

def score_golfer(df_name, df, rounds, round_leaders, low_round_scorers,
                 complete, hole_in_ones, tie_for_2nd_blocks_3rd, current_round=None):
    """Returns (confirmed_pts, projected_pts) separately."""
    match = df[df["PLAYER"].apply(lambda n: fuzzy_match(df_name, str(n)))]
    if match.empty:
        return 0, 0
    row = match.iloc[0]
    actual_name = str(row["PLAYER"])
    confirmed = 0
    projected = 0

    # Score vs par — completed rounds go to confirmed, today's live score to projected
    completed_to_par = sum(
        (parse_score(row.get(r, "--")) or 0) - PAR_PER_ROUND
        for r in rounds
        if parse_score(row.get(r, "--")) is not None
    )
    confirmed += -completed_to_par

    if current_round and "TODAY" in df.columns:
        today_val = parse_score(row.get("TODAY", "--"))
        if today_val is not None:
            projected += -today_val

    # Hole in one — always confirmed
    if any(fuzzy_match(df_name, h) for h in hole_in_ones):
        confirmed += 5

    # Round leaders — completed rounds confirmed, live round projected
    for r, bonus in {"R1": 5, "R2": 5, "R3": 5}.items():
        if r not in round_leaders:
            continue
        if any(fuzzy_match(actual_name, l) for l in round_leaders[r]):
            if r == current_round:
                projected += bonus
            else:
                confirmed += bonus

    # Low round — completed rounds confirmed, live round projected
    for r in rounds:
        if r in low_round_scorers and any(fuzzy_match(actual_name, l) for l in low_round_scorers[r]):
            confirmed += 3
    if current_round and current_round in low_round_scorers:
        if any(fuzzy_match(actual_name, l) for l in low_round_scorers[current_round]):
            projected += 3

    # Cut — confirmed once cut has happened
    cut_has_happened = len(rounds) >= 2 and (len(rounds) >= 3 or current_round in ("R3", "R4"))
    pos_str = str(row.get("POS", ""))
    if cut_has_happened:
        if missed_cut(pos_str):
            confirmed -= 5
        else:
            confirmed += 10

    # Final finish — confirmed only when tournament done
    if complete and not missed_cut(pos_str):
        pos_num = parse_position(pos_str)
        if pos_num == 1:
            confirmed += 10
        if pos_num == 2:
            confirmed += 5
        if pos_num == 3 and not tie_for_2nd_blocks_3rd:
            confirmed += 3

    return confirmed, projected


def build_league_table(df):
    rounds = available_rounds(df)
    current_round = detect_current_round(df)
    round_leaders = get_round_leaders(df, rounds, current_round)
    low_round_scorers = get_low_round_scorers(df, rounds, current_round)
    complete = is_tournament_complete(df)

    pos_nums = df["POS"].apply(parse_position)
    tied_2nd = (pos_nums == 2).sum() if complete else 0
    tie_for_2nd_blocks_3rd = (tied_2nd >= 3)

    all_golfers = {pick for entry in LEAGUE for pick in entry[1:]}
    golfer_conf = {}
    golfer_proj = {}
    for g in all_golfers:
        c, p = score_golfer(g, df, rounds, round_leaders, low_round_scorers,
                            complete, HOLE_IN_ONES, tie_for_2nd_blocks_3rd, current_round)
        golfer_conf[g] = c
        golfer_proj[g] = p

    rows = []
    for entry in LEAGUE:
        participant = entry[0]
        t1, t2, t3, t4, captain = entry[1], entry[2], entry[3], entry[4], entry[5]
        picks = [t1, t2, t3, t4]

        conf  = [golfer_conf.get(p, 0) for p in picks]
        proj  = [golfer_proj.get(p, 0) for p in picks]
        total = [c + p for c, p in zip(conf, proj)]

        cap_conf = golfer_conf.get(captain, 0) * 2
        cap_proj = golfer_proj.get(captain, 0) * 2

        rows.append({
            "Player":       participant,
            "Tier 1":       t1,  "T1 Conf": conf[0],  "T1 Proj": proj[0],  "T1 Pts": total[0],
            "Tier 2":       t2,  "T2 Conf": conf[1],  "T2 Proj": proj[1],  "T2 Pts": total[1],
            "Tier 3":       t3,  "T3 Conf": conf[2],  "T3 Proj": proj[2],  "T3 Pts": total[2],
            "Tier 4":       t4,  "T4 Conf": conf[3],  "T4 Proj": proj[3],  "T4 Pts": total[3],
            "Captain":      captain,
            "Cap Conf":     cap_conf, "Cap Proj": cap_proj, "Cap Pts": cap_conf + cap_proj,
            "Confirmed":    sum(conf) + cap_conf,
            "Projected":    sum(proj) + cap_proj,
            "Total":        sum(total) + cap_conf + cap_proj,
        })

    result = pd.DataFrame(rows)
    return result, rounds, current_round, complete


# ── Streamlit UI ──────────────────────────────────────────────────────────────

def fmt_pts(v):
    if pd.isna(v):
        return "0"
    v = int(v)
    return f"+{v}" if v > 0 else str(v)

def colour_pts(v):
    try:
        v = int(v)
    except (TypeError, ValueError):
        return ""
    if v > 0:
        return "color: #2e7d32; font-weight: bold"
    elif v < 0:
        return "color: #c62828; font-weight: bold"
    return "color: #555"

def make_display(result, score_col, pts_suffix):
    """Build a ranked display df using score_col for sorting, showing pts_suffix columns."""
    df = result.copy().sort_values(score_col, ascending=False).reset_index(drop=True)
    df.insert(0, "Rank", df.index + 1)
    cols = ["Rank", "Player",
            "Tier 1", f"T1{pts_suffix}",
            "Tier 2", f"T2{pts_suffix}",
            "Tier 3", f"T3{pts_suffix}",
            "Tier 4", f"T4{pts_suffix}",
            "Captain", f"Cap{pts_suffix}",
            score_col]
    # rename last col to "Total" for display
    df = df[cols].rename(columns={score_col: "Total"})
    return df

def style_table(df):
    pts_cols = [c for c in df.columns if c.endswith("Pts") or c == "Total"]
    styled = df.style
    for col in pts_cols:
        styled = styled.map(colour_pts, subset=[col])
    styled = styled.format({c: fmt_pts for c in pts_cols})
    return styled


# ── App layout ────────────────────────────────────────────────────────────────

st.title("⛳ Masters Fantasy League 2026")

col1, col2 = st.columns([3, 1])
with col2:
    if st.button("🔄 Refresh data", use_container_width=True):
        st.cache_data.clear()

with st.spinner("Fetching live leaderboard..."):
    try:
        df_live = get_leaderboard()
        result, rounds, current_round, complete = build_league_table(df_live)

        # Status banner
        if current_round:
            st.info(f"🟢 **{current_round} in progress** — confirmed points are locked in, projected points reflect live scores")
        elif complete:
            st.success("🏆 Tournament complete — final standings")
        elif rounds:
            st.warning(f"⏸️ Between rounds — {len(rounds)} round(s) complete: {', '.join(rounds)}")
        else:
            st.warning("⏳ Tournament not yet started")

        with col1:
            search = st.text_input("🔍 Search for a player", placeholder="Type a name...")

        if search:
            result = result[result["Player"].str.contains(search, case=False)]

        # Two tabs
        tab_confirmed, tab_projected = st.tabs(["✅ Confirmed", "📈 Projected (inc. live round)"])

        height = min(50 + len(result) * 35, 800)

        with tab_confirmed:
            st.caption("Points locked in from fully completed rounds only. No live round scores included.")
            conf_df = make_display(result, "Confirmed", " Conf")
            st.dataframe(style_table(conf_df), use_container_width=True, height=height, hide_index=True)

        with tab_projected:
            st.caption("Confirmed points + live projections from the current round in progress.")
            proj_df = make_display(result, "Total", " Pts")
            st.dataframe(style_table(proj_df), use_container_width=True, height=height, hide_index=True)

        st.caption(f"Data auto-refreshes every 2 minutes. {len(result)} participants shown.")

    except Exception as e:
        st.error(f"Failed to fetch leaderboard: {e}")
