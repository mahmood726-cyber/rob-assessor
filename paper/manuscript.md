# RoB Assessor: An Open-Source, Browser-Based Tool for Risk of Bias Assessment Using RoB 2 and ROBINS-I Frameworks

Mahmood Ahmad^1^

^1^ Royal Free Hospital, London, United Kingdom

Correspondence: Mahmood Ahmad, mahmood.ahmad2@nhs.net
ORCID: 0009-0003-7781-4478

---

## Abstract

**Background:** Risk of bias assessment is a cornerstone of systematic review methodology, yet existing tools for conducting these assessments have significant limitations. RevMan requires desktop installation and a Cochrane account, the robvis R package is limited to visualization of completed assessments, and no widely available tool integrates both the RoB 2 and ROBINS-I frameworks with algorithm-guided domain judgment suggestions. We developed RoB Assessor, an open-source, browser-based application that supports the complete risk of bias assessment workflow without requiring installation, registration, or network connectivity.

**Methods:** RoB Assessor is implemented as a single-file HTML application using standard web technologies (HTML5, CSS3, JavaScript). It incorporates the full RoB 2 framework (5 domains, 21 signaling questions) per Sterne et al. (2019) and the ROBINS-I framework (7 domains, 26 signaling questions) per Sterne et al. (2016). The tool provides algorithm-guided judgment suggestions derived from signaling question responses, automated overall risk of bias determination using the worst-domain rule, traffic light and weighted bar chart visualizations, data export in CSV and JSON formats, and auto-generated methods text for manuscripts.

**Results:** We demonstrate the tool through a worked example assessing a hypothetical randomized trial and a non-randomized study. The algorithm-guided suggestions correctly map signaling question response patterns to domain-level judgments consistent with published guidance. The traffic light table and stacked bar chart reproduce the standard visual formats recommended by the Cochrane Handbook. Assessment data persist across sessions via browser localStorage and can be exported for integration into systematic review workflows.

**Conclusions:** RoB Assessor provides an accessible, free, and fully offline-capable tool for structured risk of bias assessment. By integrating both major risk of bias frameworks with guided judgments and publication-ready visualizations in a single portable file, it lowers barriers to rigorous bias assessment, particularly for researchers in resource-limited settings or those without institutional access to commercial software.

**Keywords:** risk of bias, systematic review, RoB 2, ROBINS-I, open-source software, meta-analysis, web application

---

## Background

Risk of bias assessment is a fundamental step in systematic reviews and meta-analyses, directly influencing the certainty of evidence and the reliability of pooled effect estimates [1]. The Cochrane Handbook for Systematic Reviews of Interventions recommends that all included studies be evaluated for risk of bias using validated, domain-based tools [2]. For randomized controlled trials, the revised Cochrane risk of bias tool (RoB 2) provides a structured framework comprising five bias domains, each assessed through signaling questions that guide evaluators toward a domain-level judgment [3]. For non-randomized studies of interventions, the ROBINS-I tool offers a parallel structure with seven domains and corresponding signaling questions [4].

Despite this importance, the landscape of available software tools presents notable gaps. Review Manager (RevMan) includes built-in risk of bias functionality but requires desktop installation or a Cochrane account, and its bias module is tightly coupled to the broader review management workflow [2]. The robvis R package generates publication-quality traffic light plots and weighted bar charts but operates exclusively on pre-existing judgment data and requires R literacy [5]. ROB-MEN integrates bias assessment with network meta-analysis but is specialized for that context and does not support ROBINS-I [6]. No widely available tool integrates both frameworks with algorithm-guided judgment suggestions in a zero-installation package.

Many systematic review teams, particularly in low- and middle-income countries, lack institutional access to commercial platforms or the infrastructure to install desktop software. We developed RoB Assessor to address these gaps: a free, open-source, browser-based application that integrates both RoB 2 and ROBINS-I with guided judgments, standard visualizations, and multiple export formats, all within a single HTML file running entirely in the user's browser.

## Implementation

### Architecture and design principles

RoB Assessor is implemented as a single self-contained HTML file (approximately 1,460 lines) comprising HTML structure, CSS styling, and JavaScript logic. This architecture was chosen deliberately: a single file can be downloaded once and opened in any modern web browser without a build step, package manager, server, or internet connection. The entire application runs client-side; no data are transmitted to any external server. Assessment data persist locally via the browser's localStorage API, ensuring that work is preserved across sessions on the same device.

