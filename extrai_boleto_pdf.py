import pdfplumber
import re
import pandas as pd


def extrair_dados_boleto(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        texto = ""
        for page in pdf.pages:
            texto += page.extract_text() + "\n"

    # Regex para os campos principais
    nome = re.search(r'Pagador:\s*(.+)', texto)
    endereco = re.search(r'Pagador:.*\n(.+)', texto)
    valor = re.search(r'Valor documento\s*\n([\d.,]+)', texto)
    vencimento = re.search(r'Vencimento\s*\n(\d{2}/\d{2}/\d{4})', texto)
    cnpj = re.search(r'CNPJ:\s*([\d./-]+)', texto)
    linha_digitavel = re.search(r'(\d{5}\.\d{5} \d{5}\.\d{6} \d{5}\.\d{6} \d \d{14})', texto)

    dados = {
        'nome_cliente': nome.group(1).strip() if nome else '',
        'endereco': endereco.group(1).strip() if endereco else '',
        'valor': valor.group(1).replace('.', '').replace(',', '.') if valor else '',
        'vencimento': vencimento.group(1) if vencimento else '',
        'cpf_cnpj': cnpj.group(1) if cnpj else '',
        'linha_digitavel': linha_digitavel.group(1) if linha_digitavel else ''
    }
    return dados

if __name__ == "__main__":
    pdf_path = input('Digite o nome do arquivo PDF do boleto (ex: boleto.pdf): ').strip()
    dados = extrair_dados_boleto(pdf_path)
    df = pd.DataFrame([dados])
    df.to_csv('boletos_extraidos.csv', index=False, encoding='utf-8', sep=';')
    print('Dados extraídos e salvos em boletos_extraidos.csv') 