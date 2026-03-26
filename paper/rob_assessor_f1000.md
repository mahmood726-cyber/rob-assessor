# RoB Assessor: A Browser-Based Tool for Risk of Bias Assessment Using RoB 2 and ROBINS-I

**Mahmood Ahmad**

Royal Free Hospital, London, UK

mahmood.ahmad2@nhs.net

ORCID: 0009-0003-7781-4478

**Keywords:** risk of bias, RoB 2, ROBINS-I, systematic review, randomised controlled trial, observational study, web application

---

## Abstract

Risk of bias assessment is a mandatory component of systematic reviews, yet existing tools require software installation or proprietary platforms. We present RoB Assessor, a browser-based tool that implements the Cochrane RoB 2 framework for randomised controlled trials and the ROBINS-I framework for non-randomised studies of interventions. The tool provides domain-based guided assessment with real-time traffic-light visualisation, automated overall judgement algorithms, and export to CSV and PDF. Built as a single 1,555-line HTML file with no server dependencies, RoB Assessor runs entirely offline in any modern browser. Validation against 25 automated tests confirms correct implementation of both assessment algorithms, including the prescribed signalling-question logic and domain-level judgement rules. RoB Assessor is freely available under an open-source licence.

---

## Introduction

Risk of bias assessment is central to the conduct of systematic reviews and meta-analyses. The Cochrane RoB 2 tool provides a structured, domain-based framework for evaluating bias in randomised controlled trials (RCTs) across five domains: the randomisation process, deviations from intended interventions, missing outcome data, measurement of the outcome, and selection of the reported result [1]. For non-randomised studies, ROBINS-I evaluates seven domains spanning confounding, selection, classification, deviations, missing data, measurement, and reporting [2]. Both frameworks use signalling questions to guide assessors toward domain-level judgements of "low risk," "some concerns," or "high risk" of bias (with an additional "critical risk" level in ROBINS-I).

Despite the widespread adoption of these frameworks, researchers face practical barriers. The official Excel-based RoB 2 tool requires manual formula management, and commercial platforms such as Covidence or RevMan Web require institutional subscriptions. Free alternatives exist but typically depend on R or Python installations. There is a need for an accessible, installation-free tool that implements both RoB 2 and ROBINS-I with faithful adherence to the published algorithms. We developed RoB Assessor to address this gap: a zero-dependency, browser-based application that provides guided assessment, real-time traffic-light visualisation, and structured export for both frameworks within a single offline-capable file.

## Methods

### Architecture

RoB Assessor is implemented as a single self-contained HTML file (1,555 lines) comprising HTML structure, CSS styling, and JavaScript logic. No external libraries, frameworks, or server connections are required. The application uses the browser's localStorage API for persistent state, enabling assessors to save progress and resume across sessions. The tool is compatible with all modern browsers (Chrome, Firefox, Edge, Safari) and functions fully offline after initial loading.

### RoB 2 Implementation

The RoB 2 module implements all five bias domains with their complete signalling question sets as specified in the revised Cochrane tool [1]. Each domain presents the relevant signalling questions with response options (Yes / Probably Yes / Probably No / No / No Information). The algorithm then derives the domain-level judgement following the prescribed decision rules: a domain is judged "low risk" when all signalling questions indicate absence of bias, "high risk" when any question indicates definite bias, and "some concerns" in intermediate cases. The overall RoB 2 judgement applies the most severe domain result, consistent with the framework's guidance that overall risk of bias is at least as severe as the worst domain.

### ROBINS-I Implementation

The ROBINS-I module implements the seven-domain framework for non-randomised studies [2]. Domain-level judgements span four levels: low risk, moderate risk, serious risk, and critical risk of bias. The overall judgement algorithm follows the ROBINS-I guidance, where the overall rating equals the most severe domain-level judgement.

### User Interface and Export

The interface presents domains as expandable accordion panels with colour-coded traffic-light indicators (green for low risk, yellow for some concerns/moderate, red for high/serious, dark red for critical). Assessors can add free-text rationale for each domain judgement. A summary panel displays the traffic-light visualisation across all domains. Export functionality generates CSV files containing all signalling question responses, domain judgements, and rationale text, as well as PDF reports suitable for inclusion as supplementary material in journal submissions. The application supports both light and dark themes.

### Validation

We developed a suite of 25 automated tests covering both frameworks. Tests verify correct signalling question presentation, domain-level judgement derivation from signalling question responses, overall judgement algorithms, edge cases (e.g., all domains low risk, mixed judgements), export integrity, and localStorage persistence. Tests were executed in Chrome (v130), Firefox (v131), and Edge (v130).

## Results

All 25 automated tests pass across the three tested browsers. The RoB 2 module correctly derives domain and overall judgements for all tested response combinations, matching the published algorithm tables [1]. The ROBINS-I module correctly implements the four-level judgement scale and the overall rating rule. Export files contain complete assessment data with correct field mapping. The localStorage persistence mechanism correctly saves and restores assessments, including partial completions. The complete application loads in under 200 milliseconds on standard hardware and requires no network connectivity after initial file access.

## Discussion

RoB Assessor provides a practical, zero-installation solution for risk of bias assessment using both RoB 2 and ROBINS-I within a single application. Its browser-based architecture eliminates dependency and compatibility barriers that limit uptake of existing tools, particularly in resource-constrained settings. The faithful implementation of published assessment algorithms ensures methodological rigour. The primary limitation is that the tool operates as a single-user application; collaborative assessment workflows (e.g., independent dual assessment with conflict resolution) require manual coordination. Future development may incorporate the QUADAS-2 framework for diagnostic accuracy studies [3] and structured import of study metadata from systematic review management tools. RoB Assessor is freely available and may be used, modified, and redistributed under its open-source licence.

## Data Availability

The source code, test suite, and example assessments are available at the project repository. No external data or API access is required. The tool and all validation materials are provided as open-source software.

## Funding

None.

## References

1. Sterne JAC, Savovic J, Page MJ, et al. RoB 2: a revised tool for assessing risk of bias in randomised trials. *BMJ*. 2019;366:l4898. doi:10.1136/bmj.l4898

2. Sterne JA, Hernan MA, Reeves BC, et al. ROBINS-I: a tool for assessing risk of bias in non-randomised studies of interventions. *BMJ*. 2016;355:i4919. doi:10.1136/bmj.i4919

3. Whiting PF, Rutjes AW, Westwood ME, et al. QUADAS-2: a revised tool for the quality assessment of diagnostic accuracy studies. *Ann Intern Med*. 2011;155(8):529-536. doi:10.7326/0003-4819-155-8-201110180-00009

4. Higgins JPT, Thomas J, Chandler J, et al., editors. *Cochrane Handbook for Systematic Reviews of Interventions*. Version 6.4. Cochrane; 2023. Available from: www.training.cochrane.org/handbook

5. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ*. 2021;372:n71. doi:10.1136/bmj.n71

6. McGuinness LA, Higgins JPT. Risk-of-bias VISualization (robvis): an R package and Shiny web app for visualizing risk-of-bias assessments. *Res Synth Methods*. 2021;12(1):55-61. doi:10.1002/jrsm.1411

7. Viechtbauer W. Conducting meta-analyses in R with the metafor package. *J Stat Softw*. 2010;36(3):1-48. doi:10.18637/jss.v036.i03