The application follows a four-panel tabbed interface: (1) Studies, for adding and managing the list of studies under assessment; (2) Assess, for conducting domain-by-domain assessment with signaling questions; (3) Summary, for viewing traffic light tables and weighted bar charts; and (4) Export, for downloading assessment data and generating methods text. All interactive elements support keyboard navigation and appropriate ARIA attributes to ensure accessibility.

### Framework implementation

#### RoB 2 (randomized trials)

The RoB 2 implementation follows Sterne et al. (2019) [3]. Five domains are assessed---randomization process (3 signaling questions), deviations from intended interventions (6 questions), missing outcome data (4 questions), measurement of the outcome (5 questions), and selection of the reported result (3 questions)---totaling 21 signaling questions. Each question accepts one of five responses: "Yes," "Probably yes," "Probably no," "No," or "No information." Domain-level judgments are "Low risk of bias," "Some concerns," or "High risk of bias."

#### ROBINS-I (non-randomized studies)

The ROBINS-I implementation follows Sterne et al. (2016) [4]. Seven domains are assessed---confounding (4 questions), selection of participants (3), classification of interventions (3), deviations from intended interventions (5), missing data (4), measurement of outcomes (4), and selection of the reported result (3)---totaling 26 signaling questions. Domain-level judgments follow the ROBINS-I scale: "Low," "Moderate," "Serious," "Critical," or "No information."

### Algorithm-guided judgment suggestions

A distinguishing feature of RoB Assessor is the provision of algorithm-guided judgment suggestions. As the assessor responds to signaling questions within a domain, the tool applies decision rules derived from the published RoB 2 guidance to suggest an appropriate domain-level judgment. For RoB 2, domain-specific algorithms are implemented. For example, in Domain 1 (randomization process), if responses to questions 1.1 and 1.2 indicate that randomization was adequate and concealed, and question 1.3 indicates no problematic baseline differences, the algorithm suggests "Low risk of bias." Conversely, if either randomization or concealment is judged inadequate, the algorithm suggests "High risk of bias."

For ROBINS-I, a conservative heuristic is applied: if all signaling questions within a domain receive favorable responses ("No" or "Probably no" to questions about bias-inducing features), the suggestion is "Low"; one affirmative response ("Yes" or "Probably yes") triggers a "Moderate" suggestion; two or more affirmative responses trigger a "Serious" suggestion. These suggestions are displayed as non-binding badges beneath the judgment selection interface, clearly marked as algorithmic suggestions. The assessor retains full authority to override the suggestion based on their substantive expertise, and a free-text rationale field accompanies each domain for documenting the basis of the judgment.

### Overall risk of bias determination

The overall risk of bias for each study is computed automatically as the worst (most severe) domain-level judgment, consistent with the approach recommended by Sterne et al. (2019) for RoB 2 and by the Cochrane Handbook [2, 3]. For RoB 2, the hierarchy is Low < Some concerns < High. For ROBINS-I, the hierarchy is Low < Moderate < Serious < Critical < No information. The overall judgment is displayed in real time and updates as domain-level judgments are entered.

### Visualization

RoB Assessor generates two standard summary visualizations directly within the browser:

1. **Traffic light table.** Each row represents a study and each column a bias domain, with colored circles indicating the domain-level judgment (green for low risk, amber for some concerns or moderate risk, red for high or serious risk, dark red for critical risk, and gray for no information). An overall column summarizes the study-level judgment. Studies assessed under RoB 2 and ROBINS-I are grouped separately with appropriate column headers.

2. **Weighted bar chart (stacked horizontal bars).** Each bar represents a domain, with segments proportional to the number of studies receiving each judgment level. An overall bar summarizes the distribution of study-level judgments. This format corresponds to the "weighted bar plot" output of the robvis package [5] and the recommended summary figure in the Cochrane Handbook [2].

Both visualizations are rendered using pure HTML and CSS without external charting libraries, ensuring zero external dependencies and consistent rendering across browsers.

### Data management and export

Assessment data are automatically saved to localStorage after every action. The tool supports CSV export (with formula injection prevention), JSON export, JSON and CSV import for data transfer, auto-generated methods text for manuscripts (including framework citations, domain enumerations, and judgment distributions), and a print-optimized layout.

