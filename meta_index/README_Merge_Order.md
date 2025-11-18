# IFNS Indicators — Meta Index (v0.18)
Generated: 2025-11-18

This index lists each deliverable pack and the recommended **merge order**. To assemble the complete project:
1. Place all ZIPs and this folder in the same directory.
2. Verify integrity:
   - Windows PowerShell:
     ```powershell
     .\verify_checksums.ps1 -IndexJson IFNS_Indicators_Packs_Index_v0_18.json
     ```
   - macOS/Linux:
     ```bash
     bash verify_checksums.sh IFNS_Indicators_Packs_Index_v0_18.json
     ```
3. Unzip packs **in ascending merge_order** into the same project root. If prompted on collisions, choose the newer pack (higher version).

See also: `IFNS_Indicators_Quickstart_v0_18.md`.

