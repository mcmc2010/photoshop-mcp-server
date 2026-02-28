#!/usr/bin/env python
"""Create a gradient button - simpler approach."""
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
btn_x = 330
btn_y = 280

print(f'Creating button ({btn_width}x{btn_height})...')

# Create button background layer
btn_layer = doc.artLayers.add()
btn_layer.name = "Button Background"

# Create rectangle selection
doc.selection.select([
    [btn_x, btn_y],
    [btn_x + btn_width, btn_y],
    [btn_x + btn_width, btn_y + btn_height],
    [btn_x, btn_y + btn_height]
])

# Create gradient from top to bottom
# Light blue at top, dark blue at bottom
gradient_color_top = ps.SolidColor()
gradient_color_top.rgb.red = 100
gradient_color_top.rgb.green = 165
gradient_color_top.rgb.blue = 240

gradient_color_bottom = ps.SolidColor()
gradient_color_bottom.rgb.red = 50
gradient_color_bottom.rgb.green = 110
gradient_color_bottom.rgb.blue = 190

# Use gradient tool via JavaScript
js_gradient = f"""
(function() {{
    var doc = app.activeDocument;

    // Define gradient colors
    var topColor = [100, 165, 240];  // Light blue
    var bottomColor = [50, 110, 190];  // Dark blue

    // Get foreground and background colors
    app.foregroundColor.rgb.red = topColor[0];
    app.foregroundColor.rgb.green = topColor[1];
    app.foregroundColor.rgb.blue = topColor[2];

    app.backgroundColor.rgb.red = bottomColor[0];
    app.backgroundColor.rgb.green = bottomColor[1];
    app.backgroundColor.rgb.blue = bottomColor[2];

    return "Colors set for gradient";
}})();
"""

ps_app.execute_javascript(js_gradient)

# Apply gradient fill
try:
    # Create gradient fill layer manually
    print('Applying gradient...')

    # Use gradient tool
    start_point = [btn_x + btn_width/2, btn_y]
    end_point = [btn_x + btn_width/2, btn_y + btn_height]

    # Simple gradient using JavaScript
    js_fill_gradient = """
    (function() {
        var doc = app.activeDocument;
        var sel = doc.selection;

        // Create gradient fill
        var desc = new ActionDescriptor();
        desc.putEnumerated(charIDToTypeID('From'), charIDToTypeID('Ordn'), charIDToTypeID('Top '));
        desc.putEnumerated(charIDToTypeID('T   '), charIDToTypeID('Ordn'), charIDToTypeID('Btom'));

        executeAction(charIDToTypeID('GrFl'), desc, DialogModes.NO);
        return "Gradient applied";
    })();
    """
    ps_app.execute_javascript(js_fill_gradient)
except Exception as e:
    print(f'Gradient error: {e}')
    # Fallback: solid fill
    fill_color = ps.SolidColor()
    fill_color.rgb.red = 74
    fill_color.rgb.green = 144
    fill_color.rgb.blue = 217
    doc.selection.fill(fill_color)

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

# White color
text_color = ps.SolidColor()
text_color.rgb.red = 255
text_color.rgb.green = 255
text_color.rgb.blue = 255
text_item.color = text_color

# Center text
text_x = btn_x + btn_width / 2
text_y = btn_y + btn_height / 2
text_item.position = [text_x, text_y]

print('\n=== Button Created ===')
print(f'Size: {btn_width}x{btn_height} px')
print(f'Position: ({btn_x}, {btn_y})')
print(f'Text: "Hello World" (14pt, centered, white)')
print('=====================')

sys.stdout.flush()
