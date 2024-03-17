const aws = require('aws-sdk')

class SecretManagerClient {
    static async getParameters(params) {
        console.log(`getting value ${JSON.stringify(params)}`)
        let param = {
            Names: params, WithDecryption: true
        };

        try {
            let options = {region: "eu-central-1"};
            const ssm = new aws.SSM(options);
            return (await ssm.getParameters(param).promise()).Parameters;

        } catch (err) {
            throw err;
        }
    }
}

module.exports = SecretManagerClient;