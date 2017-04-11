#ifndef diffml_h
#define diffml_h

#include <QMainWindow>
#include <QSplitter>
#include <QMenuBar>
#include <QFileDialog>
#include <QTreeView>

#include "inc/treemodel.hpp"

class diffML : public QMainWindow
{
        Q_OBJECT
        public:
                diffML();
        
        private:
                void initMenu();
                void open();

                QSplitter splitter;
                QTreeView view;
                TreeModel* model;
};

#endif
