```mermaid
---
title: pelaajan sisäänkirjautuminen käyttäjänimellä
---
sequenceDiagram
    InitializeGame->>LoginManager:current_user("test_user")
    LoginManager->>TextManager:username("text_user")
    TextManager->>TextManager:draw_texts()

```