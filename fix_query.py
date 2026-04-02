import re

with open('src/lib.rs', 'r') as f:
    content = f.read()

content = content.replace('type::thing($table, $id)', '#[cfg(feature = "surrealdb-nightly")] type::thing($table, $id)\n#[cfg(not(feature = "surrealdb-nightly"))] type::record($table, $id)')

with open('src/lib.rs', 'w') as f:
    f.write(content)
