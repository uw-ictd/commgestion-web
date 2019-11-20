let db = require('../models/index');
let userFactory = require('../models/user');

let User = userFactory(db.sequelize, db.Sequelize.DataTypes);

function test() {
    db.sequelize.sync().then(function() {
        return User.findOrCreate({
            where: {
                username: 'fiddle'
            },
            defaults: {
                phoneNumber: '+1(456)789-1034',
                displayName: 'Superstar',
                imsi: '1234567890',
                guti: '_',
                isLocal: true,
                role: 'user',
                connectivityStatus: 'online',
                lastTimeOnline: Date.now(),
                rateLimitKbps: -1,
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
}

module.exports = test;
