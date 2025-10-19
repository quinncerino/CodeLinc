import boto3

def create_user_benefits_table():
    """Create DynamoDB table for user benefits context"""
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    
    try:
        table = dynamodb.create_table(
            TableName='UserBenefitsContext',
            KeySchema=[
                {
                    'AttributeName': 'employee_number',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'employee_number',
                    'AttributeType': 'S'
                }
            ],
            BillingMode='PAY_PER_REQUEST'  # On-demand pricing
        )
        
        # Wait for table to be created
        table.wait_until_exists()
        print(f"Table {table.table_name} created successfully!")
        
    except dynamodb.meta.client.exceptions.ResourceInUseException:
        print("Table 'UserBenefitsContext' already exists.")
    except Exception as e:
        print(f"Error creating table: {e}")

if __name__ == "__main__":
    create_user_benefits_table()