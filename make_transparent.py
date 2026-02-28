#!/usr/bin/env python
"""Make background layer transparent in Photoshop."""
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
    sys.exit(1)

print(f'Document: {doc.name}')

# Get layers
layers = doc.artLayers
print(f'Total layers: {len(layers)}')

# Find background layer
bg_layer = None
for layer in layers:
    print(f'  - {layer.name} (isBackgroundLayer: {layer.isBackgroundLayer})')
    if layer.isBackgroundLayer:
        bg_layer = layer
        break

if bg_layer:
    print(f'\nFound background layer: {bg_layer.name}')
    print('Converting background to normal layer...')
    
    # Convert background to normal layer
    bg_layer.isBackgroundLayer = False
    bg_layer.name = 'Layer 0'
    
    # Clear the layer (make it transparent)
    print('Clearing layer to make it transparent...')
    doc.activeLayer = bg_layer
    
    # Select all and delete
    doc.selection.selectAll()
    doc.selection.clear()
    doc.selection.deselect()
    
    print('Background layer converted and cleared!')
else:
    print('\nNo background layer found.')
    print('Trying to clear the first layer...')
    
    # If no background layer, try to clear the bottom layer
    first_layer = layers[0]
    doc.activeLayer = first_layer
    doc.selection.selectAll()
    doc.selection.clear()
    doc.selection.deselect()
    print(f'Layer "{first_layer.name}" cleared!')

print('\nDone! Background is now transparent.')

sys.stdout.flush()
