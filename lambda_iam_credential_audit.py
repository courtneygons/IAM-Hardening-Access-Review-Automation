import boto3
import csv

def lambda_handler(event, context):
    iam = boto3.client('iam')

    # Generate a fresh IAM credential report
    response = iam.generate_credential_report()
    while response['State'] != 'COMPLETE':
        response = iam.generate_credential_report()

    # Download and decode the report
    report = iam.get_credential_report()['Content']
    decoded = report.decode('utf-8')

    # Parse CSV
    reader = csv.DictReader(decoded.splitlines())
    flagged_users = []

    for row in reader:
        username = row['user']
        mfa_active = row['mfa_active']
        last_login = row['password_last_used']

        # Skip root account
        if username == '<root_account>':
            continue

        # Flag users without MFA or never logged in
        if mfa_active != 'true' or last_login == 'N/A':
            flagged_users.append({
                'user': username,
                'mfa_active': mfa_active,
                'last_login': last_login
            })

    # Output results
    if not flagged_users:
        print("✅ No identity issues found.")
    else:
        print("⚠️ Flagged IAM Users:")
        for user in flagged_users:
            print(user)

    return {
        'statusCode': 200,
        'body': f'{len(flagged_users)} users flagged'
    }
