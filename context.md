# Global Data Science Challenge 8: Green Agents of Change

## PROJECT CONTEXT

Global Data Science Challenge: Green Agents of Change
We are hosting the 8th edition of the Global Data Science Challenge: Green Agents of Change. This year we're teaming up with UNICEF to help young people drive climate action where it counts, through meaningful, sustainable careers.

Our focus: empowering youth across Brazil to explore, discover, and pursue green and future-proof jobs. 

The challenge: collaborate with AI agents to sift through heaps of job descriptions and training opportunities across Brazil, match people to roles that fit their preferences and potential, and recommend concrete learning paths to get there. That means retrieval over real data (not just model memory), thoughtful matching and ranking, and smart prompt engineering.

Mistral LLM models will serve as brains for our AI agents. AWS is the cloud infra of choice for this challenge.

## Data

The dataset will include three sets:

1. **Personas**: fictional beneficiaries with a profile, constraints, and objectives. Each persona is a Mistral agent with its own custom prompt and hosted on an AWS API endpoint for participants to interact with through their solution and fetch required details about the persona to be able to make a match with job/trainings/awareness recommendations.

2. **Jobs**: structured job offers in template json in markdown format. These will be hosted on AWS S3 bucket.

3. **Trainings**: relevant training programs in template json in markdown format. These will be hosted on AWS S3 bucket.

For each persona, participant solution should define an **expected gold output** indicating the correct outcome (jobs, trainings, or awareness).

## Data Schemas

### Persona

```json
{
  "id": "pers_001",
  "domain_focus": "Marketing",
  "age": 25,
  "education_level": "Bachelor's Degree",
  "years_experience": 2,
  "current_role": "Communications Officer",
  "skills": [{"name": "SEO", "level": 3}, {"name": "Copywriting", "level": 2}],
  "interests": [{"name": "Brand strategy", "weight": 0.7}, {"name": "Data analytics", "weight": 0.3}],
  "constraints": {"location": "Paris", "mobility": "low", "contract": "Permanent"},
  "reason_for_consult": "Wants to move into a marketing project manager role",
  "expected_output_type": "jobs"
}
```

**Skill levels**: scale 0 to 4 (0 = none, 4 = expert).
**Possible constraints**: location, mobility, contract type, language, working hours, seniority, age.

### Job

```json
{
  "id": "job_001",
  "domain": "Marketing",
  "title": "Digital Marketing Project Manager",
  "seniority": "mid-level",
  "required_skills": [{"name": "SEO", "min_level": 3}, {"name": "Project Management", "min_level": 2}],
  "nice_to_have": [{"name": "HTML", "min_level": 1}],
  "location": "Paris",
  "contract": "Permanent",
  "tasks": ["Coordinate digital campaigns", "Analyze KPIs"],
  "salary_band": "35-45k€",
  "language": "FR"
}
```

### Training

```json
{
  "id": "tr_001",
  "domain": "Marketing",
  "title": "Digital Project Management Training",
  "outcomes": [{"name": "Project Management", "target_level": 3}, {"name": "SEO", "target_level": 4}],
  "prerequisites": [{"name": "Project Management", "min_level": 1}],
  "duration_weeks": 8,
  "format": "online",
  "language": "FR",
  "certification": true
}
```

## Matching Rules 

### Hard Filters

A job is incompatible if:
- Seniority is insufficient.
- Location/mobility are incompatible.
- Required language not mastered.
- Domain different from `domain_focus` if `domain_lock: true`.
- Contract type or working hours not desired.

### Skill Coverage

- Calculation:
  ```
  coverage = (# required skills satisfied) / (total required skills)
  ```
- A skill is satisfied if `level_persona ≥ min_level_job`.
- Compatible if `coverage ≥ 0.70` after passing hard filters.

## Determining the Expected Gold Output (V1)

### Case 1: Jobs

- Personas seeking a job.
- Apply hard filters and the 70% skill coverage rule.
- `gold_type = jobs`.
- `gold_items` = list of compatible jobs (possibly empty), sorted by coverage and interest alignment.
- Suggest jobs even if `coverage < 0.70`, along with trainings to fill skill gaps.
- Gold enriched with:

```json
{
  "persona_id": "pers_001",
  "gold_type": "jobs_with_upskilling",
  "items": [
    {
      "job_id": "job_001",
      "gap_skills": ["Project Management"],
      "trainings": ["tr_001"]
    }
  ]
}
```

### Case 2: Trainings

- Personas explicitly seeking to train.
- Identify their learning objectives.
- `gold_type = trainings`.
- `gold_items` = trainings matching the objectives.

### Case 3: Awareness

- Minors (<16) or personas seeking general information.
- `gold_type = awareness`.
- No recommendations required.

### Sample gold file

