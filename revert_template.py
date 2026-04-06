#!/usr/bin/env python
import os

# Revert localtime filter in my_account.html
file_path = 'myapp/templates/my_account.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Revert the localtime filter changes
old_pattern = '{{ order.created_at|localtime|date:"M d, Y" }} at {{ order.created_at|localtime|time:"h:i A" }}'
new_pattern = '{{ order.created_at|date:"M d, Y" }} at {{ order.created_at|time:"h:i A" }}'

content = content.replace(old_pattern, new_pattern)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('✓ Reverted template - removed invalid localtime filter')
