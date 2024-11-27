def generate_image_list_html(images, title):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{ font-family: Arial, sans-serif; text-align: center; margin: 50px; }}
            h1 {{ color: #2c3e50; }}
            ul {{ list-style: none; padding: 0; }}
            li {{ margin: 10px 0; }}
            a {{ text-decoration: none; color: #3498db; font-size: 18px; }}
            a:hover {{ text-decoration: underline; color: #2ecc71; }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        <ul>
    """
    if images:
        for image in images:
            html_content += f'<li><a href="/images/{image["folder"]}/{image["name"]}">{image["name"]}</a></li>'
    else:
        html_content += "<p>No images found.</p>"

    html_content += """
        </ul>
    </body>
    </html>
    """
    return html_content
