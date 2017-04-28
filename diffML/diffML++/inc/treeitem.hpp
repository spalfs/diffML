#ifndef treeitem_h
#define treeitem_h

#include <QVariant>

class TreeItem
{
        public:
                explicit        TreeItem(const QList<QVariant> &data, int d = 0, TreeItem *parentItem = 0);
                ~TreeItem();

                void            appendChild(TreeItem *child);

                TreeItem*       child(int row);
                int             childCount()            const;
                int             columnCount()           const;
                QVariant        data(int column)        const;
                int             row()                   const;
                TreeItem*       parentItem();

                void            setColorState(int colorS);
                int             getColorState(){return colorState;};
                int             getDepth(){return depth;};

        private:
                QList<TreeItem*>        m_childItems;
                QList<QVariant>         m_itemData;
                TreeItem*               m_parentItem;
                int                     colorState;
                int                     depth;
};

#endif
