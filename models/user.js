const pool = require('../db');

class User {
  constructor(id, name, email, role = 'user') {
    this.id = id;
    this.name = name;
    this.email = email;
    this.role = role;
  }

  static async create(name, email, role = 'user') {
    console.log('User.create called with:', { name, email, role });
    try {
      const [result] = await pool.execute(
        'INSERT INTO users (name, email, role) VALUES (?, ?, ?)',
        [name, email, role]
      );
      console.log('User inserted with ID:', result.insertId);
      return new User(result.insertId, name, email, role);
    } catch (error) {
      console.error('User.create error:', error);
      throw error;
    }
  }

  static async findById(id) {
    console.log('User.findById called with ID:', id);
    try {
      const [rows] = await pool.execute('SELECT * FROM users WHERE id = ?', [id]);
      if (rows.length === 0) {
        console.log('User not found');
        return null;
      }
      const row = rows[0];
      console.log('User found:', row);
      return new User(row.id, row.name, row.email, row.role);
    } catch (error) {
      console.error('User.findById error:', error);
      throw error;
    }
  }

  static async findAll(filters = {}) {
    console.log('User.findAll called with filters:', filters);
    try {
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
      console.log('Executing query:', query, 'with params:', params);
      const [rows] = await pool.execute(query, params);
      console.log('Query returned', rows.length, 'rows');
      return rows.map(row => new User(row.id, row.name, row.email, row.role));
    } catch (error) {
      console.error('User.findAll error:', error);
      throw error;
    }
  }

  async updateRole(role) {
    console.log('User.updateRole called for ID:', this.id, 'to role:', role);
    try {
      await pool.execute('UPDATE users SET role = ? WHERE id = ?', [role, this.id]);
      console.log('User role updated');
      this.role = role;
    } catch (error) {
      console.error('User.updateRole error:', error);
      throw error;
    }
  }
}

module.exports = User;