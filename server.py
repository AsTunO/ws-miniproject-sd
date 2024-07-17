# server.py

import socket
import threading
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
import time

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Chave de criptografia (carregada do arquivo .env)
chave = os.getenv('SECRET_KEY').encode()

# Criando o objeto Fernet para criptografia
cipher_suite = Fernet(chave)

# Dicionário para armazenar os clientes conectados
clients = {}

# Função para criptografar uma mensagem
def encrypt_message(message):
    return cipher_suite.encrypt(message.encode())

# Função para descriptografar uma mensagem
def decrypt_message(encrypted_message):
    return cipher_suite.decrypt(encrypted_message).decode()

# Função para lidar com a conexão de um cliente
def handle_client(client_socket, client_address):
    while True:
        try:
            # Recebe os dados do cliente
            encrypted_data = client_socket.recv(1024)
            if not encrypted_data:
                break

            # Descriptografa os dados recebidos
            data = decrypt_message(encrypted_data)

            # Trata os dados recebidos
            if data.startswith('GET'):
                # Lógica para processar uma solicitação de leitura do estoque
                loja_id = int(data.split(':')[1])
                if loja_id in estoque:
                    response = str(estoque[loja_id])
                    client_socket.send(encrypt_message(response))
                else:
                    client_socket.send(encrypt_message('Loja não encontrada'))
            elif data.startswith('TRANSFER'):
                # Lógica para processar uma solicitação de transferência de estoque
                parts = data.split(':')
                loja_origem = int(parts[1])
                loja_destino = int(parts[2])
                produto = parts[3]
                quantidade = int(parts[4])

                if loja_origem in estoque and loja_destino in estoque:
                    if produto in estoque[loja_origem] and estoque[loja_origem][produto] >= quantidade:
                        estoque[loja_origem][produto] -= quantidade
                        if produto in estoque[loja_destino]:
                            estoque[loja_destino][produto] += quantidade
                        else:
                            estoque[loja_destino][produto] = quantidade
                        client_socket.send(encrypt_message('Transferência realizada com sucesso'))
                    else:
                        client_socket.send(encrypt_message('Produto ou quantidade insuficiente na loja de origem'))
                else:
                    client_socket.send(encrypt_message('Loja de origem ou destino não encontrada'))
            else:
                send_to_all_clients(f'Servidor: {data}')
        except Exception as e:
            client_socket.send(encrypt_message(f'Erro: {str(e)}'))
            break

    client_socket.close()

# Função para enviar uma mensagem para todos os clientes conectados
def send_to_all_clients(message):
    for client in clients.values():
        try:
            client.send(encrypt_message(message))
        except:
            pass

def broadcast_service(port):
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while True:
        broadcast_message = f"SERVER:{port}".encode()
        broadcast_socket.sendto(broadcast_message, ('<broadcast>', 37020))
        time.sleep(5)

def main():
    # Carrega os dados do arquivo
    with open('dados.txt', 'rb') as file:
        global estoque
        estoque = eval(file.read())

    # Configuração do servidor
    host = '0.0.0.0'  # Endereço IP do servidor
    port = 1234  # Porta em que o servidor irá escutar

    # Criação do socket do servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Servidor iniciado em {host}:{port}")

    # Iniciar thread para enviar broadcasts
    threading.Thread(target=broadcast_service, args=(port,), daemon=True).start()

    while True:
        client_socket, client_address = server_socket.accept()
        print("Conexão estabelecida com", client_address)

        # Adiciona o cliente ao dicionário de clientes
        clients[client_address] = client_socket

        # Manipula a conexão em uma nova thread
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

        # Aguarda entrada do usuário para enviar mensagem para todos os clientes
        while True:
            message = input("Digite uma mensagem para os clientes (ou 'sair' para encerrar o servidor): ")
            if message.lower() == 'sair':
                server_socket.close()
                print("Servidor encerrado.")
                return
            else:
                send_to_all_clients(f'Servidor: {message}')

if __name__ == "__main__":
    main()
