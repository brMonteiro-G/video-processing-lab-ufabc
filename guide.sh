===================================
ESZI032-17 - Processamento de Video
===================================

==============================================
Lab.01: Ambiente de Programação e a API OpenCV
==============================================

Iniciar o Ubuntu-linux

(((0))) Entrar na pasta "Documents" e criar uma para com seu Nome + iniciais do sobrenome. 
Um exemplo: celsosk


(((1))) Abrir um TERMINAL LINUX na mesma pasta

Na área da mesma pasta criada, usando as opções do botão direito do mouse escolha "abrir um TERMINAL" .

Caso apareça no terminal a indicação (base),
digitar e aplicar o seguinte comando para sair do ambiente
e voltar ao prompt $:
-----------------------------------------------------------------
(base)  ufabc@ufabc:~$ conda deactivate
-----------------------------------------------------------------

Visualizar os ambientes conda:
-----------------------------------------------------------------
ufabc@ufabc:~$ conda env list
-----------------------------------------------------------------


(((2))) Instalar o Miniconda3:
Comandos obtidos no link:
https://www.anaconda.com/docs/getting-started/miniconda/install#linux-2 

Primeiro executar atualização:
-----------------------------------------------------------------
$ sudo apt update
-----------------------------------------------------------------

Em seguida realizar os comandos, um por vez:
-----------------------------------------------------------------
$ mkdir -p ~/miniconda3
-----------------------------------------------------------------
$ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
-----------------------------------------------------------------
$ bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
-----------------------------------------------------------------
(Obs.: executar este comando rm, de remove, após o termino da instalação.)
-----------------------------------------------------------------
$ rm ~/miniconda3/miniconda.sh
-----------------------------------------------------------------



(((3))) Fechar o TERMINAL e abrir outro terminal com as teclas CTRL+ALT+T

Observe no terminal a indicação (base)

Digitar e aplicar o seguinte comando:
-----------------------------------------------------------------
(base)  ufabc@ufabc:~$ conda deactivate
-----------------------------------------------------------------

Observe que não tem mais a indicação (base). 
Em seguida realizar este comando:
-----------------------------------------------------------------
ufabc@ufabc:~$ conda config --set auto_activate_base false
-----------------------------------------------------------------


(((4))) Fechar o TERMINAL e abrir outro terminal com as teclas CTRL+ALT+T

Entrar no ambiente  miniconda com o seguinte comando:
-----------------------------------------------------------------
ufabc@ufabc:~$ source ~/miniconda3/bin/activate
-----------------------------------------------------------------
<<<<<< ATENÇÃO: SEMPRE UTILIZE ESTE COMANDO ACIMA >>>>>>>>>>>>>>> 
<<<<<< AO ENTRAR NO TERMINAL  >>>>>>>>>>>>>>>



Dentro do (base), criar um ambiente virtual denominado PV25, com este comando:
-----------------------------------------------------------------
(base)  ufabc@ufabc:~$ conda create --name PV25 python
-----------------------------------------------------------------

Aceitar a instalação, digite "y":
-----------------------------------------------------------------
Proceed ([y]/n)? y
-----------------------------------------------------------------

Confirmando a criação, com o comando abaixo e verifique se foi criado:
-----------------------------------------------------------------
(base)  ufabc@ufabc:~$ conda env list
-----------------------------------------------------------------

---saída---------------------------------------------------------
# conda environments:
#
base                  *  /home/ufabc/miniconda3
PV25                     /home/ufabc/miniconda3/envs/PV25
-----------------------------------------------------------------


(((5))) Entre no PV25:

-----------------------------------------------------------------
(base) ufabc@ufabc:~$ conda activate PV25
-----------------------------------------------------------------

#####------------
REFERÊNCIAS para consulta e outros comandos do conda:
https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html
#####------------
https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
#####------------
Uma referência de instalar o OpenCV:

(((6))) INSTALAR o OPENCV:

Dentro do ambiente virtual PV25:
(execute um comando de cada vez, nesta sequencia)

-atualizar o repositório linux
-----------------------------------------------------------------
(PV25) ... $ sudo apt update
-----------------------------------------------------------------


