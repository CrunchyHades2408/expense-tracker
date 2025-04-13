import google.generativeai as genai

try:
    # Configure the API with your API key
    genai.configure(api_key="AIzaSyCh6wQ6b3zUy6aelsfIkeGCwEjrjpsq5TU")

    # List available models
    models = list(genai.list_models())  # Convert the generator to a list

    # Check if models were returned
    if models:
        print("Available models:")
        for model in models:
            print(model)
    else:
        print("No models found.")
except Exception as e:
    print(f"An error occurred: {e}")
