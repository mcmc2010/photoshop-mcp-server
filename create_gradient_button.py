#!/usr/bin/env python
"""Create a smaller gradient button with sharp edges."""
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

# Smaller button parameters
btn_width = 140
btn_height = 40
btn_x = 330  # Center X (800/2 - 70)
btn_y = 280  # Center Y (600/2 - 20)
corner_radius = 8

print(f'Creating smaller button ({btn_width}x{btn_height})...')

# Use JavaScript for gradient fill with rounded corners
js_gradient_button = f"""
(function() {{
    var doc = app.activeDocument;

    // Create new layer
    var btnLayer = doc.artLayers.add();
    btnLayer.name = "Button Background";

    // Button coordinates
    var x1 = {btn_x};
    var y1 = {btn_y};
    var x2 = {btn_x + btn_width};
    var y2 = {btn_y + btn_height};
    var radius = {corner_radius};

    // Create rounded rectangle selection
    // Using elliptical marquee approach for smooth corners
    var desc = new ActionDescriptor();
    var ref = new ActionReference();
    ref.putProperty(charIDToTypeID('Chnl'), charIDToTypeID('fsel'));
    desc.putReference(charIDToTypeID('null'), ref);

    var desc2 = new ActionDescriptor();
    desc2.putUnitDouble(charIDToTypeID('Left'), charIDToTypeID('#Pxl'), x1);
    desc2.putUnitDouble(charIDToTypeID('Top '), charIDToTypeID('#Pxl'), y1);
    desc2.putUnitDouble(charIDToTypeID('Rght'), charIDToTypeID('#Pxl'), x2);
    desc2.putUnitDouble(charIDToTypeID('Btom'), charIDToTypeID('#Pxl'), y2);
    desc2.putUnitDouble(charIDToTypeID('Rds '), charIDToTypeID('#Pxl'), radius);

    desc.putObject(charIDToTypeID('T   '), charIDToTypeID('RndR'), desc2);
    executeAction(charIDToTypeID('setd'), desc, DialogModes.NO);

    // Create gradient (darker blue at bottom, lighter at top)
    var gradientDesc = new ActionDescriptor();
    gradientDesc.putEnumerated(charIDToTypeID('From'), charIDToTypeID('Ordn'), charIDToTypeID('Top '));
    gradientDesc.putEnumerated(charIDToTypeID('T   '), charIDToTypeID('Ordn'), charIDToTypeID('Btom'));

    var gradientColor = new ActionDescriptor();
    var colors = new ActionList();

    // Color stop 1: lighter blue at top
    var stop1 = new ActionDescriptor();
    var color1 = new ActionDescriptor();
    color1.putDouble(charIDToTypeID('Rd  '), 100);  // Lighter
    color1.putDouble(charIDToTypeID('Grn '), 165);
    color1.putDouble(charIDToTypeID('Bl  '), 240);
    stop1.putObject(charIDToTypeID('Clr '), charIDToTypeID('RGBC'), color1);
    stop1.putUnitDouble(charIDToTypeID('Lctn'), charIDToTypeID('#Prc'), 0);
    colors.putObject(charIDToTypeID('Clrt'), stop1);

    // Color stop 2: darker blue at bottom
    var stop2 = new ActionDescriptor();
    var color2 = new ActionDescriptor();
    color2.putDouble(charIDToTypeID('Rd  '), 50);   // Darker
    color2.putDouble(charIDToTypeID('Grn '), 110);
    color2.putDouble(charIDToTypeID('Bl  '), 190);
    stop2.putObject(charIDToTypeID('Clr '), charIDToTypeID('RGBC'), color2);
    stop2.putUnitDouble(charIDToTypeID('Lctn'), charIDToTypeID('#Prc'), 100);
    colors.putObject(charIDToTypeID('Clrt'), stop2);

    gradientColor.putList(charIDToTypeID('Clrs'), colors);

    // Transparency stops
    var trans = new ActionList();
    var t1 = new ActionDescriptor();
    t1.putUnitDouble(charIDToTypeID('Lctn'), charIDToTypeID('#Prc'), 0);
    t1.putUnitDouble(charIDToTypeID('Opct'), charIDToTypeID('#Prc'), 100);
    trans.putObject(charIDToTypeID('TrnS'), t1);

    var t2 = new ActionDescriptor();
    t2.putUnitDouble(charIDToTypeID('Lctn'), charIDToTypeID('#Prc'), 100);
    t2.putUnitDouble(charIDToTypeID('Opct'), charIDToTypeID('#Prc'), 100);
    trans.putObject(charIDToTypeID('TrnS'), t2);

    gradientColor.putList(charIDToTypeID('Trns'), trans);
    gradientColor.putString(charIDToTypeID('Nm  '), "Button Gradient");

    gradientDesc.putObject(charIDToTypeID('Grad'), charIDToTypeID('Grdn'), gradientColor);

    executeAction(charIDToTypeID('GrFl'), gradientDesc, DialogModes.NO);
    doc.selection.deselect();

    return "Gradient button created";
}})();
"""

result = ps_app.execute_javascript(js_gradient_button)
print(f'Result: {result}')

# Create text layer
print('Creating centered text...')
text_layer = doc.artLayers.add()
text_layer.kind = ps.LayerKind.TextLayer
text_layer.name = "Button Text"

text_item = text_layer.textItem
text_item.contents = "Hello World"
text_item.size = 14  # Smaller font
text_item.justification = ps.Justification.Center

# White color
text_color = ps.SolidColor()
text_color.rgb.red = 255
text_color.rgb.green = 255
text_color.rgb.blue = 255
text_item.color = text_color

# Center text on button
text_x = btn_x + btn_width / 2
text_y = btn_y + btn_height / 2
text_item.position = [text_x, text_y]

print('\n=== Gradient Button Created ===')
print(f'Size: {btn_width}x{btn_height} px (smaller)')
print(f'Corner radius: {corner_radius} px')
print(f'Position: ({btn_x}, {btn_y})')
print(f'Gradient: Top light blue -> Bottom dark blue')
print(f'Text: "Hello World" (14pt, centered, white)')
print('==============================')

sys.stdout.flush()
