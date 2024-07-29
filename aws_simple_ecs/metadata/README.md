
# ECS Fargateのメタデータを調査する

## 環境変数

nginxのコンテナをECS Fargateで起動した際の環境変数

```bash
AWS_EXECUTION_ENV=AWS_ECS_FARGATE
AWS_CONTAINER_CREDENTIALS_RELATIVE_URI=/v2/credentials/813d3956-27d2-4a33-b37c-0ef40c9c070c
HOSTNAME=ip-172-31-2-72.ap-northeast-1.compute.internal
AWS_DEFAULT_REGION=ap-northeast-1
AWS_REGION=ap-northeast-1
PWD=/
ECS_CONTAINER_METADATA_URI_V4=http://169.254.170.2/v4/e40860c2b55a4200b03c3197f6c59714-2886439692
PKG_RELEASE=2~bookworm
HOME=/root
LANG=C.UTF-8
NJS_VERSION=0.8.4
ECS_AGENT_URI=http://169.254.170.2/api/e40860c2b55a4200b03c3197f6c59714-2886439692
TERM=xterm-256color
ECS_CONTAINER_METADATA_URI=http://169.254.170.2/v3/e40860c2b55a4200b03c3197f6c59714-2886439692
SHLVL=1
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
NGINX_VERSION=1.27.0
NJS_RELEASE=2~bookworm
```

## エンドポイントに対してリクエスト（ECS_CONTAINER_METADATA_URI_V4）

```bash
curl $ECS_CONTAINER_METADATA_URI_V4 | jq .
```

```json
{
  "DockerId": "e40860c2b55a4200b03c3197f6c59714-2886439692",
  "Name": "dev-yamada",
  "DockerName": "dev-yamada",
  "Image": "123456789012.dkr.ecr.ap-northeast-1.amazonaws.com/dev-nginx:latest",
  "ImageID": "sha256:79ab9c392fd2923886cd7d56fdbc7d3ee2c99c71849122b5afd5a8e31220ad13",
  "Labels": {
    "com.amazonaws.ecs.cluster": "arn:aws:ecs:ap-northeast-1:123456789012:cluster/simple-ecs-cluster",
    "com.amazonaws.ecs.container-name": "dev-yamada",
    "com.amazonaws.ecs.task-arn": "arn:aws:ecs:ap-northeast-1:123456789012:task/simple-ecs-cluster/e40860c2b55a4200b03c3197f6c59714",
    "com.amazonaws.ecs.task-definition-family": "dev-yamada",
    "com.amazonaws.ecs.task-definition-version": "3"
  },
  "DesiredStatus": "RUNNING",
  "KnownStatus": "RUNNING",
  "Limits": {
    "CPU": 2
  },
  "CreatedAt": "2024-07-29T07:35:56.728610677Z",
  "StartedAt": "2024-07-29T07:35:56.728610677Z",
  "Type": "NORMAL",
  "LogDriver": "awslogs",
  "LogOptions": {
    "awslogs-create-group": "true",
    "awslogs-group": "/ecs/dev-nginx",
    "awslogs-region": "ap-northeast-1",
    "awslogs-stream": "ecs/dev-yamada/e40860c2b55a4200b03c3197f6c59714"
  },
  "ContainerARN": "arn:aws:ecs:ap-northeast-1:123456789012:container/simple-ecs-cluster/e40860c2b55a4200b03c3197f6c59714/b31c78c2-9905-4b57-bfc1-e9f8a3689607",
  "Networks": [
    {
      "NetworkMode": "awsvpc",
      "IPv4Addresses": [
        "172.31.2.72"
      ],
      "AttachmentIndex": 0,
      "MACAddress": "0a:ae:b6:d3:34:7d",
      "IPv4SubnetCIDRBlock": "172.31.0.0/20",
      "DomainNameServers": [
        "172.31.0.2"
      ],
      "DomainNameSearchList": [
        "ap-northeast-1.compute.internal"
      ],
      "PrivateDNSName": "ip-172-31-2-72.ap-northeast-1.compute.internal",
      "SubnetGatewayIpv4Address": "172.31.0.1/20"
    }
  ],
  "Snapshotter": "overlayfs"
}
```

## エンドポイントに対してリクエスト（ECS_CONTAINER_METADATA_URI_V4/stats）

```bash
curl $ECS_CONTAINER_METADATA_URI_V4/stats | jq
```

