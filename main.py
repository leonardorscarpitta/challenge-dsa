

import json
import os
import random
DIVISOR = '=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-'
DB_PATH = os.path.join(os.path.dirname(__file__), 'insumos_aleatorios.json')

class Insumo:
    def __init__(self, id_insumo, nome, qtd_disponivel, qtd_reservada, validade=None):
        self.id_insumo = id_insumo
        self.nome = nome
        self.qtd_disponivel = qtd_disponivel
        self.qtd_reservada = qtd_reservada
        self.qtd_total = qtd_disponivel + qtd_reservada
        self.validade = validade
    def to_dict(self):
        return {
            'id_insumo': self.id_insumo,
            'nome': self.nome,
            'qtd_disponivel': self.qtd_disponivel,
            'qtd_reservada': self.qtd_reservada,
            'qtd_total': self.qtd_total,
            'validade': self.validade
        }


class FilaConsumo:
    def __init__(self):
        self.fila = []
    def registrar_consumo(self, consumo):
        self.fila.append(consumo)
    def listar_consumos(self):
        return self.fila


class PilhaConsumo:
    def __init__(self):
        self.pilha = []
    def registrar_consumo(self, consumo):
        self.pilha.append(consumo)
    def listar_consumos_inverso(self):
        return self.pilha[::-1]


def gerar_dados_aleatorios(qtd=10):
    nomes = [
        'Seringa 5ml', 'Luvas Descartáveis', 'Máscara N95', 'Algodão', 'Reagente A',
        'Reagente B', 'Tubo de coleta', 'Swab', 'Frasco esterilizado', 'Lamina'
    ]
    insumos = []
    ids_gerados = set()
    while len(insumos) < qtd:
        id_insumo = random.randint(1000, 9999)
        if id_insumo in ids_gerados:
            continue
        ids_gerados.add(id_insumo)
        nome = random.choice(nomes)
        qtd_disp = random.randint(10, 500)
        qtd_res = random.randint(0, 50)
        dias = random.randint(1, 730)
        validade = f"{2025 + dias // 365}-{(9 + (dias % 12)) % 12 + 1:02d}-{(18 + (dias % 28)) % 28 + 1:02d}"
        insumos.append(Insumo(id_insumo, nome, qtd_disp, qtd_res, validade))
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump([insumo.to_dict() for insumo in insumos], f, ensure_ascii=False, indent=4)
    print(f'Dados aleatórios gerados e salvos em {DB_PATH}')


def carregar_insumos():
    if not os.path.exists(DB_PATH):
        print('Arquivo de insumos não encontrado. Gere dados aleatórios primeiro!')
        return []
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    for insumo in dados:
        if 'qtd_total' in insumo:
            del insumo['qtd_total']
    return [Insumo(**{k: v for k, v in insumo.items() if k in ['id_insumo', 'nome', 'qtd_disponivel', 'qtd_reservada', 'validade']}) for insumo in dados]


def simular_consumo_diario():
    insumos = carregar_insumos()
    fila = FilaConsumo()
    pilha = PilhaConsumo()
    for insumo in insumos:
        consumo = {
            'id_insumo': insumo.id_insumo,
            'nome': insumo.nome,
            'qtd_consumida': random.randint(1, 5)
        }
        fila.registrar_consumo(consumo)
        pilha.registrar_consumo(consumo)
    return fila, pilha


def busca_sequencial(consumos, nome_insumo):
    for consumo in consumos:
        if consumo['nome'].lower() == nome_insumo.lower():
            return consumo
    return None


def busca_binaria(consumos, nome_insumo):
    consumos_ordenados = sorted(consumos, key=lambda x: x['nome'].lower())
    esquerda, direita = 0, len(consumos_ordenados) - 1
    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        nome_atual = consumos_ordenados[meio]['nome'].lower()
        if nome_atual == nome_insumo.lower():
            return consumos_ordenados[meio]
        elif nome_atual < nome_insumo.lower():
            esquerda = meio + 1
        else:
            direita = meio - 1
    return None


def merge_sort(insumos, chave):
    if len(insumos) <= 1:
        return insumos
    meio = len(insumos) // 2
    esquerda = merge_sort(insumos[:meio], chave)
    direita = merge_sort(insumos[meio:], chave)
    return merge(esquerda, direita, chave)


def merge(esquerda, direita, chave):
    resultado = []
    i = j = 0
    while i < len(esquerda) and j < len(direita):
        if esquerda[i][chave] <= direita[j][chave]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1
    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])
    return resultado


def quick_sort(insumos, chave):
    if len(insumos) <= 1:
        return insumos
    pivo = insumos[0]
    menores = [x for x in insumos[1:] if x[chave] <= pivo[chave]]
    maiores = [x for x in insumos[1:] if x[chave] > pivo[chave]]
    return quick_sort(menores, chave) + [pivo] + quick_sort(maiores, chave)


