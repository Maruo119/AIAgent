const mysql = require('mysql2/promise');

async function createDatabaseIfNotExists() {
  console.log('Attempting to create database if not exists...');
  try {
    const connection = await mysql.createConnection({
      host: process.env.DB_HOST,
      user: process.env.DB_USER,
      password: process.env.DB_PASSWORD,
    });
    console.log('Connected to MySQL server, creating database...');
    await connection.execute(`CREATE DATABASE IF NOT EXISTS \`${process.env.DB_NAME || 'user_management'}\``);
    console.log('Database creation/check completed');
    await connection.end();
  } catch (error) {
    console.error('Database creation error:', error);
    throw error;
  }
}

const pool = mysql.createPool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME || 'user_management',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

async function initializePool() {
  console.log('Initializing database pool...');
  await createDatabaseIfNotExists();
  console.log('Database pool initialized');
  return pool;
}

initializePool();

module.exports = pool;