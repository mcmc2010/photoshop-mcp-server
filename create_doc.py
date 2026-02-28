#!/usr/bin/env python
"""Create a new Photoshop document."""
import os
import sys

os.environ['PS_VERSION'] = '2019'

import photoshop.api as ps

print('Connecting to Photoshop...')
app = ps.Application()
print(f'Photoshop version: {app.version}')

print('Creating new document (800x600)...')
doc = app.documents.add(800, 600, 72, 'New Document', ps.NewDocumentMode.NewRGB)

print(f'Document created successfully!')
print(f'  Name: {doc.name}')
print(f'  Width: {doc.width}')
print(f'  Height: {doc.height}')
print(f'  Resolution: {doc.resolution}')

sys.stdout.flush()
