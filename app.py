from flask import Flask, jsonify, render_template, send_from_directory
import sqlite3
import os

app = Flask(__name__)

# ── Config ─────────────────────────────────────────────────────────────────────
DB_PATH        = os.environ.get('DATABASE_PATH', 'GameTest.db')
PICTURES_FOLDER = 'Pictures'

# Allow CORS for potential frontend separation later
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    return response


# ── Helpers ────────────────────────────────────────────────────────────────────
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ── Static assets ──────────────────────────────────────────────────────────────
@app.route('/pictures/<path:filename>')
def serve_picture(filename):
    return send_from_directory(PICTURES_FOLDER, filename)


# ── Pages ──────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')


# ── API: Teams ─────────────────────────────────────────────────────────────────
@app.route('/api/teams')
def get_teams():
    conn = get_db_connection()
    teams = conn.execute(
        'SELECT TeamID, name, nickname, owner FROM Teams ORDER BY name'
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in teams])


@app.route('/api/team/<int:team_id>')
def get_team(team_id):
    conn = get_db_connection()
    team = conn.execute(
        'SELECT * FROM Teams WHERE TeamID = ?', (team_id,)
    ).fetchone()
    conn.close()
    if team:
        return jsonify(dict(team))
    return jsonify({'error': 'Team not found'}), 404


# ── API: Roster ────────────────────────────────────────────────────────────────
@app.route('/api/roster/<int:team_id>')
def get_roster(team_id):
    conn = get_db_connection()
    roster = conn.execute('''
        SELECT
            r.PlayerID,
            r.Pos,
            r.DepthChart,
            p.FirstName,
            p.LastName,
            p.Age,
            p.Height,
            p.Weight,
            p.College,
            pa.overall,
            pa.overall_let,
            pa.potential,
            pa.potential_let
        FROM Rosters r
        LEFT JOIN Players        p  ON r.PlayerID = p.PlayerID
        LEFT JOIN PlayerAttributes pa ON r.PlayerID = pa.PlayerID
        WHERE r.TeamID = ?
        ORDER BY
            CASE r.Pos
                WHEN 'QB' THEN 1  WHEN 'WR' THEN 2  WHEN 'RB' THEN 3
                WHEN 'TE' THEN 4  WHEN 'OL' THEN 5  WHEN 'DE' THEN 6
                WHEN 'DT' THEN 7  WHEN 'LB' THEN 8  WHEN 'CB' THEN 9
                WHEN 'FS' THEN 10 WHEN 'SS' THEN 11 WHEN 'K'  THEN 12
                WHEN 'P'  THEN 13 ELSE 14
            END,
            r.DepthChart
    ''', (team_id,)).fetchall()
    conn.close()
    return jsonify([dict(r) for r in roster])


# ── API: Scores ────────────────────────────────────────────────────────────────
@app.route('/api/scores')
def get_scores():
    conn = get_db_connection()
    scores = conn.execute('''
        SELECT
            g.GameID, g.SeasonID,
            g.HomeTeamScore, g.AwayTeamScore,
            g.WinningTeamID, g.LosingTeamID,
            g.TieFlag, g.OvertimeFlag,
            ht.name AS HomeTeamName,
            at.name AS AwayTeamName,
            wt.name AS WinningTeamName,
            lt.name AS LosingTeamName
        FROM GameLog g
        LEFT JOIN Teams ht ON g.HomeTeamID    = ht.TeamID
        LEFT JOIN Teams at ON g.AwayTeamID    = at.TeamID
        LEFT JOIN Teams wt ON g.WinningTeamID = wt.TeamID
        LEFT JOIN Teams lt ON g.LosingTeamID  = lt.TeamID
        ORDER BY g.GameID DESC
    ''').fetchall()
    conn.close()
    return jsonify([dict(r) for r in scores])


