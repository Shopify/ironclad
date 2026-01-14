# Server Management Scripts

These scripts provide robust server lifecycle management with automatic cleanup to prevent orphaned processes and stale bytecode cache issues.

## Problem Solved

Previously, the server would leave orphaned processes running in the background, causing:
- Old code to continue running even after source changes
- Python bytecode cache (`.pyc` files) loading outdated code
- Multiple server instances competing for port 8000
- No way to track which process is the "current" server

## Scripts

### `start_server.sh`
**Usage:** `./scripts/start_server.sh`

Starts the Ironclad MCP server with automatic cleanup:
1. ✅ Kills any existing server processes (from PID file and orphaned processes)
2. ✅ Clears Python bytecode cache (`__pycache__`)
3. ✅ Validates environment (checks for service-account-key.json)
4. ✅ Sets required environment variables
5. ✅ Starts the server and saves its PID
6. ✅ Performs health check to confirm startup

**Output:**
```bash
🔧 Ironclad MCP Server Startup
Project: /Users/grantjackman/Documents/Ironclad-mcp
Log: /tmp/ironclad-mcp.log

Step 1: Checking for existing server processes...
  ✓ No old processes found

Step 2: Clearing Python bytecode cache...
  ✓ Cache cleared

Step 3: Validating environment...
  ✓ Service account key exists

Step 4: Setting environment variables...
  ✓ Environment configured

Step 5: Starting server...
✅ Server started successfully!
   PID: 12345
   Health: http://localhost:8000/health
   Logs: tail -f /tmp/ironclad-mcp.log

To stop: ./scripts/stop_server.sh
```

### `stop_server.sh`
**Usage:** `./scripts/stop_server.sh`

Stops all server instances:
1. Kills server from PID file (if exists)
2. Kills any orphaned `ironclad_mcp.http_server` processes
3. Removes PID file

### `restart_server.sh`
**Usage:** `./scripts/restart_server.sh`

Convenience script that calls `stop_server.sh` then `start_server.sh`.

**When to use:** After making code changes to ensure fresh code is loaded.

### `server_status.sh`
**Usage:** `./scripts/server_status.sh`

Shows current server status:
- PID file information
- Process running status
- Health check result
- List of all ironclad_mcp processes

**Example output:**
```bash
📊 Ironclad MCP Server Status

PID File: /Users/grantjackman/Documents/Ironclad-mcp/.server.pid
Recorded PID: 12345
Status: RUNNING ✓
Health Check: PASSED ✓
{
  "status": "healthy",
  "service": "ironclad-mcp",
  "version": "2.0.0",
  "transport": "sse"
}

All ironclad_mcp processes:
grantjackman 12345  0.2  0.6 411330464 107568  ??  SN   1:54PM   0:59.69 python3 -u -m ironclad_mcp.http_server
```

## PID File Tracking

The server's process ID is stored in `.server.pid` at the project root. This allows the scripts to:
- Know which process is the "current" server
- Kill the correct process during restarts
- Detect stale PID files (process no longer running)

The `.server.pid` file is automatically added to `.gitignore`.

## Recommended Workflow

### Starting Development
```bash
./scripts/start_server.sh
```

### After Making Code Changes
```bash
./scripts/restart_server.sh
```

### Checking Server Status
```bash
./scripts/server_status.sh
```

### Stopping Server
```bash
./scripts/stop_server.sh
```

## Integration with Cursor

After running `./scripts/restart_server.sh`, **restart Cursor** to establish a fresh connection to the updated server. This ensures Cursor's MCP client connects to the new process.

## Troubleshooting

### "Address already in use" error
Run `./scripts/stop_server.sh` to kill all existing processes, then start again.

### Server not responding after code changes
1. Run `./scripts/restart_server.sh` (clears cache + restarts)
2. Restart Cursor to reconnect
3. Test with `./scripts/server_status.sh`

### Multiple processes running
Run `./scripts/stop_server.sh` to kill all, then `./scripts/start_server.sh`.

## Benefits

✅ **No more orphaned processes** - Automatic cleanup before every start  
✅ **No more stale bytecode** - Cache cleared on every start  
✅ **Process tracking** - PID file tracks the current server  
✅ **Health validation** - Startup confirms server is responding  
✅ **Clear logging** - Color-coded output shows each step  
✅ **Foolproof restarts** - One command ensures fresh code runs




