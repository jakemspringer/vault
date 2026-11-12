---
name: Vault
description: A white financial workspace with open accounting figures and green data ink.
colors:
  primary: "#246354"
  income: "#246354"
  spending: "#A8C2B5"
  ink: "#172F27"
  muted: "#53675D"
  background: "#FFFFFF"
  pale: "#F3F7F4"
  rule: "#C9D6CD"
typography:
  headline:
    fontFamily: "Arial, Helvetica, sans-serif"
    fontSize: "2.75rem"
    fontWeight: 500
    lineHeight: 1.12
    letterSpacing: "-0.035em"
  title:
    fontFamily: "Arial, Helvetica, sans-serif"
    fontSize: "1.4rem"
    fontWeight: 500
    lineHeight: 1.3
  body:
    fontFamily: "Arial, Helvetica, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
  figures:
    fontFamily: "Arial, Helvetica, sans-serif"
    fontSize: "2.5rem"
    fontWeight: 500
    lineHeight: 1.15
    letterSpacing: "-0.035em"
rounded:
  control: "5px"
spacing:
  small: "0.5rem"
  medium: "1rem"
  section: "1.5rem"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.background}"
    rounded: "{rounded.control}"
    padding: "0.5rem 1.125rem"
    height: "44px"
  button-secondary:
    backgroundColor: "{colors.background}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "0.5rem 1.125rem"
    height: "44px"
---

# Design System: Vault

## Overview

**Creative North Star: "The financial report"**

A white financial workspace with clear figures, restrained green data ink, and flat surfaces. The user selected this direction through the visual design page, replacing the original dark glass-card layout.

**Key Characteristics:**
- White surfaces with deep green text and fine separating rules.
- Unboxed summary figures with shared alignment.
- Familiar controls and functional data graphics.

## Colors

Primary green carries actions and income. Sage distinguishes spending. Ink and muted green support readable text; pale surfaces distinguish controls and code hints. White is the user-requested ground.

**The Data Ink Rule.** Use color to distinguish data or state. Financial labels remain explicit.

## Typography

Arial with Helvetica and sans-serif fallbacks is used throughout. Financial amounts use tabular numerals. The headline is larger than section titles; summary figures remain aligned across columns. On mobile, headline and summary sizes reduce to fit.

**The Number Alignment Rule.** Right-align amounts in category lists and use tabular figures.

## Layout

The desktop content container is at most 1280px wide, with horizontal padding of 3.5rem. The summary has three open columns separated by fine rules. The overview uses a 1.85:1 chart-to-category split.

At 900px, horizontal padding becomes 1.5rem. At 640px, it becomes 1rem; totals stay in a compact three-column strip and Streamlit stacks the content columns. Top padding accounts for Streamlit's fixed toolbar. Data tables may scroll within their container.

## Elevation & Depth

Surfaces are flat. Borders and whitespace establish separation; no glass, ornamental blur, or decorative shadows are used.

## Shapes

Controls have gently squared corners using the control radius. Data bars use small rounding. Summary figures are not enclosed in independent cards.

## Components

### Buttons

Primary sign-in uses green with white text; hover deepens the green. Secondary actions use white surfaces, green text, and a fine border. Controls have a minimum 44px height, a visible offset focus outline, and a 160ms ease-out state transition.

### Inputs

Fields use a pale or white surface, fine green-gray borders, persistent labels, and a visible focus outline. Password visibility is the native Streamlit control.

### Accounting summary

Three equal columns show total income, spending, and net income. Labels sit above the figures. Secondary explanations are omitted at the small-screen breakpoint to preserve numeric legibility.

### Data presentation

Monthly data uses paired green and sage bars, labeled month and dollar axes, and unified hover values. Axis space is explicitly reserved. An expandable table offers exact monthly figures, formatted to cents. Category rows pair names with right-aligned totals and a proportional green bar.

### Feedback

Login identifies missing credentials and unrecognized credentials. API failures provide a retry action. Expired sessions explain the return to login. Empty results explain the absence of activity. Sample-data status appears before and after login.

## Do's and Don'ts

### Do:
- Do keep backgrounds white, labels explicit, and financial figures aligned.
- Do show the actual reporting period.
- Do preserve native keyboard and form behavior.
- Do inspect charts at desktop and mobile widths.

### Don't:
- Don't reintroduce dark glass panels or equal rounded cards as the page structure.
- Don't use effects or invented financial claims as decoration.
- Don't imply sample records are a visitor's real finances.
