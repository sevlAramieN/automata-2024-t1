from typing import List, Dict

def load_automata(filename: str) -> tuple:
    """
    Lê os dados de um autômato finito a partir de um arquivo de texto e retorna uma estrutura que representa o autômato.

    Args:
        filename (str): O nome do arquivo de texto contendo a descrição do autômato.

    Returns:
        tuple: Uma tupla contendo os componentes do autômato:
            - Q: Conjunto de estados
            - Sigma: Alfabeto
            - delta: Função de transição
            - q0: Estado inicial
            - F: Conjunto de estados finais

    Raises:
        Exception: Se o formato do arquivo do autômato for inválido.
    """

    with open(filename, 'r') as arquivo:
        # Ler o alfabeto
        Sigma = arquivo.readline().strip().split()
        # Validar se o símbolo '&' está presente no alfabeto
        if '&' not in Sigma:
            raise Exception("O símbolo '&' para a palavra vazia deve estar presente no alfabeto.")

        # Ler os estados
        Q = arquivo.readline().strip().split()

        # Ler o estado inicial
        q0 = arquivo.readline().strip()
        # Validar se o estado inicial é válido
        if q0 not in Q:
            raise Exception("O estado inicial não está presente na lista de estados.")

        # Ler os estados finais
        F = arquivo.readline().strip().split()
        # Validar se os estados finais são válidos
        for estado_final in F:
            if estado_final not in Q:
                raise Exception(f"O estado final '{estado_final}' não está presente na lista de estados.")

        # Inicializar a função de transição como um dicionário
        delta = {}

        # Ler as transições
        for linha in arquivo:
            partes = linha.strip().split()
            if len(partes) != 3:
                raise Exception("Formato de transição inválido. Cada linha deve ter três partes: estado_origem simbolo_transicao estado_destino")
            estado_origem, simbolo_transicao, estado_destino = partes
            # Validar se o estado de origem e o estado de destino são válidos
            if estado_origem not in Q or estado_destino not in Q:
                raise Exception(f"Estado de origem '{estado_origem}' ou estado de destino '{estado_destino}' inválido.")
            # Validar se o símbolo de transição é válido
            if simbolo_transicao not in Sigma and simbolo_transicao != '&':
                raise Exception(f"Símbolo de transição '{simbolo_transicao}' inválido.")

            chave = (estado_origem, simbolo_transicao)
            if chave not in delta:
                delta[chave] = []
            delta[chave].append(estado_destino)

    return Q, Sigma, delta, q0, F


def process(automata, word: list[str]) -> Dict[str, str]:
    """
    Processa uma lista de palavras utilizando o autômato dado e retorna um mapa associando cada palavra ao resultado do autômato.

    Args:
        automata (tuple): Uma tupla contendo os componentes do autômato:
            - Q: Conjunto de estados
            - Sigma: Alfabeto
            - delta: Função de transição
            - q0: Estado inicial
            - F: Conjunto de estados finais
        word (List[str]): A lista de palavras a serem processadas.

    Returns:
        Dict[str:str]: Um dicionário que mapeia cada palavra para o resultado do autômato:
            - "ACEITA": Se a palavra é aceita pelo autômato.
            - "REJEITA": Se a palavra é rejeitada pelo autômato.
            - "INVALIDA": Se a palavra contém símbolos inválidos (não pertencentes ao alfabeto).
    """
    Q, Sigma, delta, q0, F = automata

    resultados = {}
    for palavra in word:
        # Verificar se a palavra contém símbolos inválidos
        for simbolo in palavra:
            if simbolo not in Sigma:
                resultados[palavra] = "INVALIDA"
                break
        else:
            # Se a palavra for válida, simular o autômato
            estado_atual = q0
            for simbolo in palavra:
                if (estado_atual, simbolo) in delta:
                    estado_atual = delta[(estado_atual, simbolo)][0]  # Assumindo que delta é uma função determinista
                else:
                    resultados[palavra] = "REJEITA"
                    break
            else:
                # Se o autômato chegou a um estado final, a palavra é aceita
                if estado_atual in F:
                    resultados[palavra] = "ACEITA"
                else:
                    resultados[palavra] = "REJEITA"

    return resultados


# Exemplo de uso
if __name__ == "__main__":
    try:
        automata = load_automata("automato.txt")
        palavras = ["aba", "ab", "abb", "aa", "c"]
        resultados = process(automata, palavras)
        for palavra, resultado in resultados.items():
            print(f"Palavra: {palavra}, Resultado: {resultado}")
    except Exception as e:
        print(f"Erro: {e}")
