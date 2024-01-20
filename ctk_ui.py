import customtkinter as ctk
import logging

from prompts import Prompts

logger = logging.getLogger()


class UI(ctk.CTk):
    prompt_choices = list(Prompts.prompts.keys())
    model_choices = ["gpt-4-1106-preview", "gpt-3.5-turbo-0301"]
    font_size = 20
    freeze_state = [True]
    width = 1000
    height = 900

    def __init__(self, transcriber, responder, audio_queue):
        super().__init__()
        self.transcriber, self.responder, self.audio_queue = transcriber, responder, audio_queue
        self.default_prompt = ctk.StringVar(value=self.prompt_choices[0])
        self.default_model = ctk.StringVar(value=self.model_choices[-1])

        self.create_ui_components()
        transcript_textbox = self.create_transcript_textbox()
        response_textbox = self.create_response_textbox()
        update_interval_slider_label, update_interval_slider = self.create_update_interval_slider()
        self.freeze_button = self.create_freeze_button()
        self.create_prompt_option()
        self.create_model_option()
        self.create_clear_transcript_button()

        logger.info("READY")

        self.tabview.grid_rowconfigure(0, weight=100)
        self.tabview.grid_rowconfigure(1, weight=1)
        self.tabview.grid_rowconfigure(2, weight=1)
        self.tabview.grid_rowconfigure(3, weight=1)
        self.tabview.grid_columnconfigure(0, weight=2)
        self.tabview.grid_columnconfigure(1, weight=1)

        # Add the clear transcript button to the UI

        # Using list to be able to change its content inside inner functions

        update_interval_slider_label.configure(text=f"Update interval: {update_interval_slider.get()} seconds")

        self.update_transcript_UI(transcriber, transcript_textbox)
        self.update_response_UI(responder, response_textbox, update_interval_slider_label, update_interval_slider,
                                self.freeze_state)

        self.mainloop()

    def freeze_unfreeze(self):
        self.freeze_state[0] = not self.freeze_state[0]  # Invert the freeze state
        self.freeze_button.configure(text="Unfreeze" if self.freeze_state[0] else "Freeze")

    def clear_context(self, transcriber, audio_queue):
        transcriber.clear_transcript_data()
        with audio_queue.mutex:
            audio_queue.queue.clear()

    def update_response_UI(self, responder, textbox, update_interval_slider_label, update_interval_slider,
                           freeze_state):
        if not freeze_state[0]:
            response = responder.response

            textbox.configure(state="normal")
            self.write_in_textbox(textbox, response)
            textbox.configure(state="disabled")

            update_interval = int(update_interval_slider.get())
            responder.update_response_interval(update_interval)
            update_interval_slider_label.configure(text=f"Update interval: {update_interval} seconds")
            responder.update_status(True)
        else:
            responder.update_status(False)
        textbox.after(300, self.update_response_UI, responder, textbox, update_interval_slider_label,
                      update_interval_slider,
                      freeze_state)

    def write_in_textbox(self, textbox, text):
        textbox.delete("0.0", "end")
        textbox.insert("0.0", text)

    def prompt_menu_callback(self, choice):
        print("optionmenu dropdown clicked:", choice)
        Prompts.chosen_prompt = choice
    def model_menu_callback(self, choice):
        print("optionmenu dropdown clicked:", choice)
        self.responder.model_name = choice

    def update_transcript_UI(self, transcriber, textbox):
        transcript_string = transcriber.get_transcript()
        self.write_in_textbox(textbox, ''.join(transcript_string))
        textbox.after(300, self.update_transcript_UI, transcriber, textbox)

    def create_transcript_textbox(self):
        transcript_textbox = ctk.CTkTextbox(self.tabview.tab("Transcribe"), width=600,
                                            height=600, font=("Arial", self.font_size),
                                            text_color='#FFFCF2',
                                            wrap="word")
        transcript_textbox.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")
        return transcript_textbox

    def create_clear_transcript_button(self):
        clear_transcript_button = ctk.CTkButton(self.tabview.tab("Transcribe"), text="Clear Transcript",
                                                command=lambda: self.clear_context(self.transcriber,
                                                                                   self.audio_queue, ))
        clear_transcript_button.grid(row=1, column=0, padx=10, pady=3, sticky="nsew")
        return clear_transcript_button

    def create_prompt_option(self):
        prompt_option_label = ctk.CTkLabel(self.tabview.tab("Settings"), text=f"prompt options", font=("Arial", 12),
                                           text_color="#FFFCF2")
        prompt_option_label.grid(row=0, column=3, padx=10, pady=3, sticky="nsew")
        prompt_option = ctk.CTkOptionMenu(master=self.tabview.tab("Settings"),
                                          values=self.prompt_choices,
                                          command=self.prompt_menu_callback,
                                          variable=self.default_prompt,
                                          width=20,
                                          font=("Arial", self.font_size),
                                          text_color='#639cdc',
                                          )
        prompt_option.grid(row=1, column=3, padx=10, pady=3, sticky="nsew")
        return prompt_option

    def create_model_option(self):
        model_option_label = ctk.CTkLabel(self.tabview.tab("Settings"), text=f"model", font=("Arial", 12),
                                           text_color="#FFFCF2")
        model_option_label.grid(row=0, column=2, padx=10, pady=3, sticky="nsew")
        model_option = ctk.CTkOptionMenu(master=self.tabview.tab("Settings"),
                                         values=self.model_choices,
                                         command=self.model_menu_callback,
                                         variable=self.default_model,
                                         width=20,
                                         font=("Arial", self.font_size),
                                         text_color='#639cdc',
                                         )
        model_option.grid(row=1, column=2, padx=10, pady=3, sticky="nsew")
        return model_option

    def create_response_textbox(self):
        response_textbox = ctk.CTkTextbox(self.tabview.tab("Transcribe"),
                                          width=300,
                                          height=600,
                                          font=("Arial", self.font_size),
                                          text_color='#639cdc',
                                          wrap="word")
        response_textbox.grid(row=0, column=1, padx=10, pady=20, sticky="nsew")
        return response_textbox

    def create_freeze_button(self):
        freeze_button = ctk.CTkButton(self.tabview.tab("Transcribe"), text="UnFreeze", command=None)
        freeze_button.grid(row=1, column=1, padx=10, pady=3, sticky="nsew")
        freeze_button.configure(command=self.freeze_unfreeze)
        return freeze_button

    def create_update_interval_slider(self):
        update_interval_slider_label = ctk.CTkLabel(self.tabview.tab("Transcribe"), text=f"", font=("Arial", 12),
                                                    text_color="#FFFCF2")
        update_interval_slider_label.grid(row=2, column=1, padx=10, pady=3, sticky="nsew")

        update_interval_slider = ctk.CTkSlider(self.tabview.tab("Transcribe"), from_=1, to=10, width=300, height=20,
                                               number_of_steps=9)
        update_interval_slider.set(2)
        update_interval_slider.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
        return update_interval_slider_label, update_interval_slider

    def create_ui_components(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.title("GPT_meetings_UI")
        self.configure(bg='#252422')
        self.geometry(f"{self.width}x{self.height}")

        self.tabview = ctk.CTkTabview(self, width=self.width, height=self.height)
        self.tabview.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
        self.tabview.add("Transcribe")
        self.tabview.add("Settings")

        return
