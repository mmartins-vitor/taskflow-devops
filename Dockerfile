# imagem oficial do py
FROM python:3.11-slim 

# Diretorio de trabalho dentro do container
WORKDIR /app

# copiando arquivos de dependencia
COPY requirements.txt .

# Instalar dependencias 
RUN pip install --no-cache-dir -r requirements.txt

# copiando codigo da aplicação para dentro do container
COPY . .

# Expondo porta 8080 (usada pelo Uvicorn)
EXPOSE 8080

# comando padrao para rodas api 
# uvicorn app.main:app --reload
CMD [ "Uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080" ]