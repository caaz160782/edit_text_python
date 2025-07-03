from fpdf import FPDF


def open_txt_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()


def save_txt_file(path, content):
    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)


def save_as_pdf(path, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in content.split('\n'):
        pdf.multi_cell(0, 10, line)

    pdf.output(path)
