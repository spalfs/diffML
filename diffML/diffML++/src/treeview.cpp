#include "inc/treeview.hpp"

TreeView::TreeView()
{
        setUniformRowHeights(true);

        expandAction = new QAction(tr("&Expand All"), this);
        connect(expandAction, &QAction::triggered, this, &TreeView::expand);

        collapseAction = new QAction(tr("&Collapse All"), this);
        connect(collapseAction, &QAction::triggered, this, &TreeView::collapse);
}

void TreeView::contextMenuEvent(QContextMenuEvent* event)
{
        QMenu menu(this);
        menu.addAction(expandAction);
        menu.addAction(collapseAction);
        menu.exec(event->globalPos());
}

void TreeView::expand()
{
        expandAll();
}

void TreeView::collapse()
{
        collapseAll();
}
