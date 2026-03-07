require('dotenv').config();
const express = require('express');
const userRoutes = require('./routes/users');
const pool = require('./db');

const app = express();
const PORT = process.env.PORT || 3000;

async function initializeDatabase() {
  try {
    console.log('Initializing database...');
    await pool.execute(`
      CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        role VARCHAR(50) DEFAULT 'user'
      )
    `);
    console.log('Database initialized successfully');
  } catch (error) {
    console.error('Database initialization error:', error);
  }
}

async function checkDatabaseConnection() {
  try {
    console.log('Checking database connection...');
    await pool.execute('SELECT 1');
    console.log('Database connection successful');
    return true;
  } catch (error) {
    console.error('Database connection failed:', error.message);
    return false;
  }
}

app.use(express.json());
app.use(express.static('public'));
app.use('/users', userRoutes);

// Health check endpoint
app.get('/health', async (req, res) => {
  console.log('Health check requested');
  const dbConnected = await checkDatabaseConnection();
  if (dbConnected) {
    console.log('Health check: OK');
    res.json({ status: 'OK', database: 'connected' });
  } else {
    console.log('Health check: ERROR');
    res.status(500).json({ status: 'ERROR', database: 'disconnected' });
  }
});

// Middleware to log requests
app.use((req, res, next) => {
  console.log(`${req.method} ${req.url}`);
  next();
});

app.listen(PORT, async () => {
  console.log(`Server starting on port ${PORT}`);
  await checkDatabaseConnection();
  await initializeDatabase();
  console.log(`Server running on port ${PORT}`);
});