```json
{"persona_id": "pers_tou_001", "gold_type": "trainings_only", "trainings": ["tr_tou_cultural_awareness_02", "tr_tou_problem_solving_02"]}
{"persona_id": "pers_tou_002", "gold_type": "jobs+trainings", "jobs": [{"job_id": "job_tou_010", "suggested_trainings": []}]}
{"persona_id": "pers_tou_003", "gold_type": "awareness", "gold_items": "too_young"}
{"persona_id": "pers_tou_004", "gold_type": "trainings_only", "trainings": ["tr_tou_multilingual_communication_02"]}
{"persona_id": "pers_tou_005", "gold_type": "trainings_only", "trainings": ["tr_tou_marketing_and_promotion_tourism__03"]}
```

The solution will also be graded based on how green it is i.e. optimal use of resources, LLM tokens etc.

The participant population is expected to be a mix of technical and non technical folks with varying degrees of coding experience.
We intend to provide them relevant trainings before diving into the challenge.

---

# EXAMPLE TRAININGS FROM GDSC 7 CONTEXT

Below are the sample trainings from last year:

## Tutorial 1: Set up your account for GDSC 2024

Welcome to the first tutorial of the 2024 GDSC: The Grade-AI Generation! The tutorials will teach you all the necessary steps to participate in (and hopefully win) the challenge. 

This first tutorial covers the (boring) groundwork that we need to cover before we can jump into the AI parts. It explains how to create an account, sign in, create and join a team and how to access AWS.

