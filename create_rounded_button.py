#!/usr/bin/env python
"""Create a rounded button with centered text in Photoshop."""
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

# Delete old button layers if they exist
print('Cleaning up old layers...')
layers_to_delete = ["Button Background", "Hello World"]
for layer in doc.artLayers:
    if layer.name in layers_to_delete or layer.name.startswith("Hello World"):
        try:
            layer.delete()
            print(f'  Deleted: {layer.name}')
        except:
            pass

# Button dimensions
btn_width = 200
btn_height = 50
btn_x = 300  # Center X
btn_y = 275  # Center Y
corner_radius = 10

print(f'Creating rounded button ({btn_width}x{btn_height}, radius={corner_radius})...')

# Use JavaScript to create proper rounded rectangle
js_script = """
try {
    var doc = app.activeDocument;

    // Set foreground color to blue (#4A90D9)
    var btnColor = new SolidColor();
    btnColor.rgb.hexValue = "4A90D9";
    app.foregroundColor = btnColor;

    // Rounded rectangle coordinates
    var x1 = 300;
    var y1 = 275;
    var x2 = 500;
    var y2 = 325;
    var radius = 10;

    // Create path for rounded rectangle
    var idPath = charIDToTypeID('Path');
    var idAdd = charIDToTypeID('Add ');

    // Create the rounded rectangle path using action manager
    var desc = new ActionDescriptor();
    var ref = new ActionReference();
    ref.putClass(idPath);
    desc.putReference(charIDToTypeID('null'), ref);

    var desc2 = new ActionDescriptor();
    desc2.putUnitDouble(charIDToTypeID('Left'), charIDToTypeID('#Pxl'), x1);
    desc2.putUnitDouble(charIDToTypeID('Top '), charIDToTypeID('#Pxl'), y1);
    desc2.putUnitDouble(charIDToTypeID('Rght'), charIDToTypeID('#Pxl'), x2);
    desc2.putUnitDouble(charIDToTypeID('Btom'), charIDToTypeID('#Pxl'), y2);
    desc2.putUnitDouble(charIDToTypeID('Rds '), charIDToTypeID('#Pxl'), radius);
    desc2.putBoolean(charIDToTypeID('AntA'), true);

    desc.putObject(charIDToTypeID('T   '), charIDToTypeID('Rctn'), desc2);
    executeAction(idAdd, desc, DialogModes.NO);

    // Fill the path
    var fillDesc = new ActionDescriptor();
    fillDesc.putBoolean(charIDToTypeID('AntA'), true);
    executeAction(charIDToTypeID('Fl  '), fillDesc, DialogModes.NO);

    // Delete the work path
    var pathRef = new ActionReference();
    pathRef.putProperty(charIDToTypeID('Path'), charIDToTypeID('WrkP'));
    var pathDesc = new ActionDescriptor();
    pathDesc.putReference(charIDToTypeID('null'), pathRef);
    executeAction(charIDToTypeID('Dlt '), pathDesc, DialogModes.NO);

    // Rename layer
    doc.activeLayer.name = "Button Background";

    'Button created successfully';
} catch(e) {
    'Error: ' + e.toString();
}
"""

result = ps_app.execute_javascript(js_script)
print(f'JavaScript result: {result}')

# Create text layer with centered text
print('Creating centered text...')

# Create new text layer
text_layer = doc.artLayers.add()
text_layer.kind = ps.LayerKind.TextLayer
text_layer.name = "Button Text"

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

# Calculate center position for text
text_x = btn_x + btn_width / 2  # 400
text_y = btn_y + btn_height / 2  # 300

# Adjust for text baseline (approximately)
text_y -= 8

text_item.position = [text_x, text_y]

print('Rounded button created successfully!')
print(f'  Button: {btn_width}x{btn_height} px')
print(f'  Corner radius: {corner_radius} px')
print(f'  Position: ({btn_x}, {btn_y})')
print(f'  Text: "Hello World" (centered, white)')

sys.stdout.flush()
