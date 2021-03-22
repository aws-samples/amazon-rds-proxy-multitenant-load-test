// Access layer, no proxy
const mysql = require('mysql2/promise');
require('tls').DEFAULT_MIN_VERSION = 'TLSv1'; //enables TLS 1.0 rather than TLS 1.2 (which is not supported my the MySQL Aurora 5.6)
var user_name = 'user';
var database_name = 'user_database';
var AWS = require('aws-sdk');
var dbPort = 3306;
var dbRegion = process.env['region'];
var dbHost = process.env['endpoint'];


exports.handler = async (event) => {

    var random_ints = [];
    for (var i = 0; i < 5; i++) {
        random_ints.push(Math.floor(Math.random() * 1000));
    }
    var where_clause = `(${random_ints[0]}, ${random_ints[1]}, ${random_ints[2]}, ${random_ints[3]}, ${random_ints[4]})`;
    var query = `SELECT * FROM mytable WHERE ID IN ${where_clause};`;

    // tenant id
    var tenant_id = event.queryStringParameters.tenant;
    var dbUser = user_name.concat(tenant_id);
    // var dbUser = 'user100';

    // database
    var database = database_name.concat(tenant_id);
    // var database = 'user_database100';

    // Resource name
    //   var resource_a = 'arn:aws:rds-db:us-east-1:account-no:dbuser:*/user';
    var resource_a = process.env['cluster_endpoint_resource'];
    var resource = resource_a.concat(tenant_id);
    // var resource = 'arn:aws:rds-db:us-east-1:account-no:dbuser:*/user100';

    //   var arn = 'arn:aws:iam::account-no:role/MB3_role_for_all_users';
    var arn = process.env['iam_arn'];

    var session_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "rds-db:connect",
                "Resource": resource
            }]};

    let dbToken = await new Promise((resolve, reject) => {
        let sts = new AWS.STS({});

        sts.assumeRole({
            RoleArn: arn,
            RoleSessionName: "test",
            Policy: JSON.stringify(session_policy)
        }, (err, iamCredentialResponse) => {
            if (err) {
                return reject(err);
            }

            let iamCredentials = new AWS.Credentials({
                accessKeyId: iamCredentialResponse.Credentials.AccessKeyId,
                secretAccessKey: iamCredentialResponse.Credentials.SecretAccessKey,
                sessionToken: iamCredentialResponse.Credentials.SessionToken
            });

            //   console.log(iamCredentials);
            let signer = new AWS.RDS.Signer({
                credentials: iamCredentials
            });

            signer.getAuthToken({
                region: dbRegion,
                hostname: dbHost,
                port: dbPort,
                username: dbUser
            }, (err, token) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(token);
                }
            });
        });
    });

    const connection = await mysql.createConnection({
        host     : dbHost,
        user     : dbUser,
        ssl: 'Amazon RDS',
        password : dbToken,
        port: dbPort,
        database: database,
        authSwitchHandler: function (data, cb) { // modifies the authentication handler
            if (data.pluginName === 'mysql_clear_password') { // authentication token is sent in clear text but connection uses SSL encryption
                cb(null, Buffer.from(dbToken + '\0'));
            }
        }
    });

    const result = await connection.query(query);
    var result2 = result[0];
    connection.end();
    const response = {
        statusCode: 200,
        body: JSON.stringify(result2),
    };
    console.log(dbUser);
    console.log(response);
    return response;
};