# ── API: Standings ─────────────────────────────────────────────────────────────
@app.route('/api/standings')
def get_standings():
    conn = get_db_connection()
    teams = conn.execute('SELECT TeamID, name FROM Teams').fetchall()

    standings = []
    for team in teams:
        tid  = team['TeamID']
        name = team['name']

        wins   = conn.execute(
            'SELECT COUNT(*) FROM GameLog WHERE WinningTeamID=? AND TieFlag=0', (tid,)
        ).fetchone()[0]
        losses = conn.execute(
            'SELECT COUNT(*) FROM GameLog WHERE LosingTeamID=?  AND TieFlag=0', (tid,)
        ).fetchone()[0]
        ties   = conn.execute(
            'SELECT COUNT(*) FROM GameLog WHERE (HomeTeamID=? OR AwayTeamID=?) AND TieFlag=1',
            (tid, tid)
        ).fetchone()[0]

        row = conn.execute('''
            SELECT
                SUM(CASE WHEN HomeTeamID=? THEN HomeTeamScore ELSE 0 END) +
                SUM(CASE WHEN AwayTeamID=? THEN AwayTeamScore ELSE 0 END) AS pf,
                SUM(CASE WHEN HomeTeamID=? THEN AwayTeamScore ELSE 0 END) +
                SUM(CASE WHEN AwayTeamID=? THEN HomeTeamScore ELSE 0 END) AS pa
            FROM GameLog WHERE HomeTeamID=? OR AwayTeamID=?
        ''', (tid, tid, tid, tid, tid, tid)).fetchone()

        pf = row['pf'] or 0
        pa = row['pa'] or 0

        standings.append({
            'TeamID': tid, 'name': name,
            'wins': wins, 'losses': losses, 'ties': ties,
            'points_for': pf, 'points_against': pa, 'point_diff': pf - pa
        })

    conn.close()
    standings.sort(key=lambda x: (x['wins'], x['point_diff']), reverse=True)
    return jsonify(standings)


# ── API: Season Stats ──────────────────────────────────────────────────────────
@app.route('/api/season-stats')
def get_season_stats():
    conn = get_db_connection()
    stats = conn.execute('''
        SELECT
            s.PlayerID,
            p.FirstName, p.LastName, p.Position,
            t.name AS TeamName,
            COUNT(DISTINCT s.GameID)        AS gamesPlayed,
            SUM(s.snaps)                    AS snaps,
            SUM(s.passingAttempts)          AS passingAttempts,
            SUM(s.passingCompletions)       AS passingCompletions,
            SUM(s.passingYards)             AS passingYards,
            SUM(s.passingTDs)               AS passingTDs,
            SUM(s.passingInterceptions)     AS passingInterceptions,
            SUM(s.rushAttempts)             AS rushAttempts,
            SUM(s.rushYards)                AS rushYards,
            SUM(s.rushTDs)                  AS rushTDs,
            SUM(s.rushFumbles)              AS rushFumbles,
            SUM(s.receivingTargets)         AS receivingTargets,
            SUM(s.receivingReceptions)      AS receivingReceptions,
            SUM(s.receivingYards)           AS receivingYards,
            SUM(s.receivingTDs)             AS receivingTDs,
            SUM(s.defensiveTackles)         AS defensiveTackles,
            SUM(s.defensiveSacks)           AS defensiveSacks,
            SUM(s.defensiveFumbles)         AS defensiveFumbles,
            SUM(s.defensiveInterceptions)   AS defensiveInterceptions,
            SUM(s.defensivePassBreakups)    AS defensivePassBreakups,
            SUM(s.defensiveTFL)             AS defensiveTFL,
            SUM(s.fgAttempt)                AS fgAttempt,
            SUM(s.fgMake)                   AS fgMake,
            SUM(s.puntAttempt)              AS puntAttempt,
            SUM(s.puntYards)                AS puntYards
        FROM SeasonStats s
        LEFT JOIN Players  p ON s.PlayerID = p.PlayerID
        LEFT JOIN Rosters  r ON s.PlayerID = r.PlayerID
        LEFT JOIN Teams    t ON r.TeamID   = t.TeamID
        WHERE s.season = 2025
        GROUP BY s.PlayerID
        ORDER BY p.LastName
    ''').fetchall()
    conn.close()
    return jsonify([dict(r) for r in stats])


# ── API: News ──────────────────────────────────────────────────────────────────
@app.route('/api/news')
def get_news():
    conn = get_db_connection()
    news = conn.execute('''
        SELECT NewsID, WeekID, SeasonID, NewsType, ProfilePicture, Media, Handle, Name, Content
        FROM NewsFeed
        ORDER BY SeasonID DESC, WeekID DESC, NewsID DESC
    ''').fetchall()
    conn.close()
    return jsonify([dict(r) for r in news])


# ── Run ────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    if debug:
        print("=" * 60)
        print("WFL Team Manager - Starting Server")
        print("=" * 60)
        print(f"Database : {DB_PATH}")
        print(f"URL      : http://127.0.0.1:{port}")
        print("=" * 60)
        print("Make sure GameTest.db is in the same folder as app.py")
        print("and that the 'templates' folder contains index.html\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
