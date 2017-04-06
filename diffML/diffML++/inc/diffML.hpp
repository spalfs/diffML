#ifndef diffml_h
#define diffml_h

#include <QtWidgets/QMainWindow>
#include <QtWidgets/QSplitter>
#include <QtWidgets/QMenuBar>

class diffML : public QMainWindow
{
        public:
                diffML();
        
        private:
                void initMenu();
};

#endif
