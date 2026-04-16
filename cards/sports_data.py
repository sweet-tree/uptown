"""
Sports data registry — exact visual DNA per team.

Fields used by the Uptowns prompt engine:
  uptowns_stadium_prompt  — illustration-friendly stadium description
  uptowns_skyline_prompt  — architectural elements and landmark heights (what's there)
  uptowns_sky_prompt      — atmosphere, color, and die-cut top-edge anchor (how it looks)

  uptowns_skyline_prompt and uptowns_sky_prompt serve distinct purposes:
  skyline = architecture and relative heights; sky = color, mood, and which element
  is the TALLEST (defines the die-cut top). Keep them separate and non-redundant.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


@dataclass
class RosterPlayer:
    """Single player entry from the active roster."""
    name: str
    number: str
    position: str   # qb / rb / wr / te / de / dt / lb / cb / db / s / ot / og / c / k / p / ls


@dataclass
class PlayerSpec:
    """Card-slot assignment — a RosterPlayer with a facing side, pose, and ball."""
    name: str
    number: str
    position: str
    side: str  = "left"   # "left" → faces right | "right" → faces left
    pose: str  = "auto"   # auto / throwing / rushing / catching / jump_catch / route /
                           # pass_rush / speed_rush / bull_rush / linebacker / coverage /
                           # press_coverage / kicking / stiff_arm / hurdle / celebration
    ball: str  = "auto"   # auto / yes / no


@dataclass
class CardSpec:
    team: "TeamData"
    players: list[PlayerSpec]
    title: Optional[str] = None


class Sport(str, Enum):
    NFL      = "nfl"
    SOCCER   = "soccer"
    HOCKEY   = "hockey"
    BASEBALL = "baseball"


@dataclass
class TeamData:
    name: str
    city: str
    abbreviation: str
    sport: Sport
    primary_hex: str
    secondary_hex: str
    stadium_name: str
    uptowns_stadium_prompt: str
    uptowns_skyline_prompt: str
    jersey_prompt: str
    pants_prompt: str
    helmet_prompt: str
    number_style: str
    logo_prompt: str
    uptowns_sky_prompt: str = ""
    card_players: list = field(default_factory=list)  # list[PlayerSpec] — default left/right for the card
    roster: dict = field(default_factory=dict)         # dict[number_str, RosterPlayer] — full active roster


NFL_TEAMS = {
    "BAL": TeamData(
        name="Baltimore Ravens", city="Baltimore", abbreviation="BAL", sport=Sport.NFL,
        primary_hex="#241773", secondary_hex="#9E7C0C",
        stadium_name="M&T Bank Stadium",
        uptowns_stadium_prompt="M&T Bank Stadium illustrated front-facing — brick and steel exterior with arched windows, dark purple and gold banners on the facade, Ravens shield logos on the building panels, trees and landscaping at the base",
        uptowns_skyline_prompt="Baltimore skyline: the tall cylindrical Baltimore World Trade Center tower centered (tallest, distinctive rounded top), flanked by shorter rectangular downtown office buildings stepping down at varying heights on both sides, Inner Harbor waterfront at the base",
        uptowns_sky_prompt="Rich purple and gold dusk sky over Baltimore — deep royal purple at the top fading to warm amber and gold near the horizon from the Inner Harbor glow below. Dramatic volumetric clouds at dramatically varied heights: a tall billowing formation high on the left, the Baltimore World Trade Center's distinctive cylindrical top piercing through lower clouds at center, and a wide lower cloud bank on the right — each at a different height, creating a richly irregular silhouette. Deep purple sky visible in gaps between formations. Cinematic, premium, Ravens colors throughout.",
        jersey_prompt="deep purple NFL jersey — 'RAVENS' in white block letters across chest, white block numbers with thick black outline on chest and back, white shoulder stripes, purple sleeves with black and gold trim bands",
        pants_prompt="black NFL pants with purple and gold side stripes",
        helmet_prompt="glossy purple helmet, face fully visible through open visor — Ravens shield logo on both sides (black raven head on purple and gold shield with letter B), black face mask, thin gold center stripe",
        number_style="large white block numerals with thick black outline, collegiate style",
        logo_prompt="Ravens shield: black raven head facing left, purple and gold shield, bold letter B, gold trim border",
        card_players=[
            PlayerSpec(name="Lamar Jackson",  number="8",  position="qb", side="left"),
            PlayerSpec(name="Derrick Henry",  number="22", position="rb", side="right"),
        ],
    ),
    "KC": TeamData(
        name="Kansas City Chiefs", city="Kansas City", abbreviation="KC", sport=Sport.NFL,
        primary_hex="#E31837", secondary_hex="#FFB81C",
        stadium_name="GEHA Field at Arrowhead Stadium",
        uptowns_stadium_prompt="Arrowhead Stadium illustrated front-facing — distinctive arrowhead-shaped roofline, red brick exterior, Chiefs arrowhead logos on the facade panels, trees and parking lot surrounding",
        uptowns_skyline_prompt="Kansas City skyline: the Liberty Memorial obelisk tower (tall, slender stone needle) dominates center as the tallest landmark, flanked by downtown office towers of varying heights — some tall glass buildings, some shorter brick — Missouri River glimpsed at the base",
        uptowns_sky_prompt="Vivid amber and crimson Chiefs sunset sky — deep red-orange at the horizon fading to rich gold above. Dramatic volumetric clouds at dramatically varied heights: a towering golden cloud pillar rising very high on the left, the Liberty Memorial obelisk needle piercing sharply upward at center-left through a lower cloud bank, a wide mid-height cloud formation at center-right, and a smaller scattered group low on the right — each formation at a distinctly different height. Warm cinematic golden-hour light illuminates the cloud bases from below. Rich, saturated, premium Chiefs red and gold throughout.",
        jersey_prompt="red NFL jersey — 'CHIEFS' in white block letters across chest, white block numbers with red outline on chest and back, white shoulder panels, red sleeves with white and gold trim bands",
        pants_prompt="white NFL pants with red and gold side stripes",
        helmet_prompt="red helmet, face fully visible through open visor — Chiefs arrowhead logo on both sides (solid red arrowhead with white outline), white face mask, no center stripe",
        number_style="large white block numerals with red outline",
        logo_prompt="Chiefs arrowhead: solid red arrowhead pointing right, white outline, bold clean design",
        card_players=[
            PlayerSpec(name="Patrick Mahomes", number="15", position="qb", side="left"),
            PlayerSpec(name="Travis Kelce",    number="87", position="te", side="right"),
        ],
    ),
    "DAL": TeamData(
        name="Dallas Cowboys", city="Dallas", abbreviation="DAL", sport=Sport.NFL,
        primary_hex="#003594", secondary_hex="#869397",
        stadium_name="AT&T Stadium",
        uptowns_stadium_prompt="AT&T Stadium illustrated front-facing — massive domed silver roof, Cowboys star centered on the facade, glass and steel exterior, Cowboys helmet logos on the building panels",
        uptowns_skyline_prompt="Dallas skyline: Reunion Tower with its distinctive spherical globe top is the most recognizable landmark (mid-height, iconic shape), flanked by tall glass skyscrapers including the Bank of America Plaza and Renaissance Tower at varying heights, deep indigo sky",
        uptowns_sky_prompt="Vivid Texas noon sky — deep Cowboys navy-blue at the top fading to bright cerulean and warm gold at the horizon. Large dramatic white cumulus clouds at dramatically varied heights: a massive towering cloud column rising very high on the right with Reunion Tower's globe visible just beside it, a wide mid-height cloud bank at center, and lower scattered clouds on the left with Dallas skyline towers poking through at varying heights. Bright, vivid, cinematic Texas sunshine — warm golden light on every cloud surface. Bold contrast, premium collector card atmosphere.",
        jersey_prompt="white home NFL jersey — 'COWBOYS' in navy blue block letters across chest, navy blue numbers with silver metallic outline on chest and back, blue shoulder stripe panels, white sleeves with navy trim",
        pants_prompt="silver metallic NFL pants with navy and white side stripes",
        helmet_prompt="high-gloss silver metallic helmet, face fully visible through open visor — iconic blue five-pointed star centered on both sides, blue face mask, no center stripe",
        number_style="large white block numerals with silver metallic outline",
        logo_prompt="Cowboys star: large blue five-pointed star, white outline, centered on silver helmet panel",
        card_players=[
            PlayerSpec(name="Dak Prescott", number="4",  position="qb", side="left",  pose="throwing",  ball="yes"),
            PlayerSpec(name="CeeDee Lamb",  number="88", position="wr", side="right", pose="route",     ball="no"),
        ],
        roster={
            "0":  RosterPlayer("DeMarvion Overshown",  "0",  "lb"),
            "1":  RosterPlayer("P.J. Locke",           "1",  "db"),
            "2":  RosterPlayer("Cobie Durant",         "2",  "cb"),
            "4":  RosterPlayer("Dak Prescott",         "4",  "qb"),
            "5":  RosterPlayer("Bryan Anger",          "5",  "p"),
            "7":  RosterPlayer("Rashan Gary",          "7",  "lb"),
            "9":  RosterPlayer("KaVontae Turpin",      "9",  "wr"),
            "10": RosterPlayer("Joe Milton III",       "10", "qb"),
            "13": RosterPlayer("Sam Howell",           "13", "qb"),
            "14": RosterPlayer("Markquese Bell",       "14", "s"),
            "15": RosterPlayer("Derion Kendrick",      "15", "cb"),
            "19": RosterPlayer("Ryan Flournoy",        "19", "wr"),
            "21": RosterPlayer("Caelen Carson",        "21", "cb"),
            "23": RosterPlayer("Jaydon Blue",          "23", "rb"),
            "25": RosterPlayer("Trikweze Bridges",     "25", "cb"),
            "26": RosterPlayer("DaRon Bland",          "26", "cb"),
            "28": RosterPlayer("Malik Hooker",         "28", "s"),
            "33": RosterPlayer("Javonte Williams",     "33", "rb"),
            "34": RosterPlayer("Shavon Revel Jr.",     "34", "cb"),
            "35": RosterPlayer("Marist Liufau",        "35", "lb"),
            "36": RosterPlayer("Corey Ballentine",     "36", "cb"),
            "37": RosterPlayer("Phil Mafah",           "37", "rb"),
            "38": RosterPlayer("Alijah Clark",         "38", "db"),
            "40": RosterPlayer("Hunter Luepke",        "40", "rb"),
            "41": RosterPlayer("Donovan Ezeiruaku",    "41", "de"),
            "43": RosterPlayer("Malik Davis",          "43", "rb"),
            "44": RosterPlayer("Trent Sieg",           "44", "ls"),
            "45": RosterPlayer("Justin Barron",        "45", "lb"),
            "50": RosterPlayer("Shemar James",         "50", "lb"),
            "52": RosterPlayer("Tyler Booker",         "52", "og"),
            "53": RosterPlayer("James Houston",        "53", "de"),
            "56": RosterPlayer("Cooper Beebe",         "56", "c"),
            "60": RosterPlayer("Tyler Guyton",         "60", "ot"),
            "69": RosterPlayer("Ajani Cornelius",      "69", "ot"),
            "71": RosterPlayer("Nate Thomas",          "71", "ot"),
            "72": RosterPlayer("Matt Hennessy",        "72", "og"),
            "73": RosterPlayer("Tyler Smith",          "73", "og"),
            "76": RosterPlayer("Trevor Keegan",        "76", "og"),
            "78": RosterPlayer("Terence Steele",       "78", "ot"),
            "81": RosterPlayer("Jonathan Mingo",       "81", "wr"),
            "85": RosterPlayer("Princeton Fant",       "85", "te"),
            "86": RosterPlayer("Luke Schoonmaker",     "86", "te"),
            "87": RosterPlayer("Jake Ferguson",        "87", "te"),
            "88": RosterPlayer("CeeDee Lamb",          "88", "wr"),
            "89": RosterPlayer("Brevyn Spann-Ford",    "89", "te"),
            "90": RosterPlayer("Tyrus Wheat",          "90", "de"),
            "91": RosterPlayer("Otito Ogbonnia",       "91", "dt"),
            "92": RosterPlayer("Quinnen Williams",     "92", "dt"),
            "93": RosterPlayer("Jay Toia",             "93", "dt"),
            "95": RosterPlayer("Kenny Clark",          "95", "dt"),
            "98": RosterPlayer("Jonathan Bullard",     "98", "de"),
        },
    ),
    "GB": TeamData(
        name="Green Bay Packers", city="Green Bay", abbreviation="GB", sport=Sport.NFL,
        primary_hex="#203731", secondary_hex="#FFB612",
        stadium_name="Lambeau Field",
        uptowns_stadium_prompt="Lambeau Field illustrated front-facing — classic circular open-air bowl stadium, dark green and gold exterior, large Packers G logos on the facade panels, snow on the ground, pine trees surrounding the base. The stadium bowl is open at the front — you can see inside the seating bowl, the packed crowd in green and gold, and the field from this front angle.",
        uptowns_skyline_prompt="Green Bay winter scene: tall pointed pine trees of dramatically varying heights rise above the stadium — some very tall and narrow, others medium, others short — with snow-covered rooftops of low buildings visible between the trees",
        uptowns_sky_prompt="Crisp Wisconsin winter sky — deep steel grey-blue at the top with warm amber stadium glow rising from below. Dramatic grey-white cloud formations at dramatically varied heights: a tall billowing cloud tower rising high on the left, a very tall snow-dusted pine tree spiking sharply at center-left piercing through a low cloud, a wide mid-height cloud bank at center with another tall pine visible through it, and more pine tips at varying heights on the right — each pine and cloud at a distinctly different height. Cold winter air, light snowfall visible. Packers gold warmth glowing from the stadium lights below the clouds.",
        jersey_prompt="dark forest green NFL jersey — 'PACKERS' in gold block letters across chest, gold block numbers with white outline on chest and back, gold shoulder panels, green sleeves with gold and white trim bands",
        pants_prompt="gold NFL pants with green and white side stripes",
        helmet_prompt="matte gold helmet, face fully visible through open visor — Packers G logo on both sides (dark green oval with large white letter G centered), white face mask, no center stripe",
        number_style="large gold block numerals with white outline",
        logo_prompt="Packers G: dark green oval, large white letter G centered, clean bold design",
        card_players=[
            PlayerSpec(name="Jordan Love",  number="10", position="qb", side="left"),
            PlayerSpec(name="Jayden Reed",  number="11", position="wr", side="right"),
        ],
    ),
    "CHI": TeamData(
        name="Chicago Bears", city="Chicago", abbreviation="CHI", sport=Sport.NFL,
        primary_hex="#0B162A", secondary_hex="#C83803",
        stadium_name="Soldier Field",
        uptowns_stadium_prompt="Soldier Field illustrated front-facing — iconic neoclassical stone columns flanking both sides of the modern bowl, Bears C logos on the facade panels, Lake Michigan visible behind",
        uptowns_skyline_prompt="Chicago skyline: Willis Tower (Sears Tower) dominates center-left — tallest building with two slim antenna towers at the top. John Hancock Center with distinctive X-bracing stands to the right at second height. Shorter skyscrapers at many varying heights fill the rest. Lake Michigan shoreline at the base.",
        uptowns_sky_prompt="Dramatic Chicago dusk sky — deep navy blue at the top fading to vivid burnt orange and amber from the city glow near the horizon. Dramatic clouds at dramatically varied heights: Willis Tower's twin steel antenna tips pierce sharply upward through a low cloud bank at center — the antennas are the absolute highest point, far above everything else. John Hancock's X-braced silhouette clears a wider cloud bank at the right at a distinctly lower height. A tall billowing cloud formation rises high on the left. Navy blue sky visible between formations. Bears navy and orange throughout — cinematic Chicago dusk energy.",
        jersey_prompt="navy blue NFL jersey — 'BEARS' in orange block letters across chest, orange block numbers with white outline on chest and back, navy shoulder panels, navy sleeves with orange and white trim bands",
        pants_prompt="navy blue NFL pants with orange and white side stripes",
        helmet_prompt="navy blue helmet, face fully visible through open visor — Bears C logo on both sides (bold orange letter C with navy outline), navy face mask, no center stripe",
        number_style="large orange block numerals with white outline",
        logo_prompt="Bears C: bold orange letter C, navy outline, classic Chicago Bears design",
        card_players=[
            PlayerSpec(name="Caleb Williams", number="18", position="qb", side="left"),
            PlayerSpec(name="DJ Moore",        number="2",  position="wr", side="right"),
        ],
    ),
    "LV": TeamData(
        name="Las Vegas Raiders", city="Las Vegas", abbreviation="LV", sport=Sport.NFL,
        primary_hex="#000000", secondary_hex="#A5ACAF",
        stadium_name="Allegiant Stadium",
        uptowns_stadium_prompt="Allegiant Stadium illustrated front-facing — iconic massive smooth black dome, known as the 'Death Star' of NFL stadiums, seamless dark curved roof covering the entire structure, Raiders shield logo on the exterior facade panels, 'ALLEGIANT STADIUM' lettered in large silver text on the EXTERIOR facade wall below the roof — NOT on glass, NOT inside the stadium, exterior signage only, palm trees at the base",
        uptowns_skyline_prompt="Las Vegas Strip skyline: the Strat (Stratosphere) needle tower rises highest on the right (tallest, extremely slim with small pod near top), the massive spherical Sphere venue dominates the left, the Eiffel Tower replica at Paris Las Vegas stands center, surrounded by casino resort towers of dramatically varying heights",
        uptowns_sky_prompt="Las Vegas night sky — deep black-purple above with vivid neon glow rising from the Strip: electric pink, magenta, cyan and gold light blazing up from below. Dramatic cloud formations at dramatically varied heights: a wide charcoal cloud bank very high on the left with the MSG Sphere's colorful LED surface glowing below it, the Eiffel Tower replica rising tall and golden at center through a gap in the clouds, the Stratosphere needle piercing sharply upward at the right — the single tallest element — with a lower cloud around it. Each landmark at a distinctly different height. Deep purple-black sky visible between formations, lit by neon from below. Vivid, electric, unmistakably Vegas — Raiders black and silver with neon Strip energy.",
        jersey_prompt="black NFL jersey — 'RAIDERS' in silver block letters across chest, silver block numbers with white outline on chest and back, black shoulder panels with silver trim, black sleeves with silver trim bands",
        pants_prompt="silver NFL pants with black side stripes",
        helmet_prompt="high-gloss silver metallic helmet, face fully visible through open visor — Raiders shield logo on both sides (black shield with silver crossed swords and pirate eye patch), black face mask, no center stripe",
        number_style="large silver block numerals with white outline",
        logo_prompt="Raiders shield: black shield, silver crossed swords, silver football, silver pirate eye patch, bold iconic design",
        card_players=[
            PlayerSpec(name="Maxx Crosby",  number="98", position="de",  side="left"),
            PlayerSpec(name="Brock Bowers", number="89", position="te",  side="right"),
        ],
    ),
}

HOCKEY_TEAMS = {
    "TOR": TeamData(
        name="Toronto Maple Leafs", city="Toronto", abbreviation="TOR", sport=Sport.HOCKEY,
        primary_hex="#00205B", secondary_hex="#FFFFFF",
        stadium_name="Scotiabank Arena",
        uptowns_stadium_prompt="Scotiabank Arena illustrated front-facing — modern glass and steel exterior, large Maple Leafs logo on the facade, 'SCOTIABANK ARENA' lettering, downtown Toronto setting with CN Tower visible behind",
        uptowns_skyline_prompt="Toronto skyline: the CN Tower dominates as the unmistakable tallest landmark — tall thin needle with observation pod and slim antenna at the top — flanked by downtown glass office towers of many varying heights, Lake Ontario shoreline at the base",
        uptowns_sky_prompt="Crisp royal blue and white winter sky with cold clear atmosphere. The CN Tower's needle antenna is the absolute TALLEST die-cut point — its slim profile rises far above all other elements. Downtown office towers step down dramatically on both sides at varying heights, each at a different level. Die-cut traces the CN Tower's iconic profile and every individual building rooftop — a clean, unmistakable Toronto city silhouette.",
        jersey_prompt="royal blue hockey jersey — large 31-point maple leaf logo centered on chest, white block numbers on chest and back, white shoulder yoke, blue sleeves with white stripe bands",
        pants_prompt="royal blue hockey pants with white stripe",
        helmet_prompt="royal blue hockey helmet — Maple Leafs 31-point leaf logo on both sides, white cage",
        number_style="large white block numerals",
        logo_prompt="Maple Leafs: 31-point maple leaf in royal blue, white outline, centered",
    ),
    "EDM": TeamData(
        name="Edmonton Oilers", city="Edmonton", abbreviation="EDM", sport=Sport.HOCKEY,
        primary_hex="#041E42", secondary_hex="#FF4C00",
        stadium_name="Rogers Place",
        uptowns_stadium_prompt="Rogers Place illustrated front-facing — modern angular glass and steel exterior, large Oilers logo on the facade, 'ROGERS PLACE' lettering, downtown Edmonton setting",
        uptowns_skyline_prompt="Edmonton skyline: downtown office towers of varying heights, Rogers Place arena's curved angular roofline visible at the base, Northern Lights aurora borealis in vivid green and orange ribbons dancing above the tallest buildings",
        uptowns_sky_prompt="Deep navy Alberta night sky with Northern Lights aurora borealis rippling in vivid green and orange ribbons across the upper sky. The aurora's organic undulating waves define the die-cut top edge — sweeping curves at different heights, flowing and irregular, never a straight line. Downtown tower rooftops silhouette at the base of the aurora. Warm orange arena glow rises from the horizon.",
        jersey_prompt="navy blue hockey jersey — Oilers logo centered on chest (orange oil drop with navy 'OILERS' text inside), orange block numbers with white outline on chest and back, orange shoulder yoke, navy sleeves with orange and white stripe bands",
        pants_prompt="navy blue hockey pants with orange and white stripes",
        helmet_prompt="navy blue hockey helmet — Oilers oil drop logo on both sides, orange cage",
        number_style="large orange block numerals with white outline",
        logo_prompt="Oilers: orange oil drop shape, navy 'OILERS' text inside, white outline",
    ),
    "VGK": TeamData(
        name="Vegas Golden Knights", city="Las Vegas", abbreviation="VGK", sport=Sport.HOCKEY,
        primary_hex="#B4975A", secondary_hex="#333F42",
        stadium_name="T-Mobile Arena",
        uptowns_stadium_prompt="T-Mobile Arena illustrated front-facing — modern exterior with dramatic entrance, Golden Knights shield logo on the facade, 'T-MOBILE ARENA' lettering, Las Vegas Strip setting",
        uptowns_skyline_prompt="Las Vegas Strip skyline: the Strat (Stratosphere) needle tower rises highest on the right (tallest), the massive spherical Sphere venue dominates the left, the Eiffel Tower replica at Paris Las Vegas stands center, MGM Grand and resort towers at dramatically varying heights surrounding",
        uptowns_sky_prompt="Warm gold and deep charcoal desert night sky. The Strat needle tip is the TALLEST die-cut point. The Sphere's massive curved dome, the Eiffel Tower replica's pointed peak, and the resort towers at dramatically different heights create a richly irregular skyline silhouette across the full width. Soft gold neon glow from the Strip bathes the horizon. Die-cut traces this complex, varied Vegas profile exactly.",
        jersey_prompt="steel gray hockey jersey — Golden Knights medieval knight helmet logo centered on chest in gold with black outline, gold block numbers with black outline on chest and back, gold shoulder panels, gray sleeves with gold and black stripe bands",
        pants_prompt="steel gray hockey pants with gold and black stripes",
        helmet_prompt="steel gray hockey helmet — Golden Knights medieval knight helmet logo on both sides in gold with black outline, gold cage",
        number_style="large gold block numerals with black outline",
        logo_prompt="Golden Knights: medieval knight helmet in gold, black outline, bold angular design",
    ),
}

BASEBALL_TEAMS = {
    "NYY": TeamData(
        name="New York Yankees", city="New York", abbreviation="NYY", sport=Sport.BASEBALL,
        primary_hex="#003087", secondary_hex="#1C2841",
        stadium_name="Yankee Stadium",
        uptowns_stadium_prompt="Yankee Stadium illustrated front-facing — classic white limestone and steel exterior, interlocking NY logo on the facade, 'YANKEE STADIUM' lettering, Bronx setting",
        uptowns_skyline_prompt="New York City skyline: One World Trade Center (Freedom Tower) with its sharp pointed spire is the tallest landmark, the Empire State Building with its iconic stepped crown and antenna stands iconic center-left, surrounded by dense Manhattan skyscrapers of many different heights, East River glimpsed at the base",
        uptowns_sky_prompt="Deep navy blue Manhattan night sky with warm gold and white city glow. One World Trade Center's spire is the TALLEST die-cut point — its sharp tip rises above all others. The Empire State Building's crown and antenna are the second most prominent vertical. Dense Manhattan rooftops at many different heights fill the space between and around them, creating a richly complex, dense city skyline profile. Die-cut traces every spire tip and rooftop — a definitive, iconic NYC silhouette.",
        jersey_prompt="white pinstripe baseball jersey — 'Yankees' in flowing navy cursive script across chest, vertical navy pinstripes throughout, navy block numbers on back, navy interlocking NY logo on left chest, white sleeves with navy trim",
        pants_prompt="white pinstripe baseball pants with navy stirrups",
        helmet_prompt="navy batting helmet, face fully visible — white interlocking NY logo on left side, navy brim, no visor",
        number_style="large navy block numerals, classic baseball style",
        logo_prompt="Yankees NY: interlocking navy N and Y letters, classic serif style, white outline",
    ),
    "LAD": TeamData(
        name="Los Angeles Dodgers", city="Los Angeles", abbreviation="LAD", sport=Sport.BASEBALL,
        primary_hex="#005A9C", secondary_hex="#EF3E42",
        stadium_name="Dodger Stadium",
        uptowns_stadium_prompt="Dodger Stadium illustrated front-facing — classic 1960s circular design, Dodger blue exterior, interlocking LA logo on the facade, tall California palm trees surrounding, Hollywood Hills visible behind",
        uptowns_skyline_prompt="Los Angeles skyline: Griffith Observatory with its classic domed towers sits prominently on the Hollywood Hills (distinct silhouette), tall slender California palm trees of dramatically varying heights in the foreground, downtown LA glass towers in the distance, Santa Monica Mountains as the backdrop",
        uptowns_sky_prompt="Golden California sunset sky in warm amber and coral fading to bright blue above. Tall California palm trees of dramatically varying heights spike upward — their feathery fronds define the die-cut top edge in a naturally irregular, tropical silhouette. Some palms tower very high, others shorter. The Griffith Observatory domes are visible on the hillside at mid-height. Die-cut follows every palm frond tip and dome curve — organic, tropical, never smooth.",
        jersey_prompt="Dodger blue baseball jersey — 'Dodgers' in flowing white cursive script across chest, white block numbers on back, white sleeves with Dodger blue trim",
        pants_prompt="white baseball pants with Dodger blue stirrups",
        helmet_prompt="Dodger blue batting helmet, face fully visible — white interlocking LA logo on left side, Dodger blue brim, no visor",
        number_style="large white block numerals",
        logo_prompt="Dodgers LA: interlocking blue L and A letters, classic script style, white outline",
    ),
    "CHC": TeamData(
        name="Chicago Cubs", city="Chicago", abbreviation="CHC", sport=Sport.BASEBALL,
        primary_hex="#0E3386", secondary_hex="#CC3433",
        stadium_name="Wrigley Field",
        uptowns_stadium_prompt="Wrigley Field illustrated front-facing — classic red brick exterior, iconic hand-operated scoreboard above the outfield, Cubs C logo on the facade, ivy-covered outfield walls visible, Wrigleyville neighborhood rooftops behind",
        uptowns_skyline_prompt="Chicago skyline from Wrigley Field's perspective: Willis Tower's twin antennas dominant in the far distance (tallest), Wrigleyville neighborhood brick rooftops of varying heights in the mid-ground, the Wrigley Field scoreboard rising above the stadium",
        uptowns_sky_prompt="Bright Chicago summer afternoon sky, vivid blue with large white cumulus clouds. Willis Tower's twin antenna tips define the highest die-cut points in the far distance. Large white fluffy clouds billow above the Wrigleyville rooftops — their soft rounded tops create an organically curvy die-cut silhouette. The varying heights of the neighborhood brick buildings add irregular texture throughout. Die-cut is a friendly, neighborhood-scale urban and cloud silhouette.",
        jersey_prompt="Cubs blue baseball jersey — 'Cubs' in flowing red cursive script across chest, red pinstripes, blue block numbers on back, blue sleeves with red trim",
        pants_prompt="white baseball pants with blue and red stirrups",
        helmet_prompt="Cubs blue batting helmet, face fully visible — red C logo on left side, blue brim, no visor",
        number_style="large blue block numerals with red outline",
        logo_prompt="Cubs C: bold red letter C, blue outline, classic Chicago Cubs design",
    ),
}

SOCCER_TEAMS = {
    "RM": TeamData(
        name="Real Madrid", city="Madrid", abbreviation="RM", sport=Sport.SOCCER,
        primary_hex="#FFFFFF", secondary_hex="#00529F",
        stadium_name="Santiago Bernabeu",
        uptowns_stadium_prompt="Santiago Bernabeu illustrated front-facing — modern circular exterior with distinctive metallic perforated facade, Real Madrid royal crest on the building, 'SANTIAGO BERNABEU' lettering, Madrid city setting",
        uptowns_skyline_prompt="Madrid skyline: the four Cuatro Torres business skyscrapers (four towers of noticeably different heights) dominate the background, the Royal Palace with its baroque domed towers visible center-left, Gran Via boulevard's classic ornate architecture at the base",
        uptowns_sky_prompt="Warm Mediterranean evening sky in deep royal blue fading to gold at the horizon. The tallest Cuatro Torres skyscraper is the highest die-cut point — its glass peak rises above the other three towers, which each stand at different heights, creating an irregular modern skyline. The Royal Palace's baroque domes and Gran Via cornices create historic architectural detail at a lower level. Evening light glows gold from below. Die-cut traces this varied mix of modern towers and historic silhouettes.",
        jersey_prompt="all-white Real Madrid jersey — Real Madrid royal crest badge on left chest (royal blue and gold shield with crown), gold block numbers on chest and back, white sleeves with gold trim",
        pants_prompt="white shorts with gold trim",
        helmet_prompt="no helmet — soccer player",
        number_style="large gold block numerals",
        logo_prompt="Real Madrid crest: royal blue and gold shield, crown on top, RM letters, purple diagonal stripe",
    ),
}

ALL_TEAMS = {**NFL_TEAMS, **HOCKEY_TEAMS, **BASEBALL_TEAMS, **SOCCER_TEAMS}


def get_team(abbreviation: str) -> TeamData:
    key = abbreviation.upper()
    if key not in ALL_TEAMS:
        raise ValueError(
            f"Unknown team '{abbreviation}'. Available: {list(ALL_TEAMS.keys())}")
    return ALL_TEAMS[key]
