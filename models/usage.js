'use strict';
module.exports = (sequelize, DataTypes) => {
  const Usage = sequelize.define('Usage', {
    userid: DataTypes.INTEGER,
    throughput: DataTypes.DOUBLE,
    timestamp: DataTypes.DATE
  }, {});
  Usage.associate = function(models) {
    // associations can be defined here
  };
  return Usage;
};