import pdfplumber
import re
import pandas as pd
import os

def extrair_dados_boleto(pdf_path):
    import pdfplumber
    import re
    import os

    with pdfplumber.open(pdf_path) as pdf:
        texto = ""
        for page in pdf.pages:
            texto += page.extract_text() + "\n"

    print("\n===== TEXTO EXTRAÍDO DO PDF =====\n")
    print(texto)
    print("\n===== FIM DO TEXTO EXTRAÍDO =====\n")

    # Nome do cliente (Pagador) - removendo CPF/CNPJ que vem depois
    nome = re.search(r'Pagador:\s*(.+?)(?:\s+CPF\s*/\s*CNPJ|$)', texto)

    # CPF/CNPJ - padrão específico da instituição (no final da linha do endereço)
    cpf_cnpj = ''
    cpf_match = re.search(r'([\d]{3}\.[\d]{3}\.[\d]{3}-[\d]{2})', texto)
    if cpf_match:
        cpf_cnpj = cpf_match.group(1)

    # Endereço - extração separada
    endereco = ''
    endereco_match = re.search(r'CPF ?/ ?CNPJ[:\s]*[\d.\-/]+\s+(.+?PALMAS.*?)\s*-?\s*(\d{8})', texto)
    if endereco_match:
        endereco = f"{endereco_match.group(1)} - {endereco_match.group(2)}"
    else:
        # Busca alternativa para endereço
        endereco_match = re.search(r'(.+?PALMAS.*?)\s*-?\s*(\d{8})', texto)
        if endereco_match:
            endereco = f"{endereco_match.group(1)} - {endereco_match.group(2)}"

    valor = re.search(r'Valor do Documento.*?(\d{1,3}(?:\.\d{3})*,\d{2})', texto, re.DOTALL)

    vencimento = re.search(r'Local de Pagamento.*?(\d{2}/\d{2}/\d{4})', texto, re.DOTALL)

    descricao = re.search(r'(MENSALIDADE:.*)', texto)

    linha_digitavel = re.search(r'(\d{5}\.\d{5} \d{5}\.\d{6} \d{5}\.\d{6} \d \d{13,14}-?\d)', texto)

    # Extrair turma
    turma_match = re.search(r'TURMA[:\s]+([A-Z0-9]+)', texto)
    turma = turma_match.group(1) if turma_match else ''

    # Mapeamento CNAE e atividade
    if turma.startswith('J'):
        cnae = '8513900'
        atividade = '0801'
    elif turma.startswith('G'):
        cnae = '8520100'
        atividade = '0801'
    else:
        cnae = ''
        atividade = ''

    dados = {
        'arquivo_pdf': os.path.basename(pdf_path),
        'nome_cliente': nome.group(1).strip() if nome else '',
        'cpf_cnpj': cpf_cnpj,
        'endereco': endereco.strip(),
        'valor': valor.group(1).replace('.', '').replace(',', '.') if valor else '',
        'vencimento': vencimento.group(1) if vencimento else '',
        'descricao': descricao.group(1).strip() if descricao else 'serviços educacionais',
        'linha_digitavel': linha_digitavel.group(1) if linha_digitavel else '',
        'turma': turma,
        'cnae': cnae,
        'atividade': atividade
    }

    return dados


if __name__ == "__main__":
    pasta = 'boletos'

    if not os.path.exists(pasta):
        os.makedirs(pasta)
        print(f'Pasta "{pasta}" criada. Coloque seus PDFs de boletos nela e rode o script novamente.')
        exit()

    arquivos = [f for f in os.listdir(pasta) if f.lower().endswith('.pdf')]

    if not arquivos:
        print(f'Nenhum PDF encontrado na pasta "{pasta}". Coloque seus boletos lá e rode novamente.')
        exit()

    todos_dados = []

    for arquivo in arquivos:
        caminho = os.path.join(pasta, arquivo)
        print(f'Extraindo dados de: {arquivo}')
        try:
            dados = extrair_dados_boleto(caminho)
            todos_dados.append(dados)
        except Exception as e:
            print(f'Erro ao processar {arquivo}: {e}')

    if todos_dados:
        df = pd.DataFrame(todos_dados)
        df.to_csv('boletos_extraidos.csv', index=False, encoding='utf-8', sep=';')
        print(f'Dados extraídos de {len(todos_dados)} boletos e salvos em boletos_extraidos.csv')
    else:
        print('Nenhum dado extraído.')
