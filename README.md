# MOR Entertainment – Auto Daily EPG (XMLTV)

Continuous 24/7 Electronic Program Guide for **MOR Entertainment** (ABS-CBN online radio).

Based on the official weekday program grid, generated every day automatically via GitHub Actions.

## Program Schedule (Asia/Manila)

| Time              | Show                  |
|-------------------|-----------------------|
| 5:00 AM – 7:00 AM | Ready, Set, MORe      |
| 7:00 AM – 11:00 AM| MORe sa Umaga         |
| 11:00 AM – 1:00 PM| MORe sa Tanghali      |
| 1:00 PM – 3:00 PM | Dear MOR              |
| 3:00 PM – 6:00 PM | MORe sa Hapon         |
| 6:00 PM – 9:00 PM | MORe sa Gabi Xpress   |
| 9:00 PM – 12:00 AM| MORe sa Gabi          |
| 12:00 AM – 5:00 AM| MORe sa Magdamag      |

> The same schedule runs **every day** (weekdays & weekends) without interruption.

## Quick Start (use the generated EPG)

After you push this repo and the first workflow run finishes, you can use:

```
https://github.com/<your-username>/mor-epg/releases/download/latest/mor_entertainment.xml
```

Or the raw file on the main branch:

```
https://raw.githubusercontent.com/<your-username>/mor-epg/main/epg/mor_entertainment.xml
```

Paste either URL into any IPTV player / XMLTV-compatible app (TiviMate, IPTV Smarters, VLC, Kodi, etc.).

## How it works

1. `scripts/generate_epg.py` builds a clean XMLTV file covering the previous day + next 14 days.
2. GitHub Actions runs every day at **00:15 Asia/Manila**.
3. The workflow:
   - Regenerates the XML
   - Commits it back to the repo
   - Uploads it as a workflow artifact
   - Publishes/updates a GitHub Release tagged `latest` so you always have a stable download URL

## Setup on your own GitHub account

1. Create a new repository (public or private).
2. Upload all files from this zip (or clone & push).
3. Go to **Settings → Actions → General** and make sure “Read and write permissions” is enabled for workflows (or leave the default and the commit step will just be skipped).
4. Go to the **Actions** tab and run the workflow manually once (“Generate MOR Entertainment EPG” → Run workflow).
5. After it succeeds, the `epg/mor_entertainment.xml` file and the `latest` release will be ready.

## Local generation

```bash
python scripts/generate_epg.py
# → creates epg/mor_entertainment.xml
```

## Customization

Edit `scripts/generate_epg.py`:

- Change `DAYS_AHEAD` (default 14)
- Modify titles / descriptions
- Change `CHANNEL_ID` / `CHANNEL_NAME` / icon URL
- Add more channels later if needed

## License

Free to use. Not officially affiliated with ABS-CBN / MOR Entertainment.
