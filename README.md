# 🏈 WFL Team Manager

A pure static web application for managing WFL team data. Runs entirely in the browser using JavaScript and SQL.js - no server required!

## ✨ Features

- 📊 **Team Rosters** - View complete player rosters with stats
- 🏆 **Standings** - Real-time team rankings
- 📈 **Season Stats** - Player statistics by skill category
- 🗞️ **WFL News** - Twitter-style news feed
- 🎨 **Team Logos** - Visual branding throughout
- 📱 **Responsive Design** - Works on all devices
- ⚡ **100% Static** - No backend server needed!

## 🚀 Quick Deploy to GitHub Pages

### Step 1: Push to GitHub

```bash
cd your-project-folder

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - WFL Team Manager"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git

# Push to GitHub
git push -u origin main
```

### Step 2: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** (top right)
3. Click **Pages** in the left sidebar
4. Under "Source", select:
   - Branch: `main`
   - Folder: `/ (root)`
5. Click **Save**
6. Wait 1-2 minutes for deployment

Your site will be live at:
```
https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/
```

That's it! 🎉

## 📦 File Structure

```
your-repo/
├── index.html          # Main application (all-in-one)
├── GameTest.db         # SQLite database
├── Pictures/           # Team logos and images
│   ├── Mustangs.png
│   ├── Umbrellas.png
│   └── ...
└── README.md
```

## 🎮 How It Works

Unlike traditional web apps, this runs **entirely in your browser**:

1. **SQL.js** - SQLite compiled to WebAssembly, runs in the browser
2. **No Backend** - Database is loaded directly as a file
3. **Static Hosting** - Works on GitHub Pages, Netlify, Vercel, or any static host
4. **Fast** - Everything runs locally in your browser

## 🔄 Updating Your Site

### Update Database
1. Replace `GameTest.db` with your new database
2. Commit and push:
```bash
git add GameTest.db
git commit -m "Update database"
git push
```
3. GitHub Pages will auto-update in 1-2 minutes

### Update Code
1. Edit `index.html`
2. Commit and push
3. Changes go live automatically

### Add/Update Team Logos
1. Add PNG files to `Pictures/` folder
2. Name them exactly as team names in database
3. Commit and push

## 🖼️ Adding Team Logos

1. Save logos as PNG files in `Pictures/` folder
2. Name them **exactly** as team names in database
   - Example: `Mustangs.png`, `Umbrellas.png`
3. Recommended: 200x200 to 500x500 pixels, transparent background

## 📝 Database Requirements

Your `GameTest.db` must have these tables:
- `Teams` - Team information
- `Players` - Player data
- `Rosters` - Team rosters
- `PlayerAttributes` - Player ratings (with `overall_let`, `potential_let` columns)
- `GameLog` - Game results
- `SeasonStats` - Player stats per game
- `NewsFeed` - News articles (with `ProfilePicture`, `Media` columns)

## 🐛 Troubleshooting

**"Database not loading"**
- Make sure `GameTest.db` is in the root of your repo
- Check browser console (F12) for errors
- Verify file was pushed to GitHub

**"Images not loading"**
- Verify files are in `Pictures/` folder (case-sensitive)
- Check file names match database values exactly
- Ensure files were committed and pushed

**"Page shows old data"**
- Clear browser cache (Ctrl+F5 or Cmd+Shift+R)
- Try incognito/private browsing mode
- Wait a few minutes for GitHub Pages to rebuild

**"Site not accessible"**
- Check GitHub Pages is enabled in Settings
- Verify branch and folder are set correctly
- Give it 2-3 minutes after first enabling

## 💡 Alternative Hosting

This works on **any** static hosting:

### Netlify
1. Drag and drop your folder to [netlify.com](https://netlify.com)
2. Site goes live instantly

### Vercel
1. Import from GitHub at [vercel.com](https://vercel.com)
2. Auto-deploys on push

### Your Own Server
Just upload all files to your web server!

## 🔧 Local Development

To test locally:

1. Start a local web server (required for CORS):
```bash
# Python 3
python -m http.server 8000

# OR Node.js
npx serve
```

2. Open browser to `http://localhost:8000`

**Note:** Can't just open `index.html` directly - browsers block loading `.db` files without a web server.

## ⚠️ Important Notes

- Database loads on page load (~1-5 MB = ~1-2 seconds)
- All processing happens in browser (private and secure)
- No data is sent to any server
- Works offline after first load (browser cache)

## 📊 Database Size Limits

- GitHub Pages: No hard limit, but keep under 100MB per file
- Recommended: Keep database under 50MB for best performance
- Larger databases take longer to load initially

## 🎯 Best Practices

1. **Compress your database** - Remove unused tables/data
2. **Optimize images** - Compress PNGs before uploading
3. **Use GitHub releases** - For versioning different seasons
4. **Branch for development** - Keep `main` branch stable

## 🆘 Need Help?

- Check browser console (F12) for errors
- Verify all files are on GitHub
- Make sure GitHub Pages is enabled
- Wait 2-3 minutes after enabling/pushing

---

Made with ⚡ by converting Python/Flask to pure JavaScript with SQL.js
