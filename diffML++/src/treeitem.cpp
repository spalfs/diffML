#include "inc/treeitem.hpp"

TreeItem::TreeItem(const QList<QVariant> &data, int d, TreeItem *parent)
{
        m_parentItem = parent;
        m_itemData = data;
        depth = d;
}

TreeItem::~TreeItem()
{
        qDeleteAll(m_childItems);
}

void TreeItem::appendChild(TreeItem *item)
{
        m_childItems.append(item);
}

TreeItem *TreeItem::child(int row)
{
        return m_childItems.value(row);
}

int TreeItem::childCount() const
{
        return m_childItems.count();
}

int TreeItem::row() const
{
        if (m_parentItem)
                return m_parentItem->m_childItems.indexOf(const_cast<TreeItem*>(this));
        
        return 0;
}

int TreeItem::columnCount() const
{
        return m_itemData.count();
}

QVariant TreeItem::data(int column) const
{
        return m_itemData.value(column);
}

TreeItem *TreeItem::parentItem()
{
        return m_parentItem;
}

void TreeItem::setColorState(int colorS){
        colorState = colorS;
}
