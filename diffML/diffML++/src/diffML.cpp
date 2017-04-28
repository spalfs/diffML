#include "inc/diffML.hpp"

diffML::diffML(){
        setCentralWidget(&splitter);

        initMenu();
        splitter.addWidget(&view);

        model = NULL;

        this->show();
}

void diffML::initMenu(){
        QMenu *file = menuBar()->addMenu("&File");

        QAction *open = new QAction("&Open", this);
        connect(open, &QAction::triggered, this, &diffML::open);
        file->addAction(open);

        //QMenu *edit = menuBar()->addMenu("&Edit");

        QMenu *view = menuBar()->addMenu("&View");

        QMenu *colorMenu = view->addMenu("&Color");
        QActionGroup *colorGroup = new QActionGroup(this);
        colorGroup->setExclusive(true);

        QAction *none = new QAction("&None", this);
        connect(none, &QAction::triggered, this, [this]{diffML::setColorState(NONE);});
        none->setCheckable(true);
        none->setChecked(true);
        colorGroup->addAction(none);
        colorMenu->addAction(none);

        QAction *hier = new QAction("&Hierarchy", this);
        connect(hier, &QAction::triggered, this, [this]{diffML::setColorState(HIERARCHY);});
        hier->setCheckable(true);
        colorGroup->addAction(hier);
        colorMenu->addAction(hier);
        
        //QMenu *help = menuBar()->addMenu("&Help");
}

void diffML::open(){
        QFileDialog FileDialog;
        QString path = FileDialog.getOpenFileName(this);

        model = new TreeModel(path);
        view.setModel(model);
}

void diffML::setColorState(int colorState){
        if (model)
                model->setColorState(colorState);
}
