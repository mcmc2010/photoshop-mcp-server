#!/usr/bin/env python
"""Create a button with 'Hello World' text in Photoshop."""
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
print('Creating button shape...')

# Button dimensions
btn_width = 200
btn_height = 50
btn_x = 300  # Center X (800/2 - 100)
btn_y = 275  # Center Y (600/2 - 25)
corner_radius = 10

# Use JavaScript to create rounded rectangle button
js_script = f"""
try {{
    var doc = app.activeDocument;
    
    // Create a new layer for the button
    var btnLayer = doc.artLayers.add();
    btnLayer.name = "Button Background";
    
    // Set foreground color to blue (#4A90D9)
    var btnColor = new SolidColor();
    btnColor.rgb.hexValue = "4A90D9";
    app.foregroundColor = btnColor;
    
    // Create rounded rectangle selection
    var x1 = {btn_x};
    var y1 = {btn_y};
    var x2 = {btn_x} + {btn_width};
    var y2 = {btn_y} + {btn_height};
    var radius = {corner_radius};
    
    // Use rounded rectangle tool via selection
    doc.selection.select([
        [x1 + radius, y1],
        [x2 - radius, y1],
        [x2, y1],
        [x2, y1 + radius],
        [x2, y2 - radius],
        [x2, y2],
        [x2 - radius, y2],
        [x1 + radius, y2],
        [x1, y2],
        [x1, y2 - radius],
        [x1, y1 + radius],
        [x1, y1]
    ]);
    
    // Create rounded rectangle using path
    var desc = new ActionDescriptor();
    var ref = new ActionReference();
    ref.putClass(charIDToTypeID('Path'));
    desc.putReference(charIDToTypeID('null'), ref);
    
    var list = new ActionList();
    var pointList = new ActionList();
    
    // Top edge
    pointList.putUnitDouble(charIDToTypeID('Hrzn'), charIDToTypeID('#Pxl'), x1 + radius);
    pointList.putUnitDouble(charIDToTypeID('Vrtc'), charIDToTypeID('#Pxl'), y1);
    
    pointList.putUnitDouble(charIDToTypeID('Hrzn'), charIDToTypeID('#Pxl'), x2 - radius);
    pointList.putUnitDouble(charIDToTypeID('Vrtc'), charIDToTypeID('#Pxl'), y1);
    list.putList(charIDToTypeID('Pts '), pointList);
    
    desc.putList(charIDToTypeID('T   '), list);
    executeAction(charIDToTypeID('setd'), desc, DialogModes.NO);
    
    // Fill with color
    doc.selection.selectAll();
    doc.selection.fill(app.foregroundColor);
    doc.selection.deselect();
    
    // Actually draw the rounded rectangle
    // Simple approach: draw filled rounded rectangle
    var artLayer = doc.activeLayer;
    
    'Button created';
}} catch(e) {{
    'Error: ' + e.toString();
}}
"""

# Simpler approach: create a solid color layer and shape
print('Creating button background...')

# Create a new layer for button background
btn_layer = doc.artLayers.add()
btn_layer.name = "Button Background"
doc.activeLayer = btn_layer

# Create selection for rounded rectangle (approximated)
# Top-left corner to bottom-right
x1, y1 = btn_x, btn_y
x2, y2 = btn_x + btn_width, btn_y + btn_height

# Simple rectangle selection
doc.selection.select([
    [x1, y1],
    [x2, y1],
    [x2, y2],
    [x1, y2]
])

# Set fill color (blue)
fill_color = ps.SolidColor()
fill_color.rgb.red = 74
fill_color.rgb.green = 144
fill_color.rgb.blue = 217

# Fill selection
doc.selection.fill(fill_color)
doc.selection.deselect()

print('Button background created!')

# Create text layer
print('Adding text...')
text_layer = doc.artLayers.add()
text_layer.kind = ps.LayerKind.TextLayer

text_item = text_layer.textItem
text_item.contents = "Hello World"
text_item.size = 18
text_item.justification = ps.Justification.Center

# White text color
text_color = ps.SolidColor()
text_color.rgb.red = 255
text_color.rgb.green = 255
text_color.rgb.blue = 255
text_item.color = text_color

# Position text in center of button
text_x = btn_x + btn_width / 2
text_y = btn_y + btn_height / 2 - 10  # Adjust for baseline
text_item.position = [text_x, text_y]

print('Button created successfully!')
print(f'  Button size: {btn_width}x{btn_height}')
print(f'  Position: ({btn_x}, {btn_y})')
print(f'  Text: Hello World')

sys.stdout.flush()
