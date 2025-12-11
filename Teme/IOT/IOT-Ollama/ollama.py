import requests

class Ollama:

    BASE_URL = "http://localhost:11434/api"
    CHAT_PATH =  BASE_URL + "/chat"
    GENERATE_PATH =  BASE_URL + "/generate"
    LIST_MODELS_PATH =  BASE_URL + "/tags"


    def __init__(self):
        self.available_models = self.__check_available_models__()
        if self.available_models:
            self._current_model = self.available_models[1]
        else:
            self._current_model = ""

    def __str__(self):
        return f"Current model {self._current_model}. You can choose from {', '.join(self.available_models)}"

    def __check_available_models__(self):
        response = requests.get(Ollama.LIST_MODELS_PATH)
        return [i["name"] for i in response.json()["models"]]

    def list_models(self, force=False):
        if force:
            self.available_models = self.__check_available_models__()
        return self.available_models
    

    def set_current_model(self, model: str | int):
        if model in  self.available_models:
            self._current_model = model
        if model in range(len(self.available_models)):
            self._current_model = self.available_models[model]

    @property
    def current_model(self):
        return self._current_model
    
    @current_model.setter
    def current_model(self, model: str | int):
        if model in  self.available_models:
            self._current_model = model
        if model in range(len(self.available_models)):
            self._current_model = self.available_models[model]

    def ask(self, prompt = "", model=""):
        if not model:
            model = self.current_model
        prompt = prompt or input("Cu ce pot ajuta? \n")

        while prompt:
            payload = {
                "model" : model,
                "prompt" : prompt,
                "stream" : False
            }

            response = requests.post(Ollama.GENERATE_PATH, json=payload)

            actual_response = response.json()["response"]

            with open("chat_response_no_stream.txt", "w") as file_writer:
                file_writer.write(actual_response)

            return actual_response
            
            # prompt = input("Cu ce te pot ajuta in continuare?\n")