'use strict';
module.exports = (sequelize, DataTypes) => {
  const HostMapping = sequelize.define('HostMapping', {
    capturedhost: DataTypes.STRING,
    hostid: DataTypes.INTEGER
  }, {});
  HostMapping.associate = function(models) {
    // associations can be defined here
  };
  return HostMapping;
};