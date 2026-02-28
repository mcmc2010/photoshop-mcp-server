#!/usr/bin/env python
"""Create a text layer in Photoshop."""
import os
import sys

os.environ['PS_VERSION'] = '2019'

import photoshop.api as ps
from photoshop_mcp_server.ps_adapter.application import PhotoshopApp

print('Getting active document...')
ps_app = PhotoshopApp()
doc = ps_app.get_active_document()

if not doc:
    print('ERROR: No active document!')
    print('Please create a document first.')
    sys.exit(1)

print(f'Document: {doc.name}')
print('Creating text layer with \"Hello World\"...')

# Create text layer
text_layer = doc.artLayers.add()
text_layer.kind = ps.LayerKind.TextLayer

# Configure text
text_item = text_layer.textItem
text_item.contents = 'Hello World'
text_item.position = [100, 100]
text_item.size = 48

# Set color (black)
text_color = ps.SolidColor()
text_color.rgb.red = 0
text_color.rgb.green = 0
text_color.rgb.blue = 0
text_item.color = text_color

print(f'Text layer created successfully!')
print(f'  Layer name: {text_layer.name}')
print(f'  Text: Hello World')
print(f'  Position: (100, 100)')
print(f'  Font size: 48pt')

sys.stdout.flush()
