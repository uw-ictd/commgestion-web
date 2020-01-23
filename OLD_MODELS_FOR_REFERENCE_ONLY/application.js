'use strict';
module.exports = (sequelize, DataTypes) => {
  const Application = sequelize.define('Application', {
    host: DataTypes.STRING,
    throughput: DataTypes.DOUBLE,
    timestamp: DataTypes.DATE
  }, {});
  Application.associate = function(models) {
    // associations can be defined here
  };
  return Application;
};