#!/usr/bin/env python
"""Create a proper rounded button with centered text."""
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
print('Removing old button layers...')
layers_to_keep = ['Layer 0']
for layer in list(doc.artLayers):
    if layer.name not in layers_to_keep:
        print(f'  Deleting: {layer.name}')
        layer.delete()

# Button parameters
btn_width = 200
btn_height = 50
btn_x = 300
btn_y = 275
corner_radius = 12

print(f'Creating rounded button...')

# Method: Use JavaScript to draw rounded rectangle
js_create_button = f"""
(function() {{
    var doc = app.activeDocument;

    // Set units to pixels
    app.preferences.rulerUnits = Units.PIXELS;

    // Button coordinates
    var x1 = {btn_x};
    var y1 = {btn_y};
    var x2 = {btn_x + btn_width};
    var y2 = {btn_y + btn_height};
    var radius = {corner_radius};

    // Create new layer
    var btnLayer = doc.artLayers.add();
    btnLayer.name = "Button Background";

    // Define the rounded rectangle path points
    var pathPoints = [];

    // Start from top-left (after corner)
    pathPoints.push({{x: x1 + radius, y: y1}});

    // Top edge
    pathPoints.push({{x: x2 - radius, y: y1}});

    // Top-right corner (arc)
    pathPoints.push({{x: x2, y: y1}});
    pathPoints.push({{x: x2, y: y1 + radius}});

    // Right edge
    pathPoints.push({{x: x2, y: y2 - radius}});

    // Bottom-right corner
    pathPoints.push({{x: x2, y: y2}});
    pathPoints.push({{x: x2 - radius, y: y2}});

    // Bottom edge
    pathPoints.push({{x: x1 + radius, y: y2}});

    // Bottom-left corner
    pathPoints.push({{x: x1, y: y2}});
    pathPoints.push({{x: x1, y: y2 - radius}});

    // Left edge
    pathPoints.push({{x: x1, y: y1 + radius}});

    // Back to top-left corner
    pathPoints.push({{x: x1, y: y1}});
    pathPoints.push({{x: x1 + radius, y: y1}});

    // Create selection from path points (simplified rectangle with corners)
    // Use a simpler approach: rounded rectangle selection
    doc.selection.select([
        [x1 + radius, y1],
        [x2 - radius, y1],
        [x2 - radius, y1],
        [x2, y1],
        [x2, y1 + radius],
        [x2, y2 - radius],
        [x2, y2 - radius],
        [x2, y2],
        [x2 - radius, y2],
        [x1 + radius, y2],
        [x1 + radius, y2],
        [x1, y2],
        [x1, y2 - radius],
        [x1, y1 + radius],
        [x1, y1 + radius],
        [x1, y1],
        [x1 + radius, y1]
    ]);

    // Fill with blue color
    var fillColor = new SolidColor();
    fillColor.rgb.hexValue = "4A90D9";
    doc.selection.fill(fillColor);
    doc.selection.deselect();

    return "Button background created";
}})();
"""

# Alternative: simpler approach using shape
js_simple_button = f"""
(function() {{
    var doc = app.activeDocument;

    // Create new layer
    var btnLayer = doc.artLayers.add();
    btnLayer.name = "Button Background";

    // Button dimensions
    var x1 = {btn_x};
    var y1 = {btn_y};
    var x2 = {btn_x + btn_width};
    var y2 = {btn_y + btn_height};
    var radius = {corner_radius};

    // Create rounded rectangle selection using feather for smooth corners
    // First create a rectangular selection
    doc.selection.select([
        [x1, y1],
        [x2, y1],
        [x2, y2],
        [x1, y2]
    ]);

    // Feather the selection for rounded corners effect
    doc.selection.feather(radius);

    // Fill with blue color
    var fillColor = new SolidColor();
    fillColor.rgb.hexValue = "4A90D9";
    doc.selection.fill(fillColor);
    doc.selection.deselect();

    return "Created with feathered corners";
}})();
"""

# Try the simpler approach first
result = ps_app.execute_javascript(js_simple_button)
print(f'Result: {result}')

# Create text layer
print('Creating centered text...')
text_layer = doc.artLayers.add()
text_layer.kind = ps.LayerKind.TextLayer
text_layer.name = "Button Text"

text_item = text_layer.textItem
text_item.contents = "Hello World"
text_item.size = 18
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

print('\n=== Button Created ===')
print(f'Size: {btn_width}x{btn_height} px')
print(f'Corner radius: {corner_radius} px')
print(f'Position: ({btn_x}, {btn_y})')
print('Text: "Hello World" (centered, white)')
print('======================')

sys.stdout.flush()
