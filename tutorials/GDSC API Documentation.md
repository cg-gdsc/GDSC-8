# Persona interaction and submission API documentation

The API endpoint: https://cygeoykm2i.execute-api.us-east-1.amazonaws.com/main

## Authentication

Authentication is done via AWS, you need to be authenticated to your AWS account.

- In Sagemaker notebooks this is automatically done
- Locally you have to configure the credentials. run `aws sts get-caller-identity` to confirm you are authenticated

The endpoint must be called with AWS signing, by the code sample provided by us. Otherwise it will show access denied

## Endpoints

### `GET /health`

**Description**: always returns 200 OK. Use it to test the connection to the endpoint

### `POST /chat`

**Description**: Use it to chat with a persona

**Payload**:

For the first interaction, define a `persona_id` which ranges from `persona_001` to `persona_100`

```json
[
  {
    "persona_id": "persona_056",
    "message": "Hello how can I help?",
  }
]
```

**Response**:

```json
[
  {
    "conversation_id": "{team_id}#{persona_id}#{conv_timestamp}",
		"response": "hello I am 20 years old and interested in construction",
		"conversation_count_week": 21
  }
]
```

A `conversation_id` is generated for this conversation based on the `team_id`, `persona_id` and `conv_timestamp`, which you have to send from now on to continue talking to this persona. You are also informed how many conversation your team has had this week.

```json
[
  {
    "conversation_id": "{team_id}#{persona_id}#{conv_timestamp}",
    "message": "Hi nice to meet you, are you looking for a job or for a training?"
  }
]
```

**Response**:

```json
[
  {
    "conversation_id": "{team_id}#{persona_id}#{conv_timestamp}",
		"response": "I am not sure"
  }
]
```

You can continue this interaction until the limit of interactions per conversation is reached. See limits at the bottom of the file.

To start a new conversation, simply send a payload with another `persona_id` and no `conversation_id`

### `POST /submit`

**Description**: Use it to submit recommendations for all personas

**Payload**:

```json
[
  {
    "submission": [
			...
		]
  }
]
```

**Response**:

```json
[
	{
			"submission_id": "{team_id}#{submission_timestamp}",
			"message": "Submission saved successfully",
			"submission_count": 4
	},
]
```

A `submission_id` is generated based on the `team_id` and `submission_timestamp`.

### `GET /submit`

**Description**: Use it to fetch the submissions for your team

**Example Response**:

```json
[
	{
			"submission_id": "{team_id}#{submission_timestamp}",
			"created_at": "2025-09-15T15:27:11",
			"submission": ...,
			"score": "39"
	},
	{
			"submission_id": "{team_id}#{submission_timestamp}",
			"created_at": "2025-09-14T12:21:58",
			"submission": ...,
			"score": "44"
	},
]
```

⚠️ These are the successful requests, your code should check for the status_code of the received response and in case of error (a status_code different than 200), print out the returned error.

## API limits

- 400 conversations per week across all personas
- 20 interactions per conversation (10 each side)
- 30k tokens per conversation on GDSC API side
  - when chatting with a persona, this persona calls Mistral and consumes token. The persona should not exceed 30k tokens during the conversation
- 120 submissions in total during the challenge
