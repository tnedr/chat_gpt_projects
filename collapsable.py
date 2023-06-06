import webview


def process_dialogue(dialogue):
    sections = dialogue.split('\n\n')
    processed_dialogue = ""

    for section in sections:
        lines = section.split('\n')
        question = lines[0]
        answer = '\n'.join(lines[1:])
        processed_dialogue += f"""
            <button class="collapsible">{question}</button>
            <div class="content">
                <p>{answer}</p>
            </div>
        """

    return processed_dialogue


def generate_collapsible_html(dialogue):
    html = f"""
        <html>
            <head>
                <style>
                    .collapsible {{
                        background-color: #f9f9f9;
                        color: #444;
                        cursor: pointer;
                        padding: 18px;
                        width: 100%;
                        border: none;
                        text-align: left;
                        outline: none;
                        font-size: 15px;
                        transition: 0.4s;
                    }}

                    .active, .collapsible:hover {{
                        background-color: #ccc;
                    }}

                    .content {{
                        padding: 0 18px;
                        display: none;
                        overflow: hidden;
                        background-color: #f9f9f9;
                    }}
                </style>
            </head>
            <body>{dialogue}</body>
            <script>
                var coll = document.getElementsByClassName("collapsible");
                var i;

                for (i = 0; i < coll.length; i++) {{
                    coll[i].addEventListener("click", function() {{
                        this.classList.toggle("active");
                        var content = this.nextElementSibling;
                        if (content.style.display === "block") {{
                            content.style.display = "none";
                        }} else {{
                            content.style.display = "block";
                        }}
                    }});
                }}
            </script>
        </html>
    """

    return html


def main():
    dialogue = """
        Question 1
        Answer 1

        Question 2
        Answer 2

        Question 3
        Answer 3
    """

    processed_dialogue = process_dialogue(dialogue)
    html = generate_collapsible_html(processed_dialogue)

    webview.create_window("Collapsible Dialogue", html=html, width=800, height=600)
    webview.start()


if __name__ == '__main__':
    main()
