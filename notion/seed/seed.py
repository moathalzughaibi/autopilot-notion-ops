from notion_client import Client
import os

NOTION = Client(auth=os.environ["NOTION_TOKEN"])
ROOT = os.environ["ROOT_PAGE_ID"]

DBS = [
  {
    "title": "Autopilot_Experiments_Log",
    "properties": {
      "Date": {"date": {}},
      "Platform": {"select": {"options":[{"name":"Runpod"},{"name":"GitHub"},{"name":"Notion"}]}},
      "Title": {"title": {}},
      "Summary": {"rich_text": {}},
      "Status": {"select": {"options":[{"name":"Success"},{"name":"Failed"},{"name":"Partial"}]}},
      "Error_Message": {"rich_text": {}},
      "Root_Cause": {"rich_text": {}},
      "Fix_Or_Workaround": {"rich_text": {}},
      "Code_Snippets": {"rich_text": {}},
      "Links": {"url": {}},
      "Tags": {"multi_select": {}},
      "Owner": {"people": {}}
    }
  },
  {
    "title": "Autopilot_Decisions_Log",
    "properties": {
      "Date":{"date":{}},
      "Area":{"select":{"options":[{"name":"Architecture"},{"name":"Process"},{"name":"Tooling"},{"name":"Scope"}]}},
      "Decision":{"title":{}},
      "Context":{"rich_text":{}},
      "Options_Considered":{"rich_text":{}},
      "Chosen_Reason":{"rich_text":{}},
      "Impact":{"rich_text":{}},
      "Status":{"select":{"options":[{"name":"Proposed"},{"name":"Approved"},{"name":"Deprecated"}]}},
      "Related_Links":{"url":{}},
      "Owner":{"people":{}}
    }
  },
  {
    "title":"Autopilot_Tasks_Backlog",
    "properties":{
      "Task_ID":{"rich_text":{}},
      "Title":{"title":{}},
      "Type":{"select":{"options":[{"name":"Research"},{"name":"Setup"},{"name":"Dev"},{"name":"Debug"},{"name":"Doc"}]}},
      "Priority":{"select":{"options":[{"name":"High"},{"name":"Medium"},{"name":"Low"}]}},
      "Status":{"select":{"options":[{"name":"To Do"},{"name":"Doing"},{"name":"Done"}]}},
      "Assignee":{"people":{}},
      "Due":{"date":{}},
      "Parent_Epic":{"rich_text":{}},
      "Related_Notion_Page":{"relation":{}},
      "Notes":{"rich_text":{}}
    }
  },
  {
    "title":"Autopilot_Glossary",
    "properties":{
      "Term":{"title":{}},
      "Definition":{"rich_text":{}},
      "Category":{"select":{}},
      "Source_Link":{"url":{}},
      "Notes":{"rich_text":{}},
      "Owner":{"people":{}}
    }
  },
  {
    "title":"Autopilot_Variables_Config",
    "properties":{
      "Name":{"title":{}},
      "Scope":{"select":{"options":[{"name":"Runpod"},{"name":"Notion"},{"name":"GitHub"},{"name":"Cloud"}]}},
      "Current_Value":{"rich_text":{}},
      "Is_Secret":{"checkbox":{}},
      "Location_Path_or_Key":{"rich_text":{}},
      "Notes":{"rich_text":{}},
      "Last_Updated":{"date":{}}
    }
  },
  {
    "title":"Autopilot_Architecture_Notes",
    "properties":{
      "Topic":{"title":{}},
      "Layer":{"select":{"options":[{"name":"UX"},{"name":"UI"},{"name":"Backend"},{"name":"Data"},{"name":"Infra"}]}},
      "Doc_Type":{"select":{"options":[{"name":"Idea"},{"name":"Spec"},{"name":"ADR"},{"name":"Diagram"}]}},
      "Summary":{"rich_text":{}},
      "Link":{"url":{}},
      "Status":{"select":{"options":[{"name":"Draft"},{"name":"Review"},{"name":"Final"}]}},
      "Owner":{"people":{}},
      "Notes":{"rich_text":{}}
    }
  }
]

def ensure_db(root_id: str, spec: dict):
    title = [{"type":"text","text":{"content":spec["title"]}}]
    return NOTION.databases.create(
        parent={"type":"page_id","page_id":root_id},
        title=title,
        is_inline=False,
        properties=spec["properties"]
    )

if __name__ == "__main__":
    for spec in DBS:
        print(f"Creating DB: {spec['title']}")
        ensure_db(ROOT, spec)
    print("Done.")