```json
{
  "read": "2024-07-29T08:11:46.738958213Z",
  "preread": "2024-07-29T08:11:36.739871215Z",
  "pids_stats": {},
  "blkio_stats": {
    "io_service_bytes_recursive": [
      {
        "major": 259,
        "minor": 0,
        "op": "Read",
        "value": 0
      },
      {
        "major": 259,
        "minor": 0,
        "op": "Write",
        "value": 11169792
      },
      {
        "major": 259,
        "minor": 0,
        "op": "Sync",
        "value": 1519616
      },
      {
        "major": 259,
        "minor": 0,
        "op": "Async",
        "value": 9650176
      },
      {
        "major": 259,
        "minor": 0,
        "op": "Discard",
        "value": 0
      },
      {
        "major": 259,
        "minor": 0,
        "op": "Total",
        "value": 11169792
      }
    ],
    "io_serviced_recursive": [
      {
        "major": 259,
        "minor": 0,
        "op": "Read",
        "value": 0
      },
      {
        "major": 259,
        "minor": 0,
        "op": "Write",
        "value": 65
      },
      {
        "major": 259,
        "minor": 0,
        "op": "Sync",
        "value": 47
      },
      {
        "major": 259,
        "minor": 0,
        "op": "Async",
        "value": 18
      },
      {
        "major": 259,
        "minor": 0,
        "op": "Discard",
        "value": 0
      },
      {
        "major": 259,
        "minor": 0,
        "op": "Total",
        "value": 65
      }
    ],
    "io_queue_recursive": [],
    "io_service_time_recursive": [],
    "io_wait_time_recursive": [],
    "io_merged_recursive": [],
    "io_time_recursive": [],
    "sectors_recursive": []
  },
  "num_procs": 0,
  "storage_stats": {},
  "cpu_stats": {
    "cpu_usage": {
      "total_usage": 8362360740,
      "percpu_usage": [
        2979697897,
        5382662843
      ],
      "usage_in_kernelmode": 1280000000,
      "usage_in_usermode": 6380000000
    },
    "system_cpu_usage": 4633550000000,
    "online_cpus": 2,
    "throttling_data": {
      "periods": 0,
      "throttled_periods": 0,
      "throttled_time": 0
    }
  },
  "precpu_stats": {
    "cpu_usage": {
      "total_usage": 8350640319,
      "percpu_usage": [
        2975314799,
        5375325520
      ],
      "usage_in_kernelmode": 1280000000,
      "usage_in_usermode": 6370000000
    },
    "system_cpu_usage": 4613650000000,
    "online_cpus": 2,
    "throttling_data": {
      "periods": 0,
      "throttled_periods": 0,
      "throttled_time": 0
    }
  },
  "memory_stats": {
    "usage": 60391424,
    "max_usage": 125136896,
    "stats": {
      "active_anon": 0,
      "active_file": 18788352,
      "cache": 22437888,
      "dirty": 0,
      "hierarchical_memory_limit": 3221225472,
      "hierarchical_memsw_limit": 9223372036854772000,
      "inactive_anon": 33386496,
      "inactive_file": 3514368,
      "mapped_file": 135168,
      "pgfault": 128502,
      "pgmajfault": 0,
      "pgpgin": 104676,
      "pgpgout": 91110,
      "rss": 33386496,
      "rss_huge": 0,
      "total_active_anon": 0,
      "total_active_file": 18788352,
      "total_cache": 22437888,
      "total_dirty": 0,
      "total_inactive_anon": 33386496,
      "total_inactive_file": 3514368,
      "total_mapped_file": 135168,
      "total_pgfault": 128502,
      "total_pgmajfault": 0,
      "total_pgpgin": 104676,
      "total_pgpgout": 91110,
      "total_rss": 33386496,
      "total_rss_huge": 0,
      "total_unevictable": 0,
      "total_writeback": 135168,
      "unevictable": 0,
      "writeback": 135168
    },
    "limit": 9223372036854772000
  },
  "name": "dev-yamada",
  "id": "e40860c2b55a4200b03c3197f6c59714-2886439692",
  "networks": {
    "eth1": {
      "rx_bytes": 83705709,
      "rx_packets": 59279,
      "rx_errors": 0,
      "rx_dropped": 0,
      "tx_bytes": 638407,
      "tx_packets": 3962,
      "tx_errors": 0,
      "tx_dropped": 0
    }
  },
  "network_rate_stats": {
    "rx_bytes_per_sec": 12.001095331570145,
    "tx_bytes_per_sec": 15.001369164462682
  }
}
```

## タスクエンドポイントに対してリクエスト（ECS_CONTAINER_METADATA_URI_V4/task）

```bash
curl $ECS_CONTAINER_METADATA_URI_V4/task | jq .
```

