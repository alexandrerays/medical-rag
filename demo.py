"""Gradio demo interface for MedReg MCP."""

import asyncio
import time

import gradio as gr

from app.rag import answer_question


def respond(message: str, history: list[dict]) -> tuple:
    if not message.strip():
        return history, "", "0 seconds", "—"

    start = time.time()
    response = asyncio.run(answer_question(message))
    elapsed = time.time() - start

    output = response.answer

    if response.citations:
        output += "\n\n---\n**Sources:**\n"
        for i, citation in enumerate(response.citations, start=1):
            output += f"\n[{i}] [{citation.source_title}]({citation.source_url})"

    if response.safety_triggered:
        output = "⚠️ " + output

    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": output})

    inference_time = f"{elapsed:.1f} seconds"
    sources_count = f"{len(response.citations)} sources cited"

    return history, "", inference_time, sources_count


def clear_chat():
    return [], "", "0 seconds", "—"


def set_question(question: str):
    return question


EXAMPLE_QUESTIONS = [
    "What does FDA say about AI/ML-enabled medical devices?",
    "What does WHO recommend for ethical AI in health?",
    "What is a predetermined change control plan?",
    "What are the guiding principles of good machine learning practice?",
    "How should teams think about model updates in AI/ML medical software?",
]

with gr.Blocks(title="Medical RAG") as demo:
    gr.Markdown("# Medical RAG — Healthcare AI Documentation Assistant")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Settings")

            top_k = gr.Slider(
                minimum=1,
                maximum=10,
                value=5,
                step=1,
                label="Top-K Results",
            )

            gr.Markdown("---")
            gr.Markdown("### Stats")

            inference_time = gr.Textbox(
                label="Inference Time",
                value="0 seconds",
                interactive=False,
            )

            sources_used = gr.Textbox(
                label="Sources Cited",
                value="—",
                interactive=False,
            )

            gr.Markdown("---")
            gr.Markdown("### Example Questions")

            example_btns = []
            for question in EXAMPLE_QUESTIONS:
                btn = gr.Button(question, size="sm", variant="secondary")
                example_btns.append((btn, question))

        with gr.Column(scale=3):
            chatbot = gr.Chatbot(
                label="Chatbot",
                height=500,
            )

            msg = gr.Textbox(
                label="Ask a question",
                placeholder="e.g. What does FDA say about AI/ML-enabled medical devices?",
                lines=1,
            )

            with gr.Row():
                submit_btn = gr.Button("Submit", variant="primary")
                clear_btn = gr.Button("Clear")

            gr.Markdown(
                "*This tool answers questions about FDA/WHO regulatory documentation. "
                "It does not provide medical advice.*"
            )

    for btn, question in example_btns:
        btn.click(fn=lambda q=question: q, outputs=[msg])

    submit_btn.click(
        fn=respond,
        inputs=[msg, chatbot],
        outputs=[chatbot, msg, inference_time, sources_used],
    )

    msg.submit(
        fn=respond,
        inputs=[msg, chatbot],
        outputs=[chatbot, msg, inference_time, sources_used],
    )

    clear_btn.click(
        fn=clear_chat,
        outputs=[chatbot, msg, inference_time, sources_used],
    )

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft(primary_hue="blue"))
