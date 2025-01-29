## Architecture diagram

![ezgif-216486315a301](https://github.com/user-attachments/assets/91907695-b6f2-4ef7-83db-92d8702b1593)


## Description
Data engineering project focusing on deploying Generative AI API via AWS Lambda for image analysis.


## How does it work?

Image is sent to the Lambda API Endpoint which is then used to provide insights - image's analysis, description and sentiment.

## Additional info
- LLM : Llama 3.2 Vision - 90B
- Used a Docker + ECR setup for Lambda Function
  
## Endpoints
#### `/api/v1/image/description`

Example response:
```json
{
  "description": "The image displays the Google logo in its traditional, multicolored form. The first letter 'G' is blue, the second letter 'O' is green, the third letter 'O' is yellow, the fourth letter 'g' is blue, the fifth letter 'l' is green, and the sixth letter 'e' is red. The logo is centered against a solid black background. The colors are vibrant and the logo appears to be a standard, official version of the Google logo.",
  "tags": [
    "google"
  ]
}
```
#### `/api/v1/image/analysis`

Example response:
```json
{
  "description": "A table set for two with a vase of flowers against a back wall",
  "objects": [
    "table",
    "objects",
    "vase",
    "flowers",
    "tablecloth",
    "bottle"
  ],
  "colors": [
    "red",
    "green"
  ]
}
```

#### `/api/v1/image/sentiment`
```json
{
  "description": "The image exudes a positive mood, characterized by a warmly inviting table setting adorned with vibrant flowers and a soft color palette, evoking a sense of joy and celebration.",
  "score": 90
}
```


## Getting started

#### Configuring python environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Building the docker image

```bash
docker build -t image-analysis:latest .
```
