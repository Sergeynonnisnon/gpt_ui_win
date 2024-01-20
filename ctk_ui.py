import customtkinter as ctk
import logging

from prompts import Prompts

logger = logging.getLogger()


class UI:
    choices = list(Prompts.prompts.keys())
    font_size = 20

    def __init__(self, transcriber, responder, audio_queue):
        self.root = ctk.CTk()
        self.optionmenu_var = ctk.StringVar(value=self.choices[0])
        self.create_ui_components()
        transcript_textbox = self.create_transcript_textbox()
        response_textbox = self.create_response_textbox()
        update_interval_slider_label, update_interval_slider = self.create_update_interval_slider()
        freeze_button = self.create_freeze_button()

        logger.info("READY")

        self.root.grid_rowconfigure(0, weight=100)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=2)
        self.root.grid_columnconfigure(1, weight=1)

        # Add the clear transcript button to the UI
        clear_transcript_button = ctk.CTkButton(self.root, text="Clear Transcript",
                                                command=lambda: self.clear_context(transcriber, audio_queue, ))
        clear_transcript_button.grid(row=1, column=0, padx=10, pady=3, sticky="nsew")

        freeze_state = [False]  # Using list to be able to change its content inside inner functions

        def freeze_unfreeze():
            freeze_state[0] = not freeze_state[0]  # Invert the freeze state
            freeze_button.configure(text="Unfreeze" if freeze_state[0] else "Freeze")

        freeze_button.configure(command=freeze_unfreeze)

        update_interval_slider_label.configure(text=f"Update interval: {update_interval_slider.get()} seconds")

        self.update_transcript_UI(transcriber, transcript_textbox)
        self.update_response_UI(responder, response_textbox, update_interval_slider_label, update_interval_slider,
                                freeze_state)

        self.root.mainloop()

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

    def optionmenu_callback(self, choice):
        print("optionmenu dropdown clicked:", choice)
        Prompts.chosen_prompt = choice

    def update_transcript_UI(self, transcriber, textbox):
        transcript_string = transcriber.get_transcript()
        self.write_in_textbox(textbox, ''.join(transcript_string))
        textbox.after(300, self.update_transcript_UI, transcriber, textbox)

    def create_transcript_textbox(self):
        transcript_textbox = ctk.CTkTextbox(self.root, width=300, font=("Arial", self.font_size), text_color='#FFFCF2',
                                            wrap="word")
        transcript_textbox.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")
        return transcript_textbox

    def create_prompt_option(self):
        prompt_option = ctk.CTkOptionMenu(master=self.root,
                                          values=self.choices,
                                          command=self.optionmenu_callback,
                                          variable=self.optionmenu_var,
                                          width=300,
                                          font=("Arial", self.font_size),
                                          text_color='#639cdc',
                                          )
        prompt_option.grid(row=6, column=1, padx=10, pady=10, sticky="nsew")
        return prompt_option

    def create_response_textbox(self):
        response_textbox = ctk.CTkTextbox(self.root, width=300, font=("Arial", self.font_size), text_color='#639cdc',
                                          wrap="word")
        response_textbox.grid(row=0, column=1, padx=10, pady=20, sticky="nsew")
        return response_textbox

    def create_freeze_button(self):
        freeze_button = ctk.CTkButton(self.root, text="Freeze", command=None)
        freeze_button.grid(row=1, column=1, padx=10, pady=3, sticky="nsew")
        return freeze_button

    def create_update_interval_slider(self):
        update_interval_slider_label = ctk.CTkLabel(self.root, text=f"", font=("Arial", 12), text_color="#FFFCF2")
        update_interval_slider_label.grid(row=2, column=1, padx=10, pady=3, sticky="nsew")

        update_interval_slider = ctk.CTkSlider(self.root, from_=1, to=10, width=300, height=20, number_of_steps=9)
        update_interval_slider.set(2)
        update_interval_slider.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
        return update_interval_slider_label, update_interval_slider

    def create_ui_components(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.root.title("GPT_meetings_UI")
        self.root.configure(bg='#252422')
        self.root.geometry("1000x600")

        return
