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


NFL_TEAMS = {
    "BAL": TeamData(
        name="Baltimore Ravens", city="Baltimore", abbreviation="BAL", sport=Sport.NFL,
        primary_hex="#241773", secondary_hex="#9E7C0C",
        stadium_name="M&T Bank Stadium",
        uptowns_stadium_prompt="M&T Bank Stadium illustrated front-facing — brick and steel exterior with arched windows, dark purple and gold banners on the facade, Ravens shield logos on the building panels, trees and landscaping at the base",
        uptowns_skyline_prompt="Baltimore skyline: the tall cylindrical Baltimore World Trade Center tower centered (tallest, distinctive rounded top), flanked by shorter rectangular downtown office buildings stepping down at varying heights on both sides, Inner Harbor waterfront at the base",
        uptowns_sky_prompt="Deep purple and gold night sky. The World Trade Center's cylindrical rounded top is the single highest die-cut point — flanking buildings step down from it in both directions, each rooftop at a different level, creating a complex jagged urban silhouette. Warm amber glow from Inner Harbor lights rises from below. Die-cut traces every individual rooftop — never a smooth arc.",
        jersey_prompt="deep purple NFL jersey — 'RAVENS' in white block letters across chest, white block numbers with thick black outline on chest and back, white shoulder stripes, purple sleeves with black and gold trim bands",
        pants_prompt="black NFL pants with purple and gold side stripes",
        helmet_prompt="glossy purple helmet, face fully visible through open visor — Ravens shield logo on both sides (black raven head on purple and gold shield with letter B), black face mask, thin gold center stripe",
        number_style="large white block numerals with thick black outline, collegiate style",
        logo_prompt="Ravens shield: black raven head facing left, purple and gold shield, bold letter B, gold trim border",
    ),
    "KC": TeamData(
        name="Kansas City Chiefs", city="Kansas City", abbreviation="KC", sport=Sport.NFL,
        primary_hex="#E31837", secondary_hex="#FFB81C",
        stadium_name="GEHA Field at Arrowhead Stadium",
        uptowns_stadium_prompt="Arrowhead Stadium illustrated front-facing — distinctive arrowhead-shaped roofline, red brick exterior, Chiefs arrowhead logos on the facade panels, trees and parking lot surrounding",
        uptowns_skyline_prompt="Kansas City skyline: the Liberty Memorial obelisk tower (tall, slender stone needle) dominates center as the tallest landmark, flanked by downtown office towers of varying heights — some tall glass buildings, some shorter brick — Missouri River glimpsed at the base",
        uptowns_sky_prompt="Warm golden-red sunset sky, deep crimson at the horizon fading to amber above. The Liberty Memorial obelisk is the TALLEST die-cut point — its stone needle tip rises highest above everything else. Downtown towers step down from it left and right, each at a different height. Wispy golden sunset clouds drift above the towers, their soft organic tops adding curvy variation to the die-cut silhouette.",
        jersey_prompt="red NFL jersey — 'CHIEFS' in white block letters across chest, white block numbers with red outline on chest and back, white shoulder panels, red sleeves with white and gold trim bands",
        pants_prompt="white NFL pants with red and gold side stripes",
        helmet_prompt="red helmet, face fully visible through open visor — Chiefs arrowhead logo on both sides (solid red arrowhead with white outline), white face mask, no center stripe",
        number_style="large white block numerals with red outline",
        logo_prompt="Chiefs arrowhead: solid red arrowhead pointing right, white outline, bold clean design",
    ),
    "DAL": TeamData(
        name="Dallas Cowboys", city="Dallas", abbreviation="DAL", sport=Sport.NFL,
        primary_hex="#003594", secondary_hex="#869397",
        stadium_name="AT&T Stadium",
        uptowns_stadium_prompt="AT&T Stadium illustrated front-facing — massive domed silver roof, Cowboys star centered on the facade, glass and steel exterior, Cowboys helmet logos on the building panels",
        uptowns_skyline_prompt="Dallas skyline: Reunion Tower with its distinctive spherical globe top is the most recognizable landmark (mid-height, iconic shape), flanked by tall glass skyscrapers including the Bank of America Plaza and Renaissance Tower at varying heights, deep indigo sky",
        uptowns_sky_prompt="Bright Texas daytime sky, vivid navy-blue fading to lighter blue at the horizon. Large white fluffy cumulus clouds billow upward above the skyline — their soft rounded tops define the die-cut top edge in a naturally curvy, varied silhouette. Some cloud peaks tower high, others lower. Reunion Tower's globe is visible against the bright sky between the clouds. Die-cut follows every cloud curve — organic and flowing.",
        jersey_prompt="navy blue NFL jersey — 'COWBOYS' in white block letters across chest, white block numbers with silver metallic outline on chest and back, white shoulder panels with silver trim, navy sleeves",
        pants_prompt="silver metallic NFL pants with navy and white side stripes",
        helmet_prompt="high-gloss silver metallic helmet, face fully visible through open visor — iconic blue five-pointed star centered on both sides, blue face mask, no center stripe",
        number_style="large white block numerals with silver metallic outline",
        logo_prompt="Cowboys star: large blue five-pointed star, white outline, centered on silver helmet panel",
    ),
    "GB": TeamData(
        name="Green Bay Packers", city="Green Bay", abbreviation="GB", sport=Sport.NFL,
        primary_hex="#203731", secondary_hex="#FFB612",
        stadium_name="Lambeau Field",
        uptowns_stadium_prompt="Lambeau Field illustrated front-facing — classic circular bowl stadium, dark green and gold exterior, large Packers G logos on the facade panels, snow on the ground, pine trees surrounding the base",
        uptowns_skyline_prompt="Green Bay winter scene: tall pointed pine trees of dramatically varying heights rise above the stadium — some very tall and narrow, others medium, others short — with snow-covered rooftops of low buildings visible between the trees",
        uptowns_sky_prompt="Cold Wisconsin winter sky in deep forest green fading to warm gold. The tallest pine trees spike upward to define the die-cut top edge — their sharp irregular pointed tips create a naturally jagged organic silhouette, no two pine peaks at the same height. Light snow dusts the branches. Warm gold glow rises from stadium lights at the horizon. Die-cut traces every pine tip — spiky and organic, never smooth.",
        jersey_prompt="dark forest green NFL jersey — 'PACKERS' in gold block letters across chest, gold block numbers with white outline on chest and back, gold shoulder panels, green sleeves with gold and white trim bands",
        pants_prompt="gold NFL pants with green and white side stripes",
        helmet_prompt="matte gold helmet, face fully visible through open visor — Packers G logo on both sides (dark green oval with large white letter G centered), white face mask, no center stripe",
        number_style="large gold block numerals with white outline",
        logo_prompt="Packers G: dark green oval, large white letter G centered, clean bold design",
    ),
    "CHI": TeamData(
        name="Chicago Bears", city="Chicago", abbreviation="CHI", sport=Sport.NFL,
        primary_hex="#0B162A", secondary_hex="#C83803",
        stadium_name="Soldier Field",
        uptowns_stadium_prompt="Soldier Field illustrated front-facing — iconic neoclassical stone columns flanking both sides of the modern bowl, Bears C logos on the facade panels, Lake Michigan visible behind",
        uptowns_skyline_prompt="Chicago skyline: Willis Tower (Sears Tower) dominates center-left — tallest building with two slim antenna towers at the top. John Hancock Center with distinctive X-bracing stands to the right at second height. Shorter skyscrapers at many varying heights fill the rest. Lake Michigan shoreline at the base.",
        uptowns_sky_prompt="Deep navy blue Chicago night sky with burnt orange glow from city lights. Large dramatic clouds billow high on the left side, their uneven organic tops rising well above the buildings. Willis Tower's twin antenna tips are the TALLEST point at center. John Hancock Center rises to the right as the second peak. Left side high clouds, center Willis Tower peak, right side stepping down — a strongly asymmetric irregular silhouette across the full width.",
        jersey_prompt="navy blue NFL jersey — 'BEARS' in orange block letters across chest, orange block numbers with white outline on chest and back, navy shoulder panels, navy sleeves with orange and white trim bands",
        pants_prompt="navy blue NFL pants with orange and white side stripes",
        helmet_prompt="navy blue helmet, face fully visible through open visor — Bears C logo on both sides (bold orange letter C with navy outline), navy face mask, no center stripe",
        number_style="large orange block numerals with white outline",
        logo_prompt="Bears C: bold orange letter C, navy outline, classic Chicago Bears design",
    ),
    "LV": TeamData(
        name="Las Vegas Raiders", city="Las Vegas", abbreviation="LV", sport=Sport.NFL,
        primary_hex="#000000", secondary_hex="#A5ACAF",
        stadium_name="Allegiant Stadium",
        uptowns_stadium_prompt="Allegiant Stadium illustrated front-facing — iconic massive smooth black dome, known as the 'Death Star' of NFL stadiums, seamless dark curved roof covering the entire structure, Raiders shield logo on the facade, 'ALLEGIANT STADIUM' lettering, palm trees at the base",
        uptowns_skyline_prompt="Las Vegas Strip skyline: the Strat (Stratosphere) needle tower rises highest on the right (tallest, extremely slim with small pod near top), the massive spherical Sphere venue dominates the left, the Eiffel Tower replica at Paris Las Vegas stands center, surrounded by casino resort towers of dramatically varying heights",
        uptowns_sky_prompt="Deep charcoal desert dusk sky fading to silver-grey. The Strat needle antenna tip is the single TALLEST die-cut point — slim, extreme, and unmistakable. The Sphere's massive curved dome creates a unique rounded silhouette on the left. The Eiffel Tower replica's pointed peak and the varying resort tower rooftops create a richly irregular skyline profile across the full width. Subtle warm amber neon glow from the Strip at the horizon. Die-cut traces this dramatic, diverse Vegas skyline exactly.",
        jersey_prompt="black NFL jersey — 'RAIDERS' in silver block letters across chest, silver block numbers with white outline on chest and back, black shoulder panels with silver trim, black sleeves with silver trim bands",
        pants_prompt="silver NFL pants with black side stripes",
        helmet_prompt="high-gloss silver metallic helmet, face fully visible through open visor — Raiders shield logo on both sides (black shield with silver crossed swords and pirate eye patch), black face mask, no center stripe",
        number_style="large silver block numerals with white outline",
        logo_prompt="Raiders shield: black shield, silver crossed swords, silver football, silver pirate eye patch, bold iconic design",
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
