#include "inc/diffML.hpp"

diffML::diffML(){
        setCentralWidget(&splitter);

        initMenu();
        splitter.addWidget(&view);

        this->show();
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

        model = new TreeModel(path);
        view.setModel(model);
}
