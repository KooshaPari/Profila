# PII Handling Policy

**Version:** 1.0.0  
**Last Updated:** 2026-04-02

## Overview

This document outlines how Profila handles Personally Identifiable Information (PII) to ensure compliance with data protection regulations.

## Data Classification

| Classification | Examples | Handling |
|---------------|----------|----------|
| Public | Code metrics, function names | No restrictions |
| Internal | File paths, project names | Standard handling |
| Confidential | Author names, email addresses | Anonymized in output |
| Restricted | API keys, passwords | Never stored |

## Anonymization

Profila automatically anonymizes the following:

- **Git Author Information**: Names and emails are hashed
- **File Paths**: Directories may be anonymized (e.g., `/home/user` → `/user`)
- **Function Names**: Complex function names can be replaced with generic identifiers

## Implementation

The `pii_anonymizer.py` module provides:

```python
from src.profila.pii_anonymizer import anonymize_report

# Anonymize a report before sharing
safe_report = anonymize_report(report, level='standard')
```

## Data Retention

- Profiler output files are not automatically stored
- No data is transmitted to external services
- Temporary files are cleaned up after execution

## Compliance

Profila is designed to be compliant with:
- GDPR (General Data Protection Regulation)
- CCPA (California Consumer Privacy Act)
- SOC 2 Type II requirements
