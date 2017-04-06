#include "inc/main.hpp"

int main(int argc, char **argv){
        QApplication app(argc, argv);
        
        diffML diffml;
        diffml.show();

        return app.exec();
}
