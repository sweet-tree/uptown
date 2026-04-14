"""
Sports data registry — exact visual DNA per team.
No assumptions. No generic descriptions.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass
class PlayerSpec:
    name: str
    number: str
    position: str
    side: str = "left"


@dataclass
class CardSpec:
    team: "TeamData"
    players: list[PlayerSpec]
    title: Optional[str] = None


class Sport(str, Enum):
    NFL = "nfl"
    SOCCER = "soccer"
    HOCKEY = "hockey"
    BASEBALL = "baseball"


@dataclass
class TeamData:
    name: str
    city: str
    abbreviation: str
    sport: Sport
    primary_hex: str
    secondary_hex: str
    accent_hex: str
    stadium_name: str
    stadium_prompt: str           # cinematic — used by original pipeline
    uptowns_stadium_prompt: str   # illustration-friendly — used by Uptowns pipeline
    skyline_prompt: str           # cinematic — used by original pipeline
    uptowns_skyline_prompt: str   # illustration-friendly — used by Uptowns pipeline
    jersey_prompt: str
    jersey_wordmark: str
    platform_font: str
    pants_prompt: str
    helmet_prompt: str
    number_style: str
    logo_prompt: str
    panel_color: str


NFL_TEAMS = {
    "BAL": TeamData(
        name="Baltimore Ravens", city="Baltimore", abbreviation="BAL", sport=Sport.NFL,
        primary_hex="#241773", secondary_hex="#000000", accent_hex="#9E7C0C",
        stadium_name="M&T Bank Stadium",
        stadium_prompt="M&T Bank Stadium at night seen from field level, deep purple floodlights, packed crowd glowing purple, Baltimore Inner Harbor and city skyline visible in the background behind the stadium upper deck",
        uptowns_stadium_prompt="M&T Bank Stadium illustrated front-facing, brick exterior with arched windows, purple banners on the facade, Ravens shield logos on the building panels, stadium name on the facade, surrounded by illustrated trees",
        skyline_prompt="Baltimore downtown skyline at night, Inner Harbor waterfront glowing purple and gold, distinctive World Trade Center tower and Legg Mason building visible, harbor reflections shimmering below",
        uptowns_skyline_prompt="Baltimore downtown skyline illustrated, Inner Harbor waterfront below, tall office towers including the distinctive cylindrical World Trade Center, harbor water reflecting city lights",
        jersey_prompt="deep purple NFL jersey with 'RAVENS' wordmark across chest in white block letters, white block numbers outlined in black on chest AND back, white shoulder stripes, purple sleeves with black and gold trim bands",
        jersey_wordmark="'RAVENS' in bold white collegiate block letters across the chest, with thick black outline",
        platform_font="'Baltimore Ravens' in classic bold serif font, white on dark",
        pants_prompt="black NFL pants with purple and gold side stripes",
        helmet_prompt="glossy purple helmet with Ravens logo on both sides: black raven head facing left on a purple and gold shield with letter B, black face mask, thin gold center stripe",
        number_style="large white block numerals with thick black outline, collegiate style",
        logo_prompt="Ravens shield: black raven head facing left, purple shield, gold letter B, gold trim border",
        panel_color="#241773",
    ),
    "KC": TeamData(
        name="Kansas City Chiefs", city="Kansas City", abbreviation="KC", sport=Sport.NFL,
        primary_hex="#E31837", secondary_hex="#FFB81C", accent_hex="#FFFFFF",
        stadium_name="GEHA Field at Arrowhead Stadium",
        stadium_prompt="Arrowhead Stadium at golden sunset, viewed from field level — the Kansas City skyline with Liberty Memorial silhouette rises seamlessly above the stadium upper deck rim, golden sunset sky blending the stadium floodlights and city skyline into one continuous cinematic scene, sea of red fans in the stands, warm amber and crimson light flooding the entire scene",
        uptowns_stadium_prompt="Arrowhead Stadium illustrated front-facing, distinctive arrowhead-shaped roof line, red exterior with Chiefs arrowhead logos on the facade panels, stadium name on the front, surrounded by illustrated trees and parking lot",
        skyline_prompt="Kansas City skyline naturally integrated above the stadium, Missouri River glinting gold in the distance, no visible seam between stadium and sky",
        uptowns_skyline_prompt="Kansas City skyline illustrated, Liberty Memorial obelisk prominently visible, downtown office towers, Missouri River in the distance",
        jersey_prompt="red NFL jersey with 'CHIEFS' wordmark across chest in white block letters, white block numbers outlined in red on chest AND back, white shoulder panels, red sleeves with white and gold trim bands",
        jersey_wordmark="'CHIEFS' in bold white block letters across the chest",
        platform_font="'Kansas City Chiefs' in bold block font, white on dark",
        pants_prompt="white NFL pants with red and gold side stripes",
        helmet_prompt="red helmet with Chiefs arrowhead logo on both sides: red arrowhead pointing right with white outline, white face mask, no center stripe",
        number_style="large white block numerals with red outline",
        logo_prompt="Chiefs arrowhead: solid red arrowhead pointing right, white outline, bold clean design",
        panel_color="#E31837",
    ),
    "DAL": TeamData(
        name="Dallas Cowboys", city="Dallas", abbreviation="DAL", sport=Sport.NFL,
        primary_hex="#003594", secondary_hex="#041E42", accent_hex="#869397",
        stadium_name="AT&T Stadium",
        stadium_prompt="AT&T Stadium interior at night seen from field level, massive retractable roof open to Texas night sky, enormous center-hung video board glowing, silver and navy lighting, packed crowd in the stands",
        uptowns_stadium_prompt="AT&T Stadium illustrated front-facing, massive domed silver roof, large Cowboys star on the facade, stadium name above the entrance, glass and steel exterior, Cowboys helmet logos on the building panels",
        skyline_prompt="Dallas skyline at night visible through the open roof, Reunion Tower glowing, Texas stars blazing",
        uptowns_skyline_prompt="Dallas skyline illustrated, Reunion Tower with its distinctive globe top prominently visible, downtown skyscrapers, navy blue and silver sky",
        jersey_prompt="navy blue NFL jersey with 'COWBOYS' wordmark across chest in white block letters, white block numbers outlined in silver on chest AND back, white shoulder panels with silver trim, navy sleeves",
        jersey_wordmark="'COWBOYS' in bold white block letters across the chest",
        platform_font="'Dallas Cowboys' in bold block font, white on dark",
        pants_prompt="silver metallic NFL pants with navy and white side stripes",
        helmet_prompt="high-gloss silver metallic helmet with iconic blue five-pointed star logo centered on both sides, blue face mask, no center stripe",
        number_style="large white block numerals with silver metallic outline",
        logo_prompt="Cowboys star: large blue five-pointed star, white outline, centered on silver helmet",
        panel_color="#003594",
    ),
    "GB": TeamData(
        name="Green Bay Packers", city="Green Bay", abbreviation="GB", sport=Sport.NFL,
        primary_hex="#203731", secondary_hex="#FFB612", accent_hex="#FFFFFF",
        stadium_name="Lambeau Field",
        stadium_prompt="Lambeau Field in winter seen from field level, snow falling on the frozen tundra, golden floodlights cutting through snowfall, packed crowd in green and gold in the stands",
        uptowns_stadium_prompt="Lambeau Field illustrated front-facing, classic circular bowl stadium, green and gold exterior, large Packers G logos on the facade panels, 'LAMBEAU FIELD' on the front, snow on the ground, pine trees surrounding",
        skyline_prompt="Green Bay Wisconsin winter dusk, frozen tundra and pine trees silhouetted, golden stadium lights glowing",
        uptowns_skyline_prompt="Green Bay Wisconsin illustrated, modest city skyline with low-rise buildings, snow-covered rooftops, pine trees, frozen tundra feel",
        jersey_prompt="dark forest green NFL jersey with 'PACKERS' wordmark across chest in gold block letters, gold block numbers outlined in white on chest AND back, gold shoulder panels, green sleeves with gold and white trim bands",
        jersey_wordmark="'PACKERS' in bold gold block letters across the chest",
        platform_font="'Green Bay Packers' in bold block font, white on dark",
        pants_prompt="gold NFL pants with green and white side stripes",
        helmet_prompt="matte gold helmet with Packers G logo on both sides: green oval with large white letter G centered, white face mask, no center stripe",
        number_style="large gold block numerals with white outline",
        logo_prompt="Packers G: dark green oval, large white letter G centered, clean bold design",
        panel_color="#203731",
    ),
    "CHI": TeamData(
        name="Chicago Bears", city="Chicago", abbreviation="CHI", sport=Sport.NFL,
        primary_hex="#0B162A", secondary_hex="#C83803", accent_hex="#FFFFFF",
        stadium_name="Soldier Field",
        stadium_prompt="Soldier Field at night seen from field level, historic neoclassical columns visible on the sides, navy and orange lighting, Lake Michigan dark and vast behind the open stadium",
        uptowns_stadium_prompt="Soldier Field illustrated front-facing, iconic neoclassical stone columns on both sides of the modern bowl, Bears C logos on the facade panels, 'SOLDIER FIELD' on the front, Lake Michigan visible behind",
        skyline_prompt="Chicago skyline at night, Willis Tower and John Hancock Center glowing, Lake Michigan reflecting city lights",
        uptowns_skyline_prompt="Chicago skyline illustrated, Willis Tower (Sears Tower) tallest and dominant, John Hancock Center with its distinctive antennas, Lake Michigan shoreline visible",
        jersey_prompt="navy blue NFL jersey with 'BEARS' wordmark across chest in orange block letters, orange block numbers outlined in white on chest AND back, navy shoulder panels, navy sleeves with orange and white trim bands",
        jersey_wordmark="'BEARS' in bold orange block letters across the chest",
        platform_font="'Chicago Bears' in bold block font, white on dark",
        pants_prompt="navy blue NFL pants with orange and white side stripes",
        helmet_prompt="navy blue helmet with Bears C logo on both sides: bold orange letter C with navy outline, navy face mask, no center stripe",
        number_style="large orange block numerals with white outline",
        logo_prompt="Bears C: bold orange letter C, navy outline, classic Chicago Bears design",
        panel_color="#0B162A",
    ),
    "LV": TeamData(
        name="Las Vegas Raiders", city="Las Vegas", abbreviation="LV", sport=Sport.NFL,
        primary_hex="#000000", secondary_hex="#A5ACAF", accent_hex="#FFFFFF",
        stadium_name="Allegiant Stadium",
        stadium_prompt="Allegiant Stadium interior at night seen from field level, futuristic black and silver architecture, Las Vegas Strip neon blazing through the stadium windows in the background",
        uptowns_stadium_prompt="Allegiant Stadium illustrated front-facing, sleek black domed exterior, silver Raiders shield logo centered on the facade, 'ALLEGIANT STADIUM' text on the front, modern black and silver architecture, palm trees at the base",
        skyline_prompt="Las Vegas Strip at night, neon signs blazing silver and white, desert stars overhead",
        uptowns_skyline_prompt="Las Vegas Strip skyline illustrated, recognizable hotel towers including the Sphere, Stratosphere tower, and casino resort buildings, desert sky above, illustrated in the same flat cartoon style as the stadium",
        jersey_prompt="black NFL jersey with 'RAIDERS' wordmark across chest in silver block letters, silver block numbers outlined in white on chest AND back, black shoulder panels with silver trim, black sleeves with silver trim bands",
        jersey_wordmark="'RAIDERS' in bold silver block letters across the chest",
        platform_font="'Las Vegas Raiders' in bold block font, silver on dark",
        pants_prompt="silver NFL pants with black side stripes",
        helmet_prompt="high-gloss silver metallic helmet with Raiders shield logo on both sides: black shield with silver crossed swords and pirate eye patch, black face mask, no center stripe",
        number_style="large silver block numerals with white outline",
        logo_prompt="Raiders shield: black shield, silver crossed swords, silver football, silver pirate eye patch, bold iconic design",
        panel_color="#000000",
    ),
}

HOCKEY_TEAMS = {
    "TOR": TeamData(
        name="Toronto Maple Leafs", city="Toronto", abbreviation="TOR", sport=Sport.HOCKEY,
        primary_hex="#00205B", secondary_hex="#FFFFFF", accent_hex="#00205B",
        stadium_name="Scotiabank Arena",
        stadium_prompt="Scotiabank Arena interior during playoffs seen from ice level, blue and white ice gleaming under intense floodlights, packed crowd waving blue and white towels in the stands",
        uptowns_stadium_prompt="Scotiabank Arena illustrated front-facing, modern glass and steel exterior, Maple Leafs logo on the facade, 'SCOTIABANK ARENA' text, downtown Toronto setting",
        skyline_prompt="Toronto skyline at night, CN Tower glowing blue and white, Lake Ontario dark and vast",
        uptowns_skyline_prompt="Toronto skyline illustrated, CN Tower prominently tall and distinctive, downtown office towers, Lake Ontario shoreline",
        jersey_prompt="royal blue hockey jersey with white block numbers on chest AND back, white shoulder yoke, Maple Leafs 31-point maple leaf logo centered on chest, blue sleeves with white stripe bands",
        jersey_wordmark="large 31-point maple leaf logo in royal blue with white outline, centered prominently on chest — no text, logo only",
        platform_font="'Toronto Maple Leafs' in classic serif font, white on dark",
        pants_prompt="royal blue hockey pants with white stripe",
        helmet_prompt="royal blue hockey helmet with white 31-point maple leaf logo on both sides, white cage, blue chin strap",
        number_style="large white block numerals",
        logo_prompt="Maple Leafs: 31-point maple leaf in royal blue, white outline, centered",
        panel_color="#00205B",
    ),
    "EDM": TeamData(
        name="Edmonton Oilers", city="Edmonton", abbreviation="EDM", sport=Sport.HOCKEY,
        primary_hex="#041E42", secondary_hex="#FF4C00", accent_hex="#FFFFFF",
        stadium_name="Rogers Place",
        stadium_prompt="Rogers Place interior during playoffs seen from ice level, navy and orange ice, Northern Lights aurora borealis visible through the arena roof, packed Alberta crowd in the stands",
        uptowns_stadium_prompt="Rogers Place illustrated front-facing, modern angular exterior, Oilers logo on the facade, 'ROGERS PLACE' text, Edmonton downtown setting",
        skyline_prompt="Edmonton skyline at night with Northern Lights aurora borealis in green and purple above the city",
        uptowns_skyline_prompt="Edmonton skyline illustrated, downtown office towers, Northern Lights aurora borealis in green and purple above",
        jersey_prompt="navy blue hockey jersey with orange block numbers outlined in white on chest AND back, orange shoulder yoke, Oilers logo centered on chest, navy sleeves with orange and white stripe bands",
        jersey_wordmark="Oilers logo centered large on chest: orange oil drop shape with navy 'OILERS' text inside — no other chest text",
        platform_font="'Edmonton Oilers' in bold sans-serif font, white on dark",
        pants_prompt="navy blue hockey pants with orange and white stripes",
        helmet_prompt="navy blue hockey helmet with Oilers logo on both sides: orange oil drop shape with navy Oilers text, orange cage, navy chin strap",
        number_style="large orange block numerals with white outline",
        logo_prompt="Oilers: orange oil drop shape, navy Oilers text inside, white outline",
        panel_color="#041E42",
    ),
    "VGK": TeamData(
        name="Vegas Golden Knights", city="Las Vegas", abbreviation="VGK", sport=Sport.HOCKEY,
        primary_hex="#B4975A", secondary_hex="#333F42", accent_hex="#C8102E",
        stadium_name="T-Mobile Arena",
        stadium_prompt="T-Mobile Arena interior during Golden Knights game seen from ice level, golden knight pre-game ceremony on ice, dramatic smoke and laser show, Las Vegas Strip glowing through arena windows in background",
        uptowns_stadium_prompt="T-Mobile Arena illustrated front-facing, modern exterior, Golden Knights logo on the facade, 'T-MOBILE ARENA' text, Las Vegas setting",
        skyline_prompt="Las Vegas Strip at night, neon gold and black, desert stars blazing",
        uptowns_skyline_prompt="Las Vegas Strip skyline illustrated, hotel towers and casino resorts, desert sky above",
        jersey_prompt="steel gray hockey jersey with gold block numbers outlined in black on chest AND back, gold shoulder panels, Golden Knights medieval helmet logo centered on chest, gray sleeves with gold and black stripe bands",
        jersey_wordmark="Golden Knights medieval knight helmet logo in gold with black outline, centered large on chest — no text, logo only",
        platform_font="'Vegas Golden Knights' in bold serif font, gold on dark",
        pants_prompt="steel gray hockey pants with gold and black stripes",
        helmet_prompt="steel gray hockey helmet with Golden Knights logo on both sides: medieval knight helmet in gold with black outline, gold cage, gold chin strap",
        number_style="large gold block numerals with black outline",
        logo_prompt="Golden Knights: medieval knight helmet in gold, black outline, bold angular design",
        panel_color="#B4975A",
    ),
}

BASEBALL_TEAMS = {
    "NYY": TeamData(
        name="New York Yankees", city="New York", abbreviation="NYY", sport=Sport.BASEBALL,
        primary_hex="#003087", secondary_hex="#FFFFFF", accent_hex="#C4CED4",
        stadium_name="Yankee Stadium",
        stadium_prompt="Yankee Stadium interior at night seen from field level, packed crowd in the stands, stadium floodlights blazing, Manhattan skyline and city lights visible beyond the outfield walls in the background",
        uptowns_stadium_prompt="Yankee Stadium illustrated front-facing, classic white limestone exterior, interlocking NY logo on the facade, 'YANKEE STADIUM' text, Bronx setting",
        skyline_prompt="New York City skyline at night, Empire State Building and One World Trade Center dominating, Manhattan glowing navy and white",
        uptowns_skyline_prompt="New York City skyline illustrated, Empire State Building and One World Trade Center dominant, Manhattan dense skyline",
        jersey_prompt="white pinstripe baseball jersey with 'Yankees' in navy script lettering across the chest, navy block numbers on back, navy interlocking NY logo on left chest, white sleeves with navy trim, vertical navy pinstripes throughout jersey",
        jersey_wordmark="'Yankees' in flowing navy blue cursive script lettering across the chest — classic baseball script, connected letters, elegant and iconic",
        platform_font="'New York Yankees' in classic navy serif font with elegant letterforms, white on dark",
        pants_prompt="white pinstripe baseball pants with navy stirrups",
        helmet_prompt="navy batting helmet with white interlocking NY logo on left side, navy brim",
        number_style="large navy block numerals, classic baseball style",
        logo_prompt="Yankees NY: interlocking navy N and Y letters, classic serif style, white outline",
        panel_color="#003087",
    ),
    "LAD": TeamData(
        name="Los Angeles Dodgers", city="Los Angeles", abbreviation="LAD", sport=Sport.BASEBALL,
        primary_hex="#005A9C", secondary_hex="#EF3E42", accent_hex="#FFFFFF",
        stadium_name="Dodger Stadium",
        stadium_prompt="Dodger Stadium interior at golden hour seen from field level, palm trees visible beyond the outfield, California hills glowing amber in the background, Dodger blue floodlights",
        uptowns_stadium_prompt="Dodger Stadium illustrated front-facing, classic 1960s circular design, Dodger blue exterior, interlocking LA logo on the facade, palm trees surrounding, California hills behind",
        skyline_prompt="Los Angeles skyline at golden hour, Hollywood Hills and Griffith Observatory, Pacific Ocean glinting in the distance",
        uptowns_skyline_prompt="Los Angeles skyline illustrated, Hollywood Hills with Griffith Observatory, downtown LA towers, palm trees",
        jersey_prompt="Dodger blue baseball jersey with 'Dodgers' in white script lettering across the chest, white block numbers on back, white sleeves with Dodger blue trim",
        jersey_wordmark="'Dodgers' in flowing white cursive script lettering across the chest — classic Dodgers script, connected letters",
        platform_font="'Los Angeles Dodgers' in classic serif font, white on dark",
        pants_prompt="white baseball pants with Dodger blue stirrups",
        helmet_prompt="Dodger blue batting helmet with white interlocking LA logo on left side, Dodger blue brim",
        number_style="large white block numerals",
        logo_prompt="Dodgers LA: interlocking blue L and A letters, classic script style, white outline",
        panel_color="#005A9C",
    ),
    "CHC": TeamData(
        name="Chicago Cubs", city="Chicago", abbreviation="CHC", sport=Sport.BASEBALL,
        primary_hex="#0E3386", secondary_hex="#CC3433", accent_hex="#FFFFFF",
        stadium_name="Wrigley Field",
        stadium_prompt="Wrigley Field interior during a day game seen from field level, iconic ivy-covered outfield walls in full green, hand-operated scoreboard visible, Chicago rooftops with fans visible beyond the outfield",
        uptowns_stadium_prompt="Wrigley Field illustrated front-facing, classic red brick exterior, iconic hand-operated scoreboard visible, Cubs C logo on the facade, ivy-covered walls, Wrigleyville rooftops behind",
        skyline_prompt="Chicago skyline on a summer afternoon, Lake Michigan sparkling blue, Wrigley Field neighborhood rooftops",
        uptowns_skyline_prompt="Chicago skyline illustrated, Willis Tower dominant, Wrigleyville neighborhood rooftops, Lake Michigan",
        jersey_prompt="Cubs blue baseball jersey with 'Cubs' in red script lettering across the chest, red pinstripes, blue block numbers on back, blue sleeves with red trim",
        jersey_wordmark="'Cubs' in flowing red cursive script lettering across the chest — classic Cubs script",
        platform_font="'Chicago Cubs' in classic serif font, white on dark",
        pants_prompt="white baseball pants with blue and red stirrups",
        helmet_prompt="Cubs blue batting helmet with red C logo on left side, blue brim",
        number_style="large blue block numerals with red outline",
        logo_prompt="Cubs C: bold red letter C, blue outline, classic Chicago Cubs design",
        panel_color="#0E3386",
    ),
}

SOCCER_TEAMS = {
    "RM": TeamData(
        name="Real Madrid", city="Madrid", abbreviation="RM", sport=Sport.SOCCER,
        primary_hex="#FFFFFF", secondary_hex="#00529F", accent_hex="#FFD700",
        stadium_name="Santiago Bernabeu",
        stadium_prompt="Santiago Bernabeu interior at night seen from pitch level, renovated golden LED facade glowing in the background, Champions League atmosphere, packed crowd in the stands",
        uptowns_stadium_prompt="Santiago Bernabeu illustrated front-facing, modern circular exterior with distinctive metallic facade, Real Madrid crest on the building, 'SANTIAGO BERNABEU' text, Madrid setting",
        skyline_prompt="Madrid skyline at night, Gran Via lit up, Royal Palace silhouette, Spanish night sky",
        uptowns_skyline_prompt="Madrid skyline illustrated, Gran Via boulevard, Royal Palace silhouette, Spanish architecture",
        jersey_prompt="all-white Real Madrid jersey with gold block numbers on chest AND back, Real Madrid royal crest on left chest, white sleeves with gold trim",
        jersey_wordmark="Real Madrid royal crest badge on the left chest: royal blue and gold shield with crown — no text across chest",
        platform_font="'Real Madrid' in elegant serif font, white on dark",
        pants_prompt="white shorts with gold trim",
        helmet_prompt="N/A - soccer players do not wear helmets",
        number_style="large gold block numerals",
        logo_prompt="Real Madrid crest: royal blue and gold shield, crown on top, RM letters, purple diagonal stripe",
        panel_color="#00529F",
    ),
}

ALL_TEAMS = {**NFL_TEAMS, **HOCKEY_TEAMS, **BASEBALL_TEAMS, **SOCCER_TEAMS}


def get_team(abbreviation: str) -> TeamData:
    key = abbreviation.upper()
    if key not in ALL_TEAMS:
        raise ValueError(
            f"Unknown team '{abbreviation}'. Available: {list(ALL_TEAMS.keys())}")
    return ALL_TEAMS[key]
