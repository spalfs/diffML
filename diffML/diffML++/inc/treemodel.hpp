#ifndef treemodel_h
#define treemodel_h

#include <QtCore/QAbstractItemModel>

#include "inc/treeitem.hpp"

class TreeModel : public QAbstractItemModel
{
        Q_OBJECT
        public:
                explicit TreeModel(const QString &data, QObject *parent = 0);
                ~TreeModel();

                QModelIndex     index(int row, int column, const QModelIndex &parent = QModelIndex())           const override;
                QVariant        data(const QModelIndex &index, int role = Qt::DisplayRole)                      const override;
                Qt::ItemFlags   flags(const QModelIndex &index)                                                 const override;
                QModelIndex     parent(const QModelIndex &index)                                                const override;
                QVariant        headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole)const override;
                int             rowCount(const QModelIndex &parent = QModelIndex())                             const override;
                int             columnCount(const QModelIndex &parent = QModelIndex())                          const override;

        private:
                void setupModelData(const QStringList &line, TreeItem *parent);

                TreeItem *rootItem;
};

#endif
