/**
 * Downloads nflverse roster + team colors, merges stadium metadata and optional
 * prompt overrides, writes prisma/seeds/nfl/nfl-full.generated.json for Prisma seed.
 *
 * Run: npm run build:nfl-seed-data
 */
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";
import { parse } from "csv-parse/sync";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(__dirname, "..");
const OUT = path.join(ROOT, "prisma/seeds/nfl/nfl-full.generated.json");
const OVERRIDES_PATH = path.join(ROOT, "prisma/seeds/nfl/prompt-overrides.json");

const ROSTER_URL =
  "https://github.com/nflverse/nflverse-data/releases/download/rosters/roster_2026.csv";
const TEAMS_URL =
  "https://github.com/nflverse/nflverse-data/releases/download/teams/teams_colors_logos.csv";

/** @type {Record<string, { city: string; stadiumName: string }>} */
const STADIUM = {
  ARI: { city: "Glendale", stadiumName: "State Farm Stadium" },
  ATL: { city: "Atlanta", stadiumName: "Mercedes-Benz Stadium" },
  BAL: { city: "Baltimore", stadiumName: "M&T Bank Stadium" },
  BUF: { city: "Orchard Park", stadiumName: "Highmark Stadium" },
  CAR: { city: "Charlotte", stadiumName: "Bank of America Stadium" },
  CHI: { city: "Chicago", stadiumName: "Soldier Field" },
  CIN: { city: "Cincinnati", stadiumName: "Paycor Stadium" },
  CLE: { city: "Cleveland", stadiumName: "Huntington Bank Field" },
  DAL: { city: "Dallas", stadiumName: "AT&T Stadium" },
  DEN: { city: "Denver", stadiumName: "Empower Field at Mile High" },
  DET: { city: "Detroit", stadiumName: "Ford Field" },
  GB: { city: "Green Bay", stadiumName: "Lambeau Field" },
  HOU: { city: "Houston", stadiumName: "NRG Stadium" },
  IND: { city: "Indianapolis", stadiumName: "Lucas Oil Stadium" },
  JAX: { city: "Jacksonville", stadiumName: "EverBank Stadium" },
  KC: { city: "Kansas City", stadiumName: "GEHA Field at Arrowhead Stadium" },
  LA: { city: "Inglewood", stadiumName: "SoFi Stadium" },
  LAC: { city: "Inglewood", stadiumName: "SoFi Stadium" },
  LV: { city: "Las Vegas", stadiumName: "Allegiant Stadium" },
  MIA: { city: "Miami Gardens", stadiumName: "Hard Rock Stadium" },
  MIN: { city: "Minneapolis", stadiumName: "U.S. Bank Stadium" },
  NE: { city: "Foxborough", stadiumName: "Gillette Stadium" },
  NO: { city: "New Orleans", stadiumName: "Caesars Superdome" },
  NYG: { city: "East Rutherford", stadiumName: "MetLife Stadium" },
  NYJ: { city: "East Rutherford", stadiumName: "MetLife Stadium" },
  PHI: { city: "Philadelphia", stadiumName: "Lincoln Financial Field" },
  PIT: { city: "Pittsburgh", stadiumName: "Acrisure Stadium" },
  SEA: { city: "Seattle", stadiumName: "Lumen Field" },
  SF: { city: "Santa Clara", stadiumName: "Levi's Stadium" },
  TB: { city: "Tampa", stadiumName: "Raymond James Stadium" },
  TEN: { city: "Nashville", stadiumName: "Nissan Stadium" },
  WAS: { city: "Landover", stadiumName: "Northwest Stadium" },
};

function fetchText(url) {
  return fetch(url).then((r) => {
    if (!r.ok) throw new Error(`GET ${url} -> ${r.status}`);
    return r.text();
  });
}

function intOr0(v) {
  const n = Number.parseInt(String(v ?? "").trim(), 10);
  return Number.isFinite(n) ? n : 0;
}

function depth(row) {
  return String(row.depth_chart_position || row.position || "")
    .trim()
    .toUpperCase();
}

function jerseyStr(row) {
  const j = String(row.jersey_number ?? "").trim();
  return j || "0";
}

function jerseyNum(row) {
  const n = Number.parseInt(jerseyStr(row), 10);
  return Number.isFinite(n) ? n : 0;
}

/** @param {Record<string,string>[]} actRows */
function pickQb(actRows) {
  const qbs = actRows.filter((r) => depth(r) === "QB");
  if (!qbs.length) return null;
  qbs.sort((a, b) => intOr0(b.years_exp) - intOr0(a.years_exp) || jerseyNum(b) - jerseyNum(a));
  return qbs[0];
}

