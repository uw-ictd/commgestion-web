'use strict';
module.exports = (sequelize, DataTypes) => {
  const User = sequelize.define('User', {
    username: DataTypes.STRING,
    phoneNumber: DataTypes.STRING,
    displayName: DataTypes.STRING,
    imsi: DataTypes.STRING,
    guti: DataTypes.STRING,
    isLocal: DataTypes.BOOLEAN,
    role: DataTypes.ENUM('admin', 'user', 'researcher'),
    connectivityStatus: DataTypes.ENUM('online', 'offline', 'blocked'),
    lastTimeOnline: DataTypes.DATE,
    rateLimitKbps: DataTypes.INTEGER,
    salt: DataTypes.STRING.BINARY,
    passwordSha256: DataTypes.STRING.BINARY
  }, {});
  User.associate = function(models) {
    // associations can be defined here
  };
  return User;
};
