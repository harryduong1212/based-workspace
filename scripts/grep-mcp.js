const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Dynamically resolve the path to the sibling grep_app directory
// __dirname is .../based-workspace/scripts
// path.resolve maps to .../grep_app_mcp/dist/server-stdio.js
const serverPath = path.resolve(__dirname, '../../grep_app_mcp/dist/server-stdio.js');

// Pre-flight check to ensure the file exists across different OS clones
if (!fs.existsSync(serverPath)) {
    console.error(`[grep_app wrapper] Fatal Error: Could not find server at ${serverPath}`);
    console.error(`[grep_app wrapper] Ensure grep_app_mcp is cloned adjacent to based-workspace.`);
    process.exit(1);
}

// Spawn the process with warnings suppressed
const child = spawn('node', ['--no-warnings', serverPath], {
    stdio: ['inherit', 'pipe', 'inherit'],
    shell: process.platform === 'win32' // Required for stable binary execution on Windows
});

let buffer = '';

// Intercept and sanitize the stdout stream
child.stdout.on('data', (data) => {
    buffer += data.toString();
    let lines = buffer.split(/\r?\n/);

    // Keep the last partial segment in the buffer until the line completes
    buffer = lines.pop();

    for (const line of lines) {
        if (!line.trim()) continue;
        try {
            // Verify the line is valid JSON
            JSON.parse(line);
            // If successful, pass it safely to Antigravity
            process.stdout.write(line + '\n');
        } catch (e) {
            // If it fails to parse, it is garbage text polluting the stream. 
            // Route it safely to stderr so it does not crash the agent.
            process.stderr.write(`[grep_app sanitized log] ${line}\n`);
        }
    }
});

child.on('error', (err) => {
    console.error('Failed to start grep_app process:', err);
});

child.on('exit', (code) => {
    process.exit(code || 0);
});