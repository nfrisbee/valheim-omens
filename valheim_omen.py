#!/usr/bin/env python3
"""
Valheim Daily Omen — posts a random Hugin-style omen to a Discord channel
via a webhook. Meant to be run once a day (e.g. by a GitHub Actions cron
job or a system cron job).

Setup:
    1. In Discord: channel Settings -> Integrations -> Webhooks -> New Webhook.
       Copy the Webhook URL.
    2. Set it as the environment variable DISCORD_WEBHOOK_URL.
    3. pip install requests
    4. python valheim_omen.py
"""

import os
import random
import sys
from datetime import date

import requests

OMENS = [
    "The wind carries the scent of iron and blood. A great battle looms.",
    "Hugin circles low tonight. Something ancient stirs beneath the roots.",
    "The mistlands whisper your name. Do not answer.",
    "A raven was seen flying backwards over the village at dawn — turn back if you sail west.",
    "The boar-herds have gone silent. Silence before the storm.",
    "Frost clings to the longhouse door though it is not yet winter. Beware the deep woods.",
    "Your hammer rang true in a dream — Odin favors the builder today.",
    "The sea was calm, then it wasn't. Trust no calm water this week.",
    "A wolf howled thrice at the new moon. Thrice means the dead are restless.",
    "The forge sparked green last night. Someone nearby is being watched by unseen eyes.",
    "Crows gathered on the palisade and would not scatter. A guest arrives, welcome or not.",
    "The troll's roar echoed twice from two different valleys. It is not the same troll.",
    "Your shield arm itched before sunrise — an old omen for a coming skirmish.",
    "The stars over the Black Forest dimmed for a heartbeat. Something passed between worlds.",
    "A single antler was found at your door, unbroken. Fortune favors the hunt today.",
    "The mead soured in its barrel overnight. Do not trust today's bargains.",
    "Hugin dropped a black feather on the roof. Sharpen your axe before you sleep.",
    "The bog grew quiet where it should croak and creak. Something large moves beneath.",
    "A ring of mushrooms grew overnight by the well. Do not drink from it until moonrise.",
    "The ashlands glow brighter than usual tonight — the dead are near.",
    "Your compass needle trembled toward no true direction. The way forward is uncertain.",
    "Two moons were seen reflected in the fjord. A choice made today will echo twice.",
    "The wind shifted three times before noon. Odin cannot decide your fate today — so decide it yourself.",
    "A stag crossed your path and did not flee. Peace is offered; do not waste it.",
    "The runestones near the burial mound hummed at dusk. Old knowledge wants to be found.",
    "Smoke rose straight up with no wind to bend it. The gods are watching closely today.",
    "A serpent's shadow crossed the sun at midday. The deep sea holds a grudge.",
    "The dogs of the village barked at nothing, then fell silent together. Trust their fear.",
    "Your dreams were full of gold and empty of faces. Wealth comes, but alone.",
    "Lightning struck the sea with no storm in sight. Njord is displeased with someone's voyage.",
]

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")


def build_payload(omen: str) -> dict:
    return {
        "username": "Hugin",
        "embeds": [
            {
                "title": "🐦 Today's Omen",
                "description": omen,
                "color": 0x2E3B2E,
                "footer": {"text": date.today().strftime("%A, %B %d, %Y")},
            }
        ],
    }


def main() -> int:
    if not WEBHOOK_URL:
        print("ERROR: DISCORD_WEBHOOK_URL environment variable is not set.", file=sys.stderr)
        return 1

    omen = random.choice(OMENS)
    payload = build_payload(omen)

    response = requests.post(WEBHOOK_URL, json=payload, timeout=15)
    if response.status_code not in (200, 204):
        print(f"ERROR: Discord returned {response.status_code}: {response.text}", file=sys.stderr)
        return 1

    print(f"Posted omen: {omen}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
