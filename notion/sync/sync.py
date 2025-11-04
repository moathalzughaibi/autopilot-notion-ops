def find_database_by_title(notion: Client, title: str):
    resp = notion.search(
        query=title,
        filter={"value": "database", "property": "object"},
        sort={"direction": "ascending", "timestamp": "last_edited_time"},
    )
    for item in resp.get("results", []):
        if item.get("object") == "database" and item["title"]:
            # قارن بالاسم الظاهر في Notion (عنوان قاعدة البيانات)
            db_title = "".join([t.get("plain_text", "") for t in item["title"]])
            if db_title.strip() == title.strip():
                return item
    return None
