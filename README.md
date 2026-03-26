# RoB Assessor

Browser-based risk of bias assessment tool implementing the RoB 2 and ROBINS-I frameworks.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Overview

RoB Assessor provides a structured, guided workflow for assessing risk of bias in both randomized and non-randomized studies. It implements the full RoB 2 framework (5 domains, Sterne et al. 2019) for randomized controlled trials and the ROBINS-I framework (7 domains, Sterne et al. 2016) for non-randomized studies of interventions. The tool runs entirely in the browser with no server dependencies, producing publication-ready traffic light tables and weighted bar charts.

## Features

- Full RoB 2 implementation: 5 domains with signalling questions and algorithm-guided judgment suggestions
- Full ROBINS-I implementation: 7 domains (Confounding through Selection of reported result) with 4-level judgments (Low, Moderate, Serious, Critical)
- Algorithm-guided overall judgment based on domain-level responses (follows Cochrane guidance)
- Interactive domain navigator with colour-coded completion status
- Traffic light summary table for all assessed studies
- Domain-level weighted bar chart visualization
- Mixed frameworks within a single assessment (RoB 2 and ROBINS-I side by side)
- CSV batch import for adding multiple studies at once
- JSON import/export to save and restore full assessment state
- Auto-generated methods text for manuscripts
- MAIF (Meta-Analysis Interchange Format) export for cross-tool data flow
- Dark mode with WCAG-compliant contrast
- Print-optimized layout for appendices

## Quick Start

1. Download `rob-assessor.html`
2. Open in any modern browser
3. No installation, no dependencies, works offline

## Built-in Examples

No built-in datasets. Add studies individually or batch-import via CSV with format: `study_id, framework` (e.g., `Smith 2020, rob2`).

## Methods

- **RoB 2**: Randomization process, Deviations from intended interventions, Missing outcome data, Measurement of the outcome, Selection of the reported result
- **ROBINS-I**: Confounding, Selection of participants, Classification of interventions, Deviations from intended interventions, Missing data, Measurement of outcomes, Selection of the reported result
- Algorithm-guided judgment suggestions based on signalling question responses

## Screenshots

> Screenshots can be added by opening the tool and using browser screenshot.

## Validation

- 25/25 Selenium tests pass
- Domain structures and judgment algorithms cross-checked against Cochrane RoB 2 guidance (Sterne et al. 2019) and ROBINS-I tool (Sterne et al. 2016)

## Export

- CSV (study-level judgments and domain scores)
- JSON (full assessment state, restorable)
- Methods text (clipboard, manuscript-ready)
- Print-optimized summary
- MAIF (Meta-Analysis Interchange Format) for cross-tool data flow

## Citation

If you use this tool, please cite:

> Ahmad M. RoB Assessor: A browser-based risk of bias assessment tool implementing RoB 2 and ROBINS-I. 2026. Available at: https://github.com/mahmood726-cyber/rob-assessor

## Author

**Mahmood Ahmad**
Royal Free Hospital, London, United Kingdom
ORCID: [0009-0003-7781-4478](https://orcid.org/0009-0003-7781-4478)

## License

MIT
