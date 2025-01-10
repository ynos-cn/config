import os
from ebooklib import epub
import ebooklib
from weasyprint import HTML, CSS


def convert_epub_to_pdf(epub_path, pdf_path):
    book = epub.read_epub(epub_path)

    # 创建一个空的 HTML 字符串用于存放所有内容
    html_content = ""

    # 遍历每个项目（主要是 XHtml 文件）
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            # 将每个文档的内容添加到 HTML 字符串中
            html_content += item.content.decode("utf-8")

    # 创建一个临时文件来保存合并后的 HTML 内容
    temp_html_file = "temp.html"
    with open(temp_html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    # 使用 WeasyPrint 将 HTML 转换为 PDF
    html = HTML(filename=temp_html_file)
    css = CSS(
        string="""
        body {
            font-family: Arial, sans-serif;
        }
        h1, h2, h3 {
            text-align: center;
        }
    """
    )

    # 渲染并保存 PDF 文件
    html.write_pdf(pdf_path, stylesheets=[css])

    # 删除临时 HTML 文件
    os.remove(temp_html_file)


if __name__ == "__main__":
    epub_file = "example.epub"
    pdf_output = "output.pdf"
    convert_epub_to_pdf(epub_file, pdf_output)