-Step 1. Install OpenCV Dependencies and Build Tools
-----------------------------------------------------------------
(PV25) ... $ sudo apt install build-essential cmake git pkg-config libgtk-3-dev \
   libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
   libxvidcore-dev libx264-dev libjpeg-dev libpng-dev libtiff-dev \
   gfortran openexr libatlas-base-dev python3-dev python3-numpy \
   libtbbmalloc2 libtbb-dev libdc1394-dev libopenexr-dev \
   libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev
-----------------------------------------------------------------

Obs.: aceitar os pacotes.


-Step 2. Clone OpenCV and Its Repositories
-----------------------------------------------------------------
(PV25) ... $  mkdir ~/opencv_build && cd ~/opencv_build
-----------------------------------------------------------------


-----------------------------------------------------------------
(PV25) ... $  git clone https://github.com/opencv/opencv.git
-----------------------------------------------------------------


-----------------------------------------------------------------
(PV25) ... $ git clone https://github.com/opencv/opencv_contrib.git
-----------------------------------------------------------------


-Step 3: Create a Build Directory
-----------------------------------------------------------------
(PV25) ... $  cd ~/opencv_build/opencv
-----------------------------------------------------------------


-----------------------------------------------------------------
(PV25) ... $  mkdir -p build && cd build
-----------------------------------------------------------------


-----------------------------------------------------------------
(PV25) ... $ cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_C_EXAMPLES=ON \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_build/opencv_contrib/modules \
    -D BUILD_EXAMPLES=ON ..
-----------------------------------------------------------------


-Step 4: Start Compilation

Obs.: o comando nproc devolve a quantidade de processadores do computador, e este numero será usado no comando make:
-----------------------------------------------------------------
(PV25) ... $  nproc
-----------------------------------------------------------------

Em cada computador utilize o número disponível.
Neste exempo, usamos nproc=12, portanto o comando make fica assim:

-----------------------------------------------------------------
(PV25) ... $  make -j12
-----------------------------------------------------------------

Obs.: este passo pode levar vários minutos, é necessário aguardar o término, antes de prosseguir adiante.

-Step 5: Install OpenCV
-----------------------------------------------------------------
(PV25) ... $ sudo make install
-----------------------------------------------------------------


-Step 6: Confirm Installation
o comando abaixo irá apresentar a versão do opencv que foi instalada.


-----------------------------------------------------------------
(PV25) ... $ pkg-config --modversion opencv4
-----------------------------------------------------------------


#####------------
Uma referência de instalar o OpenCV:
https://linuxize.com/post/how-to-install-opencv-on-ubuntu-20-04/
#####------------


-Step 7: OpenCV-Python Installation

o comando abaixo irá instalar o opencv-python:
-----------------------------------------------------------------
(PV25) ... $  pip install opencv-python
-----------------------------------------------------------------


instalar também o opencv-contrib-python:
-----------------------------------------------------------------
(PV25) ... $  pip install opencv-contrib-python
-----------------------------------------------------------------


verifique a versão instalada:
-----------------------------------------------------------------
(PV25) ... $  python3 -c "import cv2; print(cv2.__version__)"
-----------------------------------------------------------------



(((7))) EXECUTAR UM PROGRAMA de TESTE com o OPENCV:

Baixar o arquivo do programa de teste e o arquivo da imagem de teste na sua pasta pessoal:
-teste_messi.py
-messi5.jpg

Verificar se o programa executa satisfatoriamente, através deste tipo de comando:
-----------------------------------------------------------------
(PV25) ... $  cd ~/Documents/SuaPasta
-----------------------------------------------------------------

-----------------------------------------------------------------
(PV25) ... $  python3 teste_messi.py
-----------------------------------------------------------------

Obs.: Tecle ESC para fechar a janela da imagem.



(((8))) INSTALE O PROGRAMA VLC PARA VISUALIZAR IMAGENS E VIDEOS

-----------------------------------------------------------------
(PV25) ... $  sudo apt update
(PV25) ... $  sudo apt install vlc -y
-----------------------------------------------------------------
