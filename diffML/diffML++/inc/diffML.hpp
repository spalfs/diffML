#ifndef diffml_h
#define diffml_h

#include <QtWidgets/QMainWindow>
#include <QtWidgets/QSplitter>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QFileDialog>
#include <QtWidgets/QTreeView>

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
