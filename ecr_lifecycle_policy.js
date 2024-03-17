const AWS = require('aws-sdk');
const ecr = new AWS.ECR({apiVersion: '2015-09-21', region: 'eu-central-1'});

const ECR_REPOSITORY_NAME = `serverless-credit-recommendation-service-`
const LIFE_CYCLE_POLICY_TEXT = {
    'rules': [{
        'rulePriority': 1,
        'description': 'Only keep 1 images',
        'selection': {'tagStatus': 'any', 'countType': 'imageCountMoreThan', 'countNumber': 1},
        'action': {'type': 'expire'}
    }]
}


async function describeECRRepoLifeCyclePolicy(registryId, repositoryName) {
    return await ecr.getLifecyclePolicy({registryId: registryId, repositoryName: repositoryName}).promise();
}

async function putECRRepoLifeCyclePolicy(registryId, repositoryName, lifecyclePolicyText) {
    return await ecr.putLifecyclePolicy({
        registryId: registryId,
        repositoryName: repositoryName,
        lifecyclePolicyText: JSON.stringify(lifecyclePolicyText)
    }).promise();
}


(async main => {
    if (!process.env.ENVIRONMENT)
        throw Error(`Please provide environment value`);

    if (!process.env.AWS_ACCOUNT_ID)
        throw Error(`Please provide aws account id value`);

    let repositoryName = ECR_REPOSITORY_NAME + process.env.ENVIRONMENT;

    let registryId = process.env.AWS_ACCOUNT_ID;
    console.log(`registryId :: ${registryId}`)

    let lifeCyclePolicy
    try {
        lifeCyclePolicy = await describeECRRepoLifeCyclePolicy(registryId, repositoryName);
    } catch (err) {
        if (err.code === 'LifecyclePolicyNotFoundException') {
            console.log(`LifeCycle not found for repo - "${ECR_REPOSITORY_NAME}${process.env.ENVIRONMENT}" not found`)
            const lifeCycleResponse = await putECRRepoLifeCyclePolicy(registryId, repositoryName, LIFE_CYCLE_POLICY_TEXT);
            console.log(`Created lifeCycleResponse for registry :: "${registryId}" and "repository ${repositoryName}"`)
        } else {
            throw err;
        }
    }
    if (lifeCyclePolicy)
        console.log(`lifeCyclePolicy found for registry :: "${registryId}" and repository "${repositoryName}"`)
})()