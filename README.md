# Echo Server

Trabalho de Redes de Computadores.

Implementação de uma aplicação multithreading cliente-servidor utilizando a biblioteca socket.

## Como executar

Abra duas instâncias do seu terminal e execute os seguintes comandos...

Para executar o servidor:
```python
python3 server.py
```

Para executar o cliente:
```python
python3 client.py
```

## Conexão do Cliente

Ao iniciar, você deverá digitar as informações de conexão com o servidor:

- IP do servidor (host)
- Porta do servidor
- Nome do usuário

Exemplo:
```
Host: 127.0.0.1
Port: 4444
Name: *opcional*
```

## Protocolo

Quando conectado, você poderá utilizar os seguintes comandos:

- `echo <msg>`: Envia a mensagem para o servidor
- `help`: Exibe a lista de comandos disponíveis
- `exit`: Encerra a conexão
