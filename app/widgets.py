from flask_appbuilder.widgets import SearchWidget, as_unicode


class BillSearchWidget(SearchWidget):
    def __call__(self, **kwargs):
        """ create dict labels based on form """
        """ create dict of form widgets """
        """ create dict of possible filters """
        """ create list of active filters """
        label_columns = {}
        form_fields = {}
        search_filters = {}
        dict_filters = self.filters.get_search_filters()
        for col in self.template_args["include_cols"]:
            label_columns[col] = as_unicode(
                self.template_args["form"][col].label.text
            )
            form_fields[col] = self.template_args["form"][col]()
            search_filters[col] = [
                as_unicode(flt.name) for flt in dict_filters[col]
            ]

        search_filters["meterbox"] = [as_unicode("Starts with")]

        kwargs["label_columns"] = label_columns
        kwargs["form_fields"] = form_fields
        kwargs["search_filters"] = search_filters
        kwargs["active_filters"] = self.filters.get_filters_values_tojson()
        return super(BillSearchWidget, self).__call__(**kwargs)
