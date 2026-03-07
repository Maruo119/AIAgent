const express = require('express');
const { User, users } = require('../models/user');

const router = express.Router();

// ユーザー登録
router.post('/register', (req, res) => {
  const { name, email, role } = req.body;
  if (!name || !email) {
    return res.status(400).json({ error: 'Name and email are required' });
  }
  const user = new User(name, email, role);
  users.push(user);
  res.status(201).json(user);
});

// ユーザーロール変更
router.put('/:id/role', (req, res) => {
  const { id } = req.params;
  const { role } = req.body;
  const user = users.find(u => u.id === id);
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  user.role = role;
  res.json(user);
});

// ユーザー検索
router.get('/search', (req, res) => {
  const { name, email, role } = req.query;
  let filteredUsers = users;
  if (name) {
    filteredUsers = filteredUsers.filter(u => u.name.toLowerCase().includes(name.toLowerCase()));
  }
  if (email) {
    filteredUsers = filteredUsers.filter(u => u.email.toLowerCase().includes(email.toLowerCase()));
  }
  if (role) {
    filteredUsers = filteredUsers.filter(u => u.role === role);
  }
  res.json(filteredUsers);
});

module.exports = router;