/** @param {Record<string,string>[]} actRows */
function pickRightFeatured(actRows) {
  const orderTry = ["WR", "TE", "RB"];
  for (const pos of orderTry) {
    const pool = actRows.filter((r) => depth(r) === pos);
    if (!pool.length) continue;
    pool.sort((a, b) => intOr0(b.years_exp) - intOr0(a.years_exp) || jerseyNum(b) - jerseyNum(a));
    return { player: pool[0], position: pos.toLowerCase() };
  }
  const defPool = actRows.filter((r) =>
    ["DE", "DT", "OLB", "ILB", "MLB", "LB", "CB", "SAF", "FS", "SS"].includes(depth(r)),
  );
  if (defPool.length) {
    defPool.sort((a, b) => intOr0(b.years_exp) - intOr0(a.years_exp) || jerseyNum(b) - jerseyNum(a));
    const p = defPool[0];
    return { player: p, position: depth(p).toLowerCase() };
  }
  actRows.sort((a, b) => intOr0(b.years_exp) - intOr0(a.years_exp) || jerseyNum(b) - jerseyNum(a));
  const p = actRows[0];
  return p ? { player: p, position: depth(p).toLowerCase() || "ath" } : null;
}

function cardPoseBall(side, posLower) {
  if (side === "left") return { pose: "throwing", ball: "yes" };
  if (posLower === "rb") return { pose: "rushing", ball: "yes" };
  if (posLower === "te") return { pose: "rushing", ball: "yes" };
  if (posLower === "wr") return { pose: "route", ball: "no" };
  if (["de", "dt", "olb", "ilb", "mlb", "lb"].includes(posLower))
    return { pose: "speed_rush", ball: "no" };
  return { pose: "auto", ball: "auto" };
}

function ensureHash(hex) {
  const h = String(hex || "").trim();
  if (!h) return "#000000";
  return h.startsWith("#") ? h : `#${h}`;
}

function templatedPrompts(meta, teamRow) {
  const nick = teamRow.team_nick || teamRow.team_abbr;
  const p1 = ensureHash(teamRow.team_color);
  const p2 = ensureHash(teamRow.team_color2);
  const { stadiumName, city } = meta;
  const word = nick.toUpperCase();
  return {
    stadiumPrompt: `${stadiumName} illustrated front-facing — modern NFL stadium exterior, ${nick} colors (${p1} and ${p2}), ${nick} wordmarks and logos on facade panels, dramatic approach and plaza`,
    skylinePrompt: `${city} area skyline beyond the stadium: layered buildings and towers at varied heights, regional character, soft atmospheric depth`,
    skyPrompt: `Cinematic gameday sky for the ${nick} — deep tones blending ${p1} and ${p2} in the upper atmosphere, warm horizon glow from stadium and city lights below, dramatic volumetric clouds at varied heights, premium sports photography mood`,
    jerseyPrompt: `${nick} NFL jersey in team palette (${p1} primary, ${p2} accents) — '${word}' across chest, bold TV-style numbers, authentic NFL paneling and shoulder striping`,
    pantsPrompt: `${nick} NFL pants matching team striping (${p1} / ${p2})`,
    helmetPrompt: `${nick} NFL helmet in team colors with correct shell finish, team logo on both sides, face visible through open visor, pro facemask`,
    numberStyle: `Bold pro-style numerals matching ${nick} color rules`,
    logoPrompt: `${nick} official NFL team mark: clean silhouette, correct colors (${p1}, ${p2}), no invented symbols`,
  };
}

