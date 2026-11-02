# Mascot lane

Pick **exactly one** path. Never run both in the same request.

## Decision

| Use **wobnimo** when… | Use **ip-logo** when… |
| --- | --- |
| In-app assistant, chatbot face, tool buddy, workspace companion | Brand IP / logo-like character mark for marketing or identity |
| Living 3D animated mascot with moods (thinking, working, celebrating…) | Flat, centered graphic character meant as a static brand asset |
| More playful, tool-based, product-UI energy | More professional, polished SaaS brand feel |
| Needs to be wired into the app as an interactive component | Needs transparent PNG / composable brand art |

**Defaults when ambiguous**
- Interactive product UI, AI tool, or "give the app a face" → **wobnimo**
- Landing, brand kit, logo-adjacent, or "professional mascot/IP" → **ip-logo**
- If still unclear, ask one short clarifying question, then commit to a single path

## Execute

1. State the chosen path and a one-line rationale.
2. Read and follow **only** that skill:
   - **wobnimo** → [../wobnimo/skills/wobnimo-mascot/SKILL.md](../wobnimo/skills/wobnimo-mascot/SKILL.md) (Blacnova fork; do not npm-update upstream)
   - **ip-logo** → [../ip-logo/SKILL.md](../ip-logo/SKILL.md)
3. Do not generate assets, scaffolds, or check passes from the unused path.
4. If the user later explicitly switches paths, stop the old path and start the new one cleanly.
5. For wobnimo marketing embeds: transparent canvas, `framing` >= 1.35, no white plate behind the host.
6. Performance: ship a static WebP fallback as LCP. Idle-load or click-to-boot `wobnimo/element` so the ~engine chunk does not block first paint.
