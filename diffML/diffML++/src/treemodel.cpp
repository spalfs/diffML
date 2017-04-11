#include "inc/treemodel.hpp"

TreeModel::TreeModel(const QString &path, QObject *parent) : QAbstractItemModel(parent)
{
        QList<QVariant> rootData;
        rootData << "Tag" << "Text" << "Attributes";
        rootItem = new TreeItem(rootData);

        
        setupModelData(path, rootItem);
}

TreeModel::~TreeModel()
{
        delete rootItem;
}

QModelIndex TreeModel::index(int row, int column, const QModelIndex &parent) const
{
        if (!hasIndex(row, column, parent))
                return QModelIndex();

        TreeItem *parentItem;

        if (!parent.isValid())
                parentItem = rootItem;
        else
                parentItem = static_cast<TreeItem*>(parent.internalPointer());

        TreeItem *childItem = parentItem->child(row);
        if (childItem)
                return createIndex(row, column, childItem);
        else
                return QModelIndex();
}

QVariant TreeModel::data(const QModelIndex &index, int role) const
{
        if (!index.isValid())
                return QVariant();

        if (role != Qt::DisplayRole)
                return QVariant();

        TreeItem *item = static_cast<TreeItem*>(index.internalPointer());

        return item->data(index.column());
}

Qt::ItemFlags TreeModel::flags(const QModelIndex &index) const
{
        if(!index.isValid())
                return 0;
        
        return QAbstractItemModel::flags(index);
}

QModelIndex TreeModel::parent(const QModelIndex &index) const
{
        if (!index.isValid())
                return QModelIndex();

        TreeItem *childItem = static_cast<TreeItem*>(index.internalPointer());
        TreeItem *parentItem = childItem->parentItem();

        if (parentItem == rootItem)
                return QModelIndex();
        
        return createIndex(parentItem->row(), 0, parentItem);
}

QVariant TreeModel::headerData(int section, Qt::Orientation orientation, int role) const
{
        if (orientation == Qt::Horizontal && role == Qt::DisplayRole)
                return rootItem->data(section);

        return QVariant();
}

int TreeModel::rowCount(const QModelIndex &parent) const
{
        TreeItem *parentItem;
        if (parent.column() > 0)
                return 0;

        if (!parent.isValid())
                parentItem = rootItem;
        else 
                parentItem = static_cast<TreeItem*>(parent.internalPointer());

        return parentItem->childCount();
}

int TreeModel::columnCount(const QModelIndex &parent) const
{
        if (parent.isValid())
                return static_cast<TreeItem*>(parent.internalPointer())->columnCount();
        else
                return rootItem->columnCount();
}

void TreeModel::setupModelData(const QString &path, TreeItem *parent)
{
        QList<QVariant> columnData;

        columnData << "zz" << "aa" << "zz";

        TreeItem* child = new TreeItem(columnData, parent);
        parent->appendChild(child);

        TreeItem* childtwo = new TreeItem(columnData, child);
        child->appendChild(childtwo);
}
