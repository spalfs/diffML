#ifndef treeview_h
#define treeview_h

#include <QtWidgets>

class TreeView : public QTreeView
{
        Q_OBJECT
        public:
                explicit TreeView();
        protected:
                void contextMenuEvent(QContextMenuEvent* event) override;
        private slots:
                void expand();
                void collapse();
        private:
                QAction* expandAction;
                QAction* collapseAction;
};

#endif
