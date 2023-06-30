import openai

openai.api_key = open("key.txt", "r").read()


class GPT_QA:
    def __init__(self,config):
        self.chat_gpt_model = config['chat_gpt_model']

    def read(self, question, passage):
        messages = [
            dict(
                role="system",
                content="you are an intelligent question-answering assistant, you will answer the questions based on context text fed to you.",
            )
        ]

        messages.append(dict(role="user", content=passage))
        messages.append(
            dict(
                role="user",
                content=f"\n\n Based on the above text answer this question \n\n, question: {question}",
            )
        )

        response = openai.ChatCompletion.create(
            model=self.chat_gpt_model, messages=messages
        )

        return response["choices"][0]["message"]["content"]


# if __name__ == "__main__":
#     # test the function
#     question = "Do I need to bond when the customer has solar power? "
#     context = "If these conditions are not met, notify your supervisor and customer that a valid bonding option is not available. 1.1.3 All technicians must comply with local electrical codes, as some juri ictions do not permit certain bonding methods. Figure 6-2 Drop Bonding to Metal Frame / I-Beam of the Structure 7 Solar Power Bonding 7.1 Per NEC Article 690.43 (Solar Photovoltaic (PV) Systems - Equipment Grounding and Bonding), the solar power system is required to be grounded and the grounded conductor is required to be bonded to the grounded ele rode conductor of the power system."
#     reader = GPTTurboReader()
#     response = reader.read(question=question, passage=context)
#     print(response)