# DAta da ultima modificação: 12/05/2024 
# objetivo do programa: Subir arquivos para o servidor SFTP da empresa de maneira simples e rápida
#
# Modo de utilização: Ao chamar o programa, pode-se passar como argumentos os arquivos que deseja subir no servidor
#ou pode-se executar o programa sem parametros que ele ira pedir os arquivos como parametro. 
#
# Codigo para compilação: 
#pyinstaller upload.py -p pyFileDir --onefile 

import sys,os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pysftp
import configparser 

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

BARSIZE = 40

def importfile() -> dict:
    
    parser = configparser.ConfigParser()
    parser.read("C:\\Users\\Gabriel\\Documents\\Gabriel\\Pyhton\\UploadFiles\\config.ini")
    
    return {
        "SFtpInterno": parser["FTPCONFIG"]["SFtpInterno"],
        "SFTPInternoPorta":parser["FTPCONFIG"]["SFTPInternoPorta"],
        "SFTPExterno":parser["FTPCONFIG"]["SFTPExterno"],
        "SFTPExternoPorta":parser["FTPCONFIG"]["SFTPExternoPorta"],
        "SFTPPass":parser["FTPCONFIG"]["SFTPPass"],
        "SFTPUser":parser["FTPCONFIG"]["SFTPUser"],
        "ProgramPassword": parser["FTPCONFIG"]["ProgramPassword"]
    }

def printmenu() -> None:
    """ only prints a simple menu 
    """
    print("      ----------------------- Upload file ------------------------------- ")
    print("         Pode-se chamar o programa no prompt passando o nome do arquivo para um upload automatico")
    print("         Exemplo: Updater file1 file2 - o(s) arquivo(s) sera(ão) Enviados para o Servidor \n")
    print("         Digite 0 para encerrar o programa !! \n")
    
def getInput()-> str:
    """Gets the entry of the menu 
    
    Returns the entry of the user """
    printmenu()
    var: str =  input("Digite o nome do arquivo:")
    
    if(var == "0"):
        print("Encerrando ...")
        exit(0)
    return var.split(" ")

def getArgcArgv()-> list[str]:
    """get the args that are passed in the call of the program

    args: 
        none
    Returns:
        list[str]: returns all of the args 
    """
    argv = sys.argv
    argc = len(sys.argv)
    
    # print("Argc: ",argc," Argv: ", argv)

    return argv

def connectSFTP(connectionData: dict) -> pysftp.Connection:
    """
        Makes the connetion with the SFTP server
        
        args: 
            A dict that contains all the connection parameters to make a connection
            
        returns the object of the connection
    """
    #print(connectionData.get("SFTPExterno"),connectionData.get("SFTPUser"),connectionData.get("SFTPPass"),connectionData.get("SFTPExternoPorta"))
    try:
        connection = pysftp.Connection(
            host=connectionData.get("SFTPExterno"),
            cnopts=cnopts,
            username=connectionData.get("SFTPUser"),
            password=connectionData.get("SFTPPass"),
            port=int(connectionData.get("SFTPExternoPorta"))
        )
    except Exception as error:
        print("Erro ao tentar estabelecer conexão: ",error)
    else:
        return connection

def uploadFile(file: str, connectionData: dict) ->None:
    """Upload a file to the specified direcotry in the SFTP """
    connection = connectSFTP(connectionData)
    
    print("Realizando upload para pasta: /Servidor200/Suporte/13-SFTPTool/",file,sep="")
    with connection.cd():
        connection.cwd("/Servidor200/Suporte/13-SFTPTool")
        try:
            connection.put(localpath=file,callback=progressBar)
        except FileNotFoundError as error:
            print("Arquivo digitado não encontrado ")
            os.system("pause")
        except Exception as error:
            print("Erro ",error)
            
    print("")
    connection.close()
        
def progressBar(downloaded: int, totalFile: int):
    """ this is a funtion that print a progress bar in 

    Args:
        downloaded (int): bytes Downloaded  
        totalFile (int): total of bytes to be downloaded
    """
    progress = int(downloaded*BARSIZE/totalFile)
    completed = str(int(downloaded*100/totalFile)) + '%'
    # exit =  str(f''[',chr(9608)*progress,' ',completed, '.'*(BARSIZE),']',str(downloaded)+'/'+str(totalFile)')
    exit = f"[{'.'*progress}{completed}{'.'*((BARSIZE)-progress)}]"
    sys.stdout.write(exit + '\r')
    sys.stdout.flush()   
    
def main()-> None:
    configurations = importfile()
    args = getArgcArgv()
    
    if(not(getUserPassword(configurations.get("ProgramPassword")))):
        print("Senha digitada invalida")
        os.system("Pause")
        return 0
    
    if len(args) == 1:
        files = getInput()
        #uploadFile(file=file,connectionData=configurations)
        for file in files:
            uploadFile(file=file,connectionData=configurations)
    else:
        for file in args[1:]:
         uploadFile(file=file,connectionData=configurations)
    
    os.system("pause")
    
def getUserPassword(password: str) -> bool:
    _password = input("Digite a senha de utilização: ")
    
    if(password == _password):
        return True
    else:
        return False 
     
if __name__ == "__main__":
    main()