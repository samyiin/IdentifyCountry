import openai
import json

file_path = "llm_function_calling_schema.txt"

with open(file_path, "r") as f:
    function_definition = json.load(f)


def llm_map_location_to_country(location,  opanai_apikey):
    openai.api_key = opanai_apikey
    response = openai.ChatCompletion.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "user",
                "content": location,
            }
        ],
        functions=[function_definition],
        function_call={"name": "extract_countries"}
    )

    # Parse the result
    return json.loads(response["choices"][0]["message"]["function_call"]["arguments"])["countries"]