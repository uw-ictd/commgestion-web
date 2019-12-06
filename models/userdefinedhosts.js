'use strict';
module.exports = (sequelize, DataTypes) => {
  const UserDefinedHosts = sequelize.define('UserDefinedHosts', {
    name: DataTypes.STRING
  }, {});
  UserDefinedHosts.associate = function(models) {
    // associations can be defined here
  };
  return UserDefinedHosts;
};