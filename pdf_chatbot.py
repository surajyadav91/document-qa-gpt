import gradio as gr

from gpt_qa import GPT_QA
from config import config
from retriever import Retriever
from read_file_create_chunks import ReadCreateChunk

read_and_create_chunk = ReadCreateChunk(config)
read_and_create_chunk.store_chunks(config['file_path'])
retriever = Retriever(config)
gpt_qa = GPT_QA(config)

with gr.Blocks() as demo:
    gr.Markdown(
        """<h1><center>PDF-GPT</center></h1>
    """
    )
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    def user(user_message, history):
        return "", history + [[user_message, None]]

    def bot(history):
        question = history[-1][0]

        passages = retriever.retrieve(question)
        reply = gpt_qa.read(question, passages)
        history[-1][1] = reply
        return history

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch(server_name='0.0.0.0',server_port=8080,debug=True)