#ifndef diffml_h
#define diffml_h

#include <QMainWindow>
#include <QSplitter>
#include <QMenuBar>
#include <QFileDialog>
#include <QTreeView>

#include "inc/treemodel.hpp"
#include "inc/treeview.hpp"
#include "inc/filter.hpp"
#include "inc/constants.hpp"

class diffML : public QMainWindow
{
        Q_OBJECT
        public:
                diffML();
        
        private:
                void initMenu();
                void open();
                void setColorState(int colorState);
                void update();

                QSplitter*      splitter;
                TreeView*       view;
                TreeModel*      model;
                Filter*         filter;
                QLineEdit*      filterText;
};

#endif
