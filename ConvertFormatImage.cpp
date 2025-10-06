#include <opencv2/opencv.hpp>
#include <iostream>

using namespace cv;

int main(int argc, char** argv)
{
    std::string imagePath;

    // Se nenhum argumento for passado, usar messi5.jpg como default
    if (argc == 1) {
        imagePath = "messi5.jpg";
    } else if (argc == 2) {
        imagePath = argv[1];
    } else {
        std::cout << "Uso: " << argv[0] << " [caminho_imagem]" << std::endl;
        return -1;
    }

    // Carregar a imagem
    Mat image = imread(imagePath, IMREAD_COLOR);
    if (!image.data) {
        std::cout << "Erro ao abrir ou encontrar a imagem: " << imagePath << std::endl;
        return -1;
    }

    // Exibir a imagem
    namedWindow("Imagem", WINDOW_AUTOSIZE);
    imshow("Imagem", image);

    // Salvar a imagem em .png
    std::string outputFile = "./resources/messi5.png";
    if (imwrite(outputFile, image)) {
        std::cout << "Imagem salva com sucesso: " << outputFile << std::endl;
    } else {
        std::cout << "Erro ao salvar a imagem." << std::endl;
    }

    waitKey(0); // Espera tecla para fechar janela
    destroyAllWindows();

    return 0;
}
