import openai

from prompts import  INITIAL_RESPONSE ,Prompts
import time

from dotenv import load_dotenv
import os

load_dotenv(".env")
openai.api_key = os.environ["OPENAI_API_KEY"]


def generate_response_from_transcript(transcript):

    messages = [{"role": "system", "content": Prompts.prompts[Prompts.chosen_prompt]}]
    messages.extend([{"role": "user", "content": i} for i in transcript])

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301",
            messages=messages,
            temperature=0.0
        )
    except Exception as e:
        print(e)
        return ''
    full_response = response.choices[0].message.content
    try:
        print(full_response)
        return full_response.split('[')[1].split(']')[0]
    except Exception as e:
        print('error')
        print(e)
        return ''


class GPTResponder:
    def __init__(self):
        self.response = INITIAL_RESPONSE
        self.response_interval = 2

    def respond_to_transcriber(self, transcriber):
        while True:
            if transcriber.transcript_changed_event.is_set():
                start_time = time.time()

                transcriber.transcript_changed_event.clear()
                transcript_list = transcriber.get_transcript()
                response = generate_response_from_transcript(transcript_list)

                end_time = time.time()  # Measure end time
                execution_time = end_time - start_time  # Calculate the time it took to execute the function

                if response != '':
                    self.response = response

                remaining_time = self.response_interval - execution_time
                if remaining_time > 0:
                    time.sleep(remaining_time)
            else:
                time.sleep(0.3)

    def update_response_interval(self, interval):
        self.response_interval = interval
