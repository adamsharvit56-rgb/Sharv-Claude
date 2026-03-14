# Remote Control Spawn Option for Server Mode

## Overview

When running Claude Code in server mode via `claude remote-control`, the `--spawn` option controls how concurrent sessions are created when multiple remote clients connect. This determines whether sessions share the same working directory or get isolated environments.

## Spawn Modes

### `same-dir` (default)

All sessions share the current working directory.

```bash
claude remote-control --spawn same-dir
```

- Sessions operate in the same directory simultaneously
- Suitable when sessions work on different files or tasks
- **Caution:** Sessions can conflict if editing the same files concurrently

### `worktree`

Each on-demand session gets its own isolated git worktree.

```bash
claude remote-control --spawn worktree
```

- Requires a git repository as the working directory
- Each session receives a separate copy of the repo via `git worktree`
- Prevents file conflicts between concurrent sessions
- Ideal for parallel development workflows

You can toggle between `same-dir` and `worktree` at runtime by pressing `w` in the terminal.

## Usage Examples

```bash
# Start server mode with default spawn (same-dir)
claude remote-control

# Start with worktree isolation and a custom name
claude remote-control --name "My Project" --spawn worktree

# Limit concurrent sessions and enable verbose logging
claude remote-control --spawn worktree --capacity 10 --verbose

# Enable sandboxing for additional filesystem/network isolation
claude remote-control --spawn worktree --sandbox
```

## Server Mode CLI Flags

| Flag | Description |
|------|-------------|
| `--spawn <mode>` | Session creation strategy: `same-dir` (default) or `worktree` |
| `--name "title"` | Custom session title visible at claude.ai/code |
| `--capacity <N>` | Maximum concurrent sessions (default: 32) |
| `--verbose` | Show detailed connection and session logs |
| `--sandbox` | Enable filesystem and network sandboxing |
| `--no-sandbox` | Explicitly disable sandboxing (default) |

## How It Works

1. Run `claude remote-control` on your local machine — this registers the session with the Anthropic API
2. Connect from a remote client by opening the session URL, scanning the QR code (press spacebar), or finding the session at claude.ai/code
3. When a remote client connects, the spawn mode determines the session environment:
   - **same-dir**: The session runs directly in the current working directory
   - **worktree**: A new git worktree is created for the session, providing an isolated copy of the repository
4. All execution happens locally — only outbound HTTPS requests are made; no inbound ports are opened

## When to Use Each Mode

| Scenario | Recommended Mode |
|----------|-----------------|
| Single user, one session at a time | `same-dir` |
| Multiple users collaborating on separate features | `worktree` |
| CI/CD or automated pipelines | `worktree` |
| Quick ad-hoc remote access | `same-dir` |
| Parallel code reviews or experiments | `worktree` |

## Security

- All traffic routes through the Anthropic API over TLS
- Credentials are short-lived and scoped to single purposes
- No inbound ports are opened on your machine
- Optional `--sandbox` flag adds filesystem and network isolation per session
