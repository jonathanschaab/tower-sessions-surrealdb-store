with open('src/lib.rs', 'r') as f:
    content = f.read()

content = content.replace('"select expiry_date, data from type::thing($table, $id)\nwhere expiry_date > time::unix(time::now())",', 'if cfg!(feature = "surrealdb-nightly") { "select expiry_date, data from type::thing($table, $id)\nwhere expiry_date > time::unix(time::now())" } else { "select expiry_date, data from type::record($table, $id)\nwhere expiry_date > time::unix(time::now())" },')

with open('src/lib.rs', 'w') as f:
    f.write(content)