async function main() {
  const [rosterCsv, teamsCsv] = await Promise.all([fetchText(ROSTER_URL), fetchText(TEAMS_URL)]);

  const roster = parse(rosterCsv, { columns: true, skip_empty_lines: true, relax_column_count: true });
  const teamRows = parse(teamsCsv, { columns: true, skip_empty_lines: true });

  /** @type {Record<string, Record<string,string>>} */
  const teamByAbbr = {};
  for (const t of teamRows) {
    teamByAbbr[t.team_abbr] = t;
  }

  const byTeam = new Map();
  for (const row of roster) {
    const abbr = row.team;
    if (!abbr) continue;
    if (!byTeam.has(abbr)) byTeam.set(abbr, []);
    byTeam.get(abbr).push(row);
  }

  const abbrs = [...byTeam.keys()].sort();
  if (abbrs.length !== 32) {
    console.warn(`Expected 32 teams, got ${abbrs.length}:`, abbrs.join(", "));
  }

  let overrides = {};
  try {
    overrides = JSON.parse(readFileSync(OVERRIDES_PATH, "utf8"));
  } catch {
    console.warn("No prompt-overrides.json or invalid JSON — using templates only.");
  }

  const teams = [];

  for (const abbr of abbrs) {
    const stadium = STADIUM[abbr];
    if (!stadium) {
      throw new Error(`Missing STADIUM entry for ${abbr}`);
    }
    const trow = teamByAbbr[abbr];
    if (!trow) {
      throw new Error(`Missing teams_colors row for ${abbr}`);
    }

    const allRows = byTeam.get(abbr) || [];
    const act = allRows.filter((r) => r.status === "ACT");
    const ovr = overrides[abbr] || {};

    const primaryHex = ensureHash(ovr.primaryHex ?? trow.team_color);
    const secondaryHex = ensureHash(ovr.secondaryHex ?? trow.team_color2);
    const name = ovr.name ?? trow.team_name;
    const city = ovr.city ?? stadium.city;
    const stadiumName = ovr.stadiumName ?? stadium.stadiumName;

    const basePrompts = templatedPrompts({ stadiumName, city }, { ...trow, team_color: primaryHex, team_color2: secondaryHex });

    const qb = pickQb(act);
    const rightPick = pickRightFeatured(act.filter((r) => depth(r) !== "QB"));
    let cardPlayers;
    if (Array.isArray(ovr.cardPlayers) && ovr.cardPlayers.length) {
      cardPlayers = ovr.cardPlayers;
    } else if (qb && rightPick) {
      const rl = cardPoseBall("left", "qb");
      const rr = cardPoseBall("right", rightPick.position);
      cardPlayers = [
        {
          name: qb.full_name,
          number: jerseyStr(qb),
          position: "qb",
          side: "left",
          pose: rl.pose,
          ball: rl.ball,
          order: 0,
        },
        {
          name: rightPick.player.full_name,
          number: jerseyStr(rightPick.player),
          position: rightPick.position,
          side: "right",
          pose: rr.pose,
          ball: rr.ball,
          order: 1,
        },
      ];
    } else if (act.length >= 2) {
      const sorted = [...act].sort(
        (a, b) => intOr0(b.years_exp) - intOr0(a.years_exp) || jerseyNum(b) - jerseyNum(a),
      );
      const a = sorted[0];
      const b = sorted[1];
      const pa = (a.position || "").toLowerCase() || "ath";
      const pb = (b.position || "").toLowerCase() || "ath";
      const p0 = cardPoseBall("left", pa);
      const p1 = cardPoseBall("right", pb);
      cardPlayers = [
        { name: a.full_name, number: jerseyStr(a), position: pa, side: "left", pose: p0.pose, ball: p0.ball, order: 0 },
        { name: b.full_name, number: jerseyStr(b), position: pb, side: "right", pose: p1.pose, ball: p1.ball, order: 1 },
      ];
    } else if (act.length === 1) {
      const a = act[0];
      const pa = (a.position || "").toLowerCase() || "ath";
      const p0 = cardPoseBall("left", pa);
      cardPlayers = [{ name: a.full_name, number: jerseyStr(a), position: pa, side: "left", pose: p0.pose, ball: p0.ball, order: 0 }];
    } else {
      cardPlayers = [];
    }

    const rosterEntries = act
      .map((r) => ({
        name: r.full_name,
        number: jerseyStr(r),
        position: (r.position || r.depth_chart_position || "").toLowerCase() || "—",
      }))
      .sort((a, b) => a.name.localeCompare(b.name));

    teams.push({
      abbreviation: abbr,
      name,
      city,
      primaryHex,
      secondaryHex,
      stadiumName,
      stadiumPrompt: ovr.stadiumPrompt ?? basePrompts.stadiumPrompt,
      skylinePrompt: ovr.skylinePrompt ?? basePrompts.skylinePrompt,
      skyPrompt: ovr.skyPrompt ?? basePrompts.skyPrompt,
      jerseyPrompt: ovr.jerseyPrompt ?? basePrompts.jerseyPrompt,
      pantsPrompt: ovr.pantsPrompt ?? basePrompts.pantsPrompt,
      helmetPrompt: ovr.helmetPrompt ?? basePrompts.helmetPrompt,
      numberStyle: ovr.numberStyle ?? basePrompts.numberStyle,
      logoPrompt: ovr.logoPrompt ?? basePrompts.logoPrompt,
      cardPlayers,
      roster: rosterEntries,
    });
  }

  const payload = {
    meta: {
      generatedAt: new Date().toISOString(),
      rosterUrl: ROSTER_URL,
      teamsUrl: TEAMS_URL,
      rosterSeason: 2026,
      actPlayerRows: roster.filter((r) => r.status === "ACT").length,
    },
    teams,
  };

  writeFileSync(OUT, JSON.stringify(payload, null, 2) + "\n", "utf8");
  console.log(`Wrote ${teams.length} teams, ${payload.meta.actPlayerRows} ACT roster rows -> ${path.relative(ROOT, OUT)}`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
