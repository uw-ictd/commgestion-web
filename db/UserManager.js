let db = require('../models/index');
let userFactory = require('../models/user');

let User = userFactory(db.sequelize, db.Sequelize.DataTypes);

let Actions = {
    findTotalUsers: function() {
        return User.count()
    },
    insertUser: function(name, randomness) {
        db.sequelize.sync().then(function() {
                return User.findOrCreate({
                    where: {
                        username: name
                    },
                    defaults: {
                        phoneNumber: '+1(456)789-1034',
                        displayName: 'Superstar',
                        imsi: '123456789'+randomness,
                        guti: '_',
                        isLocal: true,
                        role: 'user',
                        connectivityStatus: 'online',
                        lastTimeOnline: Date.now(),
                        rateLimitKbps: Math.random() * 100,
                        salt: 'fish',
                        passwordSha256: 'undefined'
                    }
                }).then(([createdUser, created]) => {
                    if (!created) {
                        console.error("User already exists. Avoiding the creation of a duplicate entry");
                    } else {
                        console.log(createdUser.get({
                            plain: true
                        }));
                    }
                });
            });
    },

}

module.exports = Actions;