But before we jump in make sure you join the [GDSC Teams channel](https://teams.microsoft.com/l/team/19%3a4017a2e9af4942e7aa157d6ec9d751b4%40thread.skype/conversations?groupId=7d77d672-dff1-4c9f-ac55-3c837c1bebf9&tenantId=76a2ae5a-9f00-4f6b-95ed-5d33d77c4d61/) for all updates from the organisation team and meeting and connecting with other participants. This is also the place to ask questions if you are stuck.

Here is a quick overview of what we'll cover:

- [1. Signing up and logging to the website](#1-signing-up-and-logging-to-the-website)
- [2. Creating and joining a team](#2-creating-and-joining-a-team)
- [3. Setting up your AWS accounts](#3-setting-up-your-aws-accounts)
- [4. How to use AWS](#4-how-to-use-aws)
  - [4.1. Accessing GenAI Models with AWS Bedrock](#41-accessing-genai-models-with-aws-bedrock)
  - [4.2. Managing source code with AWS CodeCommit](#42-managing-source-code-with-aws-codecommit)
  - [4.3. Developing AI solutions with Sagemaker](#43-developing-ai-solutions-with-sagemaker)
  - [4.4. Keeping track of the costs](#44-keeping-track-of-the-costs)
- [5. Running the tutorials](#5-running-the-tutorials)
- [6. Conclusion](#6-conclusion)
- [7. Appendix - Where to develop your solution](#7-appendix---where-to-develop-your-solution)
  - [7.1. With AWS Sagemaker](#71-with-aws-sagemaker)
  - [7.2. On your laptop](#72-on-your-laptop) 

### 1. Signing up and logging to the website:

The very first thing you need to do to participate in the GDSC is to sign up! Here's how:

1. Navigate to the GDSC Portal's Sign-up page - [https://gdsc.ce.capgemini.com/app/signup/](https://gdsc.ce.capgemini.com/app/signup/). Make sure to enter your Capgemini email. The full name is not mandatory to sign up, but it is necessary to receive a certificate of completion after the challenge.

2. Once you Sign-up, you will receive an e-mail from gdsc.ce@capgemini.com.

3. Please click on the Verification link provided in the e-mail. You will receive an error but do not worry, you can now login to the website.

4. To login to the website, navigate to the login page - [https://gdsc.ce.capgemini.com/app/login/](https://gdsc.ce.capgemini.com/app/login/) and enter your credentials.

5. Once you login you will have access to the Resources - [https://gdsc.ce.capgemini.com/app/portal/resources/](https://gdsc.ce.capgemini.com/app/portal/resources/).

### 2. Creating and joining a team

The next step is to form or join a team. Every participant needs to be in a team to participate in a challenge. You have three options:
* Create a team only for yourself
* Create a team, find other people to join, share their team id with them. They will request to join and you can accept
* Request to join an existing team

We highly recommend that you form a team with other participants. This will help you to share ideas, learn from each other and have a better chance of winning the challenge.

If you don't have a team, you can find other people in the GDSC Teams channel ['Looking for Team'](https://teams.microsoft.com/l/channel/19%3Aa32e03d38fc940ee9d4b20a7cc9e030d%40thread.skype/Looking%20for%20Team?groupId=7d77d672-dff1-4c9f-ac55-3c837c1bebf9&tenantId=76a2ae5a-9f00-4f6b-95ed-5d33d77c4d61).

To actually create a new team you need to:

1. Go to the 'My Team 'page - [https://gdsc.ce.capgemini.com/app/portal/](https://gdsc.ce.capgemini.com/app/portal/).

2. Enter your team name (keeping in mind that there is a prize for the 'best' name) and press the 'Create Team' button.

3. Once a team is created, you are assigned a Team ID and an AWS account.

### 3. Setting up your AWS accounts

AWS is an integral part of the GDSC. It is where you will be developing your solution and accessing the LLM models. You will be assigned an AWS account when you create a team.

### 4. How to use AWS

Almost done! Now that you have access to AWS, let's see how you can use it for the GDSC.

#### 4.1. Accessing GenAI Models with AWS Bedrock

Large Language Models (LLM) are the core of the GDSC. We'll access them via AWS Bedrock. The `Base models` lists all models that are available on AWS. For the GDSC, we gave you access to Claude 3 Haiku and Claude 3.5 Sonnet.

#### 4.2. Managing source code with AWS CodeCommit

Source code is usually managed via a version control system like Git. AWS CodeCommit is a managed service that hosts secure Git repositories.

To test your code before submitting a solution, you'll need to push it to the branch `test_submission`. 
To actually submit a solution you need to push the code to the branch `submission`.

#### 4.3. Developing AI solutions with Sagemaker

AWS Sagemaker is a fully managed service that provides every developer and data scientist with the ability to build, train, and deploy machine learning models quickly.

#### 4.4. Keeping track of the costs

Finally, it is important to keep track of the costs of the AWS services you are using. Each teams gets a fixed budget every week. **If you spent more than your budget, you will not be able to access the services anymore for the rest of the week!**

---

## Tutorial 2 - Understanding the PIRLS dataset

Welcome in the next part of our tutorials for Global Data Science Challenge 2024. Today, we embark on a comprehensive exploration of our dataset for this year's GDSC, featuring the PIRLS 2021 dataset.

This tutorial is structured into three primary components: a video, a website, and this notebook. To begin, I recommend watching the [PIRLS 2021 video](https://youtu.be/jUv1QowWmqI?feature=shared), which provides a solid foundation on what this study encompasses.

The goal of the GDSC is to build AI agents that automatically answer complex questions about educational topics, utilizing the PIRLS 2021 data.

### Agenda

1. [Set up the environment](#set-up-the-environment) - Provides all the essential functions needed to configure the environment for developing and executing queries

2. [The database schema](#the-database-schema) - Describes the structure of the relational database
    - [The database overview](#the-database-overview) - Offers a high-level overview of the database schema
    - [Tables about student questionnaires](#tables-about-student-questionnaires) - Delves into the specifics of the tables related to student questionnaires
    - [Tables about student achievement scores](#tables-about-student-achievement-scores) - Explores the specifics of the tables related to student achievement scores
    - [Tables about school, home, and curriculum questionnaires](#tables-about-school-home-and-curriculum-questionnaires) - Highlights key points for the tables related to school, home, and curriculum questionnaires
    - [Table about teacher questionnaires](#table-about-teacher-questionnaire) - Highlights key points for the tables related to teacher questionnaires
        
3. [Querying the database](#querying-the-database) - Demonstrates how to effectively extract meaningful insights from the database
    - [Show available tables](#show-available-tables)
    - [Understanding the content of a table](#understanding-the-content-of-a-table)
    - [Example graphs for visualizing data](#example-graphs-for-visualizing-data)
    - [What types of questions to expect during the challenge](#what-types-of-questions-to-expect-during-the-challenge)
    
4. [Conclusion](#conclusion) - Summarizes what we learned and how to proceed
  
5. [Appendix](#appendix) - Additional resources
    - [More example questions with SQL queries](#more-example-questions-with-sql-queries)

### Set up the environment

Firstly we install and import necessary python modules.

```python
# Installing necessary modules
!pip install psycopg2-binary pandas seaborn matplotlib
```

```python
import psycopg2 # module for connecting to a PostgreSQL database
import pandas as pd  # module for data manipulation and analysis

import seaborn as sns # library for visualization of data
import matplotlib.pyplot as plt # library for visualization of data

pd.set_option('display.max_colwidth', None) # display all the contents of a column
```

We define the login information for the database:

```python
DB_ENDPOINT = 'INSERT DB URL HERE'
DB_PORT = '5432'
DB_USER = 'INSERT USER HERE'
DB_PASSWORD ='INSERT PASSWORD HERE'
DB_NAME ='postgres'
```

And some helper functions for database connectivity:

```python
def create_connection() -> psycopg2.extensions.connection:
    """
    Creates a connection to the PostgreSQL database.
    """
    return psycopg2.connect(
        host=DB_ENDPOINT,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def get_from_db(connection: psycopg2.extensions.connection, query: str) -> pd.DataFrame:
    """
    Executes the given SQL query on the provided database connection and returns the result as a pandas DataFrame.
    """
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
    except psycopg2.Error as e:
        print(f"Error executing query: {e}")
        return pd.DataFrame()

    return pd.DataFrame(result, columns=column_names)
```

Establish a connection with the database:

```python
connection = create_connection()
```

Test connection:

```python
query_connection_check = '''
        SELECT * FROM Countries
'''
query_connection_check_df = get_from_db(connection, query_connection_check)
query_connection_check_df
```

**[Example output placeholder - Countries table with country_id, code, name, benchmark, testtype columns]**

### The Database Schema

#### The database overview

The dataset is pretty massive and quite complex. The biggest subtable has over 27 millions rows! But fear not! We've done the heavy lifting for you and organized the data into a more convenient structure. We've uploaded the data to a relational database based on this schema.

![Database Schema](../images/t2_db_schema.png)

#### Tables about student questionnaires

All the green boxes in the diagram above are related to students. To simplify things, we've divided the green section into smaller parts: one for the questionnaire and the other for students' achievement scores.

Every block in this diagram represents a table. `Students` is the main table for the whole dataset. Each student in the `Students` table has:
- a primary key (PK) **Student_ID** and several foreign keys (FK), such as 
- **Country_ID**, indicating the student's country of origin, 
- **School_ID**, indicating the school the student attends, and 
- **Home_ID**, indicating the student's parents or guardians.

Data about student questionnaires are split into two tables:
- The `Student Questionnaire Entries` table lists the questions that the students were asked
- The `Student Questionnaire Answers` table contains the answers to the questions

Example query to get student answers:

```sql
SELECT * FROM StudentQuestionnaireAnswers
WHERE Student_ID = 51250010201 AND Code='ASBG01';
```

**[Example output placeholder]**

To find the question text:

```sql
SELECT * FROM StudentQuestionnaireEntries
WHERE Code='ASBG01';
```

**[Example output placeholder]**

Combined query to get questions and answers:

```sql
SELECT S.Student_ID, E.Code, E.Question, A.Answer, E.Type FROM Students AS S
LEFT JOIN StudentQuestionnaireAnswers AS A ON S.Student_ID = A.Student_ID
LEFT JOIN StudentQuestionnaireEntries AS E ON A.Code = E.Code
LIMIT(750);
```

**[Example output placeholder]**

#### Tables about student achievement scores

Moving on to the next segment, we're diving into students' achievement scores. The setup is similar to what we've seen before. In the `StudentScoreEntries` table, you'll find the **Code** for each score, the **Name** of the score, and a **Type** field. The `StudentScoreResults` table contains the actual **Score** values.

Example query for student scores:

```sql
SELECT * FROM StudentScoreResults
WHERE Student_ID = 51250010201 AND Code='ASRREA_avg';
```

**[Example output placeholder]**

Combined query for scores:

```sql
SELECT S.Student_ID, E.Code, E.Name, R.Score, E.Type FROM Students AS S
LEFT JOIN StudentScoreResults AS R ON S.Student_ID = R.Student_ID
LEFT JOIN StudentScoreEntries AS E ON R.Code = E.Code
LIMIT(100);
```

**[Example output placeholder]**

##### Clarification - Student Score Entries

The `Student Score Entries` table contains information about different types of scores:

```sql
SELECT * FROM StudentScoreEntries;
```

**[Example output placeholder - showing score types like ASRREA_avg, ASRLIT_avg, etc.]**

The test was segmented into four distinct sections:
- **Literary Experience** (ASRLIT)
- **Acquire and Use Information** (ASRINF)
- **Interpreting, Integrating and Evaluating** (ASRIIE)
- **Retrieving and Straightforward Inferencing** (ASRRSI)
- **Overall Reading Score (ASRREA)** - aggregates overall performance

Each score has two metrics: average and standard deviation.

##### Clarification - Benchmarks

The `Benchmarks` table stores benchmark information:

```sql
SELECT * FROM Benchmarks;
```

**[Example output placeholder showing benchmark levels: Low (400), Intermediate (475), High (550), Advanced (625)]**

A benchmark is a marker used to measure reading abilities. If a student scores 700, they've met all benchmark levels below that score.

### Querying the database

#### Show available tables

Here is a listing of all tables within our database schema:

```python
query = '''
        SELECT table_name FROM information_schema.tables
        WHERE table_schema='public'
        '''
table_names_df = get_from_db(connection, query)

# Initialize an empty list to store the results
results = []

# Iterate over the table names, count the rows, and append the results
for table_name in table_names_df['table_name']:
    count_query = f"SELECT COUNT(*) as row_count FROM {table_name}"
    row_count_df = get_from_db(connection, count_query)
    row_count = row_count_df.iloc[0]['row_count']
    results.append({'Table Name': table_name, 'Number of Rows': row_count})

# Convert the results into a DataFrame
results_df = pd.DataFrame(results)
results_df = results_df.sort_values(by='Number of Rows')
```

**[Example output placeholder - table showing all database tables and their row counts]**

#### Understanding the content of a table

To understand a table structure:

```python
query_countries_info = '''
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_name = 'countries'
    '''
df_countries_info = get_from_db(connection, query_countries_info)
```

**[Example output placeholder - showing column names and data types for countries table]**

To see table content:

```python
query_countries = '''
        SELECT * FROM Countries;
        '''
df_countries = get_from_db(connection, query_countries)
```

**[Example output placeholder - showing sample country data]**

#### Example graphs for visualizing data

Example query for visualizing student scores:

```python
query_graph = '''
    SELECT S.Student_ID, R.Score
    FROM Students AS S
    LEFT JOIN StudentScoreResults AS R ON S.Student_ID = R.Student_ID
    LEFT JOIN StudentScoreEntries AS E ON R.Code = E.Code
    WHERE E.Code = 'ASRREA_avg';
'''

df_graph = get_from_db(connection, query_graph)
```

**[Example output placeholder]**

Create visualization:

```python
plt.figure(figsize=(10, 6))
plt.hist(df_graph['score'], bins=30, edgecolor='black')
plt.title('Distribution of Student Scores')
plt.xlabel('ASRREA_avg')
plt.ylabel('Count')
plt.grid(True)
plt.show()
```

**[Example graph placeholder showing score distribution]**

#### What types of questions to expect during the challenge

Here are the types of questions your solutions will need to tackle. We'll walk through an example question step by step:

**Example Question 1: "Which country had all schools closed for more than eight weeks?"**

##### 1. Question Analysis
The objective is to identify countries where all schools experienced closures for more than eight weeks due to the COVID-19 pandemic.

##### 2. Table Selection
We'll utilize these tables:
- `Countries`: Contains information about participating countries
- `Schools`: Holds details about schools
- `School questionnaire entries`: Stores questions from the school questionnaire
- `School questionnaire answers`: Contains responses to school questionnaire questions

##### 3. Query Development

First, find question types:

```sql
SELECT DISTINCT Type FROM SchoolQuestionnaireEntries;
```

**[Example output placeholder showing question types including "COVID-19 Pandemic"]**

Find COVID-19 related questions:

```sql
SELECT * FROM SchoolQuestionnaireEntries
WHERE Type = 'COVID-19 Pandemic';
```

**[Example output placeholder showing COVID-19 questions]**

Find possible answers to the relevant question:

```sql
SELECT DISTINCT Answer 
FROM SchoolQuestionnaireAnswers
WHERE Code = 'ACBG19';
```

**[Example output placeholder showing possible answers including "More than eight weeks of instruction"]**

Get schools with closures > 8 weeks:

```sql
SELECT C.Name, S.School_ID, SQA.Code, SQA.Answer FROM SchoolQuestionnaireAnswers AS SQA
JOIN Schools AS S ON S.School_ID = SQA.School_ID
JOIN Countries AS C ON C.Country_ID = S.Country_ID
WHERE SQA.Code = 'ACBG19' AND SQA.Answer = 'More than eight weeks of instruction';
```

**[Example output placeholder showing schools with extended closures]**

Count schools per country:

```sql
SELECT C.Name, COUNT(S.School_ID) AS schools_in_country
FROM Schools AS S
JOIN Countries AS C ON C.Country_ID = S.Country_ID
GROUP BY C.Name;
```

**[Example output placeholder showing school counts by country]**

Final query to find countries with 100% school closures:

```sql
WITH schools_all AS (
    SELECT C.Name, COUNT(S.School_ID) AS schools_in_country
    FROM Schools AS S
    JOIN Countries AS C ON C.Country_ID = S.Country_ID
    GROUP BY C.Name
),
schools_closed AS (
    SELECT C.Name, COUNT(DISTINCT SQA.School_ID) AS schools_in_country_morethan8
    FROM SchoolQuestionnaireEntries AS SQE
    JOIN SchoolQuestionnaireAnswers AS SQA ON SQA.Code = SQE.Code
    JOIN Schools AS S ON S.School_ID = SQA.School_ID
    JOIN Countries AS C ON C.Country_ID = S.Country_ID
    WHERE SQE.Code = 'ACBG19' AND SQA.Answer = 'More than eight weeks of instruction'
    GROUP BY C.Name
),
percentage_calc AS (
    SELECT A.Name, schools_in_country_morethan8 / schools_in_country::float * 100 AS percentage
    FROM schools_all A
    JOIN schools_closed CL ON A.Name = CL.Name
)
SELECT *
FROM percentage_calc
WHERE percentage = 100;
```

**[Example output placeholder showing Czech Republic with 100.0%]**

#### Key insights

- **Query Construction Skills**: Developing precise queries is vital for effective data analysis
- **Data Understanding Tools**: Visualization libraries like seaborn and matplotlib are powerful for data exploration

### Exercises

Practice questions for you to try:

1. What was Egypt's average score for fourth graders in reading?
2. What percentage of students in Germany met the high reading standards?
3. How many countries reported that at least 85% of their students reached the Low International Benchmark?

### Conclusion

In this tutorial, we learned about the PIRLS 2021 database structure, saw examples of content and how to access it. This understanding is crucial for building successful AI systems.

---

## Tutorial 3 - Introduction to AI Agents

After getting to know the data, it's time to build our first generative AI solution.

### What is Generative AI?

Generative AI refers to artificial intelligence systems that can create new content, ideas, or solutions. Unlike traditional AI that primarily analyzes existing data, GenAI can produce original text, images, code, or even music.

### Why AI Agents?

AI agents take GenAI a step further. An AI agent is like a virtual assistant with a specific role, expertise, and set of goals. Learning about AI agents is valuable because:

- Automation of Complex Tasks
- Enhanced Problem-Solving  
- Personalized Experiences
- Improved Decision-Making
- Future-Proofing Your Skills

### Agenda

1. [What are AI agents](#what-are-ai-agents)
2. [Hello GenAI World](#hello-genai-world)
3. [Building Our First AI Agent](#building-our-first-ai-agent)
4. [Creating a first solution](#creating-a-first-solution)
5. [Conclusion](#conclusion)
6. [Appendix](#appendix)

### What are AI Agents?

AI agents are like smart digital assistants with specific roles and goals. They use large language models (LLMs) to perform tasks, make decisions, and solve problems.

Key components of an AI agent system:

1. **Agents**: Core "actors" with specific roles, skills, goals, and decision-making abilities
2. **Tools**: Functions or capabilities that agents can use (code execution, database queries, web search, etc.)
3. **Tasks**: Specific jobs or objectives assigned to agents
4. **Crew**: A group of agents working together to achieve a common goal

### Hello GenAI World

Before building complex AI agent systems, we need to understand how to interact with Large Language Models (LLMs).

#### Setting Up Amazon Bedrock

```python
# Install required packages
!pip install crewai -r ../requirements.txt
```

```python
import dotenv
assert dotenv.load_dotenv()
```

```python
# Import required libraries
import os
from langchain_aws import ChatBedrock

# Set up the model ID for Claude
MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"

# Initialize the ChatBedrock instance
llm = ChatBedrock(model_id=MODEL_ID, model_kwargs={'temperature': 0})
```

#### Your First Interaction with the LLM

```python
message = [
    ("system", "You are a helpful assistant that translates English to French."),
    ("human", "Translate the following sentence: 'Hello, world!'")
]

response = llm.invoke(message)
print(response)
```

**[Example output placeholder showing French translation]**

### Building Our First AI Agent

Now let's build a Python Help Crew using CrewAI consisting of:
1. A Python Developer agent that writes code
2. A Tester agent that evaluates and tests the code

```python
# Imports
import os
from crewai import Agent, Crew, Process, Task
from crewai.project import agent, crew, task
from langchain_aws import ChatBedrock
from langchain_core.tools import tool
```

```python
class PythonHelpCrew:
    def __init__(self, llm: ChatBedrock) -> None:
        self.llm = llm

    def run(self, prompt: str) -> str:
        self.prompt = prompt
        return self.crew().kickoff().raw

    @agent
    def pythonDeveloper(self) -> Agent:
        return Agent(
            role="Python developer", 
            backstory="Experienced Python developer with deep knowledge in Python programming.",
            goal="Write a Python code to solve the user's question.",
            llm=self.llm,
            allow_delegation=False,
            verbose=True)

    @agent
    def tester(self) -> Agent:
        return Agent(
            role="Tester",
            backstory="Experienced tester with deep knowledge in testing and using provided tools.",
            goal="Test the Python code to ensure it works correctly. Only if you are sure that there is an issue with the code, send it back to the Python developer.",
            llm=self.llm,
            allow_delegation=True,
            tools = [eval_python_code],
            verbose=True)

    @task
    def code_python_task(self) -> Task: 
        return Task(
            description=f"Write a python code to solve the user's question: {self.prompt}.",
            expected_output="Python code that solves the user's question. Only return Python code. NO additional explanations.",
            agent=self.pythonDeveloper())
    
    @task
    def test_code_task(self) -> Task:
        return Task(
            description="Test the python code to ensure it works correctly.",
            expected_output="Only the tested Python code. NO additional explanations.",
            agent=self.tester())

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            max_iter=5,
            cache=False
        )

@tool
def eval_python_code(code: str) -> str:
    """
    Evaluate the given Python code and return the result.
    """
    import sys
    import io

    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    try:
        exec(code, {})
        result = redirected_output.getvalue()
        return result if result else "Code executed successfully."
    except Exception as e:
        return f"Error during execution: {str(e)}"
    finally:
        sys.stdout = old_stdout
```

Test the crew:

```python
pythonCrew = PythonHelpCrew(llm=llm)
print(pythonCrew.run("Write a function to get the n-th Fibonacci number."))
```

**[Example output placeholder showing the crew's collaborative process]**

### Creating a first solution

For the GDSC, we need an AI system that can answer education-related questions using the PIRLS 2021 dataset.

First, create a tool for accessing the PIRLS database:

```python
import sqlalchemy

DB_ENDPOINT = 'ENDPOINT'
DB_PORT = 'DB_PORT'
DB_USER = 'DB_USER'
DB_PASSWORD ='DB_PASSWORD'
DB_NAME ='DB_NAME'

connection_string = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_ENDPOINT}:{DB_PORT}/{DB_NAME}'
db_engine = sqlalchemy.create_engine(connection_string)

@tool
def query_database(query: str) -> str:
    """Query the PIRLS postgres database and return the results as a string."""
    with db_engine.connect() as connection:
        try:
            res = connection.execute(sqlalchemy.text(query))
        except Exception as e:
            return f'Encountered exception {e}.'
    ret = '\n'.join(", ".join(map(str, result)) for result in res)
    return f'Query: {query}\nResult: {ret}'
```

Create a basic PIRLS crew:

```python
import sys
sys.path.append('..') 
from textwrap import dedent
from src.static.submission import Submission 

class BasicPIRLSCrew(Submission):
    
    def __init__(self, llm: ChatBedrock):
        self.llm = llm
    
    def run(self, prompt: str) -> str:
        return self.crew().kickoff(inputs={"prompt": prompt}).raw   
    
    @agent
    def database_expert(self) -> Agent:
        return Agent(
            role="PIRLS Student Database Expert",
            backstory=dedent("""
                You are a senior data engineer that has a lot of experience in working with the PIRLS data.
                Given a question, you come up with an SQL query that get the relevant data and run it with the'query_database' tool.
                
                You know that there is the table 'Students' with columns Student_ID and Country_ID, and a table 'Countries' with columns 'Country_ID', 'Name' and 'Code'.
            """),
            goal="Use the tool to query the database and answer the question.",
            llm=self.llm,
            allow_delegation=False,
            verbose=True,
            tools=[query_database]
        )
    
    @task
    def answer_question(self) -> Task:
        return Task(
            description="Query the database and answer the question \"{prompt}\".",
            expected_output="Answer to the question",
            agent=self.database_expert()
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            max_iter=3,
            cache=False
        )
```

Test the basic crew:

```python
crew = BasicPIRLSCrew(llm=llm)
print(crew.run("How many students participated in PIRLS 2021."))
```

### Conclusion

In this tutorial, we've learned:
- What AI agents are and how they differ from traditional LLMs
- How to use Amazon Bedrock to access powerful language models
- The basics of the CrewAI framework
- How to build and test a simple AI agent for code assistance
- How to build a basic solution for the GDSC task

---

## Tutorial 4 - Submitting Your Solution

You learned about AI agents in the previous tutorial and about the data in tutorial 2. Now, it's time to combine this knowledge into one working solution!

Unlike previous GDSCs where you were asked to hand in results, this year we ask you to submit running `source code`. You will create a full blown chatbot API.

### Agenda

1. [Understanding the project structure](#understanding-the-project-structure)
2. [Create your first application](#create-your-first-application)
3. [How to test your code](#how-to-test-your-code)
4. [How to submit your code](#how-to-submit-your-code)
5. [How does the evaluation work](#how-does-the-evaluation-work)
6. [Chatbot Arena](#chatbot-arena)
7. [Human evaluation questions](#human-evaluation-questions)

### Understanding the project structure

#### Code Commit

When you created or joined a team, you gained access to an AWS account with a CodeCommit repository.

#### Code structure

In your CodeCommit repository, you will find three folders:
- `images` - All images used in tutorials
- `src` - **Source code you will submit**
- `tutorials` - The training tutorials

In the `src` folder:
- `submission` - **Your modifiable code directory**
- `static` - Unmodifiable code (replaced with each submission)

The most important file is `src/submission/create_submission.py`:

```python
from src.static.ChatBedrockWrapper import ChatBedrockWrapper
from src.static.submission import Submission

def create_submission(call_id: str) -> Submission:
    ...
```

This function is **the entry point** for your submission. It must take a `call_id` string and return a `Submission` object.

#### What is `Submission`

`Submission` is an abstract class that enforces implementation of a run method:

```python
from abc import ABC, abstractmethod

class Submission(ABC):
    @abstractmethod
    def run(self, prompt: str) -> str:
        ...
```

### Create your first submission

The `BasicPIRLSCrew` is already extracted into a Python script. Here's how to configure it:

```python
from src.submission.crews.basic_PIRLS_crew import BasicPIRLSCrew
from src.static.ChatBedrockWrapper import ChatBedrockWrapper
from src.static.submission import Submission

def create_submission(call_id: str) -> Submission:
    llm = ChatBedrockWrapper(
        model_id='anthropic.claude-3-haiku-20240307-v1:0',
        model_kwargs={'temperature': 0},
        call_id=call_id
    )
    crew = BasicPIRLSCrew(llm=llm)
    return crew
```

**Important**: You **must** use `ChatBedrockWrapper` instead of the standard ChatBedrock for token counting and cost tracking.

### How to test your code?

There are two ways to test:
- In AWS by pushing to the test branch
- On your local machine

#### How to push to the submission branch?

Open terminal in JupyterLab and use these git commands:

1. Check status: `git pull`
2. See branches: `git branch`  
3. Create test branch: `git checkout -b test_submission`
4. Check status: `git status`
5. Add files: `git add .`
6. Commit: `git commit -m "descriptive message"`
7. Push: `git push`

After pushing to **test_submission**, check ECS for your running application's public IP.

Test your endpoint:

```python
import requests

def ask_question(question: str, url: str):
    data = {'prompt': question}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# Use your public IP
REMOTE_HOST = 'http://ADD_YOUR_PUBLIC_IP_HERE:8000/run'
res = ask_question("How many students participated in the study?", REMOTE_HOST)
print(res['result'])
```

**[Example output placeholder showing response with result, time, tokens, cost, etc.]**

### How to submit your code?

Submit by pushing to the `submission` branch. This triggers automatic evaluation.

### How does the evaluation work?

After submission, your code is tested with automatic evaluation questions. Your submission must:
- Yield correct answers
- Respond within the timeout limit

Each question is asked 3 times, and evaluation can take up to 1 hour.

### Chatbot Arena

The [Chatbot Arena](https://gdsc.ce.capgemini.com/app/arena/) is where human evaluators compare submissions:

1. Choose a question from the list
2. See how 2 random submissions responded  
3. Vote for the better answer
4. Your votes determine submission rankings using the Glicko 2 rating system

#### Why should I rank battles?

Human evaluation is essential for assessing answer quality. Teams need to rank battles to make additional submissions beyond the first two free ones.

### Human Evaluation Questions

You can submit your own questions to the arena - especially ones that highlight your crew's strengths! All participant questions are verified before being added.

---

## Tutorial 5 - Advanced AI Agents

In the previous tutorials, you learned to create AI agents and access PIRLS data. However, the basic solution wasn't sufficient. This tutorial shows how to improve your solution.

### Agenda

1. [How to improve?](#how-to-improve)
2. [Modify your code and submit changes](#modify-your-code-and-submit-changes)
3. [Submission status on the website](#submission-status-on-the-website)
4. [When is your ranking updated?](#when-is-your-ranking-updated)
5. [Ways to improve](#ways-to-improve)

### How to improve?

The `BasicPIRLSCrew` only knew about two tables: Students and Countries. But our database is much more complex:

![Database Schema](../images/t2_db_schema.png)

The solution is the `AdvancedPIRLSCrew` with:
- 2 agents: data analyst and data engineer  
- Configuration in separate YAML files
- Better database knowledge

```python
@CrewBase
class AdvancedPIRLSCrew(Submission):
    """Data Analysis Crew for the GDSC project."""
    agents_config = PROJECT_ROOT / 'submission' / 'config' / 'agents.yaml'
    tasks_config = PROJECT_ROOT / 'submission' / 'config' / 'tasks.yaml'

    def __init__(self, llm):
        self.llm = llm

    def run(self, prompt: str) -> str:
        return self.crew().kickoff(inputs={'user_question': prompt}).raw
```

The agents.yaml file contains extensive backstories:

```yaml
lead_data_analyst:
  role: >
    PIRLS lead data analyst
  goal: >
    Answer the research questions using the PIRLS 2021 dataset
  backstory: >
    You are the Lead Data Analyst for the Progress in International Reading Literacy Study (PIRLS) project. 
    Your expertise in data analysis and interpretation is crucial for providing insights into the dataset.
    Your analysis will be used to inform educational policies and practices.
    You focus on questions related to reading literacy and educational outcomes!
    
    While you have a good overview of PIRLS, you always rely on your data engineer to provide you with the necessary data.
    When delegating a task to a coworker, remember to explicitly name the coworker you want to delegate to.
```

The tasks.yaml file uses parameterization:

```yaml
answer_question_task:
  description: >
    Answer the following question:   
    {user_question}
    
    When applicable, search for relevant data in the PIRLS 2021 dataset.
    
    When answering, always:   
    - Do not comment on topics outside the area of your expertise.   
    - Ensure that your analysis is accurate and relevant to the research questions.
    - Unless instructed otherwise, explain how you come to your conclusions and provide evidence to support your claims.
    - Use markdown format for your final answer.
  expected_output: >
    A clear and concise answer to the question
```

### Advanced Tools

The data engineer has access to specialized tools like `get_possible_answers_to_question`:

```python
@tool
def get_possible_answers_to_question(
    general_table: Literal['Students', 'Curricula', 'Homes', 'Teachers', 'Schools'],
    questionnaire_answers_table: Literal['StudentQuestionnaireAnswers', 'CurriculumQuestionnaireAnswers', 'HomeQuestionnaireAnswers', 'TeacherQuestionnaireAnswers', 'SchoolQuestionnaireAnswers'],
    questionnaire_entries_table: Literal['StudentQuestionnaireEntries', 'CurriculumQuestionnaireEntries', 'HomeQuestionnaireEntries', 'TeacherQuestionnaireEntries', 'SchoolQuestionnaireEntries'],
    question_code: str
) -> str:
    """Query the database and returns possible answer to a given question"""
    # Implementation details...
```

This tool helps agents understand the possible answers for questionnaire questions, reducing the complexity of SQL generation.

### Ways to improve

There are many potential improvements:
- Broader context and better descriptions
- More agents with specialized roles
- Better tools for database access
- Additional tools (arithmetic, internet access)
- Testing with arena questions to find challenges

### Conclusions

The key to success lies in:
- Enhancing your AI agents with better context
- Using clean code structure with YAML configurations
- Paying attention to database structure
- Providing comprehensive information to agents

Armed with this knowledge, you should be ready to compete effectively in this year's GDSC!

---

## END CONTEXT

*Help to generate similar tutorials for this year's Global Data Science Challenge.*