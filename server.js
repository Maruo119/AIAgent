require('dotenv').config();
const express = require('express');
const userRoutes = require('./routes/users');
const pool = require('./db');

const app = express();
const PORT = process.env.PORT || 3000;

async function initializeDatabase() {
  try {
    const connection = await pool;
    await connection.execute(`
      CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        role VARCHAR(50) DEFAULT 'user'
      )
    `);
    console.log('Database initialized');
  } catch (error) {
    console.error('Database initialization error:', error);
  }
}

app.use(express.json());
app.use(express.static('public'));
app.use('/users', userRoutes);

app.listen(PORT, async () => {
  console.log(`Server running on port ${PORT}`);
  await initializeDatabase();
});