### Additional features

The tool includes dark mode with persistent preference, responsive design that adapts from desktop to tablet viewports, and accessibility support via ARIA roles, keyboard navigation, screen-reader labels, and a `prefers-reduced-motion` media query.

## Results and use case

### Worked example: assessing a randomized trial with RoB 2

To illustrate the assessment workflow, consider a hypothetical double-blind, placebo-controlled trial ("Smith 2023") evaluating a new antihypertensive agent. The assessor adds the study in the Studies panel, selects "RoB 2 (Randomized Trials)" as the framework, and navigates to the Assess panel.

**Domain 1 (Randomization process).** The assessor selects "Yes" for question 1.1 (allocation sequence was random, as the trial used computer-generated random numbers), "Yes" for question 1.2 (concealment via central telephone randomization), and "No" for question 1.3 (no baseline differences suggesting problems). The algorithm-guided suggestion displays "Low," and the assessor confirms this judgment.

**Domain 2 (Deviations from intended interventions).** The trial was double-blind; the assessor selects "No" for questions 2.1 and 2.2 (participants and carers unaware). Intention-to-treat analysis was used (question 2.5: "Yes"). The suggestion is "Low."

**Domain 3 (Missing outcome data).** Outcome data were available for 96% of participants (question 3.1: "Yes"). The suggestion is "Low."

**Domain 4 (Measurement of the outcome).** Blood pressure was measured using a validated automated device (question 4.1: "No," the method was not inappropriate). Assessors were blinded (question 4.3: "No"). The suggestion is "Low."

**Domain 5 (Selection of the reported result).** The primary outcome was pre-specified in the protocol registration (question 5.1: "Yes"), and there is no evidence of selective reporting (questions 5.2 and 5.3: "No"). The suggestion is "Low."

The overall judgment is automatically computed as "Low risk of bias," reflecting that no domain raised concerns. Had any single domain been judged as "Some concerns" or "High," the overall judgment would have escalated accordingly.

### Worked example: assessing a non-randomized study with ROBINS-I

For a hypothetical cohort study ("Garcia 2022") comparing surgical versus medical management of aortic stenosis, the assessor selects the ROBINS-I framework. The seven-domain assessment proceeds analogously, with the algorithm providing conservative suggestions based on signaling question patterns. If the confounding domain (Domain 1) receives a "Serious" judgment due to uncontrolled confounders, and all other domains are "Low," the overall judgment is automatically set to "Serious risk of bias."

### Summary outputs

After completing assessments for multiple studies, the Summary panel displays the traffic light table and weighted bar chart. The Export panel allows the assessor to download the complete dataset and copy a pre-formatted methods paragraph referencing the frameworks used, the number of studies assessed under each, and the distribution of overall judgments.

## Comparison with existing tools

Table 1 compares RoB Assessor with three established tools used in risk of bias assessment and visualization.

| Feature | RevMan (5/Web) | robvis (R) | ROB-MEN | **RoB Assessor** |
|---|---|---|---|---|
| RoB 2 support | Yes | Visualization only | Yes (NMA context) | **Yes** |
| ROBINS-I support | Yes | Visualization only | No | **Yes** |
| Signaling questions | Yes | No | Partial | **Yes (full set)** |
| Guided judgment suggestions | No | No | No | **Yes** |
| Traffic light table | Yes | Yes | Yes | **Yes** |
| Weighted bar chart | No | Yes | No | **Yes** |
| Auto-generated methods text | No | No | No | **Yes** |
| Installation required | Desktop/browser | R + packages | Stata | **None** |
| Offline capable | Desktop only | Yes (local R) | Yes (local Stata) | **Yes (any browser)** |
| Open source | No | Yes | No | **Yes** |
| Registration/account | Cochrane account | None | None | **None** |
| Data export (CSV/JSON) | Limited | CSV | Stata format | **CSV + JSON** |
| Cost | Free (Cochrane) | Free | Stata license | **Free** |

RoB Assessor is the only tool in this comparison that combines full signaling question sets for both frameworks, algorithm-guided suggestions, standard visualizations, and multiple export formats in a zero-installation, fully offline-capable package.

## Discussion

### Strengths and scope

