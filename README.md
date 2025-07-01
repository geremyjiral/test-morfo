# Technical Test Morfo

## Run

```
docker compose up
```

## Test

```
uv run pytest
```

## Deploy strategy on AWS

### 1. Object Storage: S3
Structure: s3://your-bucket/batch_{1..5}/img_{1..20}.png

Batches are folders, each with 20 images.

### 2. Event Coordination: AWS Step Functions
Coordinates the logic:

- Detects presence of all batches
- Triggers analysis
- Publishes to DB
- Sends notification

### 3. Analysis Code: AWS Lambda or Fargate
#### Lambda:

If image size < 10MB and lightweight processing

Auto-scaling, serverless

#### Fargate (ECS):

If image sizes are large or need more RAM

More control over environment

### 4. Metadata Store: Amazon RDS (PostgreSQL)
Stores stats per batch and color:

avg, std, min, max, batch number, color, timestamp, etc.

### 5. Messaging: SNS / SES / SQS
SNS (Simple Notification Service): to notify users (email/SMS/HTTP).

Optional: notify a downstream queue (SQS or EventBridge) for further automation.


### Trigger Logic
The system needs to wait until 5 batches of 20 images are available:

#### Option A: Polling with Scheduled Lambda

A scheduled Lambda (e.g. every 5 min) checks S3:

list_objects_v2 for each batch

Counts files

If all 5 batches have 20 files → triggers processing

#### Option B: EventBridge + State Tracking

Each PutObject in S3 triggers a Lambda

Lambda updates a DynamoDB counter per batch

When all counts reach 20 → fires the analysis

Option B is more event-driven and reactive.

### Database Schema Proposal (RDS)
| Field           | Type      | Description                        |
| --------------- | --------- | ---------------------------------- |
| `id`            | UUID/INT  | PK                                 |
| `batch_id`      | TEXT      | batch_1 to batch_5                 |
| `color`         | TEXT      | 'black' or 'white'                 |
| `avg_pixels`    | FLOAT     | Average pixels in batch            |
| `std_pixels`    | FLOAT     | Standard deviation                 |
| `min_pixels`    | INT       | Minimum count                      |
| `max_pixels`    | INT       | Maximum count                      |
| `created_at`    | TIMESTAMP | Timestamp of processing            |
| `source_prefix` | TEXT      | S3 path prefix (optional metadata) |


We can also add a user_id or job_id to track requests by user/session.


## Error handling

This project will be used by lambda for small batches, so there isn't error handling and an error will raise directly in lambda

If this project should run with many batches then error handling should be provide to avoid inexpected interuption of the process due to errors.
