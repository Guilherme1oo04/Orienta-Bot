# OrientaBot

## Docker

**Atenção:** mova o arquivo `.env.example` para `.env` e insira a chave da API; caso contrário, erros podem ocorrer no Docker!

### Construir a imagem Docker

Utilize o seguinte comando para construir a imagem Docker:

```bash
docker build -t orientabot .
```

### Iniciar o Docker

Para iniciar o contêiner Docker, utilize o comando:

```bash
docker run orientabot
```

### Executar em segundo plano

Se preferir executar o contêiner em segundo plano, utilize o comando:

```bash
docker run -d orientabot
```