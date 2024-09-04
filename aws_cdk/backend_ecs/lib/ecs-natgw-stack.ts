import { Construct } from 'constructs';

import * as cdk from 'aws-cdk-lib';
import { aws_ec2 } from 'aws-cdk-lib';

export class EcsNatgwStack extends cdk.Stack {
    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);
        const Vpc = aws_ec2.Vpc.fromLookup(this, 'sample-vpc', {
            vpcName: 'sample-vpc',
        });
        const EcsSubnet = Vpc.publicSubnets[0];

        const eip = new aws_ec2.CfnEIP(this, 'EIP', {
            domain: 'vpc',
        });

        const cfnNatGateway = new aws_ec2.CfnNatGateway(this, 'NatGateway', {
            subnetId: EcsSubnet.subnetId,
            allocationId: eip.attrAllocationId
        });
    }
}
    