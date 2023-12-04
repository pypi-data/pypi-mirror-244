#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import syz.common


print(syz.tools.current_python_file_path())
print(syz.tools.current_python_file_path(__file__))
