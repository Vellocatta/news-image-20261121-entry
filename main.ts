// news-image-20261121 entry (Node 22, standard library only).
//
// The entry is the front-page image beside this file: "Saturday 21
// November 2026: 50 stories, 6 continents, one front page" — a broadsheet
// poster summing up the world news of Saturday 21 November 2026, drawn
// with PIL by gen_frontpage21.py (12 featured stories with decks, 38
// one-line briefs, lead story: missiles fall on Poland). The program
// copies entry.png to /output/entry.png, byte-identical on every run.
//
// Run locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const source = fileURLToPath(new URL('./entry.png', import.meta.url));
copyFileSync(source, join(outDir, 'entry.png'));
