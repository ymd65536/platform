#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { BackendEcsStack } from '../lib/backend-ecs-stack';
import { EcsNatgwStack } from '../lib/ecs-natgw-stack';

const app = new cdk.App();
new BackendEcsStack(app, 'BackendEcsStack', {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION,
  },
});

new EcsNatgwStack(app, 'EcsNatgwStack', {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION,
  },
});