```json
{
  "Cluster": "arn:aws:ecs:ap-northeast-1:123456789012:cluster/simple-ecs-cluster",
  "TaskARN": "arn:aws:ecs:ap-northeast-1:123456789012:task/simple-ecs-cluster/e40860c2b55a4200b03c3197f6c59714",
  "Family": "dev-yamada",
  "Revision": "3",
  "DesiredStatus": "RUNNING",
  "KnownStatus": "RUNNING",
  "Limits": {
    "CPU": 1,
    "Memory": 3072
  },
  "PullStartedAt": "2024-07-29T07:35:51.031284568Z",
  "PullStoppedAt": "2024-07-29T07:35:55.478277684Z",
  "AvailabilityZone": "ap-northeast-1c",
  "LaunchType": "FARGATE",
  "Containers": [
    {
      "DockerId": "e40860c2b55a4200b03c3197f6c59714-2886439692",
      "Name": "dev-yamada",
      "DockerName": "dev-yamada",
      "Image": "123456789012.dkr.ecr.ap-northeast-1.amazonaws.com/dev-nginx:latest",
      "ImageID": "sha256:79ab9c392fd2923886cd7d56fdbc7d3ee2c99c71849122b5afd5a8e31220ad13",
      "Labels": {
        "com.amazonaws.ecs.cluster": "arn:aws:ecs:ap-northeast-1:123456789012:cluster/simple-ecs-cluster",
        "com.amazonaws.ecs.container-name": "dev-yamada",
        "com.amazonaws.ecs.task-arn": "arn:aws:ecs:ap-northeast-1:123456789012:task/simple-ecs-cluster/e40860c2b55a4200b03c3197f6c59714",
        "com.amazonaws.ecs.task-definition-family": "dev-yamada",
        "com.amazonaws.ecs.task-definition-version": "3"
      },
      "DesiredStatus": "RUNNING",
      "KnownStatus": "RUNNING",
      "Limits": {
        "CPU": 2
      },
      "CreatedAt": "2024-07-29T07:35:56.728610677Z",
      "StartedAt": "2024-07-29T07:35:56.728610677Z",
      "Type": "NORMAL",
      "LogDriver": "awslogs",
      "LogOptions": {
        "awslogs-create-group": "true",
        "awslogs-group": "/ecs/dev-nginx",
        "awslogs-region": "ap-northeast-1",
        "awslogs-stream": "ecs/dev-yamada/e40860c2b55a4200b03c3197f6c59714"
      },
      "ContainerARN": "arn:aws:ecs:ap-northeast-1:123456789012:container/simple-ecs-cluster/e40860c2b55a4200b03c3197f6c59714/b31c78c2-9905-4b57-bfc1-e9f8a3689607",
      "Networks": [
        {
          "NetworkMode": "awsvpc",
          "IPv4Addresses": [
            "172.31.2.72"
          ],
          "AttachmentIndex": 0,
          "MACAddress": "0a:ae:b6:d3:34:7d",
          "IPv4SubnetCIDRBlock": "172.31.0.0/20",
          "DomainNameServers": [
            "172.31.0.2"
          ],
          "DomainNameSearchList": [
            "ap-northeast-1.compute.internal"
          ],
          "PrivateDNSName": "ip-172-31-2-72.ap-northeast-1.compute.internal",
          "SubnetGatewayIpv4Address": "172.31.0.1/20"
        }
      ],
      "Snapshotter": "overlayfs"
    }
  ],
  "ClockDrift": {
    "ClockErrorBound": 0.556966,
    "ReferenceTimestamp": "2024-07-29T07:57:08Z",
    "ClockSynchronizationStatus": "SYNCHRONIZED"
  },
  "EphemeralStorageMetrics": {
    "Utilized": 281,
    "Reserved": 20496
  }
}
```

## タスクエンドポイントに対してリクエスト（ECS_CONTAINER_METADATA_URI_V4/task/stats）

```bash
curl $ECS_CONTAINER_METADATA_URI_V4/task/stats | jq .
```