RoB Assessor fills a specific gap: the need for a portable tool supporting the complete assessment workflow from signaling questions to summary visualizations. Its single-file architecture eliminates barriers related to installation, licensing, and technical prerequisites. The tool is suited for standalone assessment by review teams, teaching contexts, resource-limited settings, and rapid or scoping reviews. The algorithm-guided suggestions help novice assessors understand the mapping between signaling question responses and domain-level judgments, potentially improving inter-rater consistency.

### Limitations

The ROBINS-I judgment suggestions employ a simplified conservative heuristic rather than the full published decision tree. The tool does not support RoB 1, QUADAS-2, or other specialized instruments. localStorage persistence is device- and browser-specific, though JSON export enables manual transfer. The visualizations do not currently include forest-plot-with-bias figures or exportable image formats.

### Future development

Planned enhancements include QUADAS-2 and Newcastle-Ottawa Scale support, SVG export of visualizations, multi-user collaboration via shared JSON, and inter-rater reliability calculation for paired assessments.

## Availability and requirements

- **Project name:** RoB Assessor
- **Project home page:** https://github.com/mahmood726-cyber/rob-assessor
- **Archived version:** [TO BE DEPOSITED]
- **Operating system(s):** Platform-independent (any modern web browser)
- **Programming language:** HTML5, CSS3, JavaScript (ES5+)
- **Other requirements:** Any modern web browser (Chrome, Firefox, Safari, Edge)
- **License:** MIT
- **Any restrictions to use by non-academics:** None

The tool is distributed as a single HTML file that can be downloaded and opened locally. No server, build tools, package managers, or internet connection are required after the initial download. The source code is available under an open-source license at https://github.com/mahmood726-cyber/rob-assessor.

## Abbreviations

- ARIA: Accessible Rich Internet Applications
- CSS: Cascading Style Sheets
- CSV: Comma-Separated Values
- HTML: HyperText Markup Language
- JSON: JavaScript Object Notation
- NMA: Network meta-analysis
- QUADAS-2: Quality Assessment of Diagnostic Accuracy Studies, version 2
- RCT: Randomized controlled trial
- RoB: Risk of bias
- RoB 2: Revised Cochrane risk of bias tool for randomized trials
- ROBINS-I: Risk Of Bias In Non-randomized Studies of Interventions
- SVG: Scalable Vector Graphics

## Declarations

### Ethics approval and consent to participate

Not applicable.

### Consent for publication

Not applicable.

### Availability of data and materials

The application source code and example datasets are available at https://github.com/mahmood726-cyber/rob-assessor. An archived version is deposited at [TO BE DEPOSITED].

### Competing interests

The author declares no competing interests.

### Funding

No external funding.

### Authors' contributions

MA conceived, designed, implemented, tested, and wrote the manuscript.

### Acknowledgements

None.

## References

1. Page MJ, McKenzie JE, Bossuyt PM, Boutron I, Hoffmann TC, Mulrow CD, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ. 2021;372:n71. doi:10.1136/bmj.n71.

2. Higgins JPT, Thomas J, Chandler J, Cumpston M, Li T, Page MJ, Welch VA, editors. Cochrane Handbook for Systematic Reviews of Interventions version 6.3 (updated February 2022). Cochrane, 2022. Available from: www.training.cochrane.org/handbook.

3. Sterne JAC, Savovic J, Page MJ, Elbers RG, Blencowe NS, Boutron I, et al. RoB 2: a revised tool for assessing risk of bias in randomised trials. BMJ. 2019;366:l4898. doi:10.1136/bmj.l4898.

4. Sterne JA, Hernan MA, Reeves BC, Savovic J, Berkman ND, Viswanathan M, et al. ROBINS-I: a tool for assessing risk of bias in non-randomised studies of interventions. BMJ. 2016;355:i4919. doi:10.1136/bmj.i4919.

5. McGuinness LA, Higgins JPT. Risk-of-bias VISualization (robvis): An R package and Shiny web app for visualizing risk-of-bias assessments. Research Synthesis Methods. 2021;12(1):55-61. doi:10.1002/jrsm.1411.

6. Papakonstantinou T, Nikolakopoulou A, Higgins JPT, Egger M, Salanti G. ROB-MEN: a tool to assess risk of bias due to missing evidence in network meta-analysis. BMC Medicine. 2022;20:363. doi:10.1186/s12916-022-02536-x.
