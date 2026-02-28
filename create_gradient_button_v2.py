#!/usr/bin/env python
"""Create gradient button using gradient fill layer."""
import os
import sys

os.environ['PS_VERSION'] = '2019'

import photoshop.api as ps
from photoshop_mcp_server.ps_adapter.application import PhotoshopApp

print('Connecting to Photoshop...')
ps_app = PhotoshopApp()
doc = ps_app.get_active_document()

if not doc:
    print('ERROR: No active document!')
    sys.exit(1)

print(f'Document: {doc.name}')

# Delete existing button layers
print('Removing old layers...')
layers_to_keep = ['Layer 0']
for layer in list(doc.artLayers):
    if layer.name not in layers_to_keep:
        print(f'  Deleting: {layer.name}')
        layer.delete()

# Button parameters
btn_width = 140
btn_height = 40
btn_x = 330
btn_y = 280

print(f'Creating gradient button ({btn_width}x{btn_height})...')

# Create selection for button area
doc.selection.select([
    [btn_x, btn_y],
    [btn_x + btn_width, btn_y],
    [btn_x + btn_width, btn_y + btn_height],
    [btn_x, btn_y + btn_height]
])

# Create new layer
btn_layer = doc.artLayers.add()
btn_layer.name = "Button Background"

# Set foreground and background colors for gradient
app = ps.Application()
app.foregroundColor.rgb.hexValue = "64A5F0"  # Light blue
app.backgroundColor.rgb.hexValue = "326EBE"  # Dark blue

# Apply gradient using Action Manager
print('Applying gradient...')
js_gradient = """
try {
    var desc = new ActionDescriptor();
    desc.putEnumerated(charIDToTypeID('From'), charIDToTypeID('Ordn'), charIDToTypeID('Top '));
    desc.putEnumerated(charIDToTypeID('T   '), charIDToTypeID('Ordn'), charIDToTypeID('Btom'));
    desc.putBoolean(charIDToTypeID('Dthr'), false);
    desc.putBoolean(charIDToTypeID('UsMs'), false);
    desc.putEnumerated(stringIDToTypeID('gradientType'), stringIDToTypeID('gradientType'), stringIDToTypeID('linear'));

    executeAction(charIDToTypeID('GrFl'), desc, DialogModes.NO);
    'Gradient applied';
} catch(e) {
    'Error: ' + e.toString();
}
"""

result = ps_app.execute_javascript(js_gradient)
print(f'Gradient result: {result}')

doc.selection.deselect()

# Create text layer
print('Creating text...')
text_layer = doc.artLayers.add()
text_layer.kind = ps.LayerKind.TextLayer
text_layer.name = "Button Text"

text_item = text_layer.textItem
text_item.contents = "Hello World"
text_item.size = 14
text_item.justification = ps.Justification.Center

text_color = ps.SolidColor()
text_color.rgb.red = 255
text_color.rgb.green = 255
text_color.rgb.blue = 255
text_item.color = text_color

text_x = btn_x + btn_width / 2
text_y = btn_y + btn_height / 2
text_item.position = [text_x, text_y]

print('\n=== Gradient Button Created ===')
print(f'Size: {btn_width}x{btn_height} px')
print(f'Gradient: Light blue (#64A5F0) -> Dark blue (#326EBE)')
print(f'Text: "Hello World" (14pt, white, centered)')
print('==============================')

sys.stdout.flush()
