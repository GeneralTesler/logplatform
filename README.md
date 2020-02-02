# Log Search Platform

## Services

- Kafka (+Zookeeper): Used for initial ingestion
- Fluentd: transitions logs from Kafka to Minio
- Minio: Log storage
- Drill: Log querying
- Jupyter: Front-end for queries

## Setup

- Move **example.env** to **.env** and fill out variables
  - COMPOSE_ROOT = root directory of project
- Change **KAFKA_ADVERTISED_HOST_NAME** in Kafka service to your IP
- (Optional) Change **MINIO_ACCESS_KEY** and **MINIO_SECRET_KEY** in Minio and Fluentd services
  - If you do, also change values in **drill/core-sites.xml**

## Jupyter Additions

### Exposed Objects/Functions

- "drill" : [PyDrill](https://github.com/PythonicNinja/pydrill) object for managing connection to Drill
  - tip: use "drill.is_active()" to check connection

### Magic Queries

```
%query   : query drill
           Example: %query select * from minio.root.logs

%tquery  : time-bound %query; time in minutes
           Example: %tquery select * from minio.root.logs 10
         
%wquery  : query drill and filter dataframe to winlog data (also flatten json)
           Example: %wquery select * from minio.root.logs
         
%twquery : time-bound %wquery; time in minutes
           Example: %twquery select * from minio.root.logs 10
```

*Note: use "minio.root.logs" to access logs*

## Example Winlogbeat Config

```
winlogbeat.event_logs:
  - name: Application
  - name: Security
  - name: System
  - name: Microsoft-windows-sysmon/operational
  - name: Microsoft-windows-PowerShell/Operational
    event_id: 4103, 4104
  - name: Windows PowerShell
    event_id: 400,600
  - name: Microsoft-Windows-WMI-Activity/Operational
    event_id: 5857,5858,5859,5860,5861
output.kafka:
  hosts: ["<IP>:9092"]
  topic: "winlogbeat"
  max_retries: 2
  max_message_bytes: 1000000
```

based on: https://github.com/Cyb3rWard0g/HELK/blob/master/configs/winlogbeat/winlogbeat.yml

## Some Limitations

- Currently, this only set-up to work with Winlogbeat as that is my primary use case
  - if you want to add additional sources, simply adjust the **KAFKA_CREATE_TOPICS** environment variable in the Kafka service to include an additional topic then clone both blocks in **fluentd/fluent.conf**
