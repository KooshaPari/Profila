# Contributing to Profila

Thank you for your interest in contributing to Profila.

## Development Setup

```bash
# Clone the repository
git clone https://github.com/Phenotype-Enterprise/Profila
cd Profila

# Run profiler
cd profiler
./profiler.sh help
```

## Profiler Commands

| Command | Output |
|---------|--------|
| `quick` | RSS, CPU, Threads, FDs, Network |
| `full` | All system metrics |
| `network` | Connections, bandwidth |
| `disk` | I/O rates, file usage |
| `audit` | Complete system audit |
| `complexity` | Space/time analysis |
| `continuous` | Live CSV + charts |

## Making Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Make your changes
4. Test with `./profiler.sh quick codex`
5. Run full test suite
6. Commit using conventional commits
7. Push and create PR

## Metrics Tracked

### Memory
- RSS, VMS, VmPeak, VmData, VmStk, VmExe, VmLib
- Memory maps, shared/private

### CPU
- CPU %, threads, context switches
- Per-thread CPU time

### Files
- FD count, types (pipe, socket, anon)
- Open files, CWD, root

### Network
- TCP/UDP connections
- Bandwidth (rx/tx)

### Disk
- Read/write bytes
- I/O rates
