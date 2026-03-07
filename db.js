const mysql = require('mysql2/promise');

async function createDatabaseIfNotExists() {
  const connection = await mysql.createConnection({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
  });
  await connection.execute('CREATE DATABASE IF NOT EXISTS user_management');
  await connection.end();
}

async function getPool() {
  await createDatabaseIfNotExists();
  return mysql.createPool({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME || 'user_management',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
  });
}

const poolPromise = getPool();

module.exports = poolPromise;