with open('src/lib.rs', 'r') as f:
    content = f.read()

content = content.replace('''    async fn select_session(db: &Surreal<DB>, session: &Record) -> Option<SessionRecord> {
        db.select((SESSIONS_TABLE, session.id.to_string()))
            .await
            .expect("Error retrieving session record")
    }''', '''    async fn select_session(db: &Surreal<DB>, session: &Record) -> Option<SessionRecord> {
        db.select((surrealdb_types::Table::from(SESSIONS_TABLE), session.id.to_string()))
            .await
            .expect("Error retrieving session record")
    }''')

with open('src/lib.rs', 'w') as f:
    f.write(content)
