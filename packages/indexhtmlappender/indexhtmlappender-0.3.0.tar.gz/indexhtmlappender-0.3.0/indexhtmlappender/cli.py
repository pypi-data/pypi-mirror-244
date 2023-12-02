import os
import re
import typer

app = typer.Typer()


@app.command()
def append_index(path: str):
    """Modify HTML files to add '/index.html' suffix to relative links."""
    for root, _, files in os.walk(path):
        for file_name in files:
            if file_name.endswith(".html"):
                file_path = os.path.join(root, file_name)
                replace_relative_links_in_file(file_path)

    typer.echo("Modification complete.")


def replace_relative_links_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_data = file.read()

    pattern = r'<a href="(/[^"]+)">'
    updated_file_data = re.sub(pattern, lambda m: f'<a href="{m.group(1)}/index.html">', file_data)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(updated_file_data)


if __name__ == "__main__":
    app()
