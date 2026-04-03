# Profila Architecture Overview

## System Context

```mermaid
graph TB
    subgraph "Developer Workflow"
        A[Developer] -->|triggers| B[CI/CD Pipeline]
        A -->|runs locally| C[Profila CLI]
    end
    
    subgraph "Profila Core"
        C --> D[Complexity Analyzer]
        C --> E[Continuous Profiler]
        C --> F[System Metrics]
        C --> G[Chart Generator]
    end
    
    subgraph "Outputs"
        D --> H[JSON/CSV Reports]
        E --> H
        F --> H
        G --> I[Visualizations]
        H --> J[Audit Dashboard]
    end
```

## Component Architecture

```mermaid
graph LR
    subgraph "Data Collection Layer"
        A[complexity_analyzer.py]
        B[continuous_profiler.py]
        C[system_metrics.py]
        D[all_metrics.sh]
    end
    
    subgraph "Processing Layer"
        E[Data Aggregator]
        F[Threshold Checker]
    end
    
    subgraph "Output Layer"
        G[generate_charts.py]
        H[JSON Exporter]
        I[CI Reporter]
    end
    
    A --> E
    B --> E
    C --> E
    D --> E
    E --> F
    F --> G
    F --> H
    F --> I
```

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Language | Python 3.11 | Core profiling logic |
| AST Parsing | stdlib `ast` | Code complexity analysis |
| System Metrics | `psutil` | Cross-platform metrics |
| Visualization | `matplotlib` | Chart generation |
| CLI | `argparse` | Command-line interface |
| CI Integration | GitHub Actions | Automated execution |
| Testing | `pytest` | Unit/integration tests |

## Security Considerations

- No network connections required (offline capable)
- No code execution during analysis (AST only)
- Temporary files cleaned up after execution
- No sensitive data in generated reports
