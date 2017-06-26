#ifndef filter_h
#define filter_h

#include <QSortFilterProxyModel>

class Filter : public QSortFilterProxyModel
{
        Q_OBJECT

        public:
                Filter(QObject* parent);

        protected:
                virtual bool filterAcceptsRow(int source_row, const QModelIndex& source_parent) const override;
};

#endif
