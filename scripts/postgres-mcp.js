const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

// Read .env file from the infrastructure directory
const envPath = path.resolve(__dirname, '../infrastructure/.env');
if (fs.existsSync(envPath)) {
  const envFile = fs.readFileSync(envPath, 'utf8');
  envFile.split(/\r?\n/).forEach(line => {
    const match = line.match(/^\s*([^#=]+)\s*=\s*(.*)$/);
    if (match) {
      process.env[match[1].trim()] = match[2].trim();
    }
  });
}

const user = process.env.POSTGRES_USER || 'admin';
const pass = process.env.POSTGRES_PASSWORD || 'password';
const db = process.env.POSTGRES_DB || 'ai_memory';
const port = process.env.POSTGRES_PORT || 5432;
const url = `postgresql://${user}:${pass}@localhost:${port}/${db}`;

// Log to stderr so it doesn't break MCP protocol on stdout
console.error(`Starting MCP PostgreSQL server for database: ${db} on port: ${port}`);
const npmCmd = process.platform === 'win32' ? 'npx.cmd' : 'npx';

// Force execution context to the based-workspace root
const workspaceRoot = path.resolve(__dirname, '..');

const child = spawn(npmCmd, ['-y', '@modelcontextprotocol/server-postgres', url], {
  cwd: workspaceRoot,
  stdio: ['inherit', 'inherit', 'pipe'],
  shell: process.platform === 'win32' // Required on Windows to execute .cmd files
});

child.stderr.on('data', (data) => {
  process.stderr.write(data);
});

child.on('error', (err) => {
  console.error('Failed to start child process:', err);
});

child.on('exit', (code) => {
  process.exit(code || 0);
});