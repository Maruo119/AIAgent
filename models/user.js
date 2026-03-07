const pool = require('../db');

class User {
  constructor(id, name, email, role = 'user') {
    this.id = id;
    this.name = name;
    this.email = email;
    this.role = role;
  }

  static async create(name, email, role = 'user') {
    const [result] = await pool.execute(
      'INSERT INTO users (name, email, role) VALUES (?, ?, ?)',
      [name, email, role]
    );
    return new User(result.insertId, name, email, role);
  }

  static async findById(id) {
    const [rows] = await pool.execute('SELECT * FROM users WHERE id = ?', [id]);
    if (rows.length === 0) return null;
    const row = rows[0];
    return new User(row.id, row.name, row.email, row.role);
  }

  static async findAll(filters = {}) {
    let query = 'SELECT * FROM users WHERE 1=1';
    const params = [];
    if (filters.name) {
      query += ' AND name LIKE ?';
      params.push(`%${filters.name}%`);
    }
    if (filters.email) {
      query += ' AND email LIKE ?';
      params.push(`%${filters.email}%`);
    }
    if (filters.role) {
      query += ' AND role = ?';
      params.push(filters.role);
    }
    const [rows] = await pool.execute(query, params);
    return rows.map(row => new User(row.id, row.name, row.email, row.role));
  }

  async updateRole(role) {
    await pool.execute('UPDATE users SET role = ? WHERE id = ?', [role, this.id]);
    this.role = role;
  }
}

module.exports = User;