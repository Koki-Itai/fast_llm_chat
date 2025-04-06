from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="token-abc123",
)

console = Console()

SYSTEM_PROMPT = (
    "<Role>あなたは優秀な日本語アシスタントです。</Role>\n"
    "<Attention>\n"
    "- 出力はマークダウンで行うこと。\n"
    "- 日本語のみの生成を行うこと。英語や中国語などの他の言語は生成しないこと。\n"
    "</Attention>\n"
)

def cli_chat():
    system_message = {"role": "system", "content": SYSTEM_PROMPT}
    messages = [system_message]

    console.print("[bold blue]Starting conversation. Type `exit` or `q` to end.[/bold blue]")
    console.print("[bold blue]Type `clear` to start a new conversation.[/bold blue]")

    while True:
        try:
            user_input = console.input("[bold green]User: [/bold green]")

            if user_input.lower() in ('exit', 'q'):
                break

            if user_input.lower() == 'clear':
                messages = [system_message]
                console.print("[bold blue]Chat history cleared. Starting a new conversation.[/bold blue]")
                continue

            messages.append({"role": "user", "content": user_input})

            console.print("[bold yellow]Assistant:[/bold yellow]")

            stream = client.chat.completions.create(
                model="meta-llama/Llama-4-Scout-17B-16E-Instruct",
                messages=messages,
                stream=True
            )

            generated_content = ""
            with Live(console=console, auto_refresh=False, vertical_overflow="visible") as live:
                for chunk in stream:
                    content = chunk.choices[0].delta.content
                    if content:
                        generated_content += content
                        md = Markdown(generated_content, justify="left")
                        live.update(md, refresh=True)

            messages.append({"role": "assistant", "content": generated_content})
        except KeyboardInterrupt:
            console.print("\n[bold red]Interrupted. Type `exit` or `q` to end the session.[/bold red]")

if __name__ == "__main__":
    cli_chat()
