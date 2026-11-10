#!/usr/bin/env python3
"""
MOR Entertainment - Continuous Daily EPG Generator (XMLTV)
Generates a rolling multi-day schedule based on the fixed weekday program grid.
Runs daily via GitHub Actions. Timezone: Asia/Manila (UTC+8)
"""

from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
import sys

# ============== CONFIG ==============
CHANNEL_ID = "MOR.Entertainment.ph"
CHANNEL_NAME = "MOR Entertainment"
CHANNEL_ICON = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/MOR_Entertainment_logo.png/220px-MOR_Entertainment_logo.png"
TIMEZONE = ZoneInfo("Asia/Manila")
DAYS_AHEAD = 14          # how many days of guide to generate
OUTPUT_DIR = "epg"
OUTPUT_FILE = "mor_entertainment.xml"

# Fixed daily schedule (start hour, end hour, title, description)
# Hours are in 24h local time. The last block crosses midnight.
SCHEDULE = [
    {
        "start": time(5, 0),
        "end": time(7, 0),
        "title": "Ready, Set, MORe",
        "desc": "Start your day with the best OPM and lifestyle vibes. Ready, Set, MORe!"
    },
    {
        "start": time(7, 0),
        "end": time(11, 0),
        "title": "MORe sa Umaga",
        "desc": "Morning show packed with music, conversations, and positive energy."
    },
    {
        "start": time(11, 0),
        "end": time(13, 0),
        "title": "MORe sa Tanghali",
        "desc": "Midday entertainment and the hottest tracks to keep you company."
    },
    {
        "start": time(13, 0),
        "end": time(15, 0),
        "title": "Dear MOR",
        "desc": "Drama episodes and heartfelt stories. Also streams on Thursdays & Fridays on YouTube, Spotify, and Apple Podcasts."
    },
    {
        "start": time(15, 0),
        "end": time(18, 0),
        "title": "MORe sa Hapon",
        "desc": "Afternoon drive with great music and engaging talk."
    },
    {
        "start": time(18, 0),
        "end": time(21, 0),
        "title": "MORe sa Gabi Xpress",
        "desc": "Express edition of the evening show – fast, fun, and full of hits."
    },
    {
        "start": time(21, 0),
        "end": time(0, 0),   # midnight
        "title": "MORe sa Gabi",
        "desc": "Late night vibes with the best music and chill conversations."
    },
    {
        "start": time(0, 0),
        "end": time(5, 0),
        "title": "MORe sa Magdamag",
        "desc": "Overnight programming – continuous music and company through the night."
    },
]


def fmt_xmltv(dt: datetime) -> str:
    """Format datetime to XMLTV timestamp: YYYYMMDDHHMMSS +0000"""
    # Convert to UTC for the +0000 offset (XMLTV standard practice)
    utc = dt.astimezone(ZoneInfo("UTC"))
    return utc.strftime("%Y%m%d%H%M%S +0000")


def create_channel(root: ET.Element):
    channel = ET.SubElement(root, "channel", id=CHANNEL_ID)
    display_name = ET.SubElement(channel, "display-name")
    display_name.text = CHANNEL_NAME
    # Optional icon
    if CHANNEL_ICON:
        ET.SubElement(channel, "icon", src=CHANNEL_ICON)


def add_programme(root: ET.Element, start: datetime, stop: datetime, title: str, desc: str):
    prog = ET.SubElement(
        root,
        "programme",
        start=fmt_xmltv(start),
        stop=fmt_xmltv(stop),
        channel=CHANNEL_ID,
    )
    title_el = ET.SubElement(prog, "title", lang="en")
    title_el.text = title
    desc_el = ET.SubElement(prog, "desc", lang="en")
    desc_el.text = desc
    # Category
    cat = ET.SubElement(prog, "category", lang="en")
    cat.text = "Radio"


def generate_day(root: ET.Element, day: datetime.date):
    """Generate all programmes for one calendar day (local time)."""
    for block in SCHEDULE:
        start_dt = datetime.combine(day, block["start"], tzinfo=TIMEZONE)

        if block["end"] == time(0, 0):
            # Ends at midnight → next day 00:00
            stop_dt = datetime.combine(day + timedelta(days=1), time(0, 0), tzinfo=TIMEZONE)
        else:
            stop_dt = datetime.combine(day, block["end"], tzinfo=TIMEZONE)

        # Special case: the overnight block that starts at 00:00 belongs to the current day
        # but we also need the previous day's overnight continuation already handled by the previous day.
        add_programme(root, start_dt, stop_dt, block["title"], block["desc"])


def build_epg(days: int = DAYS_AHEAD) -> str:
    root = ET.Element("tv", attrib={
        "generator-info-name": "MOR-Entertainment-EPG-Generator",
        "generator-info-url": "https://github.com/yourusername/mor-epg",
    })

    create_channel(root)

    today = datetime.now(TIMEZONE).date()
    # Start from yesterday so overnight shows are covered, then generate forward
    for i in range(-1, days):
        day = today + timedelta(days=i)
        generate_day(root, day)

    # Pretty print
    rough = ET.tostring(root, encoding="utf-8")
    reparsed = minidom.parseString(rough)
    return reparsed.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    xml_content = build_epg()
    out_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(xml_content)
    print(f"✅ Generated: {out_path}")
    print(f"   Days covered: ~{DAYS_AHEAD + 1} (incl. yesterday for overnight continuity)")
    print(f"   Channel: {CHANNEL_NAME} ({CHANNEL_ID})")
    print(f"   Timezone: Asia/Manila")


if __name__ == "__main__":
    main()
