"""
Common class for all Bathers
"""


class Dosator():
    def __init__(self, name, index):
        self.name = name
        self.index = index
        self.zero_point = 0, 0, 0
        self.cell_size_offset = 0, 0, 0

    @property
    def pick_up_point(self):
        ret_val = [0, 0, 0]
        for dimension in range(2):
            ret_val[dimension] = self.zero_point[dimension] + self.cell_size_offset[0] * self.index

        return ret_val

    def dose(self):
        raise NotImplementedError('Define Method Dose for class {}'.format(self.__class__.__name__))


class DosatorController:
    def __init__(self, dosator_class, products):
        self._products = {product: dosator_class(product, products.index(product)) for product in products}

    def get_dosator(self, product: str):
        if product not in self._products:
            raise errors.ProductNotFoundInDosator(product=product)
        return self._products[product]
