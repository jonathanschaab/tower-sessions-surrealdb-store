with open('src/lib.rs', 'r') as f:
    content = f.read()

content = content.replace('''            .query(
                "select expiry_date, data from type::record($table, $id)
where expiry_date > time::unix(time::now())",
            )
            .bind(("id", session_id.to_string()))
            .bind(("table", self.session_table.clone()))''', '''            .query(if cfg!(feature = "surrealdb-nightly") {
                "select expiry_date, data from type::thing($table, $id)
where expiry_date > time::unix(time::now())"
            } else {
                "select expiry_date, data from type::record($table, $id)
where expiry_date > time::unix(time::now())"
            })
            .bind(("id", session_id.to_string()))
            .bind(("table", if cfg!(feature = "surrealdb-nightly") { surrealdb_types::Table::from(self.session_table.clone()) } else { surrealdb_types::Table::from(self.session_table.clone()) }))''')

with open('src/lib.rs', 'w') as f:
    f.write(content)
