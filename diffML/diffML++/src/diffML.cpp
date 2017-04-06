#include "inc/diffML.hpp"

diffML::diffML(){
        QSplitter Splitter; 
        setCentralWidget(&Splitter);

        initMenu();
}

void diffML::initMenu(){
        QMenu *file = menuBar()->addMenu("&File");
        QMenu *edit = menuBar()->addMenu("&Edit");
        QMenu *view = menuBar()->addMenu("&View");
        QMenu *help = menuBar()->addMenu("&Help");
}
