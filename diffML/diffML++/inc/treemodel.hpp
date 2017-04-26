#ifndef treemodel_h
#define treemodel_h

#include <QAbstractItemModel>
#include <libxml/xmlreader.h>

#include "inc/treeitem.hpp"

#define MAX_CONTENT 25

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
                void setupModelData(const QString &path, TreeItem *parent);
                void setupModelDataRecursive(xmlNode* element, TreeItem* parent, int depth = 0);

                TreeItem *rootItem;
};

#endif
