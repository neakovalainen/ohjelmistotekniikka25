```mermaid
---
title: Pelaaja osuu energiajuomaan ja pisteet päivittyvät ruudulle
---
sequenceDiagram
    InitializeGame->>PointCollector:collision_detector(player, energy)
    PointCollector->>PointCollector:energy_consumed()
    PointCollector->>GameStatus: energy_level + 0.25
    InitializeGame->>TextManager: draw_texts()
    TextManager-->>TextManager:text_objects()

```