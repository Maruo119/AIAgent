const { v4: uuidv4 } = require('uuid');

class User {
  constructor(name, email, role = 'user') {
    this.id = uuidv4();
    this.name = name;
    this.email = email;
    this.role = role;
  }
}

let users = [];

module.exports = { User, users };