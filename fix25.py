with open('src/lib.rs', 'r') as f:
    content = f.read()

content = content.replace('''            .query(if cfg!(feature = "surrealdb-nightly") {
                "select expiry_date, data from type::thing($table, $id)
where expiry_date > time::unix(time::now())"
            } else {
                "select expiry_date, data from type::record($table, $id)
where expiry_date > time::unix(time::now())"
            })''', '''            .query(
                "select expiry_date, data from type::record($table, $id)
where expiry_date > time::unix(time::now())",
            )''')

with open('src/lib.rs', 'w') as f:
    f.write(content)
