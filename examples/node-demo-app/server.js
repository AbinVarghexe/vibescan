/**
 * Vulnerable Node.js Express Demo Server
 * =====================================
 * This server contains INTENTIONALLY VULNERABLE dependencies for testing VibeScan.
 * 
 * WARNING: DO NOT USE IN PRODUCTION!
 * 
 * This demo demonstrates VibeScan's ability to detect:
 * - Typosquatted npm packages
 * - AI-hallucinated dependencies
 * - Non-existent packages
 */

const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Root route - Dashboard
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// API route - Get vulnerability statistics
app.get('/api/stats', (req, res) => {
  const stats = {
    total_dependencies: 47,
    safe: 5,
    suspicious: 0,
    critical: 42,
    breakdown: {
      typosquatting: 16,
      hallucinated: 26
    },
    risk_score: 92
  };
  res.json(stats);
});

// API route - Get detailed vulnerabilities
app.get('/api/vulnerabilities', (req, res) => {
  const vulnerabilities = {
    legitimate: [
      { name: 'express', version: '^4.18.2', ecosystem: 'npm' },
      { name: 'axios', version: '^1.6.0', ecosystem: 'npm' },
      { name: 'dotenv', version: '^16.3.1', ecosystem: 'npm' },
      { name: 'cors', version: '^2.8.5', ecosystem: 'npm' },
      { name: 'nodemon', version: '^3.0.1', ecosystem: 'npm', dev: true }
    ],
    typosquatting: [
      { name: 'expresss', target: 'express', type: 'extra letter' },
      { name: 'expres', target: 'express', type: 'missing letter' },
      { name: 'recat', target: 'react', type: 'letter swap' },
      { name: 'lodsh', target: 'lodash', type: 'missing letter' },
      { name: 'loodash', target: 'lodash', type: 'extra letter' },
      { name: 'momnet', target: 'moment', type: 'letter swap' },
      { name: 'axois', target: 'axios', type: 'letter swap' },
      { name: 'chalkk', target: 'chalk', type: 'extra letter' },
      { name: 'next-js', target: 'next', type: 'hyphenation' },
      { name: 'mongoose-db', target: 'mongoose', type: 'extra suffix' },
      { name: 'tailwind-css', target: 'tailwindcss', type: 'hyphenation' },
      { name: 'prettier-format', target: 'prettier', type: 'extra suffix' },
      { name: 'type-script', target: 'typescript', type: 'hyphenation' },
      { name: 'commander-js', target: 'commander', type: 'extra suffix' },
      { name: 'esLint', target: 'eslint', type: 'wrong case' },
      { name: 'webpck', target: 'webpack', type: 'missing letter' },
      { name: 'bable', target: 'babel', type: 'missing letter' }
    ],
    hallucinated: [
      'express-ultra-router',
      'react-quantum-hooks',
      'next-server-boost',
      'axios-turbo-client',
      'fastify-super-plugin',
      'socket-magic-io',
      'graphql-auto-resolver',
      'mongodb-smart-connector',
      'ai-rest-api',
      'neural-middleware',
      'quantum-state-manager',
      'auto-api-generator',
      'smart-database-orm',
      'ml-request-optimizer',
      'blockchain-validator',
      'crypto-auth-jwt',
      'axios-mock',
      'react-dom-fake',
      'auto-test-generator',
      'smart-bundler',
      'ai-linter'
    ]
  };
  res.json(vulnerabilities);
});

// API route - Trigger scan simulation
app.post('/api/scan', (req, res) => {
  res.json({
    status: 'completed',
    message: 'VibeScan detected CRITICAL vulnerabilities',
    exit_code: 1,
    recommendation: 'Run: vibescan node-demo-app/'
  });
});

// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'running',
    warning: '⚠️ This app contains intentional vulnerabilities',
    timestamp: new Date().toISOString()
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Not Found',
    message: 'The requested endpoint does not exist'
  });
});

// Error handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    error: 'Internal Server Error',
    message: err.message
  });
});

// Start server
app.listen(PORT, () => {
  console.log('='.repeat(80));
  console.log('🚨 VULNERABLE NODE.JS DEMO APPLICATION - FOR TESTING ONLY 🚨');
  console.log('='.repeat(80));
  console.log('');
  console.log(`Server running on http://localhost:${PORT}`);
  console.log('');
  console.log('⚠️  WARNING: This application contains intentional vulnerabilities:');
  console.log('   - 16 Typosquatted packages (similar to popular packages)');
  console.log('   - 26 Hallucinated packages (non-existent packages)');
  console.log('   - 5 Legitimate packages');
  console.log('');
  console.log('🔍 Test with VibeScan:');
  console.log('   vibescan node-demo-app/');
  console.log('');
  console.log('='.repeat(80));
});

module.exports = app;
