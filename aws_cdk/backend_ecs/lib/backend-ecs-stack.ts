import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as logs from 'aws-cdk-lib/aws-logs';
import * as ecr from 'aws-cdk-lib/aws-ecr';
// import * as ssm from 'aws-cdk-lib/aws-ssm';

export class BackendEcsStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    // The code that defines your stack goes here

    // VPCの作成
    const vpc = new ec2.Vpc(this, 'sample-vpc', {
      vpcName: 'sample-vpc',
      ipAddresses: ec2.IpAddresses.cidr('172.32.0.0/16'),
      natGateways: 0,
      availabilityZones: ['ap-northeast-1a'],
      subnetConfiguration: [
        {
          cidrMask: 24,
          name: 'task-network',
          subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
        },
        {
          cidrMask: 26,
          name: 'natgw-network',
          subnetType: ec2.SubnetType.PUBLIC,
        }
      ]
    });

    // タスクロールの定義
    const taskRole = iam.Role.fromRoleName(this, 'TaskRole', 'DevEcsTaskRole');

    // 実行ロールの定義
    const executionRole = iam.Role.fromRoleName(this, 'ExecutionRole', 'EcsTaskExecutionRole');

    // ログ設定
    const logGroup = new ecs.AwsLogDriver({
      streamPrefix: 'ecs',
      logGroup: new logs.LogGroup(this, 'LogGroup', {
        logGroupName: '/ecs/sample-dev',
        removalPolicy: cdk.RemovalPolicy.DESTROY,
      }),
    });

    // ECS Cluster
    const cluster = new ecs.Cluster(this, 'cluster2', {
      vpc: vpc,
      clusterName: 'cluster2',
      enableFargateCapacityProviders: true
    });

    // ECS Task Definition
    const taskDefinition = new ecs.FargateTaskDefinition(this, 'task-def', {
      family: 'sameple-task',
      cpu: 1024,
      memoryLimitMiB: 3072,
      runtimePlatform: {
        "cpuArchitecture": ecs.CpuArchitecture.X86_64,
        "operatingSystemFamily": ecs.OperatingSystemFamily.LINUX
      },
      taskRole: taskRole,
      executionRole: executionRole,
    });

    // ECR Repository
    const repository = ecr.Repository.fromRepositoryName(this, 'Repository', 'sample-container');

    // taskDefinitionにコンテナを追加
    const container = taskDefinition.addContainer('container', {
      image: ecs.ContainerImage.fromEcrRepository(repository,'latest'),
      logging: logGroup
    });

    /*
    container.addEnvironment(
      "SAMPLE_ENV",
      ssm.StringParameter.valueFromLookup(this, '/dev/ecs/SAMPLE_ENV')
    );
    */

    new ecs.FargateService(this, 'service', {
      cluster: cluster,
      taskDefinition: taskDefinition,
      serviceName: 'service',
      desiredCount: 1,
      assignPublicIp: true,
    });
  }
}
