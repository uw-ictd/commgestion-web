'use strict';
module.exports = {
  up: (queryInterface, Sequelize) => {
    return queryInterface.createTable('Users', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      username: {
        type: Sequelize.STRING
      },
      phoneNumber: {
        type: Sequelize.STRING
      },
      displayName: {
        type: Sequelize.STRING
      },
      imsi: {
        type: Sequelize.STRING
      },
      guti: {
        type: Sequelize.STRING
      },
      isLocal: {
        type: Sequelize.BOOLEAN
      },
      role: {
        type: Sequelize.ENUM('admin', 'user', 'researcher')
      },
      connectivityStatus: {
        type: Sequelize.ENUM('online', 'offline', 'blocked')
      },
      lastTimeOnline: {
        type: Sequelize.DATE
      },
      rateLimitKbps: {
        type: Sequelize.INTEGER
      },
      salt: {
        type: Sequelize.STRING.BINARY
      },
      passwordSha256: {
        type: Sequelize.STRING.BINARY
      },
      createdAt: {
        allowNull: false,
        type: Sequelize.DATE
      },
      updatedAt: {
        allowNull: false,
        type: Sequelize.DATE
      }
    });
  },
  down: (queryInterface, Sequelize) => {
    return queryInterface.dropTable('Users');
  }
};
