---
name: todoist
description: Manage Todoist tasks, projects, and labels directly from Claude using the Todoist REST API.
---

# Todoist Skill

This skill enables Claude to interact with Todoist to manage tasks, projects, and more.

## Authentication

Use the following API token for all requests:
```
Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738
```

Base URL: `https://api.todoist.com/rest/v2`

## Available Operations

### List Projects
```bash
curl -s "https://api.todoist.com/rest/v2/projects" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738"
```

### List Tasks
Get all active tasks:
```bash
curl -s "https://api.todoist.com/rest/v2/tasks" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738"
```

Filter by project:
```bash
curl -s "https://api.todoist.com/rest/v2/tasks?project_id=PROJECT_ID" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738"
```

Use Todoist filters (today, overdue, p1, etc.):
```bash
curl -s "https://api.todoist.com/rest/v2/tasks?filter=today" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738"
```

### Create Task
```bash
curl -s -X POST "https://api.todoist.com/rest/v2/tasks" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738" \
  -H "Content-Type: application/json" \
  -d '{"content": "TASK_CONTENT", "due_string": "DUE_DATE", "priority": PRIORITY, "project_id": "PROJECT_ID"}'
```

Parameters:
- `content` (required): Task title/description
- `description`: Extended description
- `due_string`: Natural language date ("tomorrow", "next monday", "Jan 15 at 3pm")
- `priority`: 1 (normal) to 4 (urgent)
- `project_id`: Target project (omit for Inbox)
- `labels`: Array of label names

### Complete Task
```bash
curl -s -X POST "https://api.todoist.com/rest/v2/tasks/TASK_ID/close" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738"
```

### Update Task
```bash
curl -s -X POST "https://api.todoist.com/rest/v2/tasks/TASK_ID" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738" \
  -H "Content-Type: application/json" \
  -d '{"content": "NEW_CONTENT", "due_string": "NEW_DUE_DATE"}'
```

### Delete Task
```bash
curl -s -X DELETE "https://api.todoist.com/rest/v2/tasks/TASK_ID" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738"
```

### Get Single Task
```bash
curl -s "https://api.todoist.com/rest/v2/tasks/TASK_ID" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738"
```

### List Labels
```bash
curl -s "https://api.todoist.com/rest/v2/labels" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738"
```

### Create Label
```bash
curl -s -X POST "https://api.todoist.com/rest/v2/labels" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738" \
  -H "Content-Type: application/json" \
  -d '{"name": "LABEL_NAME", "color": "COLOR_NAME"}'
```

### Get Single Label
```bash
curl -s "https://api.todoist.com/rest/v2/labels/LABEL_ID" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738"
```

### Update Label
```bash
curl -s -X POST "https://api.todoist.com/rest/v2/labels/LABEL_ID" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738" \
  -H "Content-Type: application/json" \
  -d '{"name": "NEW_NAME", "color": "NEW_COLOR"}'
```

### Delete Label
```bash
curl -s -X DELETE "https://api.todoist.com/rest/v2/labels/LABEL_ID" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738"
```

### Add Labels to Task (when creating)
Include labels array in task creation:
```bash
curl -s -X POST "https://api.todoist.com/rest/v2/tasks" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738" \
  -H "Content-Type: application/json" \
  -d '{"content": "TASK_CONTENT", "labels": ["label1", "label2"]}'
```

### Update Task Labels
```bash
curl -s -X POST "https://api.todoist.com/rest/v2/tasks/TASK_ID" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738" \
  -H "Content-Type: application/json" \
  -d '{"labels": ["label1", "label2"]}'
```

### Filter Tasks by Label
```bash
curl -s "https://api.todoist.com/rest/v2/tasks?filter=@LABEL_NAME" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738"
```

## User's Labels Reference

