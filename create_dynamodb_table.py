import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

try:
    table = dynamodb.create_table(
        TableName='UserBenefitsContext',
        KeySchema=[
            {'AttributeName': 'employee_number', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'employee_number', 'AttributeType': 'S'}
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    
    print("Creating table...")
    table.wait_until_exists()
    print("✅ Table created successfully!")
    print(f"Table status: {table.table_status}")
    
except Exception as e:
    print(f"Error: {e}")
    print("Table may already exist or check your AWS permissions.")