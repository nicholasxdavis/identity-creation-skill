---
name: ip-as-logo
description: Generate simple, cute, professional square IP character marks that are centered, project-matched, sized with balanced margins, and post-processed with Python into transparent PNGs. Use when creating a brand IP, logo-like mascot, or static character asset for a more professional techy SaaS product.
---

# IP as Logo

Adapted from [s1dashu/ip-as-logo-skill](https://github.com/s1dashu/ip-as-logo-skill). Blacnova path: centered professional SaaS mark plus transparent PNG export. See [../ATTRIBUTION.md](../ATTRIBUTION.md).

Create the simplest possible cute IP character: a compact, lovable professional symbol that stays recognizable at `32 × 32`, not a detailed illustration. Final deliverable is a **centered transparent PNG**.

## Workflow

1. Parse the request for an explicit IP subject and available product context. Do not ask the user to choose a color mode unless they explicitly want to control it.
2. When the user has not specified an IP subject and the current workspace is a product repository, inspect relevant read-only context before asking questions. Prefer the README, product docs, package or app metadata, landing-page copy, manifests, and design tokens. Treat context as sufficient when the product purpose, primary audience, and intended personality can be inferred with reasonable confidence.
3. When product context is insufficient, ask one consolidated round of background questions covering what the product does, who it serves, and how it should feel. Do not start a second background questionnaire. Continue with the best supported interpretation after the answer.
4. Once context is sufficient, always present three concise directions before generation and explicitly propose generating six independent candidates in one batch. Do not generate until the user agrees, unless the current request already explicitly authorizes six outputs or asks the agent to proceed without another confirmation.
5. Choose the three proposed directions deliberately:
   - When the user explicitly specifies an IP subject, keep that subject and propose three distinct design treatments based on silhouette treatment, secondary color region, defining feature, or personality emphasis.
   - When the user does not specify an IP subject, propose three genuinely different IP subjects or metaphors. Tie each one to a different product attribute or brand promise; do not return three arbitrary animals with no rationale.
6. Interpret the user's response exactly:
   - If the user accepts all three directions and the six-image proposal, generate two independent variants per direction and label them `A1`, `A2`, `B1`, `B2`, `C1`, and `C2`.
   - If the user selects one direction but accepts six images, generate six controlled variants of that direction and label them `A1` through `A6`.
   - If the user rejects the proposed quantity, directions, or distribution, follow the user's replacement instructions without arguing for the default.
7. Default every candidate to exactly three semantic colors in the complete image: exactly two IP base colors plus exactly one **solid** background color (for clean keying). Reuse the two IP colors for facial marks rather than introducing additional semantic colors.
8. Before generation, require a top-tier image model: prefer GPT Image 2; also support Seedance 5.0 Pro, Nano Banana Pro (Gemini Image Pro), or Nano Banana 2 (Gemini Image Flash). If none is available, ask the user to enable a suitable tool or provide its API key. Never fall back to SVG generation. Use another available image model only with the user's explicit consent.
9. If the runtime supports subagents, parallelize the six independent candidates up to the available concurrency. Give every subagent the same product brief, shared constraints, and one assigned direction or variant.
10. Abstract each subject using the complexity budget below. Generate every candidate as a separate full-resolution square asset; never ask an image model to compose a contact sheet.
11. **Quality gate (required before presenting the batch):** each candidate must be good enough and project-matched. Reject and regenerate a candidate (same label, one retry) when any of these fail:
    - Subject is not clearly related to the product metaphor / direction rationale
    - Subject is off-center, cropped oddly, or fills less than ~70% or more than ~90% of the frame
    - Detail is too busy to read at small size, or the silhouette is ambiguous
    - Background is not a flat solid color suitable for keying
    Deliver the batch only when every slot is acceptable or the single retry still fails (then deliver with a short note on the weak slot).
12. After the user picks a winner (or winners), run the Python transparent pass in [scripts/make_transparent.py](scripts/make_transparent.py). Do not skip this for final assets.
13. Preserve and label every generated solid-bg result plus each transparent output. Report label, direction, paths, prompt/color mapping, and dimensions.

When proposing directions before generation, describe each in one compact line: `<IP subject> / <product connection> / <defining silhouette>`. End with a direct proposal to generate six images.

## Complexity budget

- Build one dominant continuous outer silhouette from roughly `4-7` large basic geometric shapes.
- Use at most one species-defining feature.
- Use at most two broad internal color regions corresponding to the two IP base colors. Keep the face to two eyes and, only when needed, one tiny mouth.
- Remove repeated feathers, scales, fur tufts, armor plates, buttons, screws, numbers, labels, and other illustrative detail.
- Favor a large head, compact proportions, soft cheeks, widely spaced simple eyes, and a calm friendly professional expression.
- Require a readable black silhouette and recognizability at `32 × 32`.

## Shape language and composition

- Use thick, rounded, weighty contours and broad color masses.
- Forbid sharp corners, pointed ears or beaks, needle-like tails, thin antennae, thin smiles, narrow gaps, and acute tips.
- Show both members of paired identifying features.
- **Center the character** horizontally and vertically. Fill about `78-86%` of the canvas with balanced margins (~7-11% per side). Do not hug the edges.
- Do **not** use lower-left / corner-emergence compositions unless the user explicitly requests them.
- Keep the artwork upright; never rotate the canvas or tilt the main mark without an explicit request.

## Simplicity and visual treatment

- Start from large, clean semantic shapes and the strongest possible simple silhouette.
- Prefer fewer, larger, softer forms over extra definition.
- Keep facial marks tiny, simple, and subordinate.
- Keep the named background color visually solid and uniform, without scenery, texture, halo, vignette, or lighting variation.
- Keep the requested visual direction graphic and simple rather than clay, plush, or photorealistic.
- Lean slightly more professional than playful: calm expression, clean color blocks, no chaotic props.

## Color and canvas

- Exactly three semantic colors: two IP base colors + one solid background color.
- Choose IP colors from product context, subject identity, and personality. Organize into broad purposeful masses.
- Choose the background freely for keying contrast. Prefer a gently muted chromatic field that separates cleanly from the subject. Historical palettes are suggestions only.
- Name the intended solid background color directly in the generation prompt. Do not ask the image model for transparency, alpha, or checkerboards.
- Generate a direct `1:1` square. Request approximately `1536 × 1536`; accept native `1254 × 1254` when that is the service limit.

## Prompt skeleton

### Route constraints by generator capability

Determine the available image model and its actual tool schema from runtime metadata. Do not guess unsupported parameters.

Describe the requested visual as an image only. Never tell the image generator that the image is a `logo`, `brand mark`, `app icon`, or similar use-case label. This rule applies only to the generation prompt.

- For modern instruction-following models (GPT Image 2, Nano Banana Pro/2, Seedance 5.0 Pro), keep exclusions as the natural-language `Constraints:` line inside the main prompt.
- For older runtimes with `negative_prompt`, put exclusions there and omit the `Constraints:` line from the main prompt.

Minimal negative payload when a dedicated parameter exists:

```text
text, watermark, borders, frames, cards, presentation masks, extra subjects, scenery, thin fragile lines, sharp tips, photorealistic materials, strong three-dimensional rendering, external cast shadows, off-center composition, corner crop
```

Complete prompt for modern models:

```text
Create one complete full-bleed 1:1 square image.
Background: fill the entire square with solid <background>. Keep <background> uniform in every open area; no texture, vignette, or lighting variation.
Subject: place one extremely simplified, cute, endearing <subject> IP character on the background, reduced to one soft rounded continuous silhouette and one defining feature. The character should feel professional, calm, and brand-ready while remaining lovable.
Complexity: use only 4-7 large basic shapes and at most two broad internal color regions. Use two simple eyes and add one tiny mouth only when it helps the expression. Remove every nonessential line, outline, anatomical detail, texture, and decoration. Keep the character readable at 32 × 32.
Color behavior: use exactly three semantic colors in the complete image: exactly two IP base colors plus the background color. Choose the two IP colors from the subject and product context, organize both into broad purposeful masses, and reuse them for facial marks. Keep the IP, facial marks, and background clearly separated.
Composition: keep the character upright and perfectly centered horizontally and vertically. Fill about 78-86% of the square with even margins on all sides. Do not crop into the silhouette. Do not place the character in a corner.
Style: make simplification, cuteness, and clean professional appeal the strongest qualities. Use large soft forms, compact proportions, thick rounded contours, and an ultra-clean graphic treatment. Add an extremely subtle, almost imperceptible sense of depth through a barely-there neo-skeuomorphic treatment.
Finish: show only the character on the full-canvas solid background, with clean surfaces and normal square outer corners.
Constraints: Use no text or watermark. Add no borders, frames, cards, or presentation masks. Include one character only, with no extra subjects or scenery. Use no fragile lines, sharp tips, unnecessary outlines, tiny details, or decorative marks. Add no photorealistic material, dramatic bevel, glossy hotspot, deep occlusion, extrusion, strong three-dimensional rendering, or external cast shadow. Keep the background solid and uniform. Keep the subject centered : no corner emergence, no off-center placement.
```

## Transparent production (required)

After the user selects final candidate(s), run:

```bash
python scripts/make_transparent.py <candidate.png> -o <candidate>-transparent.png --size 1024 --fill 0.82
```

Optional flags:
- `--bg RRGGBB` when corner sampling mis-detects the key color
- `--tolerance` / `--feather` to tighten or soften the key
- `--size 512` or `2048` for alternate masters
- `--fill 0.78`-`0.86` to match the composition budget

Requirements: Python 3 + Pillow (`pip install pillow`).

The transparent PNG is the primary deliverable. Keep the solid-bg original alongside it for audit.

## Delivery behavior

- Present the solid-bg batch with labels, directions, and short project-fit notes.
- After selection, always produce the transparent centered master via the script above.
- Report: chosen label, solid path, transparent path, bg key used, output size, fill ratio.
- Generate refinements only when the user explicitly asks for another draw.