```json
{
  "e40860c2b55a4200b03c3197f6c59714-2886439692": {
    "read": "2024-07-29T08:13:26.739041788Z",
    "preread": "2024-07-29T08:13:16.739724087Z",
    "pids_stats": {},
    "blkio_stats": {
      "io_service_bytes_recursive": [
        {
          "major": 259,
          "minor": 0,
          "op": "Read",
          "value": 0
        },
        {
          "major": 259,
          "minor": 0,
          "op": "Write",
          "value": 11169792
        },
        {
          "major": 259,
          "minor": 0,
          "op": "Sync",
          "value": 1519616
        },
        {
          "major": 259,
          "minor": 0,
          "op": "Async",
          "value": 9650176
        },
        {
          "major": 259,
          "minor": 0,
          "op": "Discard",
          "value": 0
        },
        {
          "major": 259,
          "minor": 0,
          "op": "Total",
          "value": 11169792
        }
      ],
      "io_serviced_recursive": [
        {
          "major": 259,
          "minor": 0,
          "op": "Read",
          "value": 0
        },
        {
          "major": 259,
          "minor": 0,
          "op": "Write",
          "value": 65
        },
        {
          "major": 259,
          "minor": 0,
          "op": "Sync",
          "value": 47
        },
        {
          "major": 259,
          "minor": 0,
          "op": "Async",
          "value": 18
        },
        {
          "major": 259,
          "minor": 0,
          "op": "Discard",
          "value": 0
        },
        {
          "major": 259,
          "minor": 0,
          "op": "Total",
          "value": 65
        }
      ],
      "io_queue_recursive": [],
      "io_service_time_recursive": [],
      "io_wait_time_recursive": [],
      "io_merged_recursive": [],
      "io_time_recursive": [],
      "sectors_recursive": []
    },
    "num_procs": 0,
    "storage_stats": {},
    "cpu_stats": {
      "cpu_usage": {
        "total_usage": 8569211589,
        "percpu_usage": [
          3072683178,
          5496528411
        ],
        "usage_in_kernelmode": 1340000000,
        "usage_in_usermode": 6480000000
      },
      "system_cpu_usage": 4832340000000,
      "online_cpus": 2,
      "throttling_data": {
        "periods": 0,
        "throttled_periods": 0,
        "throttled_time": 0
      }
    },
    "precpu_stats": {
      "cpu_usage": {
        "total_usage": 8557380835,
        "percpu_usage": [
          3066368951,
          5491011884
        ],
        "usage_in_kernelmode": 1330000000,
        "usage_in_usermode": 6480000000
      },
      "system_cpu_usage": 4812420000000,
      "online_cpus": 2,
      "throttling_data": {
        "periods": 0,
        "throttled_periods": 0,
        "throttled_time": 0
      }
    },
    "memory_stats": {
      "usage": 60432384,
      "max_usage": 125136896,
      "stats": {
        "active_anon": 0,
        "active_file": 18788352,
        "cache": 22437888,
        "dirty": 0,
        "hierarchical_memory_limit": 3221225472,
        "hierarchical_memsw_limit": 9223372036854772000,
        "inactive_anon": 33251328,
        "inactive_file": 3514368,
        "mapped_file": 0,
        "pgfault": 129525,
        "pgmajfault": 0,
        "pgpgin": 105303,
        "pgpgout": 91733,
        "rss": 33251328,
        "rss_huge": 0,
        "total_active_anon": 0,
        "total_active_file": 18788352,
        "total_cache": 22437888,
        "total_dirty": 0,
        "total_inactive_anon": 33251328,
        "total_inactive_file": 3514368,
        "total_mapped_file": 0,
        "total_pgfault": 129525,
        "total_pgmajfault": 0,
        "total_pgpgin": 105303,
        "total_pgpgout": 91733,
        "total_rss": 33251328,
        "total_rss_huge": 0,
        "total_unevictable": 0,
        "total_writeback": 135168,
        "unevictable": 0,
        "writeback": 135168
      },
      "limit": 9223372036854772000
    },
    "name": "dev-yamada",
    "id": "e40860c2b55a4200b03c3197f6c59714-2886439692",
    "networks": {
      "eth1": {
        "rx_bytes": 83721227,
        "rx_packets": 59361,
        "rx_errors": 0,
        "rx_dropped": 0,
        "tx_bytes": 663800,
        "tx_packets": 4055,
        "tx_errors": 0,
        "tx_dropped": 0
      }
    },
    "network_rate_stats": {
      "rx_bytes_per_sec": 4.600313866074172,
      "tx_bytes_per_sec": 5.400368451478376
    }
  }
}
```

## 参考

- [Fargate のタスク用の Amazon ECS タスクメタデータエンドポイントバージョン 4](https://docs.aws.amazon.com/ja_jp/AmazonECS/latest/developerguide/task-metadata-endpoint-v4-fargate.html)
- [Fargate のタスク用の Amazon ECS タスクメタデータ v4 JSON レスポンス](https://docs.aws.amazon.com/ja_jp/AmazonECS/latest/developerguide/task-metadata-endpoint-v4-fargate-response.html)
- [Fargate でのタスクの Amazon ECS タスクメタデータ v4 の例](https://docs.aws.amazon.com/ja_jp/AmazonECS/latest/developerguide/task-metadata-endpoint-v4-fargate-examples.html)
