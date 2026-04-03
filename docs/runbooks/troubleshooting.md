# Troubleshooting Runbook

Common issues and their resolutions.

## Installation Issues

### Problem: ImportError for psutil

**Symptoms:**
```
ImportError: No module named 'psutil'
```

**Resolution:**
```bash
pip install psutil
pip install -e ".[dev]"
```

### Problem: Permission denied on scripts

**Symptoms:**
```
bash: ./bin/profiler.sh: Permission denied
```

**Resolution:**
```bash
chmod +x bin/*.sh
bash bin/profiler.sh
```

## Runtime Issues

### Problem: High CPU overhead during profiling

**Resolution:**
1. Reduce sampling rate: `PROFILA_SAMPLE_RATE=500 ./bin/profiler.sh`
2. Exclude large directories: `./bin/complexity_analyzer.py -d ./src --exclude ./src/vendor`

### Problem: Out of memory during analysis

**Resolution:**
1. Process files in batches
2. Monitor memory: `python3 bin/system_metrics.py --watch 1`

## Escalation

If issues persist after following this runbook:

1. Document the issue with full error message and steps to reproduce
2. Create GitHub issue with `bug` label
3. Escalate to #engineering-help if urgent
