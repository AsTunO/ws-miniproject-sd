import socket

def main():
    # Configuração do servidor
    host = '127.0.0.1'  # Endereço IP do servidor
    port = 1234  # Porta em que o servidor está escutando

    # Criação do socket do cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conexão ao servidor
        client_socket.connect((host, port))
        print("Conectado ao servidor")

        # Solicitação de leitura de estoque da loja 1
        client_socket.send(b'GET:1')
        response = client_socket.recv(1024).decode()
        print("Estoque da loja 1:", response)

        # Solicitação de leitura de estoque da loja 2
        client_socket.send(b'GET:2')
        response = client_socket.recv(1024).decode()
        print("Estoque da loja 2:", response)

        # Solicitação de transferência de produtos da loja 1 para a loja 2
        client_socket.send(b'TRANSFER:1:2:produto1:50')
        response = client_socket.recv(1024).decode()
        print("Resposta do servidor:", response)

        # Solicitação de leitura de estoque da loja 1 após a transferência
        client_socket.send(b'GET:1')
        response = client_socket.recv(1024).decode()
        print("Estoque da loja 1 após transferência:", response)

        # Solicitação de leitura de estoque da loja 2 após a transferência
        client_socket.send(b'GET:2')
        response = client_socket.recv(1024).decode()
        print("Estoque da loja 2 após transferência:", response)

    except ConnectionRefusedError:
        print("Erro: Não foi possível conectar ao servidor.")

    finally:
        # Fecha o socket do cliente
        client_socket.close()

if __name__ == "__main__":
    main()