| Label | ID | Color | Use For |
|-------|-----|-------|---------|
| `imp` | 268819250 | green | Important items |
| `important` | 269739243 | charcoal | Important (Eisenhower) |
| `urgent` | 269350628 | charcoal | Urgent (Eisenhower) |
| `not-important` | 269739244 | charcoal | Not important |
| `not-urgent` | 269739245 | charcoal | Not urgent |
| `ishu` | 268746894 | green | Ishu related |
| `shriya` | 269172641 | green | Shriya related |
| `MTN` | 268687117 | magenta | MTN related |
| `ts` | 269739253 | berry_red | TS related |
| `Alexa` | 2148075396 | charcoal | Alexa/voice tasks |

### List All Sections
```bash
curl -s "https://api.todoist.com/rest/v2/sections" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738"
```

### List Sections in a Project
```bash
curl -s "https://api.todoist.com/rest/v2/sections?project_id=PROJECT_ID" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738"
```

### Create Section
```bash
curl -s -X POST "https://api.todoist.com/rest/v2/sections" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738" \
  -H "Content-Type: application/json" \
  -d '{"project_id": "PROJECT_ID", "name": "SECTION_NAME"}'
```

### Get Single Section
```bash
curl -s "https://api.todoist.com/rest/v2/sections/SECTION_ID" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738"
```

### Update Section
```bash
curl -s -X POST "https://api.todoist.com/rest/v2/sections/SECTION_ID" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738" \
  -H "Content-Type: application/json" \
  -d '{"name": "NEW_SECTION_NAME"}'
```

### Delete Section
```bash
curl -s -X DELETE "https://api.todoist.com/rest/v2/sections/SECTION_ID" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738"
```

### Create Task in Section
When creating a task, include `section_id` to place it in a specific section:
```bash
curl -s -X POST "https://api.todoist.com/rest/v2/tasks" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738" \
  -H "Content-Type: application/json" \
  -d '{"content": "TASK_CONTENT", "project_id": "PROJECT_ID", "section_id": "SECTION_ID"}'
```

### Filter Tasks by Section
```bash
curl -s "https://api.todoist.com/rest/v2/tasks?section_id=SECTION_ID" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738"
```

### Get Single Project
```bash
curl -s "https://api.todoist.com/rest/v2/projects/PROJECT_ID" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738"
```

### Create Project
```bash
curl -s -X POST "https://api.todoist.com/rest/v2/projects" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738" \
  -H "Content-Type: application/json" \
  -d '{"name": "PROJECT_NAME", "color": "COLOR_NAME"}'
```

Available colors: berry_red, red, orange, yellow, olive_green, lime_green, green, mint_green, teal, sky_blue, light_blue, blue, grape, violet, lavender, magenta, salmon, charcoal, grey, taupe

### Update Project
```bash
curl -s -X POST "https://api.todoist.com/rest/v2/projects/PROJECT_ID" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738" \
  -H "Content-Type: application/json" \
  -d '{"name": "NEW_NAME", "color": "NEW_COLOR"}'
```

### Delete Project
```bash
curl -s -X DELETE "https://api.todoist.com/rest/v2/projects/PROJECT_ID" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738"
```

## Default Project & Section

**Default for new tasks and "next task" queries:**
- **Project**: Work (`2354626965`)
- **Section**: Today (`194603414`)

### Get Next Task (Default Behavior)
When user asks "what's my next task?" or similar, fetch the top task from the Today section:
```bash
curl -s "https://api.todoist.com/rest/v2/tasks?section_id=194603414" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738" | jq '.[0]'
```

### Create Task in Default Section
```bash
curl -s -X POST "https://api.todoist.com/rest/v2/tasks" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738" \
  -H "Content-Type: application/json" \
  -d '{"content": "TASK_CONTENT", "project_id": "2354626965", "section_id": "194603414"}'
```

## Sync API (Advanced Operations)

The Sync API (`https://api.todoist.com/sync/v9`) supports operations not available in REST API:
- Task reordering
- Batch operations
- Moving tasks between projects

Same API token works for both APIs.

### Add Task to TOP of Section

