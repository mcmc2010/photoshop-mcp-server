#!/usr/bin/env python
"""Save document as PSD in Photoshop."""
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

# Save path
save_path = r'D:\demo\photoshop-mcp-server\test.psd'
print(f'Saving to: {save_path}')

# Save as PSD
options = ps.PhotoshopSaveOptions()
doc.saveAs(save_path, options, asCopy=True)

print('Document saved successfully!')
print(f'  File: {save_path}')

sys.stdout.flush()
