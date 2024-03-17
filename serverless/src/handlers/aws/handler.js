const zlib = require('zlib');
const axios = require('axios')
const HashMap = require('hashmap')
const ssm = require('./SecretManagerClient')
const qs = require('qs')

let axiosConfig = {
    url: `https://${process.env.HOST_NAME.trim()}${process.env.SERVICE_PATH.trim()}`,
    method: "POST",
    headers: {'Content-Type': 'application/json', "User-Agent": "Axios_Nodejs_Client"}
}

function parseJSON(element) {
    try {
        return JSON.parse(element)
    } catch (err) {
        return element
    }
}

async function callAPI(config) {
    try {
        return await axios.request(config)
    } catch (err) {
        console.log(`error while calling api :: ${err}`)
        throw err;
    }
}

async function unzipPayload(buffer_payload) {
    return new Promise((resolve, reject) => {
        zlib.gunzip(buffer_payload, function (error, result) {
            if (error) {
                reject(error);
            } else {
                resolve(JSON.parse(result.toString()));
            }
        })
    })
}

function parserParams(data) {
    let paramObj = {};
    for (const record of data) {
        paramObj[record.Name] = parseJSON(record.Value)
    }
    return paramObj;
}

exports.handler = async function (input, context) {
    let unzipResponse
    try {
        console.log("unzipping the received request")
        unzipResponse = await unzipPayload(Buffer.from(input.awslogs.data, 'base64'));
    } catch (err) {
        console.log(`error occurred unzipping the received request :: ${err}`)
        return {
            statusCode: 500, headers: {
                "Content-Type": "application/json",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                "Access-Control-Allow-Credentials": false,
                "Access-Control-Allow-Origin": "*",
                "X-Requested-With": "*"
            }, body: JSON.stringify({
                errorMessage: err.message
            })
        }
    }
    let ssmResult
    try {
        console.log(`calling ssm to fetch the apiId and app client secret`)
        ssmResult = await ssm.getParameters([process.env.API_KEY, process.env.APP_CLIENT])
    } catch (err) {
        console.log(`error occurred fetching ssm parameters :: ${err}`)
        return {
            statusCode: 500, headers: {
                "Content-Type": "application/json",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                "Access-Control-Allow-Credentials": false,
                "Access-Control-Allow-Origin": "*",
                "X-Requested-With": "*"
            }, body: JSON.stringify({
                errorMessage: err.message
            })
        }
    }

    const parsedSSMParam = parserParams(ssmResult);

    const cognitoAuthData = qs.stringify({
        "client_id": parsedSSMParam[process.env.APP_CLIENT].clientId,
        "client_secret": parsedSSMParam[process.env.APP_CLIENT].clientSecret,
        "scope": process.env.SCOPE,
        "grant_type": "client_credentials"
    })

    // calling cognito endpoint to get access_token
    let tokenResponse
    try {
        console.log(`calling the cognito token endpoint to receive the access_token`)
        tokenResponse = await callAPI({
            "method": "POST", "url": process.env.COGNITO_AUTH_ENDPOINT, "headers": {
                "Content-Type": "application/x-www-form-urlencoded"
            }, data: cognitoAuthData
        })
    } catch (err) {
        console.log(`error occurred calling the cognito token endpoint with error :: ${err}`)
        return {
            statusCode: 500, headers: {
                "Content-Type": "application/json",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                "Access-Control-Allow-Credentials": false,
                "Access-Control-Allow-Origin": "*",
                "X-Requested-With": "*"
            }, body: JSON.stringify({
                errorMessage: err.message
            })
        }
    }

    const access_token = tokenResponse.data.access_token;

    axiosConfig.headers["x-api-key"] = parsedSSMParam[process.env.API_KEY];
    axiosConfig.headers["Authorization"] = `Bearer ${access_token}`;

    let recordArr = [];
    let map = new HashMap();
    for (let record of unzipResponse.logEvents) {
        let message = record.message.replaceAll('\n', '').replaceAll(`'`, `"`).replace(/\\"/g, '"').replaceAll(`"{`, `{`).replaceAll(`}"`, `}`);
        let parsedData = JSON.parse(message);

        for (let parsedDataKey in parsedData) {
            if (parsedData[parsedDataKey] instanceof Object) {
                parsedData[parsedDataKey] = JSON.stringify(parsedData[parsedDataKey])
            }
        }

        let key = parsedData.customer ? parsedData.customer : "scindo";
        if (map.has(key)) {
            let data = map.get(key);
            delete parsedData.customer
            data.push(parsedData)
            map.set(key, data)
        } else {
            delete parsedData.customer
            map.set(key, [parsedData])
        }
    }

    for (const pair of map) {
        const date = new Date();
        axiosConfig.data = JSON.stringify({
            "data": pair.value, "config": {
                "auditing_bucket_path": process.env.AUDITING_BUCKET.trim(),
                "auditing_database": process.env.AUDITING_DATABASE.trim(),
                "auditing_table_name": process.env.AUDITING_TABLE_NAME.trim(),
                "auditing_path": process.env.AUDITING_PATH.trim(),
                "partition_columns": parseJSON(process.env.PARTITION_COLUMNS),
                "date_columns": parseJSON(process.env.DATE_COLUMNS),
                "partition_data": [pair.key, date.getFullYear(), date.getMonth() + 1, date.getDate(), date.getHours()]
            }
        })
        console.log(`calling the parquet api for customer:: ${pair.key}`)
        const apiResponse = await callAPI(axiosConfig);
        console.log(`customer:: ${pair.key} response :: ${JSON.stringify(apiResponse.data)} `)
    }
    console.log(`returning the response from handler`)
    return {
        statusCode: 200, headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            "Access-Control-Allow-Credentials": false,
            "Access-Control-Allow-Origin": "*",
            "X-Requested-With": "*"
        }, body: JSON.stringify({
            message: "message saved successfully"
        })
    }

};
