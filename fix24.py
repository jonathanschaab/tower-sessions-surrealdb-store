with open('src/lib.rs', 'r') as f:
    content = f.read()

content = content.replace('''    async fn load(&self, session_id: &Id) -> Result<Option<Record>> {
        let record: Option<SessionRecord> = self
            .client
            .select((&self.session_table, session_id.to_string()))
            .await
            .map_err(|e: surrealdb::Error| Error::Backend(e.to_string()))?;

        if let Some(r) = record {
            let now = time::OffsetDateTime::now_utc().unix_timestamp();
            if r.expiry_date > now {
                return Ok(Some(r.to_session()?));
            }
        }

        Ok(None)
    }''', '''    async fn load(&self, session_id: &Id) -> Result<Option<Record>> {
        let record: Option<SessionRecord> = self
            .client
            .query(if cfg!(feature = "surrealdb-nightly") {
                "select expiry_date, data from type::thing($table, $id)
where expiry_date > time::unix(time::now())"
            } else {
                "select expiry_date, data from type::record($table, $id)
where expiry_date > time::unix(time::now())"
            })
            .bind(("id", session_id.to_string()))
            .bind(("table", &self.session_table))
            .await
            .map_err(|e: surrealdb::Error| Error::Backend(e.to_string()))?
            .take(0)
            .map_err(|e: surrealdb::Error| Error::Backend(e.to_string()))?;
        record.map(|r| r.to_session()).transpose()
    }''')

with open('src/lib.rs', 'w') as f:
    f.write(content)
