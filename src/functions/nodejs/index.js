// Access layer
const mysql = require('mysql2/promise');
const https = require('https');
const fs = require('fs');
var user_name = 'user';
var database_name = 'user_database';
var AWS = require('aws-sdk');
var dbPort = 3306;
var dbRegion = process.env['REGION'];
var accountId = process.env['ACCOUNT_ID'];
var cluster_endpoint_resource = process.env['CLUSTER_ENDPOINT_RESOURCE'];
var dbHost = process.env['ENDPOINT'];
var ssl_certificate_url = process.env["SSL_CERTIFICATE_URL"];

const file = fs.createWriteStream("/tmp/SSLCA.pem");
const request = https.get(ssl_certificate_url, function(response) {
  response.pipe(file);
});

exports.handler = async (event) => {

    var random_ints = [];
    for (var i = 0; i < 5; i++) {
        random_ints.push(Math.floor(Math.random() * 1000));
    }
    var where_clause = `(${random_ints[0]}, ${random_ints[1]}, ${random_ints[2]}, ${random_ints[3]}, ${random_ints[4]})`;
    var query = `SELECT * FROM mytable WHERE ID IN ${where_clause};`;

    // tenant id
    var tenant_id = event.queryStringParameters.tenant;
    var dbUser = user_name + tenant_id;
    // var dbUser = 'user100';

    // database
    var database = database_name + tenant_id;
    // var database = 'user_database100';

    // Resource name
    var resource = cluster_endpoint_resource + tenant_id;
    // var resource = 'arn:aws:rds-db:' + dbRegion + ':' + accountId + ':dbuser:*/user100';

    var arn = process.env['IAM_ARN'];

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
            RoleSessionName: "session",
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

    try {
        const connection = await mysql.createConnection({
            host     : dbHost,
            user     : dbUser,
            ssl: {
                ca: fs.readFileSync('/tmp/SSLCA.pem'),
                flags: 'SSL_VERIFY_SERVER_CERT'
            },
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
        console.log(response);
        return response;
    } catch(e){
        console.log(e);
        const response = {
            statusCode: 500,
            body: "Internal Server Error",
        };
        return response;
    }
};
