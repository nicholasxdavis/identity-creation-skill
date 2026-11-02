# Attribution

Identity Creation is a Blacnova skill. It merges the former `mascot-creation`, `favicon-creation`, and `og-img-creation` skills.

| Source | What we took |
| --- | --- |
| [Pouryaak/wobnimo](https://github.com/Pouryaak/wobnimo) (MIT) | Living 3D mascot engine, character data model, `wobnimo check` / `preview` agent loop. Vendored as a Blacnova fork under `wobnimo/` (see `wobnimo/FORK.md`). Upstream author: Pouryaak. |
| [s1dashu/ip-as-logo-skill](https://github.com/s1dashu/ip-as-logo-skill) | Static IP mark workflow under `ip-logo/`: three directions, six candidates, complexity budget, shape language, prompt skeleton. Blacnova adaptations: centered professional SaaS mark, solid-bg keying, Pillow transparency (`ip-logo/scripts/make_transparent.py`). Upstream: [SKILL.md](https://github.com/s1dashu/ip-as-logo-skill/blob/main/SKILL.md). |
| Local favicon pipeline | Hyper-simplified centered mark, solid key background, multi-size ICO/PNG export (`scripts/make_favicon.py`). |
| Local OG pipeline | 1200x630 safe-zone card, Pillow text/badge/mascot composite (`scripts/create_og_image.py`). |
| Open Graph / Twitter card conventions | Standard `og:*` and `twitter:card` meta shapes used industry-wide for link previews. |

Upstream licenses stay with their authors. Blacnova owns this merged skill tree and the fork deltas documented in `wobnimo/FORK.md`.
