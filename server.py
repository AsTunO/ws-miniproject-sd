import socket
import threading

# Definição das lojas e seus estoques iniciais (banco de dados em memória)
estoque = {
    1: {'produto1': 100, 'produto2': 200},
    2: {'produto1': 150, 'produto2': 250}
}

# Função para lidar com a conexão de um cliente
def handle_client(client_socket):
    while True:
        # Recebe os dados do cliente
        data = client_socket.recv(1024).decode()
        if not data:
            break
        
        # Trata os dados recebidos
        if data.startswith('GET'):
            # Lógica para processar uma solicitação de leitura do estoque
            loja_id = int(data.split(':')[1])
            if loja_id in estoque:
                response = str(estoque[loja_id])
                client_socket.send(response.encode())
            else:
                client_socket.send('Loja não encontrada'.encode())
        elif data.startswith('TRANSFER'):
            # Lógica para processar uma solicitação de transferência de estoque
            # Formato da mensagem: TRANSFER:loja_origem:loja_destino:produto:quantidade
            parts = data.split(':')
            loja_origem = int(parts[1])
            loja_destino = int(parts[2])
            produto = parts[3]
            quantidade = int(parts[4])

            if loja_origem in estoque and loja_destino in estoque:
                if produto in estoque[loja_origem] and estoque[loja_origem][produto] >= quantidade:
                    estoque[loja_origem][produto] -= quantidade
                    estoque[loja_destino][produto] += quantidade
                    client_socket.send('Transferência realizada com sucesso'.encode())
                else:
                    client_socket.send('Produto ou quantidade insuficiente na loja de origem'.encode())
            else:
                client_socket.send('Loja de origem ou destino não encontrada'.encode())

    # Fecha a conexão com o cliente
    client_socket.close()

# Função principal
def main():
    # Configuração do servidor
    host = '127.0.0.1'  # Endereço IP do servidor
    port = 1234  # Porta em que o servidor irá escutar

    # Criação do socket do servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Associa o socket do servidor ao host e porta
    server_socket.bind((host, port))

    # Habilita o servidor a aceitar conexões
    server_socket.listen(5)
    print("Servidor escutando em {}:{}".format(host, port))

    while True:
        # Aguarda uma conexão
        client_socket, client_address = server_socket.accept()
        print("Conexão estabelecida com", client_address)

        # Manipula a conexão em uma nova thread
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()