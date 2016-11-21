# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
import swapper
from menuhin.models import ModelMenuItemGroup, registry


class VarletMenu(ModelMenuItemGroup):
    model = swapper.load_model('varlet', 'Page')
registry.register(VarletMenu)
