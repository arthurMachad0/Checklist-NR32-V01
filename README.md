# O projeto possui o intuito de servir de melhoria no processo de inspeção hospitalar na Liga Contra o Câncer; 

# O grande problema neste projeto é realizar a conversão do código em python para apk utilizando os comandos de conversão, devido uma incompatibilidade de bibliotecas utilizadas:
- A solução aplicada para manter utilizando Python foi separar a interface gráfica e coleta de informações e deixar o processamento de criação do PDF para uma API;
- Outra solução aplicada foi construir o mesmo código em Flutter, assim não foi necessário ter que construir API, melhorando performance de resposta do PDF.

* Se te interessou o projeto, entre em contato que podemos conversar para mostrar as versões mais robustas e utilizadas na prática deste código.

# Dicas Iniciais:
 - Passo 1: Crie um ambiente virtual (trazendo um Python puro para sua pasta) -> py -m venv venv
 - Passo 2: Ativação do ambiente virtual criado -> \venv\Scripts\activate [ Na prática escreva: ve(aperta tab)sc(aperta tab)ac(aperta tab) ]
 
 - OBS-1: Caso dê errado e não dê nenhum aviso, tente: .\venv\Scripts\Activate.ps1 [ Na prática escreva: ve(aperta tab)sc(aperta tab)ac(aperta tab) e complete escrevendo .ps1 ]
 
 - Passo 3: Execute o seguinte comando para instalar todas as bibliotecas de uma única vez -> pip install -r \requirements.txt [ Na prática escreva: pip install -r req(aperta tab) ]

 # Ajustando Política de Privacidade:
 - OBS-2: Caso não esteja autorizando, é necessário executar o powershell como adm e verificar :
 
 - Get-ExecutionPolicy
 - Se estiver dando como restrito, utilizar este comando e autorizar -> Set-ExecutionPolicy Unrestricted
 - Depois se quiser reotrnar para política restrita utilizando -> Set-ExecutionPolicy Restricted

# Convertendo Para Executável Windows:
 - Para converter o código com flet para um executável windows, basta abrir o terminal do seu editor de código (vscode ou cursor) pressionando crtl+j e executando -> pyinstaller --onefile --windowed main.py
