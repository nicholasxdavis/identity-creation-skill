---
name: identity-creation
description: >-
  Create product identity assets: mascots (Wobnimo or IP logo), transparent
  favicons, and 1200x630 Open Graph social cards. Use when the user asks for a
  mascot, brand character, IP logo, favicon, site icon, apple-touch icon, OG
  image, social preview, Twitter card, or brand identity kit.
---

# Identity Creation

One skill for brand face + browser mark + social card. Pick the lane(s) the request needs. Do not invent work in unused lanes.

Absorbs the former `mascot-creation`, `favicon-creation`, and `og-img-creation` skills. Credits: [ATTRIBUTION.md](ATTRIBUTION.md).

## Lanes

| Lane | When | Spec |
| --- | --- | --- |
| **Mascot** | Product buddy, brand character, IP mark | [references/mascot.md](references/mascot.md) |
| **Favicon** | Tab icon, apple-touch, site icons | [references/favicon.md](references/favicon.md) |
| **OG image** | Link preview / social card 1200×630 | [references/og-image.md](references/og-image.md) |

If the user asks for a full identity kit, run mascot → favicon (from the mark) → OG (with mascot/plate) in that order.

## Quick router

1. Name the lane(s) and one-line rationale.
2. Read only the matching reference(s) above and follow them.
3. Use the scripts under [scripts/](scripts/) (and `ip-logo/scripts/` for IP transparency).
4. For Wobnimo: follow [wobnimo/skills/wobnimo-mascot/SKILL.md](wobnimo/skills/wobnimo-mascot/SKILL.md). Blacnova fork only; do not npm-update upstream. See [wobnimo/FORK.md](wobnimo/FORK.md).
5. For IP logo: follow [ip-logo/SKILL.md](ip-logo/SKILL.md).

## Mascot path choice (exactly one)

| Use **wobnimo** when… | Use **ip-logo** when… |
| --- | --- |
| In-app assistant, chatbot face, tool buddy | Brand IP / logo-like character for marketing |
| Living 3D animated mascot with moods | Flat, centered static transparent PNG |
| Playful product-UI energy | More professional SaaS brand feel |

Defaults: interactive app face → wobnimo. Landing / brand kit → ip-logo. If unclear, ask one short question, then commit.

## Scripts

```bash
# Favicon set from a solid-bg square
python scripts/make_favicon.py source.png -d favicon-out --fill 0.82

# OG card
python scripts/create_og_image.py --title "..." --subtitle "..." --badge "..." --brand "..." --background plate.png --mascot mascot.png -o og-image.png

# IP logo transparency (after generation)
python ip-logo/scripts/make_transparent.py source.png -o out/
```

Requirements: Python 3 + Pillow (`pip install pillow`).

## Install Wobnimo (projects)

```bash
npm install file:../.development/BlacnovaSkills/identity-creation/wobnimo/packages/wobnimo
```

## File map

| Path | Role |
| --- | --- |
| [references/mascot.md](references/mascot.md) | Mascot decision + execution pointers |
| [references/favicon.md](references/favicon.md) | Favicon workflow + HTML snippet |
| [references/og-image.md](references/og-image.md) | OG workflow + meta snippet |
| [wobnimo/](wobnimo/) | Blacnova Wobnimo fork + mascot skill |
| [ip-logo/](ip-logo/) | Professional static IP mark skill |
| [scripts/make_favicon.py](scripts/make_favicon.py) | Favicon export pipeline |
| [scripts/create_og_image.py](scripts/create_og_image.py) | OG compositor |