def ordenar_e_salvar_no_arquivo(campo):
    insumos = carregar_insumos()
    ordenados = merge_sort([i.to_dict() for i in insumos], campo)
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(ordenados, f, ensure_ascii=False, indent=4)
    print(f'Arquivo atualizado e ordenado por {campo} (Merge Sort).')


def painel_insumos():
    while True:
        print(DIVISOR)
        print('Painel de Controle de Insumos')
        print(DIVISOR)
        print('[1] - Gerar dados aleatórios')
        print('[2] - Visualizar consumo diário (Fila)')
        print('[3] - Visualizar últimos consumos (Pilha)')
        print('[4] - Buscar insumo por nome (Sequencial)')
        print('[5] - Buscar insumo por nome (Binária)')
        print('[6] - Ordenar insumos por quantidade consumida (Merge Sort)')
        print('[7] - Ordenar insumos por quantidade consumida (Quick Sort)')
        print('[8] - Ordenar insumos por validade (Merge Sort)')
        print('[9] - Ordenar insumos por validade (Quick Sort)')
        print('[11] - Ordenar e salvar insumos no arquivo (Merge Sort)')
        print('[10] - Relatório explicativo')
        print('[0] - Sair')
        print(DIVISOR)
        opcao = input('Escolha uma opção: ')
        match opcao:
            case '1':
                qtd = input('Quantidade de insumos aleatórios: ')
                try:
                    qtd = int(qtd)
                except:
                    qtd = 10
                gerar_dados_aleatorios(qtd)
            case '2':
                fila, _ = simular_consumo_diario()
                print('Consumo em ordem cronológica (Fila):')
                for c in fila.listar_consumos():
                    print(c)
            case '3':
                _, pilha = simular_consumo_diario()
                print('Últimos consumos (Pilha):')
                for c in pilha.listar_consumos_inverso():
                    print(c)
            case '4':
                nome = input('Nome do insumo para busca sequencial: ')
                fila, _ = simular_consumo_diario()
                resultado = busca_sequencial(fila.listar_consumos(), nome)
                print('Resultado:', resultado if resultado else 'Não encontrado')
            case '5':
                nome = input('Nome do insumo para busca binária: ')
                fila, _ = simular_consumo_diario()
                resultado = busca_binaria(fila.listar_consumos(), nome)
                print('Resultado:', resultado if resultado else 'Não encontrado')
            case '6':
                fila, _ = simular_consumo_diario()
                ordenados = merge_sort(fila.listar_consumos(), 'qtd_consumida')
                print('Insumos ordenados por quantidade consumida (Merge Sort):')
                for c in ordenados:
                    print(c)
            case '7':
                fila, _ = simular_consumo_diario()
                ordenados = quick_sort(fila.listar_consumos(), 'qtd_consumida')
                print('Insumos ordenados por quantidade consumida (Quick Sort):')
                for c in ordenados:
                    print(c)
            case '8':
                insumos = carregar_insumos()
                ordenados = merge_sort([i.to_dict() for i in insumos], 'validade')
                print('Insumos ordenados por validade (Merge Sort):')
                for c in ordenados:
                    print(c)
            case '9':
                insumos = carregar_insumos()
                ordenados = quick_sort([i.to_dict() for i in insumos], 'validade')
                print('Insumos ordenados por validade (Quick Sort):')
                for c in ordenados:
                    print(c)
            case '11':
                print('Escolha o campo para ordenar e salvar [id_insumo, nome, qtd_disponivel, qtd_reservada, qtd_total, validade]:')
                campo = input('Campo: ')
                ordenar_e_salvar_no_arquivo(campo)
            case '10':
                print(DIVISOR)
                print('RELATÓRIO EXPLICATIVO')
                print(DIVISOR)
                print('Fila: registra o consumo diário de insumos em ordem cronológica, permitindo visualizar o histórico de uso.')
                print('Pilha: permite consultar os últimos consumos realizados, útil para auditoria ou conferência rápida.')
                print('Busca sequencial: percorre todos os registros para localizar um insumo pelo nome, útil para listas pequenas.')
                print('Busca binária: localiza insumos rapidamente em listas ordenadas pelo nome, eficiente para grandes volumes.')
                print('Merge Sort e Quick Sort: organizam os insumos por quantidade consumida, validade ou qualquer campo, facilitando controle e reposição.')
                print('Merge Sort também pode ser usado para ordenar e salvar os insumos diretamente no arquivo, permitindo persistência dos dados ordenados.')
                print('Geração de dados aleatórios: permite simular cenários reais e testar todas as funcionalidades.')
            case '0':
                print('Saindo...')
                break
            case _:
                print('Opção inválida!')


if __name__ == '__main__':
    painel_insumos()
