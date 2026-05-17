# AWS-Serverless-Services-PROJECT-1

This project demonstrates how to deploy a basic serverless web application using **AWS Lambda**, **Amazon API Gateway**, and **Amazon DynamoDB**. The application loads a "Contact Us" form in the browser and successfully stores user-submitted information into a DynamoDB table.

---

## Architecture Overview
* **AWS IAM:** Manages permissions for the Lambda function to interact with DynamoDB.
* **AWS Lambda (Python 3.10):** Hosts the backend logic and serves the HTML frontend.
* **Amazon DynamoDB:** Stores the submitted form data (NoSQL database).
* **Amazon API Gateway:** Provides the public HTTP endpoints (Invoke URL) to trigger the Lambda function.

---

## Deployment Steps

### Step 1: Create an IAM Role for the Lambda Function
First, we need to create an IAM role that grants our Lambda function permission to execute and write to our DynamoDB database.

1. Navigate to the **IAM** dashboard in the AWS Management Console.
2. Go to **Roles** -> **Create Role**.
3. Under **Trusted entity type**, select **AWS Service**.
4. Under **Use Case**, select **Lambda**, then click **Next**.
5. In the **Add permissions** search bar, find and attach the following two policies:
   * `AWSLambdaBasicExecutionRole`
   * `AmazonDynamoDBFullAccess`
6. Click **Next**, give the role a **Role Name** (e.g., `LambdaDynamoDBRole`), and click **Create Role**.

### Step 2: Create the Lambda Function
Next, we will set up the compute service to run our Python code.

1. Navigate to the **Lambda** dashboard.
2. Click **Create Function**.
3. Provide a **Function Name**.
4. For the **Runtime**, select **Python 3.10**.
5. Under **Change default execution role**, select **Use Existing Role** and choose the IAM role you created in Step 1.
6. Click **Create Function**.
7. **Upload the Code:**
   * Download the project ZIP file (`project_function.zip`) from this GitHub repository.
   * Rename the downloaded ZIP file to match your Lambda function name exactly.
   * In the Lambda code source section, click **Upload from** -> **.zip file** and upload the renamed file.

### Step 3: Create the DynamoDB Table
Now, we set up the database table to store the form submissions.

1. Navigate to the **DynamoDB** dashboard.
2. Click **Create Table**.
3. Set the **Table name** to `vivektable`.
4. Set the **Partition key** to `email` (String).
5. Leave the **Table settings** on **Default settings**.
6. Click **Create Table**.

### Step 4: Configure API Gateway
Finally, we expose the Lambda function to the internet so users can access the web page.

1. Navigate to the **API Gateway** dashboard.
2. Locate **REST API** and click **Build**.
3. Select **New API**, provide an **API Name**, and set the **API endpoint type** to **Regional**.
4. Click **Create API**.

**Configure the GET Method (To load the webpage):**
1. Select the root resource (`/`).
2. Click **Create Method** and select **GET** as the Method type.
3. Enable **Lambda proxy integration**.
4. Select your AWS **Region** and type in the name of your **Lambda function**.
5. Click **Create Method**.

**Configure the POST Method (To submit the form):**
1. Select the root resource (`/`) again.
2. Click **Create Method** and select **POST** as the Method type.
3. Enable **Lambda proxy integration**.
4. Select your AWS **Region** and type in the name of your **Lambda function**.
5. Click **Create Method**.

**Deploy the API:**
1. Click **Deploy API**.
2. Select **[New Stage]** and provide a **Stage name** (e.g., `dev`).
3. Click **Deploy**.
4. Copy the generated **Invoke URL**.

---

## How It Works (Step 5)

Whenever you paste the **Invoke URL** into your web browser, API Gateway triggers the Lambda function via the `GET` method, which loads the "Contact Us" HTML web page. 

When a user fills out the information on that page and clicks submit, the form triggers the `POST` method. The Lambda function processes the request and stores the submitted data securely in the DynamoDB table.

---
**Author:** Vivek Sidu 
