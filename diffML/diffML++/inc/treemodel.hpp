#ifndef treemodel_h
#define treemodel_h

#include <QtCore/QAbstractItemModel>

class TreeModel : public QAbstractItemModel
{
        public:
                TreeModel(QString path);
        private:

};

#endif
