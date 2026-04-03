# Profila Operational Runbooks

This directory contains operational runbooks for common Profila tasks and incidents.

## Quick Reference

### Key Metrics Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| Profiler Overhead | > 3% | > 5% |
| Memory Usage | > 400MB | > 512MB |
| Analysis Time | > 30s | > 60s |

### Common Commands

```bash
# Run all tests
pytest tests/ -v

# Run specific test suite
pytest tests/unit/ -v

# Profile a directory
./bin/profiler.sh -d ./src -o ./output

# Check system metrics
python3 bin/system_metrics.py
```

### Emergency Contacts

| Team | Contact | Escalation |
|------|---------|------------|
| Platform | #platform-support | @platform-oncall |
| Security | #security-incident | @security-leads |
| Engineering | #engineering-help | @engineering-managers |
