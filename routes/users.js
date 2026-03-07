const express = require('express');
const User = require('../models/user');

const router = express.Router();

// ユーザー登録
router.post('/register', async (req, res) => {
  try {
    const { name, email, role } = req.body;
    if (!name || !email) {
      return res.status(400).json({ error: 'Name and email are required' });
    }
    const user = await User.create(name, email, role);
    res.status(201).json(user);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ユーザーロール変更
router.put('/:id/role', async (req, res) => {
  try {
    const { id } = req.params;
    const { role } = req.body;
    const user = await User.findById(id);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    await user.updateRole(role);
    res.json(user);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ユーザー検索
router.get('/search', async (req, res) => {
  try {
    const { name, email, role } = req.query;
    const users = await User.findAll({ name, email, role });
    res.json(users);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;