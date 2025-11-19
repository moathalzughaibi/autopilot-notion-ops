param([string]$RootTitle = "IFNS – UI Master (V2)")
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
if (Test-Path .\.venv\Scripts\Activate.ps1) { . .\.venv\Scripts\Activate.ps1 }
")
$Cfg = ".\IFNS_Notion_DB_Buildout_V2\config\ifns_v2_db_map.json"

# load Notion env for this run (fails fast if missing)
if (Test-Path .\local_env\notion_env.ps1) { . .\local_env\notion_env.ps1 } else { Write-Error "Missing local_env\notion_env.ps1"; exit 1 }

python .\IFNS_Notion_DB_Buildout_V2\scripts\ifns_v2_create_dbs.py --root "$RootTitle" --config $Cfg --assets `
  "FeatureSchemaV1=sync/ifns/indicator_feature_schema_v1_with_family.csv:feature_name" `
  "FeatureSchemaH1=sync/ifns/indicator_feature_schema_h1_v1_with_family.csv:feature_name" `
  "PolicyMatrix=sync/ifns/feature_policy_matrix.csv" `
  "FamilyMap=sync/ifns/feature_family_map.csv:feature_name" `
  "UniverseP2=sync/ifns/indicators_universe_catalog_phase2.csv:symbol" `
  "CatalogL1=sync/ifns/indicators_catalog_L1_phase3.csv:indicator_id" `
  "CatalogL2L3=sync/ifns/indicators_catalog_L2L3_phase4.csv:composite_id" `
  "QCWeekly=sync/ifns/qc_weekly_schema_v1.json" `
  "CalendarGaps2025=sync/ifns/calendar_gaps_2025.json"

python .\IFNS_Notion_DB_Buildout_V2\scripts\ifns_v2_sync_db_generic.py --config $Cfg --key FeatureSchemaV1
python .\IFNS_Notion_DB_Buildout_V2\scripts\ifns_v2_sync_db_generic.py --config $Cfg --key FeatureSchemaH1
python .\IFNS_Notion_DB_Buildout_V2\scripts\ifns_v2_sync_db_generic.py --config $Cfg --key PolicyMatrix
python .\IFNS_Notion_DB_Buildout_V2\scripts\ifns_v2_sync_db_generic.py --config $Cfg --key FamilyMap
python .\IFNS_Notion_DB_Buildout_V2\scripts\ifns_v2_sync_db_generic.py --config $Cfg --key UniverseP2
python .\IFNS_Notion_DB_Buildout_V2\scripts\ifns_v2_sync_db_generic.py --config $Cfg --key CatalogL1
python .\IFNS_Notion_DB_Buildout_V2\scripts\ifns_v2_sync_db_generic.py --config $Cfg --key CatalogL2L3

python .\IFNS_Notion_DB_Buildout_V2\scripts\ifns_v2_sync_qc_weekly.py --config $Cfg
python .\IFNS_Notion_DB_Buildout_V2\scripts\ifns_v2_sync_calendar_gaps.py --config $Cfg

python .\IFNS_Notion_DB_Buildout_V2\scripts\ifns_v2_wire_pages.py --root "$RootTitle" --config $Cfg
python .\IFNS_Notion_DB_Buildout_V2\scripts\ifns_v2_update_local_docs.py --config $Cfg

python .\IFNS_Notion_DB_Buildout_V2\scripts\ifns_v2_saved_views_playbook.py
python .\IFNS_Notion_DB_Buildout_V2\scripts\ifns_v2_admin_config_index.py
