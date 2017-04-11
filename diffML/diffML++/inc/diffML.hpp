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
        public:
                diffML();
        
        private:
                void initMenu();
                void open();
};

#endif
