#include "inc/diffML.hpp"

diffML::diffML(){
        QSplitter Splitter; 
        setCentralWidget(&Splitter);

        initMenu();
}

void diffML::initMenu(){
        QMenu *file = menuBar()->addMenu("&File");

        QAction *open = new QAction("&Open", this);
        connect(open, &QAction::triggered, this, &diffML::open);
        file->addAction(open);

        //QMenu *edit = menuBar()->addMenu("&Edit");
        //QMenu *view = menuBar()->addMenu("&View");
        //QMenu *help = menuBar()->addMenu("&Help");
}

void diffML::open(){
        QFileDialog FileDialog;
        QString path = FileDialog.getOpenFileName(this);
        TreeModel model(path);

        QTreeView view;
        view.setModel(&model);
        view.show();
}
