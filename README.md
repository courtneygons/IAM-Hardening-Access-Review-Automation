# IAM Hardening & Access Review Automation

This project implements real-world IAM hardening strategies and access governance automation in AWS. It simulates how a Cloud Security Engineer would secure and audit identity systems in a Zero Trust environment — aligning with DoD and enterprise compliance standards.

---

## Core Objectives

- Enforce **least-privilege IAM access** using groups and scoped policies
- Require **MFA for all IAM users**
- Enable **CloudTrail** for identity auditability
- Automate **access reviews** using credential reports and Lambda
- Flag identity risks such as missing MFA or unused credentials

---

## Project Structure

| Component                        | Purpose                                                                 |
|----------------------------------|-------------------------------------------------------------------------|
| IAM Groups & Policies            | Role-based access control (Admins, Auditors, Developers)               |
| Scoped Policy (`ScopedDeveloperAccess`) | Fine-grained access to EC2 + S3                                       |
| MFA Enforcement                  | Enabled MFA for all lab users using Authenticator App                   |
| CloudTrail                       | Multi-region logging for IAM activity                                  |
| Credential Report Analysis       | CSV-based review of password, access key, and MFA status               |
| Lambda Automation                | Flags IAM users who violate identity security baselines                |

---

## Lambda Automation: `iam-credential-audit`

### Language:
Python 3.12 (runtime: AWS Lambda)

### Actions:
- Calls `GenerateCredentialReport` and parses CSV
- Flags users with:
  - `mfa_active: false`
  - `password_last_used: N/A`
- Outputs flagged users to CloudWatch

### Sample Log Output:
```json
{
  "user": "admin-user",
  "mfa_active": "false",
  "last_login": "2025-04-29T13:01:15Z"
}
