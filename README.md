# 🏈 WFL Team Manager

A full-featured web application for managing and viewing WFL (fictional football league) team data, including rosters, standings, scores, season statistics, and news feed.

## ✨ Features

- 📊 **Team Rosters** - View complete player rosters with stats and ratings
- 🏆 **Standings** - Real-time team rankings with W-L-T records
- 📈 **Season Stats** - Player statistics by skill category (Passing, Rushing, Receiving, Defense, Kicking, Punting)
- 🗞️ **WFL News** - Twitter-style news feed with team updates
- 🎨 **Team Logos** - Visual branding throughout the interface
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.8 or higher
- pip

### Installation

1. Clone this repository:
```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
cd YOUR-REPO-NAME
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make sure you have these files in place:
   - `GameTest.db` (SQLite database)
   - `Pictures/` folder with team logos
   - `templates/index.html`

4. Run the application:
```bash
python app.py
```

5. Open your browser to:
```
http://127.0.0.1:5000
```

## 🌐 Deploying to Render

See **[DEPLOY_TO_RENDER.md](DEPLOY_TO_RENDER.md)** for complete deployment instructions.

**TL;DR:**
1. Push code to GitHub
2. Sign up at [render.com](https://render.com)
3. Create new Web Service from your repo
4. Wait 2-3 minutes for deployment
5. Your app is live! 🎉

## 📦 Project Structure

```
wfl-team-manager/
├── app.py                  # Flask backend
├── requirements.txt        # Python dependencies
├── render.yaml            # Render deployment config
├── GameTest.db            # SQLite database
├── Pictures/              # Team logos and images
│   ├── Mustangs.png
│   ├── Umbrellas.png
│   └── ...
└── templates/
    └── index.html         # Frontend interface
```

## 🎮 Usage

### Roster Tab
Select a team to view all players organized by position with their stats (Overall, Potential) and info.

### Standings Tab
View current league standings with wins, losses, ties, and point differentials.

### Scores Tab
See all game results with home vs away matchups and final scores.

### Season Stats Tab
Filter player statistics by skill category and sort by any stat.

### WFL News Tab
View league news and updates in a Twitter-style feed.

## 🖼️ Adding Team Logos

1. Save logos as PNG files in the `Pictures/` folder
2. Name them exactly as the team name appears in the database
3. Recommended size: 200x200 to 500x500 pixels
4. Use transparent backgrounds for best results

---

Made with ⚡ Flask and 💙 for football stats
