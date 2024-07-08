# Função para ler as informações do autômato a partir de um arquivo
def ler_automato(filename):
    # Abrir o arquivo especificado em modo de leitura
    with open(filename, 'r') as arquivo:
        # Ler e armazenar o estado inicial
        estado_inicial = arquivo.readline().strip()
        # Ler e armazenar o alfabeto como uma lista de símbolos
        alfabeto = arquivo.readline().strip().split()
        # Ler e armazenar a lista de estados possíveis
        estados = arquivo.readline().strip().split()
        # Ler e armazenar a lista de estados finais
        estados_finais = arquivo.readline().strip().split()
        
        # Inicializar um dicionário vazio para armazenar as transições
        transicoes = {}
        # Ler cada linha restante no arquivo
        for linha in arquivo:
            # Dividir a linha em partes usando espaços em branco como separador
            partes = linha.strip().split()
            # Extrair informações sobre a transição
            estado_origem = partes[0]
            estado_destino = partes[1]
            simbolo_transicao = partes[2]
            # Criar uma chave única para a transição usando o estado de origem e o símbolo
            chave = (estado_origem, simbolo_transicao)
            # Adicionar o estado de destino à lista de destinos para essa transição
            if chave not in transicoes:
                transicoes[chave] = []
            transicoes[chave].append(estado_destino)
            # Exibir mensagem de depuração sobre a transição lida
            print(f"Lendo transição: {chave} -> {estado_destino}")
    
    # Retornar as informações lidas do autômato
    return estado_inicial, alfabeto, estados, estados_finais, transicoes

# Função para simular o autômato com uma palavra de entrada
def simular_automato(estado_inicial, alfabeto, estados_finais, transicoes, palavra_input):
    # Inicializar o conjunto de estados atuais com o estado inicial
    estados_atuais = {estado_inicial}
    
    # Imprimir informações sobre o início da simulação
    print("\nIniciando simulação do autômato:\n")
    print(f"Estado Inicial: {estado_inicial}")
    print(f"Palavra de Entrada: {palavra_input}\n")
    
    # Iterar sobre cada símbolo na palavra de entrada
    for simbolo in palavra_input:
        # Verificar se o símbolo está no alfabeto do autômato
        if simbolo not in alfabeto:
            return f"Rejeita - Símbolo '{simbolo}' não está no alfabeto"
        
        # Imprimir informações sobre o processamento do símbolo
        print("Processando símbolo:")
        print(f"Estado atual: {estados_atuais}")
        print(f"Símbolo no estado: {get_simbolo_estado(estados_atuais, transicoes)}")
        print(f"Símbolo inserido: {simbolo}\n")
        
        # Inicializar um conjunto para armazenar os novos estados após a transição
        novos_estados = set()
        # Para cada estado atual, verificar se há uma transição com o símbolo
        for estado_atual in estados_atuais:
            chave = (estado_atual, simbolo)
            # Se houver uma transição para o símbolo, adicionar o estado de destino aos novos estados
            if chave in transicoes:
                novos_estados.update(transicoes[chave])
        
        # Verificar se houve transição possível para o símbolo atual
        if not novos_estados:
            return f"Rejeita - Transição não definida para o estado atual '{estado_atual}' e símbolo '{simbolo}'"
        
        # Atualizar os estados atuais com os novos estados obtidos após a transição
        estados_atuais = novos_estados
        # Exibir os estados atuais após processar o símbolo atual
        print(f"Estados atuais após processar símbolo '{simbolo}': {estados_atuais}\n")
    
    # Verificar se pelo menos um dos estados atuais é um estado final
    if any(estado in estados_finais for estado in estados_atuais):
        return "Aceita"  # A palavra foi aceita pelo autômato
    else:
        return "Rejeita - Estado final não alcançado"  # A palavra foi rejeitada pelo autômato

# Função auxiliar para obter o símbolo correspondente ao estado atual
def get_simbolo_estado(estados_atuais, transicoes):
    for estado in estados_atuais:
        for chave in transicoes.keys():
            if chave[0] == estado:
                return chave[1]
    return None  # Caso o símbolo não seja encontrado, retornar None

# Função principal
def main():
    filename = "automato.txt"
    estado_inicial, alfabeto, _, estados_finais, transicoes = ler_automato(filename)
    
    # Solicitar ao usuário que insira a palavra de entrada
    palavra_input = input("Digite uma palavra para testar: ")
    resultado = simular_automato(estado_inicial, alfabeto, estados_finais, transicoes, palavra_input)
    print(resultado)

if __name__ == "__main__":
    main()
