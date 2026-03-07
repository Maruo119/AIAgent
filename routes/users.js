const express = require('express');
const User = require('../models/user');

const router = express.Router();

// ユーザー登録
router.post('/register', async (req, res) => {
  console.log('POST /users/register called with body:', req.body);
  try {
    const { name, email, role } = req.body;
    if (!name || !email) {
      console.log('Registration failed: missing name or email');
      return res.status(400).json({ error: 'Name and email are required' });
    }
    console.log('Creating user:', { name, email, role });
    const user = await User.create(name, email, role);
    console.log('User created successfully:', user);
    res.status(201).json(user);
  } catch (error) {
    console.error('Registration error:', error);
    res.status(500).json({ error: error.message });
  }
});

// ユーザーロール変更
router.put('/:id/role', async (req, res) => {
  console.log(`PUT /users/${req.params.id}/role called with body:`, req.body);
  try {
    const { id } = req.params;
    const { role } = req.body;
    console.log('Finding user by ID:', id);
    const user = await User.findById(id);
    if (!user) {
      console.log('User not found:', id);
      return res.status(404).json({ error: 'User not found' });
    }
    console.log('Updating user role to:', role);
    await user.updateRole(role);
    console.log('User role updated successfully');
    res.json(user);
  } catch (error) {
    console.error('Role update error:', error);
    res.status(500).json({ error: error.message });
  }
});

// ユーザー検索
router.get('/search', async (req, res) => {
  console.log('GET /users/search called with query:', req.query);
  try {
    const { name, email, role } = req.query;
    console.log('Searching users with filters:', { name, email, role });
    const users = await User.findAll({ name, email, role });
    console.log('Search results:', users.length, 'users found');
    res.json(users);
  } catch (error) {
    console.error('Search error:', error);
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;