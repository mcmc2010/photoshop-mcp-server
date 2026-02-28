#!/usr/bin/env python
"""Check document status."""
import os
import sys

os.environ['PS_VERSION'] = '2019'

import photoshop.api as ps

print('Connecting to Photoshop...')
app = ps.Application()
print(f'Photoshop version: {app.version}')
print(f'Documents count: {len(app.documents)}')

if len(app.documents) > 0:
    doc = app.activeDocument
    print(f'\nActive document: {doc.name}')
    print(f'Size: {doc.width} x {doc.height}')
    print(f'Layers count: {len(doc.artLayers)}')
    print('\nLayers:')
    for layer in doc.artLayers:
        print(f'  [{layer.kind}] {layer.name} (visible: {layer.visible})')
else:
    print('No documents open!')

sys.stdout.flush()
