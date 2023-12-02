__all__ = [
    'pdf_to_text',
]

def pdf_to_text(file):
    import pypdf
    import assure
    # assure file is seekable to support stdin.
    file = assure.seekable(file)
    reader = pypdf.PdfReader(file)
    pages = [page.extract_text() for page in reader.pages]
    return '\n\n'.join(pages)
