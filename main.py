import os
import argparse
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import MAX_ITERS
from prompts import system_prompt
from functions.call_function import available_functions, call_function


def main():
    """
    Main function to run the Gemini-powered chatbot.

    This function initializes the argument parser, loads environment variables,
    sets up the Generative AI client, and manages the multi-turn conversation
    with the Gemini model. It handles user prompts, verbose output,
    and integrates with external tools/functions.
    """
    # Initialize argument parser to handle command-line inputs.
    # It allows users to provide a prompt and optionally enable verbose output.
    parser = argparse.ArgumentParser(description="Chatbot powered by Gemini.")
    parser.add_argument("user_prompt", type=str,
                        help="The initial prompt message to send to the Gemini model.")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose output to display detailed interaction logs, "
                             "including token usage and function call results.")
    args = parser.parse_args()

    # Load environment variables from a .env file.
    # This is crucial for securely obtaining the GEMINI_API_KEY without hardcoding it in the source.
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # If the API key is not found, the program cannot authenticate with the
    # Gemini API, so it terminates with an error.
    if not api_key:
        raise RuntimeError("No GEMINI_API_KEY was found. Please ensure it is set in your .env file.")

    # Initialize the Generative AI client using the retrieved API key.
    # This client is the primary interface for interacting with the Gemini model.
    client = genai.Client(api_key=api_key)

    # Construct the initial message for the conversation.
    # The user's prompt is set as the first message from the 'user' role.
    messages = [types.Content(
        role="user", parts=[types.Part(text=args.user_prompt)])]

    # If verbose mode is enabled, print the user's initial prompt to the console
    # for transparency and debugging purposes.
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    # Enter a loop to manage the multi-turn conversation or sequential tool use.
    # The loop continues for a maximum of MAX_ITERS to prevent infinite loops.
    for _ in range(MAX_ITERS):
        try:
            # Attempt to generate content from the Gemini model based on the
            # current conversation history (`messages`).
            final_response = generate_content(client, messages, args.verbose)
            if final_response:
                # If a final textual response is received (i.e., the model
                # no longer needs to make function calls), print it and
                # exit the program successfully.
                print("Final response:")
                print(final_response)
                return
        except Exception as e:
            # Catch and report any exceptions that occur during the content
            # generation process, which could indicate API issues or model errors.
            print(f"Error in generate_content: {e}")
            sys.exit(1) # Exit on error

    # If the loop completes without a final response, it means the maximum
    # number of iterations was reached, suggesting the conversation or
    # tool use did not converge.
    print(f"Maximum iterations ({MAX_ITERS}) reached without a final response.")
    sys.exit(1)


def generate_content(client, messages, verbose):
    """
    Generates content from the Gemini model, handling both textual responses and function calls.

    Args:
        client: The Generative AI client instance.
        messages: A list of message objects representing the conversation history.
        verbose: A boolean indicating whether to print detailed interaction logs.

    Returns:
        str: The final textual response from the model if no function calls are made,
             otherwise None (indicating further processing is needed).

    Raises:
        RuntimeError: If there is an API request failure or an empty function response.
    """
    # Call the Gemini model to generate content. This is the core interaction
    # point with the AI.
    # - `model="gemini-2.5-flash"` specifies the model version to use.
    # - `contents=messages` provides the full conversation history to the model.
    # - `tools=[available_functions]` registers a list of available tools
    #   (functions) that the model can choose to call.
    # - `system_instruction=system_prompt` guides the model's overall behavior
    #   and persona.
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt)
    )

    # It's crucial to check for usage metadata. Its absence typically indicates
    # a failure in the API request itself, rather than a model-generated empty response.
    if not response.usage_metadata:
        raise RuntimeError("No usage_metadata in the response. This likely indicates an API request failure.")

    # If verbose mode is active, display the token counts for both the prompt
    # (input) and the generated response (output). This helps in understanding
    # API costs and model efficiency.
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    # Append the model's textual content (if any) to the conversation history.
    # This maintains continuity for subsequent turns.
    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    # If the model's response does not include any function calls, it means
    # it has generated a final textual response, which is then returned.
    if not response.function_calls:
        return response.text

    # If the model has suggested one or more function calls, process them.
    function_call_results = []
    for function_call in response.function_calls:
        # Execute the function suggested by the model using the `call_function`
        # utility, which dispatches to the actual Python function.
        function_call_result = call_function(function_call, verbose)

        # Validate that the function call actually returned a meaningful response.
        # An empty response could indicate an issue with the tool's execution.
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
            or not function_call_result.parts[0].function_response.response
        ):
            raise RuntimeError(
                f"Empty function response for function: {function_call.name}. Check the tool implementation."
            )
        # In verbose mode, print the output of the function call to track the
        # interaction between the model and the tools.
        if verbose:
            print(f"-> Function call result: {function_call_result.parts[0].function_response.response}")
        function_call_results.append(function_call_result.parts[0])

    # After executing all suggested function calls, append their results
    # to the `messages` list. These results are treated as input from the
    # 'user' role for the next turn, allowing the model to incorporate
    # the tool's output into its reasoning.
    messages.append(types.Content(role="user", parts=function_call_results))

    # Return None because the model made function calls, not a final textual response.
    # The loop in `main` will call `generate_content` again with the updated messages.
    return None


if __name__ == "__main__":
    # Ensure the main function is called only when the script is executed directly.
    main()