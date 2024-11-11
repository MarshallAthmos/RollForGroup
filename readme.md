# RFG! App
Roll For Group! is supposed to help plan our DnD Community events.

## Data Model

### Sessions
- Name: str
- Player Amount: int
- DM: str
- System: str
- Length: int

### Nerd
- Name: str
- Sessions Interest: Object
- Availability: Object

### Session Interests
- Session: str

### Game Session
- Slot: int
- Session: int
- DM: str
- Players: List