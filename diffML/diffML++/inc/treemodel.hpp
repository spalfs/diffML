#ifndef treemodel_h
#define treemodel_h

#include <QtCore/QAbstractItemModel>

class TreeModel : public QAbstractItemModel
{
        public:
                TreeModel(QString path);
        private:
                QModelIndex     index(int row, int column, const QModelIndex &parent = QModelIndex()) const;
                QModelIndex     parent(const QModelIndex &index) const;
                QVariant        data(const QModelIndex &index, int role = Qt::DisplayRole) const;
                int             rowCount(const QModelIndex &parent = QModelIndex()) const;
                int             columnCount(const QModelIndex &parent = QModelIndex()) const;

};

#endif
