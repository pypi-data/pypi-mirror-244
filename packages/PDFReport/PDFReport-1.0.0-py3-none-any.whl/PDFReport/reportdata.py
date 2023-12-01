from abc import ABCMeta


class ReportData(metaclass=ABCMeta):

    def on_text_data(self, text_frame):
        pass

    def on_barcode_data(self, barcode_frame):
        pass

    def on_image_data(self, image_frame):
        pass

    def on_table_data(self, table_frame):
        pass
