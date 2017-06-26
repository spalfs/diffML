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

        TreeItem *item = static_cast<TreeItem*>(index.internalPointer());

        if (role == Qt::BackgroundRole){
                if (item->getColorState() == NONE)
                        return QBrush(Qt::transparent);
                else if (item->getColorState() == HIERARCHY){
                        if (item->getDepth() == 1)
                                return QBrush(QColor(157,159,85));
                        else if (item->getDepth() == 2)
                                return QBrush(QColor(85,157,159));
                        else if (item->getDepth() == 3)
                                return QBrush(QColor(85,120,159));
                        else if (item->getDepth() == 4)
                                return QBrush(QColor(159,87,85));
                        else if (item->getDepth() == 5)
                                return QBrush(QColor(120,159,85));
                        else if (item->getDepth() == 6)
                                return QBrush(QColor(159,85,120));
                        else if (item->getDepth() == 7)
                                return QBrush(QColor(85,159,124));
                        else if (item->getDepth() == 8)
                                return QBrush(QColor(124,85,159));
                }
        }

        if (role != Qt::DisplayRole)
                return QVariant();

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
        QByteArray ba = path.toLatin1();
        char * cp = ba.data();

        xmlDoc  *xmlDoc = xmlReadFile(cp, NULL, 0);
        xmlNode *xmlRoot= xmlDocGetRootElement(xmlDoc);

        setupModelDataRecursive(xmlRoot, parent);

        //xmlFreeDoc(xmlDoc);  

        //xmlCleanupParser();
}

void TreeModel::setupModelDataRecursive(xmlNode* element, TreeItem* parent, int depth){
        depth++;
        xmlNode* i;

        for( i = element; i; i = i->next ){
                if (i->type == XML_ELEMENT_NODE) { 
                        QList<QVariant> columnData;

                        columnData << (char*)i->name;

                        char* content = (char*)xmlNodeGetContent(i);
                        if (strlen(content) < MAX_CONTENT)
                                columnData << content;
                        else
                                columnData << "";

                        xmlAttr* j;
                        QString attribs;
                        for ( j = i->properties; j; j = j->next){
                                attribs.append('{');
                                attribs.append((char*)j->name);
                                attribs.append(':');
                                attribs.append((char*)xmlNodeListGetString(i->doc, j->children, 1));
                                attribs.append('}');
                        }

                        columnData << attribs;

                        TreeItem* element = new TreeItem(columnData, depth, parent);
                        parent->appendChild(element);

                        setupModelDataRecursive(i->children, element, depth);
                }
        }
}

void TreeModel::setColorState(int colorState){
        setColorState(colorState, rootItem);
}

void TreeModel::setColorState(int colorState, TreeItem* node){
        int i;
        for(i = 0; i < node->childCount(); i++){
                node->child(i)->setColorState(colorState);
                setColorState(colorState, node->child(i));
        }
}