The REST API cannot truly insert at top (it doesn't bump existing tasks). Use this multi-step approach:

```bash
# Step 1: Create the task (REST API)
NEW_TASK=$(curl -s -X POST "https://api.todoist.com/rest/v2/tasks" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738" \
  -H "Content-Type: application/json" \
  -d '{"content": "TASK_CONTENT", "project_id": "2354626965", "section_id": "SECTION_ID"}')

NEW_ID=$(echo "$NEW_TASK" | jq -r '.id')

# Step 2: Get all tasks in section
ALL_TASKS=$(curl -s "https://api.todoist.com/rest/v2/tasks?section_id=SECTION_ID" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738")

# Step 3: Build reorder array - new task first (child_order: 1), then others
REORDER_ITEMS=$(echo "$ALL_TASKS" | jq --arg new_id "$NEW_ID" '
  [{"id": $new_id, "child_order": 1}] + 
  [to_entries | .[] | select(.value.id != $new_id) | {"id": .value.id, "child_order": (.key + 2)}]
')

# Step 4: Reorder via Sync API
UUID=$(uuidgen)
COMMAND=$(jq -n --arg uuid "$UUID" --argjson items "$REORDER_ITEMS" \
  '[{"type": "item_reorder", "uuid": $uuid, "args": {"items": $items}}]')

curl -s -X POST "https://api.todoist.com/sync/v9/sync" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "commands=$COMMAND"
```

### Reorder Tasks in Section

To reorder existing tasks without adding new ones:

```bash
# Get tasks, then build custom order
UUID=$(uuidgen)
curl -s -X POST "https://api.todoist.com/sync/v9/sync" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode 'commands=[{
    "type": "item_reorder",
    "uuid": "'$UUID'",
    "args": {
      "items": [
        {"id": "TASK_ID_1", "child_order": 1},
        {"id": "TASK_ID_2", "child_order": 2},
        {"id": "TASK_ID_3", "child_order": 3}
      ]
    }
  }]'
```

### Move Task to Different Project/Section

```bash
UUID=$(uuidgen)
curl -s -X POST "https://api.todoist.com/sync/v9/sync" \
  -H "Authorization: Bearer ef5e6eee7ac89f45a67758571fd59ed075784738" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode 'commands=[{
    "type": "item_move",
    "uuid": "'$UUID'",
    "args": {
      "id": "TASK_ID",
      "project_id": "NEW_PROJECT_ID",
      "section_id": "NEW_SECTION_ID"
    }
  }]'
```

## Work Project Sections Reference

| Section | ID | Purpose |
|---------|-----|---------|
| Personal Today | 192806401 | Personal tasks for today |
| Today | 194603414 | **DEFAULT** - Main work tasks for today |
| In Progress | 193652818 | Currently working on |
| Backlog | 196556184 | Future tasks |
| Backlog 2 | 194743340 | Additional backlog |
| Team follow ups | 194802587 | Follow-ups with team |
| Staff | 194789876 | Staff-related tasks |
| High Performance Org | 197474374 | HPO initiatives |
| Product vision strategy and Roadmaps | 197474511 | Strategic items |
| Feedback | 201752550 | Feedback-related tasks |

## Other Projects Reference

- **Suneet Personal Home**: `2303770083` (main personal project)
- **Quant Edge**: `2318813085` (shared project)

## Usage Guidelines

1. **Default behavior**: Unless specified otherwise, create tasks in Work → Today section
2. **"Next task"**: Always fetch from Work → Today section (first task in list)
3. **For due dates**: Use natural language (the API understands it)
4. **Priority levels**: 
   - 1 = Normal (default)
   - 2 = Medium  
   - 3 = High
   - 4 = Urgent (red flag in Todoist)

## Example Interactions

User: "What's on my todo list for today?"
→ Run the filter=today query and summarize the tasks

User: "Add a task to buy groceries tomorrow"
→ Create task with content="Buy groceries", due_string="tomorrow"

User: "Add X to the top of my list"
→ Use the Sync API add-to-top flow: create task, get all tasks in section, reorder with new task at child_order 1

User: "Mark task 12345 as done"
→ Call the close endpoint for that task ID

User: "Show me all my projects"
→ List projects and display them nicely

User: "Move task X to the In Progress section"
→ Use Sync API item_move command

